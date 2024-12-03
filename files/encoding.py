import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder


class Encoding:
    """
        this class is used to encode categorical variables
    """

    def label_encoding(self,df):
        categorical_columns = df.select_dtypes(include='object').columns
        label_encoder = LabelEncoder()
        df[categorical_columns] = df[categorical_columns].apply(lambda col: label_encoder.fit_transform(col))

        return df

