from neuralprophet import NeuralProphet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib


df = pd.read_parquet(r"C:\Users\user\Downloads\weather dataset\daily_weather.parquet", engine="pyarrow")

df.head(7)

lagos = df[df["city_name"] == "Lagos"]
ilorin = df[df["city_name"] == "Ilorin"]

lagos["date"] = pd.to_datetime(lagos["date"])
ilorin["date"] = pd.to_datetime(ilorin["date"])

lagos = lagos[["date", "precipitation_mm"]]
ilorin = ilorin[["date", "precipitation_mm"]]

lagos.columns = ["ds", "y"]
ilorin.columns = ["ds", "y"]

lagos = lagos[(lagos["ds"] >= "2000-01-01") & (lagos["ds"] <= "2021-12-31")]
ilorin = ilorin[(ilorin["ds"] >= "2000-01-01") & (ilorin["ds"] <= "2021-12-31")]

lagos.dropna(inplace=True)
ilorin.dropna(inplace=True)

lagos_model = NeuralProphet()
ilorin_model = NeuralProphet()

lagos_model.fit(lagos, freq="D", epochs=2000)
ilorin_model.fit(ilorin, freq="D", epochs=2000)

lagos_forecast = lagos_model.make_future_dataframe(lagos, periods=900)
ilorin_forecast = ilorin_model.make_future_dataframe(ilorin, periods=900)

lagos_pred = lagos_model.predict(lagos_forecast)
ilorin_pred = ilorin_model.predict(ilorin_forecast)

#lagos_model.plot(lagos_pred)

joblib.dump(lagos_model, "Lagos Flood Prediction Model.pkl")
joblib.dump(ilorin_model, "Ilorin Flood Prediction Model.pkl")




