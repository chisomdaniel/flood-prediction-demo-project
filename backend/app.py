#!/bin/env python3
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from dummy import generate_dummy_forecast
from predict import (get_flood_pred,
                     save_pred_data,
                     get_pred_data_from_file,
                     get_specific_pred,
                     load_prediction_dict,
                     check_flood_status)

app = Flask(__name__)
CORS(app)

done = False
if not done:
    communities = ["Amaechi idodo", "Fangan", "Sokori", "Ibiade", "Okpanku", "Ogwuagor", "Isheri", "Lafiagi", "Pategi"]
    period = ["today", "tomorrow", "week", "month", "year"]
    prediction_dict = {}
    msr_dict = {}
    #save_pred_data(communities[1], "two_years")
    for community in communities:
        try:
            prediction_dict.update({community : get_pred_data_from_file(community)})
        except FileNotFoundError:
            save_pred_data(community, "two_years")
            prediction_dict.update({community : get_pred_data_from_file(community)})
            print("Loaded Total precipitation: ", community)
        try:
            msr_dict.update({community : get_pred_data_from_file(community, cls='msr')})
        except FileNotFoundError:
            save_pred_data(community, "two_years", cls='msr')
            msr_dict.update({community : get_pred_data_from_file(community, cls='msr')})
            print("Loaded MSR: ", community)
    done = True
    print("Done loading predictions")

@app.route("/", strict_slashes=False)
def home():
    return f"Welcome to the flood prediction API.\
        Access the endpoint '/api/v2/forecast/<community>/<period>', \
            where 'community' is one of '{communities}' \
                and period is the future days you want to get a prediction for; can be 'today, tomorrow, week, month and year' (e.g. /api/v2/forecast/sokori/week)"

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
    # community = community.capitalize()
    # print("community is: ", community)
    if community.capitalize() in communities:
        try:
            data, averg, hrd, days_pred = get_specific_pred(prediction_dict[community.capitalize()], period)
            data2, averg2, hrd2, days_pred2 = get_specific_pred(msr_dict[community.capitalize()], period, cls='msr')
            flood_status = check_flood_status(days_pred, days_pred2)
            response = {
                "community": community,
                "total_precipitation": data,
                "averg_total_precipitation": averg,
                "tp_highest_risk_day": hrd,
                "maximum_surface_runoff": data2,
                "averg_maximum_surface_runoff": averg2,
                "msr_highest_risk_day": hrd2,
                "daily_flood_status": flood_status,
            }
            #response.update(averg)
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
        #print("second is", community.capitalize())
        return make_response(jsonify(response), 400)

@app.route("/api/v2/forecast/values", methods=['GET', 'POST'], strict_slashes=False)
def values():
    """Provide the values passable to the forecaste endpoint"""
    response = {
                "message": "These are the values to choose from.",
                "community": communities,
                "period": period
            }
    return make_response(jsonify(response))


if __name__ == "__main__":
    app.run(debug=True)
