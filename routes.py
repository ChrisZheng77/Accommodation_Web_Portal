from app import app, db
from os import path, listdir, mkdir
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import render_template, abort, jsonify, request, redirect, url_for, flash, current_app
from flask_login import login_required, login_user, logout_user, current_user
from model import User, Apartment, Order, Review, Message

def get_imgs(id):
    imagepath = path.join(current_app.static_folder, 'upload', str(id))
    return list(filter(lambda x: x.find('.jpg') != -1, listdir(imagepath)))

table_header = {
    'apartment': [('id', 'ID'), ('a_name', 'Apartment Name'), ('location','Location'), ('address', 'Address'), ('price', 'Price'), ('score_mean', 'Mean Score') ],
    'order': [('id', 'ID'), ('username', 'Username'), ('apartmentname', 'Apartment Name'), ('checkin_date', 'Checkin Date'), ('checkout_date', 'Checkout Date')],
    'review': [('id', 'ID'), ('apartmentname', 'Apartment Name'), ('content', 'Content'), ('score', 'Score')]
}

@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    # get params
    location = request.values.get('location')
    daterange = request.values.get('daterange')
    # bedroom = request.values.get('bedroom')
    # guest = request.values.get('guest')
    # type = request.values.get('type')

    apartments = Apartment.query\
                            .filter(Apartment.location.ilike("%{}%".format(location)))

    if request.values.get(('type')):
        apartments = apartments.filter(Apartment.type == request.values.get('type'))

    for i in ['bedroom', 'guest']:
        if request.values.get(i):
            apartments = apartments.filter(getattr(Apartment, i) >= request.values.get(i))

    for i in ['wifi', 'parking', 'tv', 'bathroom', 'coffee']:
        if request.values.get(i) and request.values.get(i) == '1':
            apartments = apartments.filter(getattr(Apartment, i).is_(True))

    res = apartments.all()

    # change daterange string to datetime
    if daterange:
        l = daterange.split('-')
        checkin = datetime.strptime(l[0].strip(), '%m/%d/%Y').date()
        checkout = datetime.strptime(l[1].strip(), '%m/%d/%Y').date()

        # filter the list by the checkin and checkout date
        result = list(filter(lambda x: not x.checkbooking(checkin, checkout), res))
    for r in result:
        r.imgs = get_imgs(r.id)

    return render_template('search.html', data= result)

@app.route('/apartment/<int:id>', methods=['GET'])
def apartment(id):
    apartment = Apartment.query.filter_by(id=id).one_or_none()
    if apartment:
        apartment.imgs = get_imgs(apartment.id)
        apartment.nearby = Apartment.query.filter(Apartment.altitude.between(apartment.altitude-.1, apartment.altitude+.1))\
                                            .filter(Apartment.longtitude.between(apartment.longtitude-.1, apartment.longtitude+.1))\
                                            .filter(Apartment.id != apartment.id).limit(3).all()

        return render_template('apartment.html', data= apartment)
    else:
        abort(404, 'Not Found Such Infomation.')

@app.route('/booking/<int:id>', methods=['GET', 'POST'])
@login_required
def booking(id):
    apartment = Apartment.query.filter_by(id=id).first()
    if request.method == 'POST':
        daterange = request.values.get('daterange')
        if daterange:
            l = daterange.split('-')
            checkin = datetime.strptime(l[0].strip(), '%m/%d/%Y').date()
            checkout = datetime.strptime(l[1].strip(), '%m/%d/%Y').date()

            if not apartment.checkbooking(checkin, checkout):
                booking = Order(user_id= current_user.id, apartment_id= id, checkin_date= checkin, checkout_date= checkout)

                db.session.add(booking)
                db.session.commit()

                flash('This booking ordered.', 'success')
                return redirect(url_for('apartment', id= id))
            else:
                flash('This apartment is booked in this daterange', 'info')
        else:
            flash('Booking date not selected.', 'warning')
    return render_template('booking.html', data= apartment)

@app.route('/message/<int:id>', methods=['POST', 'GET'])
@login_required
def message(id):
    message = Message.query.get(id)
    to_id = message.from_id if message.from_id != current_user.id else message.to_id
    return render_template('message.html', message= message, to_id= to_id)

@app.route('/message/add/<int:id>', methods=['POST', 'GET'])
@app.route('/message/add/', defaults={'id': -1}, methods=['GET', 'POST'])
@login_required
def add_message(id):
    if int(id) != -1:
        apartment = Apartment.query.get(id)
        if apartment:
            to_id = apartment.owner_id
        else:
            flash('Something went wrong')
            return redirect(url_for('index'))


    if request.method == 'POST':
        content = request.values.get('content')
        touser_id = request.values.get('to_id')
        parent_id = request.values.get('parent_id')

        message = Message(content= content, from_id= current_user.id, to_id= touser_id, parent_id= parent_id)
        db.session.add(message)
        db.session.commit()
        flash('Messages sented.', 'success')
        return redirect(url_for('index'))


    return render_template('message.html', message= None, to_id= to_id)


@app.route('/message/list', methods= ['GET', 'POST'])
@login_required
def list_message():
    return render_template('message.html')


@app.route('/add/review/<int:id>', methods=['POST'])
@login_required
def add_review(id):
    content = request.form.get('content')
    apartment = Apartment.query.filter_by(id= id).first()
    if not content or content == '':
        flash('The content is empty', 'warning')
    elif not apartment:
        flash('The hotel is not exist.', 'warning')
    elif not apartment.checkuser(current_user.id):
        flash("You can't review it before booking.")
    else:
        review = Review(content= content, apartment_id= id, user_id= current_user.id, score= request.form.get('rating'))
        db.session.add(review)
        db.session.commit()
        flash('Review added', 'success')

    return redirect(url_for('apartment', id=id))


# list the orders the user booking
@app.route('/orders', methods=['GET'])
@login_required
def orders():
    orders = Order.query.filter_by(user_id= current_user.id).all()
    return render_template('admin/orders.html', header= table_header['order'], data= orders)

# list the reviews the user writed
@app.route('/reviews', methods=['GET'])
@login_required
def reviews():
    reviews = Review.query.filter_by(user_id= current_user.id).all()
    return render_template('admin/reviews.html', header= table_header['review'], data= reviews)

# list the apatrments the user published
@app.route('/apartments', methods=['GET'])
@login_required
def apartments():
    apartments = Apartment.query.filter_by(owner_id= current_user.id).all()
    return render_template('admin/apartments.html', data= apartments ,header= table_header['apartment'])

# add apartment
@app.route('/add/apartment', methods=['GET', 'POST'])
@login_required
def add_apartment():
    location = request.form.get('location')
    if request.method == 'POST':
        if location or location != '':
            try:
                apartment = Apartment(a_name= request.form.get('a_name'),
                                      location = request.form.get('location'),
                                      address = request.form.get('address'),
                                      postcode= request.form.get('postcode'),
                                      longtitude= request.form.get('longtitude'),
                                      altitude= request.form.get('altitude'),
                                      bedroom= request.form.get('bedroom'),
                                      guest= request.form.get('guest'),
                                      wifi= True if request.form.get('wifi') == '1' else False,
                                      parking= True if request.form.get('parking') == '1' else False,
                                      tv= True if request.form.get('tv') == '1' else False,
                                      bathroom= True if request.form.get('bathroom') == '1' else False,
                                      coffee= True if request.form.get('coffee') == '1' else False,
                                      price= request.form.get('price'),
                                      type = request.form.get('type'),
                                      description= request.form.get('description'),
                                      owner_id= current_user.id)
                db.session.add(apartment)
                db.session.flush()

                images = request.files.getlist('images')
                for img in images:
                    fname = secure_filename(img.filename)
                    if fname.find('.jpg') != -1:
                        fpath = path.join(current_app.static_folder, 'upload', str(apartment.id))
                        if not path.exists(fpath):
                            mkdir(fpath)
                        img.save(path.join(fpath, fname))

                db.session.commit()
                flash('Your apartment is added.', 'success')
            except:
                db.session.rollback()
                flash('Something went worng.', 'warning')
            finally:
                db.session.close()

            return redirect(url_for('apartments'))
        else:
            flash('You should select a location.', 'warning')

    return render_template('admin/add_apartment.html')

# delete apartment
@app.route('/del/apartment/<int:id>', methods=['GET'])
@login_required
def del_apartment(id):
    apartment = Apartment.query.filter_by(id=id).first()

    if not apartment:
        flash("The apartment isn't exist.", "warning")
    elif apartment.owner_id != current_user.id:
        flash("This apartment doesn't belong to you.", 'waring')
    else:
        db.session.delete(apartment)
        db.session.commit()
        flash("The apartment deleted.")

    return redirect(url_for('apartments'))

# the orders of the hotel
@app.route('/a/orders/<int:id>', methods=['GET'])
@login_required
def a_orders(id):
    orders = Order.query.filter_by(apartment_id= id).all()
    return render_template('admin/orders.html', header=table_header['order'], data=orders)

# the reviews of the hotel
@app.route('/a/reviews/<int:id>', methods=['GET'])
@login_required
def a_reviews(id):
    reviews = Review.query.filter_by(apartment_id = id).all()
    return render_template('admin/reviews.html', header= table_header['review'], data= reviews)

# Help route
@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.values.get('phone')
        password = request.values.get('password')

        if phone:
            user = User.query.filter_by(phone= phone).one_or_none()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Got worng username or password', 'warning')
    return render_template('login.html')

# logout route
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        confim = request.values.get('confim')
        email = request.values.get('email')
        brithday = request.values.get('brithday')
        phone = request.values.get('phone')

        brith = datetime.strptime(brithday, '%Y-%m-%d')
        age = (datetime.today() - brith).days//365

        if password != confim:
            flash('Password should be the same.', 'warning')
        elif age <18:
            flash("You're less than 18 years old", 'info')
        elif username and password and phone:
            user = User(username= username, phone= phone, email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()
            flash('Your account is set up.')

            return redirect(url_for('login'))

    return render_template('signup.html')


locationData = [
  {
    "value": "Redfern", "text": "Redfern"
  },
  {
    "value": "Sydney olympic park", "text": "Sydney olympic park"
  },
  {
    "value": "Ultimo", "text": "Ultimo"
  },
  {
    "value": "Balmain", "text": "Balmain"
  },
  {
    "value": "Surry hills", "text": "Surry hills"
  },
  {
    "value": "CBD", "text": "CBD"
  },
  {
    "value": "Rosebery", "text": "Rosebery"
  },
  {
    "value": "Bondi", "text": "Bondi"
  },
  {
    "value": "Newtown", "text": "Newtown"
  },
  {
    "value": "Sydney Harbor Bridge", "text": "Sydney Harbor Bridge"
  },
  {
    "value": "The Rocks", "text": "The Rocks"
  },
  {
    "value": "Opera House", "text": "Opera House"
  },
  {
    "value": "Kensington", "text": "Kensington"
  },
  {
    "value": "Randwick", "text": "Randwick"
  },
  {
    "value": "Kingsford", "text": "Kingsford"
  },
  {
    "value": "Mascot", "text": "Mascot"
  },
  {
    "value": "Hurstville", "text": "Hurstville"
  },
  {
    "value": "Epping", "text": "Epping"
  },
  {
    "value": "Eastwood", "text": "Eastwood"
  },
  {
    "value": "Wollongong", "text": "Wollongong"
  },
  {
    "value": "Wickham", "text": "Wickham"
  },
  {
    "value": "The Hill", "text": "The Hill"
  },
  {
    "value": "Merewether", "text": "Merewether"
  },
  {
    "value": "Warners Bay", "text": "Warners Bay"
  },
  {
    "value": "East Gosford", "text": "East Gosford"
  },
  {
    "value": "Berkeley Vale", "text": "Berkeley Vale"
  },
  {
    "value": "Toukley", "text": "Toukley"
  },
  {
    "value": "North Avoca", "text": "North Avoca"
  }
]

@app.route('/autocomplete', methods=['GET'])
def auto_complete():
    q = request.args.get('q')
    res = []
    if q:
        for i in locationData:
            if i['text'].lower().find(q.lower()) != -1:
                res.append(i)

    return jsonify(res)

