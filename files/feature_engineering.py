import pandas as pd
import numpy as np
from geopy.distance import geodesic

class FeatureEngineering:
    """
        this class is used to perform feature engineering
    """

    def extract_date_features(self,date):
        date['day'] = date.Order_Date.dt.day
        date['month'] = date.Order_Date.dt.month
        date['quater'] = date.Order_Date.dt.quarter
        date['year'] = date.Order_Date.dt.year
        date['day_of_week'] = date.Order_Date.dt.day_of_week.astype(int)
        date['is_month_start'] = date.Order_Date.dt.is_month_start.astype(int)
        date['is_month_end'] = date.Order_Date.dt.is_month_end.astype(int)
        date['is_quater_start'] = date.Order_Date.dt.is_quarter_start.astype(int)
        date['is_quater_end'] = date.Order_Date.dt.is_quarter_end.astype(int)
        date['is_year_start'] = date.Order_Date.dt.is_year_start.astype(int)
        date['is_year_end'] = date.Order_Date.dt.is_year_end.astype(int)
        date['is_weekend'] = np.where(date['day_of_week'].isin([5, 6]), 1, 0)

        return date

    def calculate_time_diff(self,df):

        df['Time_Orderd'] = pd.to_timedelta(df['Time_Orderd'])

        df['Time_Order_picked'] = pd.to_timedelta(df['Time_Order_picked'])

        df['Time_Order_Picked_Formatted'] = (df['Order_Date'] + np.where(df['Time_Order_picked'] < df['Time_Orderd'],
                                                                         pd.DateOffset(days=1),
                                                                         pd.DateOffset(days=0)) + df[
                                                 'Time_Order_picked'])

        df['Time_Orderd_Formatted'] = df['Order_Date'] + df['Time_Orderd']

        df['Time_Order_Picked_Formatted'] = pd.to_datetime(df['Time_Order_Picked_Formatted'])

        df['Order_Prepration_Time'] = (df['Time_Order_Picked_Formatted'] - df[
            'Time_Orderd_Formatted']).dt.total_seconds() / 60

        # filling the null value with median
        # df['Order_Prepration_Time'].fillna(df['Order_Prepration_Time'].median(), inplace=True)

        # Drop all time and related columns
        df.drop(
            ['Time_Orderd', 'Time_Order_picked', 'Time_Orderd_Formatted', 'Time_Order_Picked_Formatted', 'Order_Date'],
            axis=1, inplace=True)

        return df

    def calculate_distance(self,df):
        df['distance'] = np.zeros(len(df))
        restaurant_coordinate = df[['Restaurant_latitude', 'Restaurant_longitude']].to_numpy()
        delivery_location_coordinate = df[['Delivery_location_latitude', 'Delivery_location_longitude']].to_numpy()
        df['distance'] = np.array([geodesic(resturant, delivery) for resturant, delivery in
                                   zip(restaurant_coordinate, delivery_location_coordinate)])
        df['distance'] = df['distance'].astype('str').str.extract(r'(\d{1,})\.').astype('int64')

        return df
