#!/usr/bin/env python3
from implementation import Prediction

def get_flood_pred(community, timeframe):
    """Get the prediction data from the model"""
    pred_obj = Prediction(community, timeframe)

    df, start_date, end_date = pred_obj.load_dataset()
    df = pred_obj.add_features(df)
    df = pred_obj.create_future_and_lags(df, start_date, end_date)
    df = pred_obj.add_features(df)
    df = df.dropna(axis=0)
    
    pred = pred_obj.predict(df)
    value = pred_obj.get_data(df.index, pred)
    return value


