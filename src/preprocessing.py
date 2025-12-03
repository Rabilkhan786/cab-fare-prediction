import pandas as pd
import numpy as np
from .encoders import LOCATION_ENCODING, COMPANY_ENCODING, RIDE_TYPE_ENCODING

class Preprocessor:
    def __init__(self):
        # If you used scaling at train time, load scaler here
        # e.g. self.scaler = joblib.load('models/scaler.joblib')
        pass

    def _encode_location(self, loc):
        return LOCATION_ENCODING.get(loc, -1)

    def _encode_company(self, company):
        return COMPANY_ENCODING.get(company, -1)

    def _encode_ride_type(self, ride_type):
        return RIDE_TYPE_ENCODING.get(ride_type, -1)

    def transform(self, inputs: dict):
        """
        inputs: dictionary of user inputs (keys chosen in app.py)
        returns: pandas.DataFrame with single row ready for model input
        """
        df = pd.DataFrame([inputs])

        # Rename any typos if necessary (defensive)
        if 'mounth' in df.columns:
            df = df.rename(columns={'mounth': 'month'})

        # Encode categorical columns to numeric based on encoder dicts
        if 'pickup' in df.columns:
            df['pickup_location'] = df['pickup'].map(self._encode_location)
            df = df.drop(columns=['pickup'])
        if 'drop' in df.columns:
            df['drop_location'] = df['drop'].map(self._encode_location)
            df = df.drop(columns=['drop'])
        if 'company' in df.columns:
            df['company'] = df['company'].map(self._encode_company)
        if 'ride_type' in df.columns:
            df['ride_type'] = df['ride_type'].map(self._encode_ride_type)

        # Ensure consistent dtypes
        df = df.replace({np.nan: None})

        # Return DataFrame (single row). The app will align columns to the model.
        return df
