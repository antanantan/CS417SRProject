from flask import Flask, flash, jsonify, g, request, session
from flask_cors import CORS
import os, sqlite3, folium, pandas
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from database.db_models import db


app = Flask(__name__)
app.secret_key = '1nC0mPr3h3nS1b13-But-D3l1b3r@t3!' 
bcrypt = Bcrypt(app)

CORS(app, resources={r'/*': {'origins': '*'}})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
DATABASE = os.path.join(BASE_DIR, "database", "db.sqlite3")
SCHEMA = os.path.join(BASE_DIR, "database", "schema.sql")

if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')

# function to get database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# if database doesn't exist, create database
def create_db():    
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True) 
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    # create database by reading schema.sql
    with open(SCHEMA, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    db.commit()
    db.close()
create_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

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
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

    existing_user = cursor.fetchone()
    if existing_user:
        db.close()
        return jsonify({"message": "username already taken. please choose a different one."}), 401

    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
        db.commit()
        db.close()
        return jsonify ({"message": "account created successfully."}), 200
    except sqlite3.Error:   
        db.close()
        return jsonify ({"message": "error."})

# function for handling login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    db.close()  

    if user:
        stored_password_hash = user[2] 
        if bcrypt.check_password_hash(stored_password_hash.strip("'"), password):
            session['user_id'] = user[0]
            return jsonify ({"message": "user logged in successfully."}), 200
        else:
            return jsonify ({"message": "incorrect password."}), 401
    else:
        flash("username not found. please register first.")
        return jsonify ({"message": 'username not found. please register first.'}), 404
        
# function to handle user logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return jsonify ({"message": "you have been logged out."}), 200

# i wonder if we have to declare this every time we want to pull profile information for the user? TBA but it's here for now as a test function at least
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT username FROM users WHERE id = ?", (session['user_id'],))
        user = cursor.fetchone()
        db.close()

        if user:
            return jsonify({"username": user[0]}), 200 
        else:
            return jsonify({"message": "user not found."}), 404  
    else:
        return jsonify({"message": "not logged in."}), 401


# TODO: implement password reset function | take the user's email, check if it exists, and allow them to change their password.
#       not the most secure method right now but at least that page will have something to do on it
"""
@app.route('/password_reset', methods=['POST'])
def password_reset():
    data = request.get_json()
    email = data.get('email')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    db.close()  

    if user:
        stored_password_hash = user[2] 
        new_password = flash("enter new password")
        password = new_password
    else:
        flash("email not found.")
        return jsonify ({"message": 'email not found.'}), 404
"""







# TODO: link allergen information to profile 
@app.route('/add_allergy', methods=['POST'])
def add_allergy():
    username = request.form['username']
    allergies = request.form.get['allergies']
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user == user[0]:
        for allergy in allergies:
            cursor.execute("INSERT into allergies (username, allergy) VALUES (?, ?)", (username, allergies))
            db.commit()

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