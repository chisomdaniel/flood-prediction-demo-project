import numpy as np
import pandas as pd
import joblib as jb
import os

class MSRPrediction:
    periods = {"today": 1, "tomorrow": 2, "one week": 7, "one month": 30, "one year": 365, "year": 365, "two_years": 730}
    communities = [
        "Amaechi Idodo", "Fangan", "Sokori", "Ibiade", "Okpanku", "Ogwuagor", "Isheri", "Lafiagi", "Pategi"]
    csv_base_location = "predictions/msr_prediction"

    def __init__(self, community, period):
        self.period = period
        self.community = community
        for names in MSRPrediction.communities:
            if self.community.lower() == names.lower():
                self.community = names

    def load_dataset(self):
        import os
        import pandas as pd
        try:
            base_path = "../datasets"
            remaining_path = self.community.replace(" ", "_") + "_Final" + ".csv"
            true_path = os.path.join(base_path, remaining_path)
            df = pd.read_csv(true_path, usecols=["date", "surface_runoff_max"])
            df.index = pd.to_datetime(df["date"])
            df.drop(columns=["date"], inplace=True)
            start_date = df.index[-1]
            today = pd.Timestamp.today()
            end_date = today + pd.Timedelta(days=MSRPrediction.periods[self.period] - 1)
            return df, start_date, end_date
        except Exception as e:
            raise e
            print("Something went wrong at your end")

    def add_features(self, df):
        df["hour"] = df.index.day
        df["day"] = df.index.dayofweek
        df["month"] = df.index.month
        df["quater (of year)"] = df.index.quarter
        df["week"] = df.index.dayofweek
        return df

    def create_future_and_lags(self, df, start_date, end_date, frequency="D"):
        today = pd.Timestamp.today()
        end_date = today + pd.Timedelta(days=MSRPrediction.periods[self.period] - 1)
        future = pd.date_range(start_date, end_date, freq=frequency)

        future_df = pd.DataFrame(index=future)

        df = df.sort_index()
        future_df = future_df.sort_index()
        df["isFuture"] = False
        future_df["isFuture"] = True

        combined_df = pd.concat([df, future_df], axis=0)

        combined_df['lag_1'] = combined_df['surface_runoff_max'].shift(364)
        combined_df['lag_2'] = combined_df['surface_runoff_max'].shift(728)
        combined_df['lag_3'] = combined_df['surface_runoff_max'].shift(1092)

        future_with_lags = combined_df.query("isFuture").copy()
        future_with_lags.drop(columns=["surface_runoff_max", "isFuture"], inplace=True)
        return future_with_lags

    def predict(self, df):
        try:
            path = "../maximum_surface_runoff/models"
            remaining_part = self.community + " Final Stacked Surface Runoff Model (without Skewness).pkl"
            final_part = os.path.join(path, remaining_part)
            model = jb.load(final_part)

            prediction = model.predict(df)
            preds = np.expm1(prediction)

            return preds
        except Exception as e:
            print("Something went wrong from your end:", str(e))

    def save_pred_to_csv(self, x_value, prediction):
        """Save the predictions to csv"""
        file_path = os.path.join(self.csv_base_location, f"{self.community.lower()}_pred.csv")
        prediction *= 100000
        new_df = pd.DataFrame({"Date": pd.to_datetime(x_value), "Prediction": prediction})
        new_df.set_index("Date", inplace=True)

        today = pd.Timestamp.today().normalize()
        #end_date = today + pd.Timedelta(days=Prediction.periods[self.period] - 1)

        new_df = new_df.loc[today:]
        new_df.index = new_df.index.astype(str)
        new_df.reset_index(inplace=True)
        new_df.to_csv(file_path, index=False)
        return new_df
    
    @classmethod
    def get_pred_from_csv(cls, community: str):
        """Load the predicted value from a csv file"""
        file_path = os.path.join(cls.csv_base_location, f"{community.lower()}_pred.csv")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"prediction file for {community} not found")

        df = pd.read_csv(file_path)

        return df
    
    @classmethod
    def get_specific_pred(cls, df: pd.DataFrame, period: str):
        """Get the prediction for a specific time frame"""
        start_date = pd.Timestamp.today().normalize() # today
        end_date = start_date + pd.Timedelta(days=MSRPrediction.periods[period] - 1)

        new_df = df.set_index("Date", inplace=False)
        new_df.index = pd.to_datetime(new_df.index)
        new_df = new_df.loc[start_date:end_date]
        new_df.index = new_df.index.astype(str)

        average_pred = new_df['Prediction'].mean()
        if average_pred < 5:
            result = 'Low Risk'
        elif average_pred >= 5 and average_pred <15:
            result = 'Moderate Risk'
        elif average_pred >= 15 and average_pred < 25:
            result = 'High Risk'
        elif average_pred >= 25:
            result = 'Extreme Risk'

        new_df.reset_index(inplace=True)
        value_dict = new_df.to_dict(orient='records')

        return value_dict, ({'average risk': average_pred, 'message': result})



