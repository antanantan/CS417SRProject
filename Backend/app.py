from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

# we still need to implement the script for handling login/signup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
DATABASE = os.path.join(BASE_DIR, "profiles.db")

if __name__ == '__main__':
    app.run(debug=True)


# ref: CS312, https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
# ref: https://flask.palletsprojects.com/en/stable/patterns/flashing/