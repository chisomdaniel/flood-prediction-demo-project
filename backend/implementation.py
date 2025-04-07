class Prediction:
    periods = {"today": 1, "tomorrow": 2, "week": 7, "month": 30, "year": 365}
    communities = [
        "Amaechi Idodo", "Fangan", "Sokori", "Ibiade", "Okpanku", "Ogwuagor", "Isheri", "Lafiagi", "Pategi"]

    def __init__(self, community, period):
        
        if period not in Prediction.periods:
            raise ValueError("Invalid timeframe. Choose from: today, tomorrow, this week, this month, this year")
        if community not in Prediction.communities:
            raise ValueError(f"Invalid community. Choose from: {Prediction.communities}")

        self.period = period
        self.community = community
        for names in Prediction.communities:
            if self.community.lower() == names.lower():
                self.community = names

    def load_dataset(self):
        import os
        import pandas as pd
        try:
            base_path = "../datasets"
            print("Here at load dataset")
            remaining_path = "Climate_" + self.community.replace(" ", "_") + ".csv"
            true_path = os.path.join(base_path, remaining_path)
            df = pd.read_csv(true_path, usecols=["date", "total_precipitation_max"])
            df.index = pd.to_datetime(df["date"])
            df.drop(columns=["date"], inplace=True)
            start_date = df.index[-1]
            today = pd.Timestamp.today()
            end_date = today + pd.Timedelta(days=Prediction.periods[self.period] - 1)
            return df, start_date, end_date
        except Exception as e:
            print("Something went wrong at your end", e)

    def add_features(self, df):
        df["hour"] = df.index.day
        df["day"] = df.index.dayofweek
        df["month"] = df.index.month
        df["quater (of year)"] = df.index.quarter
        df["week"] = df.index.dayofweek
        return df

    def create_future_and_lags(self, df, start_date, end_date, frequency="D"):
        import pandas as pd
        today = pd.Timestamp.today()
        end_date = today + pd.Timedelta(days=Prediction.periods[self.period] - 1)
        future = pd.date_range(start_date, end_date, freq=frequency)

        future_df = pd.DataFrame(index=future)

        df = df.sort_index()
        future_df = future_df.sort_index()
        df["isFuture"] = False
        future_df["isFuture"] = True

        combined_df = pd.concat([df, future_df], axis=0)

        combined_df['lag_1'] = combined_df['total_precipitation_max'].shift(364)
        combined_df['lag_2'] = combined_df['total_precipitation_max'].shift(728)
        combined_df['lag_3'] = combined_df['total_precipitation_max'].shift(1092)

        future_with_lags = combined_df.query("isFuture").copy()
        future_with_lags.drop(columns=["total_precipitation_max", "isFuture"], inplace=True)
        return future_with_lags

    def predict(self, df):
        import joblib as jb
        import os
        try:
            path = "../models"
            print("Here at predict")
            remaining_part = self.community + " Model (GB).joblib"
            final_part = os.path.join(path, remaining_part)
            model = jb.load(final_part)

            prediction = model.predict(df)
            return prediction
        except Exception as e:
            print("Something went wrong from your end:", str(e))

    def get_data(self, x_value, prediction):
        import pandas as pd
        print("Here at get_data")

        prediction *= 10000
        new_df = pd.DataFrame({"Date": pd.to_datetime(x_value), "Prediction": prediction})
        new_df.set_index("Date", inplace=True)

        start_date = pd.Timestamp.today().normalize() # today
        #end_date = today + pd.Timedelta(days=Prediction.periods[self.period] - 1)

        print("start date is: ", start_date)
        new_df = new_df.loc[start_date:] # make this add today to the output
        new_df.index = new_df.index.astype(str)
        new_df.reset_index(inplace=True)
        value_dict = new_df.to_dict(orient='records')

        print('done')
        return value_dict

