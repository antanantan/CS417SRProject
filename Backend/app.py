from flask import Flask
from datetime import timedelta, datetime
from flask import flash, jsonify, g, request, session, make_response, url_for
from flask_cors import CORS, cross_origin
import os, sqlite3, folium, pandas, json, uuid
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt, decode_token
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from database.db_models import db, User, AllergenGroup, Allergen, UserAllergy, Restaurant, Menu, MenuOptionGroup, MenuOptionItem, MenuOptionMapping
from database.seed_data import seed_db

app = Flask(__name__)

app.config['SECRET_KEY'] = '1nC0mPr3h3nS1b13-But-D3l1b3r@t3!' 
app.config['JWT_SECRET_KEY'] = '@1S0_1nC0mPr3h3nS1b13-But-D3l1b3r@t3!'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# initialize extensions
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://127.0.0.1:3000", "http://localhost:3000"]}})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'db.sqlite3')}"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# link 'db' to the app 
db.init_app(app)

# initialize database
with app.app_context():
    db.create_all()
    seed_db()

if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return "Flask App is running!"

# function to close database connection
@app.teardown_appcontext
def close_connection(exception=None):
    db.session.remove()



guest_storage = {}

def set_guest_data(key, value):
    guest_storage[key] = {
        "value": value,
        "expires_at": datetime.now() + timedelta(hours=1)  
    }

# get guest data + delete if expired
def get_guest_data(key):
    data = guest_storage.get(key)
    if data and data["expires_at"] > datetime.now():
        return data["value"]
    elif data:
        del guest_storage[key]
    return None

#delete guest key
def del_guest_data(key):
    if key in guest_storage:
        del guest_storage[key]
        return True
    return False

def get_user_or_guest():
    try:
        jwt_data = get_jwt()
        user_id = get_jwt_identity()
        is_guest = jwt_data.get('is_guest', False)

        return {
            "user_id": user_id, 
            "is_guest": is_guest
        }
    except Exception as e:
        return{
            "user_id": None,
            "is_guest": False,
            "error": str(e)
        }


@app.route('/auth/guest', methods=['POST'])
def create_guest_session():
    #creates a unique id for the guest that just starts with guest tag
    guest_id = f'guest_{uuid.uuid4().hex}'

    token = create_access_token(identity=guest_id, expires_delta=timedelta(hours=1), additional_claims={"is_guest": True})

    return jsonify({
        "message": "Guest session created successfully.",
        "token": token,
        "is_guest": True
    }), 200

@app.route('/auth/check', methods=['GET'])
@jwt_required(optional=True)
def check_auth():
    try:
        identity = get_jwt_identity()

        if not identity:
            return jsonify({
                "authenticated": False,
                "is_guest": False,
            })
    
        jwt_data = get_jwt()
        is_guest = jwt_data.get('is_guest', False)
    
        return jsonify({
            "authenticated": True,
            "is_guest": is_guest
        }), 200

    except Exception as e:
        return jsonify({
            "authenticated": False,
            "is_guest": False,
            "error": str(e)
        }), 200


# function for handling account creation
@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    guest_token = data.get('guest_token')

    if not username or not email or not password:
        return jsonify({"message": "Missing required fields. Please try again."}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        if existing_user.email == email:
            return jsonify({"message": "Email already registered."}), 422
        if existing_user.username == username:
            return jsonify({"message": "Username already taken. Please choose a different one."}), 422
        
    try:
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        token = create_access_token(identity=str(new_user.id)) # creates a token for the new user:
        
        # add if converting from guest to transer allergies to new account
        if guest_token:
            try:
                #Extract guest ID from token
                guest_data = jwt.decode(guest_token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])

                guest_id = guest_data.get('sub')
                if guest_id:
                    # Get allergies from guest storage
                    guest_allergies = get_guest_data(f'guest_allergies:{guest_id}')
                    
                    if guest_allergies:
                        for allergy in guest_allergies:
                            allergen_id = allergy.get('allergen_id')
                            scale = allergy.get('scale', 0)  
                            
                            # Check if allergen exists in the database
                            allergen = db.session.get(Allergen, allergen_id)
                            if allergen:
                                ua = UserAllergy(user_id=new_user.id, allergen_id=allergen_id, scale=scale)
                                db.session.add(ua)
                            db.session.commit()

                    del_guest_data(f'guest_allergies:{guest_id}')  # Clear guest allergies after transfer
                    print(f'Successfully transferred allergies from guest {guest_id} to user {new_user.id}')
            except Exception as e:
                print(f'Error transferring allergies: {str(e)}')

        return jsonify({"message": "Account created successfully", 'token': token}), 201
          
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating account", "error": str(e)}), 500



# TODO: handle unique characters as appropriate and fix whatever this is



@app.route('/auth/login', methods=['POST'])
def login():
# pulling data from login form
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing required fields. Please try again."}), 400

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))

        return jsonify({"message": "user logged in successfully.", "token": access_token}), 200

    return jsonify({"message": "User not found. Please create an account first."}), 404

# function for pulling profile information from current session
@app.route('/user/profile', methods=['GET'])
@jwt_required() 
def profile():
    user_data = get_user_or_guest()

    if user_data["is_guest"]:
        guest_id = user_data["user_id"]
        guest_allergies = get_guest_data(f'guest_allergies:{guest_id}')
        allergies = []

        #gets allergy profile
        if guest_allergies:
            allergens_ids = [allergy.get('allergen_id') for allergy in guest_allergies]
            allergens = Allergen.query.filter(Allergen.id.in_(allergens_ids)).all()
            allergies = [allergen.name for allergen in allergens]
            
        return jsonify({
            "username": "Guest",
            "email": "",
            "allergies": allergies,
            "is_guest": True,
        }), 200

    #normal user
    else: 
        user_id = user_data["user_id"]
        user = db.session.get(User, user_id)

        if user:
            allergies = db.session.query(Allergen.name).join(UserAllergy).filter(UserAllergy.user_id == user_id).all()
            allergy_list = [allergy[0] for allergy in allergies]
            
            return jsonify({
                "username": user.username,
                "email": user.email,
                "allergies": allergy_list,
                "is_guest": False,
            }), 200
        return jsonify({"message": "User not found."}), 404


# function to handle user logout
@app.route('/auth/logout', methods=['POST'])
@jwt_required() # user must be logged in to log out
def logout():
    user_data = get_user_or_guest()
    if user_data["is_guest"]:
        guest_id = user_data["user_id"]
        del_guest_data(f'guest_allergies:{guest_id}')
        del_guest_data(guest_id)
        return jsonify({"message": "Guest session ended."}), 200
    
    return jsonify ({"message": "you have been logged out."}), 200 # frontend token gets deleted from local storage and redirect to login page

@app.route('/user/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    user_data = get_user_or_guest()

    if user_data["is_guest"]:
        return jsonify({"message": "Guest accounts cannot be deleted."}), 403

    user_id = user_data["user_id"]
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"message": "User not found."}), 404
    
    try:
        UserAllergy.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Account deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting account.", "error": str(e)}), 500



# TODO: implement password reset function | take the user's email, check if it exists, and allow them to change their password.
#       not the most secure method right now but at least that page will have something to do on it
@app.route('/auth/password_reset', methods=['POST'])
def password_reset():
    data = request.get_json()
    email = data.get('email')  # don't we need username too?
    new_password = data.get('new_password')  # this is the new password the user wants to set

    if not email or not new_password:
        return jsonify({"message": "Missing required fields"}), 400
    
    user = User.query.filter_by(email=email).first()

    if user:
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password  # update password
        db.session.commit()  # save changes to database

        return jsonify({"message": "Password has been reset successfully."}), 200
    else:
        return jsonify({"message": "Email not found."}), 404

# function for handling zip code input
@app.route('/location', methods=['POST'])
def create_map(country='US'):
    zip_code = request.json.get('zip_code')
    cuisine = request.json.get('cuisine')

    if not zip_code:
        return jsonify({"error": "please enter a valid zip code"}), 400
    try:
        geolocator = Nominatim(user_agent="app")
        location = geolocator.geocode(f"{zip_code}, {country}")
        if not location:
            return jsonify({"error": "Could not find location for the given zip code."}), 400
        
        # map = folium.Map(location=[location.latitude, location.longitude], zoom_start=12)

# marker for the initial zip code, but no need if the restaurants are already marked --> folium.Marker([location.latitude, location.longitude]).add_to(map)

# adjust as needed
        restaurants = Restaurant.query.filter(
            Restaurant.latitude.between(location.latitude - 0.1, location.latitude + 0.1),
            Restaurant.longitude.between(location.longitude - 0.1, location.longitude + 0.1)
        ).all()

        if cuisine:
            query = query.filter_by(cuisine=cuisine)

        markers = [{
            'id': restaurant.id,
            'name': restaurant.name,
            'latitude': restaurant.latitude,
            'longitude': restaurant.longitude,
            'address': restaurant.address,
        } for restaurant in restaurants]
        return jsonify(markers)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        """
        for restaurant in restaurants:
            restaurant_location = [restaurant.latitude, restaurant.longitude]
            restaurant_info = f"<b>{restaurant.name}</b><br>{restaurant.address}<br>Phone: {restaurant.phone if restaurant.phone else 'N/A'}"
            
            folium.Marker(
                restaurant_location,
                popup=folium.Popup(restaurant_info, max_width=300),
                title=restaurant.name
            ).add_to(map)

            marker_data_script = f
            <script>
            setTimeout(function() {{
                var marker = document.querySelector('.leaflet-marker-icon[title="{restaurant.name.replace("'", "\\'")}"]');
                if (marker) {{
                    marker.addEventListener('click', function() {{
                        var markerData = {{
                            id: {restaurant.id},
                            name: '{restaurant.name.replace("'", "\\'")}',
                            address: '{restaurant.address.replace("'", "\\'")}'
                        }};
                        
                        fetch('/location_select', {{
                            method: 'POST',
                            headers: {{'Content-Type': 'application/json'}},
                            body: JSON.stringify(markerData)
                        }})
                        .then(response => response.json())
                        .then(data => {{console.log('Marker data received:', data);}})
                        .catch(error => {{console.error('Error sending marker data:', error);}});
                    }});
                }} else {{console.error('Marker not found with title: {restaurant.name}');}}
            }}, 500); 
            </script>
            
            map.get_root().html.add_child(folium.Element(marker_data_script))

        map_path = os.path.join('static', 'map.html')

        map.save(map_path)
        print("request received!")

        response = jsonify({"map_url": "/static/map.html"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200"
    """
    
@app.route('/location_select', methods=['POST'])
def handle_marker_selection():
    print("Location select route hit!")
    try:
        data = request.json  
        if not data:
            return jsonify({"error": "No data received"}), 400
        print(f"Received marker data: {data}") 
        return jsonify({
            "status": "success",
            "selected_marker": data
        }), 200 
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while processing the data."}), 500

# TODO: link allergen information to profile. implementation is *almost* there, just need to ensure that the allergen list is properly saved to a unique user.

@app.route('/allergens', methods=['GET'])
@cross_origin(origins="http://localhost:3000")
def get_allergens():
    allergen_groups = [
        {"id": group.id, "name": group.name} for group in AllergenGroup.query.all()
    ]
    
    allergen_items = [
        {"id": allergen.id, "name": allergen.name, "group_id": allergen.group_id}
        for allergen in Allergen.query.all()
    ]

    return jsonify({"allergen_groups": allergen_groups, "allergen_items": allergen_items}), 200


@app.route('/user/allergies', methods=['GET', 'POST'])
@jwt_required()
def user_allergies():
    user_data = get_user_or_guest()
    user_id = user_data["user_id"]
    is_guest = user_data["is_guest"]

    if request.method == 'GET':

        if is_guest:
            #checks for guest user's allergies which is stored in temp storage
            guest_allergies = get_guest_data(f'guest_allergies:{user_id}')
            if guest_allergies:
                #adds allergy names 
                result = []
                for allergy in guest_allergies:
                    allergen_id = allergy.get('allergen_id')
                    allergen = db.session.get(Allergen, allergen_id)
                    if allergen:
                        result.append({
                            'allergen_id': allergen.id,
                            'name': allergen.name,
                            'scale': allergy.get('scale', 0)
                        })
                return jsonify(result), 200
            return jsonify([]), 200
        
        # normal user, check db
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"message": "Not logged in or user not found."}), 404
        
        #retrieve allergies 
        allergies = (
            db.session.query(UserAllergy, Allergen)
            .join(Allergen, UserAllergy.allergen_id == Allergen.id) 
            .filter(UserAllergy.user_id == user.id)
            .all()
        )
        result = [
            {
                'allergen_id': allergen.id,
                'name': allergen.name,
                'scale': ua.scale
            }
            for ua, allergen in allergies
        ]
        return jsonify(result), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        print("Received data:", data)
        allergies = data.get('allergies') 
        if allergies is None:
            return jsonify({"message": "No allergies data found."}), 400

        if len(allergies) == 0:
            if is_guest:
                #clear temp storage
                del_guest_data(f'guest_allergies:{user_id}')
            else:
                #clear from db for normal users
                user = db.session.get(User, user_id)
                if not user:
                    return jsonify({"message": "User not found."}), 404 
                UserAllergy.query.filter_by(user_id=user.id).delete()
                db.session.commit()
            return jsonify({"message": "Allergy information cleared."}), 200

        if is_guest:
            valid_allergies = []  
            # store allergies in temp storage 
            for allergy in allergies:
                allergen_id = allergy.get("allergen_id")
                scale = allergy.get("scale", 0)  

                if allergen_id is None:
                    continue

                if scale not in [0, 1, 2, 3]:
                    return jsonify({"message": f"Invalid scale value: {scale}. Allowed values are 0, 1, 2, 3."}), 400
                
                allergen = db.session.get(Allergen, allergen_id)
                if allergen:
                    valid_allergies.append({
                        "allergen_id": allergen_id,
                        "scale": scale
                    })
            #store valid allergies for guest 
            set_guest_data(f'guest_allergies:{user_id}', valid_allergies)
            return jsonify({"message": "Allergy information updated successfully."}), 200
        else:
            # normal user, store allergies
            user = db.session.get(User, user_id)
            if not user:
                return jsonify({"message": "User not found."}), 404
            
            #clears existing allergies to replace with new ones
            UserAllergy.query.filter_by(user_id=user.id).delete() 
                
            #add new allergy info
            try:
                for allergy in allergies:
                    allergen_id = allergy.get("allergen_id")
                    scale = allergy.get("scale", '')  
                    if allergen_id is None or scale is None:
                        continue
                    if scale not in [0, 1, 2, 3]: 
                        return jsonify({"message": f"Invalid scale value: {scale}. Allowed values are 0, 1, 2, 3."}), 400

                    allergen = db.session.get(Allergen, allergen_id)
                    if allergen:
                        ua = UserAllergy(user_id=user.id, allergen_id=allergen_id, scale=scale)
                        db.session.add(ua)

                db.session.commit()
                print("Committed successfully. Allergies count:", UserAllergy.query.filter_by(user_id=user.id).count())
                return jsonify({"message": "Allergy information updated successfully."}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": "Error updating allergy information.", "error": str(e)}), 500    


# endpoint for getting menu information
# later change it to '/menu/<restaurant_id>
@app.route('/menu', methods=['GET'])
@cross_origin(origins="http://localhost:3000")
def get_menu():
    restaurant = Restaurant.query.filter_by(name="JP's Diner").first()
    
    if not restaurant:
        return jsonify({"error": "JP's Diner not found"}), 404

    #checks for user allergies if authenticated
    user_allergens = []
    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Bearer '):
        try:
            token = auth_header.split(' ')[1]

        #verify and decode token
            user_data = None
            try:    
                user_data = decode_token(token)
                user_id = user_data.get('sub')
                is_guest = user_data.get('is_guest', False)

                if is_guest:
                    guest_allergies = get_guest_data(f'guest_allergies:{user_id}')
                    if guest_allergies:
                        #process guest allergies for filtering
                        for allergy in guest_allergies:
                            allergen_id = allergy.get('allergen_id')
                            allergen = db.session.get(Allergen, allergen_id)
                            if allergen:
                                user_allergens.append({
                                    'name': allergen.name,
                                    'scale': allergy.get('scale', 0)
                                })
                else:
                    #regular user 
                    user_allergies = UserAllergy.query.filter_by(user_id=user_id).all()
                    for ua in user_allergies:
                        allergen = db.session.get(Allergen, ua.allergen_id)
                        if allergen:
                            user_allergens.append({
                                'name': allergen.name,
                                'scale': ua.scale
                            })
            except Exception as e:
                return jsonify({"error": f"Error decoding token: {str(e)}"}), 401
        except Exception as ef:
            return jsonify({"error": "Error decoding token"}), 401

    menu_items = Menu.query.filter_by(restaurant_id=restaurant.id).all()
    menu_list = []


    for item in menu_items:
        # get all option mappings for the menu item
        option_mappings = MenuOptionMapping.query.filter_by(menu_id=item.id).all()
        
        # change option mappings to a dictionary for easier access
        option_groups = {}
        for mapping in option_mappings:
            option_group = MenuOptionGroup.query.get(mapping.option_group_id)
            if not option_group:
                continue
            
            # make option items a list for each group
            if option_group.description not in option_groups:
                option_groups[option_group.description] = []
            
            option_items = MenuOptionItem.query.filter_by(group_id=option_group.id).all()
            for option_item in option_items:
                option_groups[option_group.description].append({
                    "name": option_item.name,
                    "extra_price": option_item.extra_price
                })

        menu_list.append({
            "id": item.id,
            "name": item.name,
            "category": item.category if item.category else None,
            "sub_category": item.sub_category if item.sub_category else None,
            "price": item.price,
            "ingredients": item.ingredients.split(", ") if item.ingredients else [],
            "allergens": item.allergens.split(", ") if item.allergens else [],
            "description": item.description if item.description else None,
            "image": url_for('static', filename=f"menu_img/{item.image_filename}", _external=True) if item.image_filename else None,
            "options": option_groups  # put a list of option items for each group
        })

    # calculate open status for the restaurant
    try:
        hours = json.loads(restaurant.hours) if restaurant.hours else {}
    except json.JSONDecodeError:
        hours = {}
    today = datetime.today().strftime('%A')
    current_time = datetime.now().strftime('%I:%M %p')
    status = "Closed"
    if isinstance(hours, dict) and today in hours and "Closed" not in hours[today]:
        try:
            open_time, close_time = hours[today].split(" - ")
            if open_time <= current_time <= close_time:
                status = f"Open, Closes {close_time}"
            else:
                status = f"Closed, Opens {open_time}"
        except ValueError:
            status = "Unknown hours format"

    return jsonify({
        "restaurant": {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "phone": restaurant.phone,
            "category": restaurant.category if restaurant.category else None,
            "price_range": restaurant.price_range if restaurant.price_range else None,
            "hours": json.dumps(hours),
            "status": status,
            "image": url_for('static', filename=f"restaurant_img/{restaurant.image_filename}", _external=True) if restaurant.image_filename else None
        },
        "menu": menu_list
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




# ref: CS312, https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
# ref: https://flask.palletsprojects.com/en/stable/patterns/flashing/