from flask import Flask, flash, jsonify, g, redirect, request, send_from_directory, session, url_for
from flask_cors import CORS
import os, sqlite3, json
from flask_bcrypt import Bcrypt
import folium
from geopy.geocoders import Nominatim
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


app = Flask(__name__)
app.secret_key = '1nC0mPr3h3nS1b13-But-D3l1b3r@t3!' 
bcrypt = Bcrypt(app)

CORS(app, resources={r'/*': {'origins': '*'}})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
DATABASE = os.path.join(BASE_DIR, "profiles.db")

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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            allergy_data TEXT
        )
    ''')
    db.commit()
    db.close()

create_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if not os.path.exists('static'):
    os.makedirs('static')

# function for handling location feature (DONE)
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
        return jsonify({"message": "username already taken. please choose a different one."})

    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
        db.commit()
        db.close()
        return jsonify ({"message": "account created successfully."})
    except sqlite3.Error:   
        db.close()
        return jsonify ({"message": "error."})
    

"""
may or may not use this script
def insert_data(username, form_data):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    form_data_json = json.dumps(form_data)  
    cursor.execute('''
        INSERT OR REPLACE INTO form_data (username, form_data)
        VALUES (?, ?)
    ''', (username, form_data_json))
    db.commit()
    db.close()
"""



@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        db.close()  

        if user:
            stored_password_hash = user[2] 
            if bcrypt.check_password_hash(stored_password_hash, password):
                session['username'] = username  
                return redirect("/profile")  
            else:
                flash('invalid credentials. please try again.')
                return redirect("/login") 
        else:
            flash('username not found. please register first.')
            return redirect("/create")
        

# TODO: consider putting allergen profile handling information in a separate python file

@app.route('/add_allergy', methods=['POST'])
def add_allergy():
    username = request.form['username']
    allergies = request.form.get['allergies']
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user_id == user[0]:
        for allergy in allergies:
            cursor.execute("INSERT into allergies (username, allergy) VALUES (?, ?)", (username, allergies))
            db.commit()

#remove allergy

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