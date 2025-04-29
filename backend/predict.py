#!/usr/bin/env python3
from precipitation_pred import Prediction as TPPrediction
from maximum_surface_runoff import MSRPrediction

def get_flood_pred(community, timeframe):
    """Get the prediction data from the model"""
    return None
    pred_obj = Prediction(community, timeframe)

    df, start_date, end_date = pred_obj.load_dataset()
    df = pred_obj.add_features(df)
    df = pred_obj.create_future_and_lags(df, start_date, end_date)
    df = pred_obj.add_features(df)
    df = df.dropna(axis=0)
    
    pred = pred_obj.predict(df)
    value = pred_obj.get_data(df.index, pred)
    return value

def save_pred_data(community, period, cls='tp'):
    """Save the prediction data for a communities in a csv file"""

    Prediction = MSRPrediction if cls == 'msr' else TPPrediction
    pred_obj = Prediction(community, "two_years")
    df, start_date, end_date = pred_obj.load_dataset()
    df = pred_obj.add_features(df)
    df = pred_obj.create_future_and_lags(df, start_date, end_date)
    df = pred_obj.add_features(df)
    df = df.dropna(axis=0)
    
    pred = pred_obj.predict(df)
    pred_obj.save_pred_to_csv(df.index, pred)

def get_pred_data_from_file(community: str, cls='tp'):
    """Get the predictions for a location from a file
    Return: a pandas dataframe
    """
    Prediction = MSRPrediction if cls == 'msr' else TPPrediction
    return Prediction.get_pred_from_csv(community)

def get_specific_pred(df, period, cls='tp'):
    """Get the prediction for a specific time frame
    Return: a dict value added to the response
    """
    Prediction = MSRPrediction if cls == 'msr' else TPPrediction
    return Prediction.get_specific_pred(df, period)

def load_prediction_dict(communities, cls='tp'):
    prediction_dict = {}
    for i in communities:
        prediction_dict.extend({i : get_pred_data_from_file(i, cls=cls)})
    
    return prediction_dict

def check_flood_status(total_prec, msr):
    flood_status = {'Unlikely': [],
                    'Neutral': [],
                    'High Chance': []}
    for i in total_prec['Low Risk']:
        if i in msr['Low Risk']:
            flood_status['Unlikely'].append(i)
        elif i in msr['Moderate Risk']:
            flood_status['Unlikely'].append(i)
        elif i in msr['High Risk']:
            flood_status['High Chance'].append(i)
    for i in total_prec['Moderate Risk']:
        if i in msr['Low Risk']:
            flood_status['Unlikely'].append(i)
        elif i in msr['Moderate Risk']:
            flood_status['Neutral'].append(i)
        elif i in msr['High Risk']:
            flood_status['Neutral'].append(i)
    for i in total_prec['High Risk']:
        if i in msr['Low Risk']:
            flood_status['Neutral'].append(i)
        elif i in msr['Moderate Risk']:
            flood_status['Neutral'].append(i)
        elif i in msr['High Risk']:
            flood_status['High Chance'].append(i)
    
    return flood_status
