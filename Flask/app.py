from flask import Flask, redirect, url_for, request, render_template
from flask_cors import CORS
# from flask.ext.cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# @app.route('/')
# def hello_world():
#     return 'Hello World'

@app.route('/', methods = ['GET', 'POST'])
def home():
    # return "take to the screen"
    return render_template('home.html')

# @app.route('/getreq', methods = ['GET'])
# def getter():
#     return "take to the screen"

# @app.route('/postreq', methods = ['GET', 'POST'])
# def poster():
#     if request.method == 'POST':
#         userplace = request.form["place"]
#         return userplace
#     if request.method == 'GET':
#         return "get the place first using post"

# @app.route()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)