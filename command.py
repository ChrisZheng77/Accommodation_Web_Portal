from datetime import timedelta, date
from model import User, Apartment, Order, Review, Message
def add_commands(app, db):
    @app.cli.command()
    def init_db():
        # drop old database, create new one then create all tables
        db.drop_all()
        db.create_all()

    @app.cli.command()
    def add_val():
        # add user to database
        admin = User(username='admin', phone='12345')
        admin.set_password('12345678')
        user = User(username='user', phone= '0000')
        user.set_password('12345678')
        u1 = User(username='test01', phone='0001')
        u1.set_password('test01')
        u2 = User(username='test02', phone='0002')
        u2.set_password('test02')
        # add the data to session
        db.session.add_all([admin, user, u1, u2])
        db.session.flush()
        # add apartment to database
        a1 = Apartment(a_name='Stroll around Victoria Park from a Stylish Loft',
                       location='Ultimo',
                       address='348 Bulware Rd,Ultimo, New South Wales, Australia',
                       postcode='2007', longtitude='151.1993252', altitude='-33.8808471',
                       price='150', type='loft', bedroom= 1, guest= 2, wifi= True, owner_id=user.id,
                       description= "<p>4 guests  1 bedroom  1 bed  1 bath</p>" + \
                                    "<p> Entire loft</p>" + \
                                    "<p>This split-level modest but cozy studio has been recently renovated, making excellent use of the space with high ceilings and nice modern new flooring. Choice of queen bed (upstairs) or sofa bed (downstairs). Our unit is located in a large twin building complex (apartment, student accommodation, hotel, mall) and is perfectly located next to a bus stop (every 2-3min). 10-15min walk to Central station and Paddy's Market, 20min walk to Darling Harbor.</p>")
        a2 = Apartment(a_name='Designer Apartment close CBD & Airport & Beach',
                       location='Rosebery',
                       address='11 rosebery avenue, rosebery, 2018,Sydney',
                       postcode='2018', longtitude='151.2076137', altitude='-33.9137544',
                       price='130', type='apartment', bedroom=1, guest=3, wifi=True, parking=True, tv=True, bathroom=True, owner_id=admin.id,
                       description="<p>3 guests  1 bedroom  2 beds  1 bathroom</p>" + \
                                   "<p> Entire apartment</p>" + \
                                   "<p>Welcome to Rosebery!This modern town is just 5.5 km from Sydney. This one-bedroom apartment with special designer awards is limited to 1 minute walk to Sydney city centre / CBD, University of New South Wales and Bondi Junction / Bondi Beach / Coogee Beach (no transfer required)- 14 minutes walk to Green Square Station- 10 minutes drive from CBD and Sydney Airport- Walking distance to East Village Shopping Centre, public schools, restaurants, medical clinics and other facilities.</p>")
        a3 = Apartment(a_name='Newtown - Entire house, BEST location & parking',
                       location='Newtown',
                       address='267 king street，newtown，2042, Sydney',
                       postcode='2042', longtitude='151.1802630', altitude='-33.8960238',
                       price='141', type='townhouse', bedroom=2, guest=4, wifi=True, parking=True, tv=True, bathroom=True, owner_id=admin.id,
                       description="<p>4 guests  2 bedrooms   3 beds  1.5 bathrooms</p>" + \
                                   "<p>This cute 2 bedroom Victorian terrace is in the heart of Newtown's. 50 metres to the King St/ Enmore Rd junction - where you will find over 600 cafes, restaurants and bars to choose from as well as Newtown train station and buses. 2 minute walk to Enmore Theatre. 5 minute walk to Royal Prince Alfred (RPA) Hospital and 10 minutes to Sydney University.</p>")
        a4 = Apartment(a_name='The Lucky Dog Bondi Beach 3 Bed+ 2 Bath + garden',
                       location='Bondi',
                       address='3 Jaques avenue, Bondi Beach, 2036, Sydney',
                       postcode='2036', longtitude='151.2725109', altitude='-33.8910443',
                       price='412', type='house', bedroom=3, guest=7, wifi=True, parking=True, tv=True, bathroom=True, owner_id=user.id,
                       description="<p>7 guests   3 bedrooms    4 beds    2 bathrooms</p>" + \
                                   "<p>Cool, sleek and sophisticated, this newly renovated 3 bedroom, 2 bathroom home is enveloped in light and comfort. White interiors are complimented by accents of blue and yellow to radiate beach vibes. Walk to cafes, shops and the beach just minutes away<p/>")
        a5 = Apartment(a_name='Studio in the heart of Sydney CBD',
                       location='the rocks',
                       address='4 bridge street，the rocks，2000',
                       postcode='2000', longtitude='151.2078309', altitude='-33.8634198',
                       price='170', type='apartment', bedroom=1, guest=3, wifi=True, parking=False, tv=True, bathroom=True, owner_id=u1.id,
                       description="<p>3 guests  Studio   1 bedroom   1 bathroom</p>" + \
                                   "<p>My apartment is amazingly located in the heart of Sydney CBD, near Circular Quay, Opera House, Royal Botanic Garden and many restaurants, pubs and the shopping area, all the best Sydney can offer. The unit has everything you need to spend a great time in the city. Access to all public transport, unfortunately no parking on the building. *we may expect some noise coming from the street due to construction work on the new light rail*</p>")
        a6 = Apartment(a_name='Darling Harbour: Entire apartment one bedroom',
                       location='darling harbour',
                       address='243 pyrmont street，darling harbor，2007',
                       postcode='2007',longtitude='151.1971769',altitude='-33.8739808',
                       price='175',type='apartment', bedroom=1, guest=4, wifi=True, parking=False, tv=True, bathroom=True, owner_id=u2.id,
                       description="<p>4 guests  1 bedroom  2 beds   1 bathroom</p>" + \
                                   "<p>1 bedroom apartment sleeps 4. light filled , stylish with an internal courtyard Gym /Pool /Spa amenities/ WIFI in unit. 2nd level via lift access in the historic Goldsborough Mort Hotel Pyrmont 245 Pyrmont st, Superb position at Darling harbour with direct undercover access to The International Conference Centre ,Star City Casino ,shops & restaurants. Easy access Sydney City 10 minute walk. Major Attractions inc Harbour bridge ,Opera House, Galleries 30 mins walk Or 2 minute walk to Transport</p>")
        a7 = Apartment(a_name='1BR Apt close to Allianz Stadium & Centennial Park',
                       location='kensington',
                       address='10 anzac pde，kensington，2033',
                       postcode='2033', longtitude='151.2238032', altitude='-33.9031929',
                       price='130', type='apartment', bedroom=1, guest=4, wifi=True, parking=True, tv=True, bathroom=True, owner_id=admin.id,
                       description="<p>4 guests  1 bedroom  2 beds  1 bathroom</p>" + \
                                   "<p>This apartment is ideal for those on holiday, family visit and work trip. Walk to Centennial Park or Watch the NRL's Sydney Roosters, A-League powerhouse Sydney FC & NSW Super Rugby! It can accommodate 2-4 adults, with a Queen size bed in the bedroom and a sofa bed in the living area. Linen and towels are included. For those who drives, there is a private underground parking lot in the Building.</p>")
        a8 = Apartment(a_name='Savour Minimal, Designer Style in a Heritage-listed Terrace',
                       location='surry hills',
                       address='54 Cooper St, Surry Hills, New South Wales, Australia',
                       postcode='2010', longtitude='151.2101872',altitude='-33.8857102',
                       price='132', type='loft', bedroom=1, guest=2, wifi=True, parking=False, tv=True, bathroom=True,owner_id=user.id,
                       description="<p>2 guests  1 bedroom  1 bed  1 bath</p>" + \
                                   "<p>Entire apartment</p>" + \
                                   "<p>A uniquely spacious 1 bedroom flat — it is 1 of 2 flats in a charming heritage listed terrace nestled on a lovely residential street in Sydney's hippest hood. Your home away from home flows over the entire ground floor and you will have exclusive access to your own stylishly designed apartment with slouchy leather lounges, custom designed lighting and thoughtful design throughout.</p>")
        a9 = Apartment(a_name='Cosy 11th floor apartment in the heart of Sydney',
                       location='surry hills',
                       address='4 Little Riley St, New South Wales, Australia',
                       postcode='2010', longtitude='151.2132994', altitude='-33.8806270',
                       price='82', type='apartment', bedroom=1, guest=2, wifi=True, parking=False, tv=True, bathroom=True, owner_id=user.id,
                       description="<p>2 guests  1 bedroom  1 bed  1 bath</p>" + \
                                   "<p>Entire apartment</p>" + \
                                   "<p>Cosy 11th floor studio apartment close to Oxford Street. Walking distance to Hyde Park, surrounded by cafes, bars and restaurants. 7 minutes walk form Museum train station and 2 minutes walk for many bus stops. Entire private use of the apartment including kitchen and bathroom. Rooftop pool and terrace access on level 14 until midnight. Shared access to communal laundry for the building.</p>")
        a10 = Apartment(a_name='Architect Designed Private Studio',
                        location='Redfern',
                        address='767 Maddison Ln, Redfern New South Wales, Australia',
                        postcode='2016', longtitude='151.2157247',altitude='-33.8949822',
                        price='100', type='apartment', bedroom=1, guest=2, wifi=True, parking=False, tv=True, bathroom=True, owner_id=u1.id,
                        description="<p>2 guests  1 bedroom  1 bed  1 bath</p>" + \
                                    "<p>Latest news, just updated the bed to a queen sized bed. With brand new mattress and linen. Also, if there is more than one guest, please specify the amount of guests when requesting to book. Thank you. The Studio is your escape pad in the heart of Redfern / Surry Hills. Architecturally designed. Where industrial and urban combine to give a true inner city experience. Surrounded by wonderful parks and amenities. Close to transport. Walk everywhere</p>")
        a11 = Apartment(a_name='❤️Character Filled, Cosy Federation Terrace Home❤️',
                        location='Redfern',
                        address='28 Marriott St, Redfern, New South Wales, Australia',
                        postcode='2016', longtitude='151.2112483', altitude='-33.8923530',
                        price='65', type='house', bedroom=2, guest=6, wifi=True, parking=True, tv=True, bathroom=True, owner_id=u2.id,
                        description="<p>6 guests  2 bedrooms  3 beds  1 bath</p>" + \
                                    "<p>STAY LIKE A LOCAL. Discover the essence and secrets of Redfern & Surry Hills like locals do. If you enjoy living in a house where it is filled with characters then you won't disappoint!</p>")
        a12 = Apartment(a_name='Spacious Airy Apartment',
                        location='Redfern',
                        address='85 Redfern St,Redfern, New South Wales, Australia',
                        postcode='2016', longtitude='151.2046664', altitude='-33.8930867',
                        price='31', type='apartment', bedroom=1, guest=1, wifi=True, parking=False, tv=False, bathroom=True, owner_id=admin.id,
                        description="<p>1 guest  1 bedroom  1 bed  1 shared bath</p>" + \
                                    "<p>Private room in apartment</p>" + \
                                    "<p>The place is wonderfully situated in close proximity to Redfern station but just tucked in a quiet corner, allowing for both access to Sydney and comfortable, undisturbed sleep. It is also just a few blocks away from Woolies, so grocery shopping is no issue.</p>")
        a13 = Apartment(a_name='Luxury designer 2 bedrooms Apt @syd Olympic Park',
                        location='Sydney olympic park',
                        address='4 Herb Elliott Ave, Sydney Olympic Park, New South Wales, Australia',
                        postcode='2127', longtitude='151.0707466', altitude='-33.8477265',
                        price='185', type='apartment', bedroom=2, guest=6, wifi=True, parking=False, tv=True, bathroom=True,owner_id=user.id,
                        description="<p>Complimentary tea and coffee for our guests. *5star two bedrooms high level luxury apartment *modern designer home for everyone *iconic Australia tower with amazing city views *two queen size beds and two additional single beds available *can accommodate up to 6 people *easy access to every event, transport and major facilities in Sydney Olympic Park</p>")
        a14 = Apartment(a_name='l21 ”Amazing Sky view”Sydney Olympic Park”2bedroom',
                        location='Sydney olympic park',
                        address='1 Bennelong Pkwy, Sydney Olympic Park, New South Wales, Australia',
                        postcode='2127', longtitude='151.0741738', altitude='-33.8488338',
                        price='70', type='apartment', bedroom=2, guest=5, wifi=True, parking=True, tv=True, bathroom=True, owner_id=u1.id,
                        description="<p>*Sydney olympic park / 2 bedroom / free parking Come and experience the relaxing Australian lifestyle and urban oasis that is Sydney Olympic Park. We are centrally located right in the geographic heart of the Greater Sydney Metropolitan area with world class amenities right at your door step.<p/>")
        a15 = Apartment(a_name='Stunning views, great location, close to the CBD',
                        location='Balmain',
                        address='13 Gilchrist Pl, Balmain, New South Wales, Australia.',
                        postcode='2041', longtitude='151.1906512', altitude='-33.8560522',
                        price='60', type='apartment', bedroom=1, guest=2, wifi=True, parking=False, tv=True, bathroom=True, owner_id=u2.id,
                        description="<p>Private room with a queen size bed (shared bathroom and a second toilet) in a top floor apartment, ( the whole top floor ), 2 minutes walk to Balmain high street with lots of restaurants and cafes. You’ll love my place - the views are absolutely stunning - Cockatoo Island and the top of the Sydney Harbour Bridge. My place is good for couples, solo adventurers, and business travelers. The room can take a maximum of 2 people - there is a single mattress if you want to sleep separately.</p>")
        # add the data to the session
        db.session.add_all([a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15])
        db.session.flush()

        # add order to database
        o1 = Order(user_id= u1.id, apartment_id= a1.id, checkin_date=date.today(), checkout_date= date.today()+ timedelta(days= 7), status=0)
        o2 = Order(user_id= u2.id, apartment_id= a1.id, checkin_date= date.today()+timedelta(days=10), checkout_date= date.today() + timedelta(days= 11), status= 1)
        db.session.add_all([o1, o2])
        # add review to database
        r1 = Review(score= 3, user_id= u1.id, apartment_id= a1.id, content='Absolutely incredible hosts. Went out of their way to help me out and gave me some valuable info about some of the must see things in Sydney.')
        r2 = Review(score= 4, user_id= u2.id, apartment_id= a1.id, content='Great little place to stay in Sydney. It was very clean and nicely decorated.')
        db.session.add_all([r1, r2])
        db.session.flush()

        # add messages to database
        m1 = Message(content='test01', from_id= u1.id, to_id= u2.id)
        m2 = Message(content='test 02', from_id= admin.id, to_id= u2.id)
        db.session.add_all([m1, m2])
        db.session.flush()
        m3 = Message(content='test reply to test01', from_id= u2.id, to_id=u1.id, parent_id= m1.id)
        m4 = Message(content='test reply to test02', from_id= u2.id, to_id=admin.id, parent_id= m2.id)
        db.session.add_all([m3, m4])

        # commit the data to the database
        db.session.commit()