from flask import Flask
from datetime import timedelta, datetime
from flask import flash, jsonify, g, request, session, make_response, url_for
from flask_cors import CORS, cross_origin
import os, sqlite3, folium, pandas, json
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
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

# function for handling account creation
@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

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

        token = create_access_token(identity=str(new_user.id)) # creates a token for the new user

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
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)  
    if user:
        allergies = db.session.query(Allergen.name).join(UserAllergy).filter(UserAllergy.user_id == user_id).all()
        allergy_list = [allergy[0] for allergy in allergies]
        
        return jsonify({
            "username": user.username,
            "email": user.email,
            "allergies": allergy_list
        }), 200
    return jsonify({"message": "User not found."}), 404

# function to handle user logout
@app.route('/auth/logout', methods=['POST'])
@jwt_required() # user must be logged in to log out
def logout():
    return jsonify ({"message": "you have been logged out."}), 200 # frontend token gets deleted from local storage and redirect to login page

@app.route('/user/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
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
            return jsonify({"error": "could not find location for the given zip code."}), 400
    
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
        if markers:
            print(f"Markers: {markers}")
            return jsonify(markers)
        else:
            return "no marker data for this zip code.", 200

    
    except Exception as e:
        return jsonify({"error": f"an error occurred: {str(e)}"}), 500
    
# option to save selected marker for future use
selected_marker = {}

@app.route('/location_select', methods=['POST'])
def handle_marker_selection():
    try:
        data = request.json  
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        print(f"received marker data: {data}") 

        # Save the selected marker data
        selected_marker['address'] = data.get('address')
        selected_marker['id'] = data.get('id')
        selected_marker['latitude'] = data.get('latitude')
        selected_marker['longitude'] = data.get('longitude')
        selected_marker['name'] = data.get('name') 

        # Directly return the selected marker as a response
        return jsonify({
            "status": "success",
            "selected_marker": selected_marker
        }), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while processing the data."}), 500

# Route to retrieve the selected location (for menu page)
@app.route('/send_location', methods=['GET'])
def get_selected_location():
    print("! send location route hit")
    try:
        if not selected_marker:
            return jsonify({"error": "No marker selected yet"}), 404
        
        return jsonify({
            "status": "success",
            "selected_marker": selected_marker
        }), 200 

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while fetching the data."}), 500


# TODO: implement a guest login function
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
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "Not logged in or user not found."}), 404

    if request.method == 'GET':
        # return allergen names
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

        UserAllergy.query.filter_by(user_id=user.id).delete()
        # db.session.commit()

        # if new allergies list is empty
        if len(allergies) == 0:
            db.session.commit()
            return jsonify({"message": "Allergies cleared."}), 200

        # add new allergy information
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

# endpoint for getting menu information
@app.route('/menu/<restaurant_id>', methods=['GET'])
@cross_origin(origins="http://localhost:3000")
def get_menu(restaurant_id):
    print(f"Fetching menu for restaurant_id: {restaurant_id}")  # Debugging line to check if the ID is received

    # Query restaurant by ID
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()

    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    # Fetch the menu items for the restaurant
    menu_items = Menu.query.filter_by(restaurant_id=restaurant.id).all()
    menu_list = []

    # Process menu items
    for item in menu_items:
        option_mappings = MenuOptionMapping.query.filter_by(menu_id=item.id).all()
        option_groups = {}

        for mapping in option_mappings:
            option_group = MenuOptionGroup.query.get(mapping.option_group_id)
            if not option_group:
                continue
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
            "options": option_groups
        })

    return jsonify({
        "restaurant": {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "phone": restaurant.phone,
            "category": restaurant.category if restaurant.category else None,
            "price_range": restaurant.price_range if restaurant.price_range else None,
            "hours": restaurant.hours,
            "status": "Open/Closed status here",  # You can calculate status here if needed
            "image": url_for('static', filename=f"restaurant_img/{restaurant.image_filename}", _external=True) if restaurant.image_filename else None
        },
        "menu": menu_list
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




# ref: CS312, https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
# ref: https://flask.palletsprojects.com/en/stable/patterns/flashing/