from flask import Flask, render_template
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/flights_info', methods = ['POST'])
def flights_information():
    request.args.get('returenDate')
    request.args['departureDate']
    return amadeus.run()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)