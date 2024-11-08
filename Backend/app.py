from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def disclaimer():
    Flask.flash("DISCLAIMER TEST", 'success')
    return Flask.render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

# ref: CS312, https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/