import joblib
from pathlib import Path

class ModelLoader:
    def __init__(self, model_path: str = "models/xgb_best_model_v1.joblib"):
        self.model_path = Path(model_path)
        self.model = None

    def load(self):
        if self.model is None:
            if not self.model_path.exists():
                raise FileNotFoundError(f"Model file not found at {self.model_path}")
            self.model = joblib.load(self.model_path)
        return self.model
