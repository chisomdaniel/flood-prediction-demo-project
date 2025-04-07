#!/bin/env python3
from flask import Flask, jsonify
from flask_cors import CORS
from dummy import generate_dummy_forecast
from predict import get_flood_pred

app = Flask(__name__)
CORS(app)

@app.route("/", strict_slashes=False)
def home():
    return "Welcome to the flood prediction API.\
        Access the endpoint '/api/forecast/< str:city >/< int:days >', where 'days' in the number of future days you want to get a prediction for (e.g. /api/forecast/lagos/23)"

@app.route("/api/forecast/<city>/<int:days>", methods=['GET', 'POST'], strict_slashes=False)
def predict(city='lagos', days='5'):
    """Get prediction"""
    return jsonify(generate_dummy_forecast(city, days))

@app.route("/api/v1/forecast/<community>/<period>", methods=['GET', 'POST'], strict_slashes=False)
def predict_v1(community=None, period=None):
    """Get prediction"""
    if not community or not period:
        response = {
            "status": "ERROR",
            "message": "Must provide a valid community and a timeframe"
        }
        return jsonify(response), 401
    
    try:
        data = get_flood_pred(community, period)
        response = {
            "community": community,
            "forecast": data
        }
    except Exception as e:
        response = {
            "status": "ERROR",
            "message": f"An error occured: {e}"
        }
    
    return jsonify(response) # add error code


if __name__ == "__main__":
    app.run(debug=True)
