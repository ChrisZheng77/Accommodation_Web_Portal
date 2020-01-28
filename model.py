from statistics import mean
from app import db, loginmanager
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Float, Date, DateTime, SmallInteger, func
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model, UserMixin):
    '''
    User Model
    '''
    __tablename__ = 'user'

    id= Column(Integer, autoincrement= True, primary_key= True)
    username = Column(String(126))
    password_hash= Column(String(126))
    email = Column(String(126))
    phone = Column(String(126))

    def set_password(self, password):
        # set the user's password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # check the user's password
        return check_password_hash(self.password_hash, password)

    @property
    def is_owner(self):
        return bool(self.apartments)

    @property
    def messages(self):
        # return self.message_sended + self.message_received
        return [m for m in self.message_sended + self.message_received if not m.parent_id]


@loginmanager.user_loader
def user_loader(id):
    return User.query.get(id)

class Apartment(db.Model):
    '''
    Apartment Model
    '''
    __tablename__ = 'apartment'

    id = Column(Integer, autoincrement= True, primary_key= True)
    a_name = Column(String(126))
    location = Column(String())
    address = Column(String(126))
    postcode = Column(String(16))
    longtitude = Column(Float)
    altitude = Column(Float)
    price = Column(Float)
    type = Column(String)
    guest = Column(SmallInteger)
    bedroom = Column(SmallInteger)
    wifi = Column(Boolean)
    parking = Column(Boolean)
    tv = Column(Boolean)
    bathroom = Column(Boolean)
    coffee = Column(Boolean)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('user.id'))

    owner = relationship('User', backref='apartments')

    @property
    def score_mean(self):
        return round(mean([ r.score if r.score else 0 for r in self.reviews]), 2) if self.reviews else None

    def checkbooking(self, checkin, checkout):
        booking = False
        for o in self.orders:
            if o.checkin_date <= checkin <= o.checkout_date or o.checkin_date<= checkout <= o.checkout_date:
                booking = True
                break
        return booking

    def checkuser(self, id):
        booking = False
        for o in self.orders:
            if o.user_id == id and int(o.status) >= 1:
                booking = True
                break
        return booking

class Order(db.Model):
    '''
    Order Model
    '''
    __tablename__ = 'order'

    id = Column(Integer, autoincrement= True, primary_key= True)
    created_at = Column(DateTime, default= func.current_timestamp())
    user_id = Column(Integer, ForeignKey('user.id'))
    apartment_id = Column(Integer, ForeignKey('apartment.id'))
    checkin_date = Column(Date)
    checkout_date = Column(Date)
    status = Column(SmallInteger, comment='0 for ordered, 1 for payed, -1 for wrong', default=0)

    apartment = relationship('Apartment', backref='orders')
    user = relationship('User', backref='orders')

    @property
    def username(self):
        return self.user.username

    @property
    def apartmentname(self):
        return self.apartment.a_name

class Review(db.Model):
    '''
    Review Model
    '''
    __tablename__ = 'review'

    id = Column(Integer, autoincrement= True, primary_key= True)
    created_at = Column(DateTime, default= func.current_timestamp())
    score= Column(Float())
    user_id = Column(Integer, ForeignKey('user.id'))
    apartment_id = Column(Integer, ForeignKey('apartment.id'))
    content = Column(Text)

    apartment = relationship('Apartment', backref='reviews')
    user = relationship('User', backref='reviews')

    @property
    def apartmentname(self):
        return self.apartment.a_name


class Message(db.Model):
    '''
    Message Model
    '''
    __tablename__ = 'message'

    id = Column(Integer, autoincrement=True, primary_key= True)
    created_at = Column(DateTime, default= func.current_timestamp())
    content = Column(Text)
    from_id = Column(Integer, ForeignKey('user.id'))
    to_id = Column(Integer, ForeignKey('user.id'))
    parent_id = Column(Integer, ForeignKey('message.id'))

    from_user = relationship('User', backref='message_sended', foreign_keys= [from_id])
    to_user = relationship('User', backref='message_received', foreign_keys= [to_id])
    parent = relationship('Message', remote_side=[id],  backref='children')