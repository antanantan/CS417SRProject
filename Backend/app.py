from flask import Flask, flash, jsonify, g, redirect, request, send_from_directory, session, url_for
from flask_cors import CORS
import os, sqlite3, json
from flask_bcrypt import Bcrypt
import base64

# NOTE: testing app.py functionality with map inputs
import folium
from geopy.geocoders import Nominatim

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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_db():    
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True) 
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
            allergy_data TEXT
        )
    ''')
    db.commit()
    db.close()

# TODO: based on this framework, get the application to accept input of a username and password, store it in a database, and be able to associate an allergy profile with that signed-in user

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

def get_data(username): 
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('''
        SELECT form_data FROM form_data WHERE username = ?
    ''', (username,))
    result = cursor.fetchone()
    db.close()
    return json.loads(result[0]) if result else None
  

if not os.path.exists('static'):
    os.makedirs('static')

# NOTE: for testing backend functionality with the map function. will have to deal with exceptions once basic functionality is go
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


@app.route('/create', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            db.commit()
            return redirect(url_for('/profile'))
        except sqlite3.IntegrityError:
            flash('username already taken. please choose a different one.')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user[2], password):
            session['username'] = username
            return redirect("/profile")
        else:
            flash('invalid credentials. please try again.')
            return redirect(url_for('/login'))
        
# TODO: consider putting allergen profile handling informaiton in a separate python file

@app.route('/addAllergy', methods=['POST'])
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
@app.route('/removeAllergy', methods=['POST'])
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