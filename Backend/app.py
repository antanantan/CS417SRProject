from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/home', methods=['POST'])
def disclaimer():
    error: None
    Flask.flash("DISCLAIMER TEST", 'success')
    return jsonify("THIS IS A TEST")

if __name__ == '__main__':
    app.run(debug=True)

# ref: CS312, https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
# ref: https://flask.palletsprojects.com/en/stable/patterns/flashing/