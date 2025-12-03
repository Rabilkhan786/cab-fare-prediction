
# 🚕 Cab Fare Predictor (Uber & Lyft) — Machine Learning + Streamlit

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30-red.svg)
![Machine Learning](https://img.shields.io/badge/ML-Regression-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

A modern, interactive, and fully machine-learning powered **Cab Fare Prediction App** that estimates Uber & Lyft ride fares.  
The application uses a trained ML regression model and a beautiful Streamlit UI with a clean and responsive two-column layout.

This project is perfect for **ML beginners, portfolio building, and real-world application development**.

---

## 🌟 Features

### 🎨 Beautiful User Interface
- Two-column medium-width layout  
- Left: Ride Inputs (company, ride type, distance, pickup, drop)  
- Right: Weather Inputs (temperature, humidity, rainfall, wind, pressure)  
- Transparent glass cards  
- Custom full-page background image  
- Centered Predict button at bottom  
- Clean prediction box displaying final fare  

### 🤖 Machine Learning Powered
 # 🚕 Cab Fare Predictor (Uber & Lyft)

![Python](https://img.shields.io/badge/Python-3.10-blue.svg) ![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red.svg) ![ML](https://img.shields.io/badge/ML-Regression-green.svg)

A modern, interactive Streamlit app that estimates Uber & Lyft fares using a trained regression model. This repository contains the training pipeline, model serialization, and two lightweight UIs (Streamlit and Flask) for single and batch prediction.

---

## Key Features

- Clean, responsive Streamlit UI for single and batch predictions
- Model artifact versioning (under `models/v1/`)
- Reusable preprocessing and encoder utilities in `src/`
- Simple Flask alternative UI for environments where Streamlit is not desired

---

## Project Layout (important files)

```
regression_project/
├── app.py                      # Streamlit UI (top-level)
├── model.py                    # Training script (reproduces notebook pipeline)
├── models/
│   └── v1/
│       └── xgb_best_model_v1.joblib   # primary saved artifact
├── data/                       # source / cleaned data
├── src/                        # library code: preprocessing, serialize, inference, web
├── Image/                      # screenshots and assets for the UI
├── requirements.txt
└── README.md
```

---

## Quickstart (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the Streamlit UI:

```powershell
streamlit run app.py
```

If the app cannot find the model artifact automatically, set the `MODEL_FILE` environment variable to point at your artifact and re-run:

```powershell
$env:MODEL_FILE = 'models/v1/xgb_best_model_v1.joblib'
streamlit run app.py
```

---

## Model artifact

- Current artifact: `models/v1/xgb_best_model_v1.joblib` (the UI will attempt common locations).
- Preferred artifact format: either a raw model object or a dictionary containing keys: `model`, optional `encoders`, and optional `meta` information.

If your artifact includes `encoders` / `feature_schema`, the app will use them to transform inputs the same way the model was trained. If encoders are absent, the Streamlit UI applies a safe fallback by converting string/object columns to categorical integer codes before predicting (this prevents dtype errors but may not match training-time encoding).

---

## How prediction works (high level)

1. User fills ride and weather inputs in the Streamlit form
2. Inputs are preprocessed and encoded (via saved encoders if present)
3. Model predicts fare
4. App displays prediction and optional model info

---

## Reproduce training (short)

1. Prepare/clean data under `data/` and update preprocessing in `src/features/preprocessing.py` as needed.
2. Run training:

```powershell
python model.py --train --output models/v1/xgb_best_model_v1.joblib
```

3. When saving artifacts, include encoders/schema alongside the model to ensure deterministic inference.

---

## Troubleshooting

- If Streamlit reports decorator-related errors (e.g. `experimental_singleton` missing), ensure dependencies are installed from `requirements.txt` and re-run `streamlit run app.py`.
- To check Streamlit version:

```powershell
python -c "import streamlit as st; print(st.__version__)"
```

---

## Tests

Run unit tests with:

```powershell
pytest -q
```

---

## License

MIT — see `LICENSE`.

---

If you'd like, I can add a small smoke test that attempts to load `models/v1/xgb_best_model_v1.joblib` and run a dummy prediction to validate the UI and artifact end-to-end.