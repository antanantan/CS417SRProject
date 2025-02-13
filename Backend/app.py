from flask import Flask, flash, jsonify, g, request, session
from flask_cors import CORS
import os, sqlite3, folium, pandas
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from database.db_models import db, User, AllergenGroup, Allergen, UserAllergy, Restaurant, Menu
from database.seed_data import seed_db


app = Flask(__name__)
app.secret_key = '1nC0mPr3h3nS1b13-But-D3l1b3r@t3!' 
bcrypt = Bcrypt(app)


CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True) # supports_credentials allows for cookies and auth headers to be passed


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'db.sqlite3')}"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# link 'db' to the app
db.init_app(app)

if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return "Flask App is running!"

# initialize database
with app.app_context():
    db.create_all()
    seed_db()

# function to close database connection
@app.teardown_appcontext
def close_connection(exception=None):
    db.session.remove()

# function for handling zip code input
@app.route('/location', methods=['POST'])
def create_map(country='US'):
    zip_code = request.json.get('zip_code')

    if not zip_code:
        return jsonify({"error": "please enter a valid zip code"}), 400

    geolocator = Nominatim(user_agent="app")
    location = geolocator.geocode(f"{zip_code}, {country}")
    
    map = folium.Map(location=[location.latitude, location.longitude], zoom_start=12)
        
    folium.Marker([location.latitude, location.longitude]).add_to(map)

    map_path = os.path.join('static', 'map.html')

    map.save(map_path)
    print("request received!")

    response = jsonify({"map_url": "/static/map.html"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
# we'd have to find a database of restaurants and their coordinates!


# function for handling account creation
@app.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"message": "username already taken. please choose a different one."}), 401

    try:
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Account created successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating account", "error": str(e)}), 500

# function for handling login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing required fields"}), 400

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id  # save user id in session
        return jsonify({"message": "user logged in successfully."}), 200
    elif user:
        return jsonify({"message": "Incorrect password."}), 401
    else:
        flash("Username not found. Please register first.")
        return jsonify({"message": "Username not found. Please register first."}), 404


# function to handle user logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return jsonify ({"message": "you have been logged out."}), 200


# i wonder if we have to declare this every time we want to pull profile information for the user? TBA but it's here for now as a test function at least
@app.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')  # get user id from cookie session
    if not user_id:
        return jsonify({"message": "Not logged in."}), 401

    user = User.query.get(user_id)

    if user:
        return jsonify({"username": user.username, "email": user.email}), 200
    else:
        return jsonify({"message": "User not found."}), 404


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


# TODO: link allergen information to profile
# TODO: implement a guest login function
# TODO: it might be expensive to save the changes every time a user adds an allergen -> save the changes in a session and then commit them all at once?
@app.route('/save_allergy', methods=['POST'])
def save_allergy():
    user_id = session.get('user_id')  # get user id from cookie session

    if not user_id:
        return jsonify({"message": "Not logged in."}), 401  # user not logged in

    data = request.get_json()
    allergies = data.get('allergies')  # a list like [{ "name": "Almond", "scale": 2 }, { "name": "Milk", "scale": 1 }]

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    # reset user's allergy information
    UserAllergy.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    # if the user has no allergies, return success message
    if not allergies:
        return jsonify({"message": "Allergy information cleared."}), 200

    # add new allergy information
    for allergy in allergies:
        allergy_name = allergy.get("name")
        scale = allergy.get("scale", 2)  # default scale value is 2 (moderate)

        if scale not in [0, 1, 2, 3]:  # check if scale value is valid
            return jsonify({"message": f"Invalid scale value: {scale}. Allowed values are 0, 1, 2, 3."}), 400

        allergen = Allergen.query.filter_by(name=allergy_name).first()

        if allergen:
            user_allergy = UserAllergy(user_id=user.id, allergen_id=allergen.id, scale=scale)
            db.session.add(user_allergy)

    db.session.commit()  # save changes to database
    return jsonify({"message": "Allergy information updated successfully."}), 200


# remove allergy

"""
@app.route('/remove_allergy', methods=['POST'])
def remove_allergy():
    username = request.form['username']
    allergies = request.form.get['allergies']

 # not really sure how to change this code right now   

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user_id == user[0]:
        for allergy in allergies:
            cursor.execute("INSERT into allergies (username, allergy) VALUES (?, ?)", (username, allergies))
            db.commit()
"""



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')




# ref: CS312, https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
# ref: https://flask.palletsprojects.com/en/stable/patterns/flashing/