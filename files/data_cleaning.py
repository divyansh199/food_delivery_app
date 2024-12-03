import pandas as pd
import numpy as np

class DataCleaning:

    """
        this class is used to clean the data frame
    """
    def extract_columns_value(self,df):

        # Extract time and convert to int
        # df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x: int(x.split(' ')[1].strip()))

        # Extract Weather conditions
        #df['weather_conditions'] = df['weather_conditions'].apply(lambda x: x.split(' ')[1].strip())

        # Extract City code from Delivery_person_ID
        df['City_code'] = df['Delivery_person_ID'].str.split('RES', expand=True)[0]
        # df_train['Delivery_person_ID'].str.extract(r'(.+?)RES')--- Alternative

        return df

    def update_datatype(self,df):

        df['Delivery_person_Age'] = df['Delivery_person_Age'].astype('float64')

        df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype('float64')

        df['multiple_deliveries'] = df['multiple_deliveries'].astype('float64')

        df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')

        return df



