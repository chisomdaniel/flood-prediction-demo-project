#!/bin/env python3
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from dummy import generate_dummy_forecast
from predict import (get_flood_pred,
                     save_pred_data,
                     get_pred_data_from_file,
                     get_specific_pred,
                     load_prediction_dict)

app = Flask(__name__)
CORS(app)

done = False
if not done:
    communities = ["Amaechi Idodo", "Fangan", "Sokori", "Ibiade", "Okpanku", "Ogwuagor", "Isheri", "Lafiagi", "Pategi"]
    prediction_dict = {}
    for community in communities:
        try:
            prediction_dict.update({community : get_pred_data_from_file(community)})
        except FileNotFoundError:
            save_pred_data(community, "two_years")
            prediction_dict.update({community : get_pred_data_from_file(community)})
            # sokari_pred_df = get_pred_data_from_file(communities_test[0])
    done = True
    print("Done loading predictions")

@app.route("/", strict_slashes=False)
def home():
    return "Welcome to the flood prediction API.\
        Access the endpoint '/api/forecast/< str:city >/< int:days >', where 'days' in the number of future days you want to get a prediction for (e.g. /api/forecast/lagos/23)"

@app.route("/api/forecast/<city>/<int:days>", methods=['GET', 'POST'], strict_slashes=False)
def predict(city='lagos', days='5'):
    """Get prediction"""
    response = {
            "status": "",
            "message": "Endpoint no longer available, try version 2. '/api/v2/forecast/<community>/<period>'"
        }
    return make_response(jsonify(response), 400)
    # return jsonify(generate_dummy_forecast(city, days))

@app.route("/api/v1/forecast/<community>/<period>", methods=['GET', 'POST'], strict_slashes=False)
def predict_v1(community=None, period=None):
    """Get prediction"""
    response = {
            "status": "",
            "message": "Endpoint no longer available, try version 2"
        }
    return make_response(jsonify(response), 400)
    '''
    if not community or not period:
        response = {
            "status": "ERROR",
            "message": "Must provide a valid community and a timeframe"
        }
        return make_response(jsonify(response), 400)
    
    try:
        data = get_flood_pred(community, period)
        response = {
            "community": community,
            "forecast": data
        }
        return make_response(jsonify(response))
    except Exception as e:
        response = {
            "status": "ERROR",
            "message": f"An error occured: {e}"
        }
        return make_response(jsonify(response), 400)
        '''


@app.route("/api/v2/forecast/<community>/<period>", methods=['GET', 'POST'], strict_slashes=False)
def predict_v2(community: str=None, period: str=None):
    community = community.capitalize()
    if community.capitalize() in communities:
        try:
            data = get_specific_pred(prediction_dict[community], period)
            response = {
                "community": community,
                "forecast": data
            }
            return make_response(jsonify(response))
        except Exception as e:
            response = {
                "status": "ERROR",
                "message": f"An error occured: {e}"
            }
            return make_response(jsonify(response), 400)
    else:
        response = {
                "status": "ERROR",
                "message": f"Choose from the list of approved communities: {communities}"
            }
        print(community.capitalize())
        return make_response(jsonify(response), 400)



if __name__ == "__main__":
    app.run(debug=True)
