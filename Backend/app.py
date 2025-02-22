from flask import Flask
from datetime import timedelta
from flask import flash, jsonify, g, request, session, make_response
from flask_cors import CORS
import os, sqlite3, folium, pandas
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from database.db_models import db, User, AllergenGroup, Allergen, UserAllergy, Restaurant, Menu
from database.seed_data import seed_db

app = Flask(__name__)

app.config['SECRET_KEY'] = '1nC0mPr3h3nS1b13-But-D3l1b3r@t3!' 
app.config['JWT_SECRET_KEY'] = '@1S0_1nC0mPr3h3nS1b13-But-D3l1b3r@t3!'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# initialize extensions
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

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
@app.route('/register', methods=['GET', 'POST'])
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
@app.route('/login', methods=['POST'])
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
@app.route('/profile', methods=['GET'])
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
@app.route('/logout', methods=['POST'])
@jwt_required() # user must be logged in to log out
def logout():
    return jsonify ({"message": "you have been logged out."}), 200 # frontend token gets deleted from local storage and redirect to login page

# TODO: implement password reset function | take the user's email, check if it exists, and allow them to change their password.
#       not the most secure method right now but at least that page will have something to do on it
@app.route('/password_reset', methods=['POST'])
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

    if not zip_code:
        return jsonify({"error": "please enter a valid zip code"}), 400
    try:
        geolocator = Nominatim(user_agent="app")
        location = geolocator.geocode(f"{zip_code}, {country}")
        if not location:
            return jsonify({"error": "Could not find location for the given zip code."}), 400
        
        map = folium.Map(location=[location.latitude, location.longitude], zoom_start=12)

# marker for the initial zip code, but no need if the restaurants are already marked --> folium.Marker([location.latitude, location.longitude]).add_to(map)

# adjust as needed
        restaurants = Restaurant.query.filter(
            Restaurant.latitude.between(location.latitude - 0.1, location.latitude + 0.1),
            Restaurant.longitude.between(location.longitude - 0.1, location.longitude + 0.1)
        ).all()

        for restaurant in restaurants:
            restaurant_location = [restaurant.latitude, restaurant.longitude]
            restaurant_info = f"<b>{restaurant.name}</b><br>{restaurant.address}<br>Phone: {restaurant.phone if restaurant.phone else 'N/A'}"
            
            folium.Marker(
                restaurant_location,
                popup=folium.Popup(restaurant_info, max_width=300)
            ).add_to(map)

        map_path = os.path.join('static', 'map.html')

        map.save(map_path)
        print("request received!")

        response = jsonify({"map_url": "/static/map.html"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# TODO: link allergen information to profile. implementation is *almost* there, just need to ensure that the allergen list is properly saved to a unique user.
# TODO: implement a guest login function
@app.route('/generate_list', methods=['GET'])
def generate_list():
    allergens = Allergen.query.all()
    allergy_data = [
        {
            "id": allergen.id,
            "name": allergen.name,
            "selected": False,  
            "severity": None  
        }
        for allergen in allergens]
    return jsonify({"allergies": allergy_data}), 200

@app.route('/save_allergy', methods=['POST'])
@jwt_required()  
def save_allergy():
    user_id = get_jwt_identity()  
    if not user_id:
        return jsonify({"message": "Not logged in."}), 404  

    data = request.get_json()
    print("Received data:", data)
    
    allergies = data.get('allergies') 
    if not allergies:
        return jsonify({"message": "No allergies data found."}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404
    UserAllergy.query.filter_by(user_id=user.id).delete()
    db.session.commit()

# add new allergy information
    for allergy in allergies:
        allergy_name = allergy.get("name")
        scale = allergy.get("scale", '')  
        if scale == None:
            continue
        if scale not in [0, 1, 2, 3]: 
            return jsonify({"message": f"Invalid scale value: {scale}. Allowed values are 0, 1, 2, 3."}), 400

        allergen = Allergen.query.filter_by(name=allergy_name).first()

        if allergen:
            user_allergy = UserAllergy(user_id=user.id, allergen_id=allergen.id, scale=scale)
            db.session.add(user_allergy)

    db.session.commit()
    return jsonify({"message": "Allergy information updated successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')




# ref: CS312, https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
# ref: https://flask.palletsprojects.com/en/stable/patterns/flashing/