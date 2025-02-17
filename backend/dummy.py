#!/bin/env python3
import pandas as pd
import numpy as np

def generate_dummy_forecast(city="Lagos", days=5):
    """
    Generate a dummy 5-day precipitation forecast.
    
    Parameters:
    - city (str): Name of the city
    - days (int): Number of days to forecast
    
    Returns:
    - dict: JSON-serializable forecast data
    """
    dates = pd.date_range(start=pd.Timestamp.today().date(), periods=days, freq="D")
    forecast_data = []

    for date in dates:
        forecast_data.append({
            "ds": date.strftime("%Y-%m-%d"),
            "yhat1": round(np.random.uniform(5, 20), 2),  # Simulated precipitation (mm)
            "trend": round(np.random.uniform(8, 15), 2),  # Simulated trend value
            "seasonal": round(np.random.uniform(0, 8), 2)  # Simulated seasonality effect
        })

    return {"city": city, "forecast": forecast_data}



