#!/bin/env python3
from flask import Flask, jsonify
from flask_cors import CORS
from dummy import generate_dummy_forecast

app = Flask(__name__)
CORS(app)

@app.route("/", strict_slashes=False)
def home():
    return "Welcome to the flood prediction API.\
        Access the endpoint '/api/forecast/< str:city >/< int:days >', where 'days' in the number of future days you want to get a prediction for (e.g. /api/lagos/23)"

@app.route("/api/forecast/<city>/<int:days>", methods=['GET', 'POST'], strict_slashes=False)
def predict(city='lagos', days='5'):
    """Get prediction"""
    return jsonify(generate_dummy_forecast(city, days))


if __name__ == "__main__":
    app.run(debug=True)
