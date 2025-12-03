import numpy as np
import pandas as pd

class Predictor:
    def __init__(self, model):
        self.model = model

    def predict_row(self, df_row: pd.DataFrame):
        """
        Accepts a single-row DataFrame and returns prediction (float).
        Tries to align DataFrame columns to model.feature_names_in_ when available.
        """
        # Defensive alignment with model features if available
        try:
            if hasattr(self.model, "feature_names_in_"):
                required_cols = list(self.model.feature_names_in_)
                # reindex will add missing cols with NaN; you may want to fillna(0) or defaults
                df_aligned = df_row.reindex(columns=required_cols)
            else:
                df_aligned = df_row
        except Exception:
            df_aligned = df_row

        # If there are any NaNs, fill them reasonably (0 here; customize if needed)
        df_aligned = df_aligned.fillna(0)

        # Model expects 2D array-like
        preds = self.model.predict(df_aligned)
        return float(np.round(preds[0], 2))
