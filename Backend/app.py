from flask import Flask, jsonify, g
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


"""
NOTE: i pulled this from a previous project. it cross-checks the database for copies of usernames when registering a new account. will have to be edited for this project

@account_bp.route('/register', methods=['GET', 'POST'])
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

    return render_template('register.html')
"""

"""
NOTE: i also pulled this from a previous project. it's for logging in returning users

@account_bp.route('/login', methods=['GET', 'POST'])
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
    return render_template('login.html')

"""

if __name__ == '__main__':
    app.run(debug=True)




# ref: CS312, https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
# ref: https://flask.palletsprojects.com/en/stable/patterns/flashing/