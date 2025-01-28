from flask import Flask, flash, jsonify, g, redirect, request, send_from_directory, session, url_for
from flask_cors import CORS
import os, sqlite3, json
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = '1nC0mPr3h3nS1b13-But-D3l1b3r@t3!' 
bcrypt = Bcrypt(app)

CORS(app, resources={r'/*': {'origins': '*'}})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
DATABASE = os.path.join(BASE_DIR, "profiles.db")


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
  
# for generating and displaying the map generated by map.py using folium library

@app.route('../frontend/src/assets/map.html') # i don't know if that route is correct
def serve_map(filename):
    return send_from_directory(os.path.join(app.root_path, 'maps'), filename)

# TODO: allow the site to accept zip code input via form, save that information to the user's profile, and generate a new map based on the user's specified location

@app.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('account.login'))
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
            return redirect("/dashboard")
        else:
            flash('invalid credentials. please try again.')
            return redirect(url_for('account.login'))

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



if __name__ == '__main__':
    app.run(debug=True)




# ref: CS312, https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
# ref: https://flask.palletsprojects.com/en/stable/patterns/flashing/