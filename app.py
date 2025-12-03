import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from src.preprocessing import Preprocessor
from src.model_loader import ModelLoader
from src.predictor import Predictor
from src.encoders import COMPANY_ENCODING, LOCATION_ENCODING, UBER_RIDES, LYFT_RIDES

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="Cab Fare Predictor", page_icon="🚕", layout="centered")


# ----------------------------------------------------------
# BACKGROUND IMAGE LOADER
# ----------------------------------------------------------
def set_bg(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}

        /* Medium width */
        .block-container {{
            max-width: 900px;
            padding-top: 1rem;
        }}

        /* Card design */
        .glass {{
            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(12px);
            padding: 18px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 0 12px rgba(0,0,0,0.25);
        }}

        /* Navbar */
        .navbar {{
            background: rgba(0,0,0,0.65);
            padding: 14px;
            font-size: 24px;
            color: white;
            text-align: center;
            border-radius: 12px;
            margin-bottom: 25px;
        }}

        /* Bottom Prediction Box */
        .prediction-box {{
            background: rgba(0,0,0,0.82);
            color: white;
            padding: 22px;
            border-radius: 15px;
            margin-top: 35px;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# Load background
set_bg(r"D:\regression_project\Image\streamlit background.jpg")

#  NAVBAR
st.markdown("<div class='navbar'>🚕 Cab Fare Predictor (Uber & Lyft)</div>", unsafe_allow_html=True)

# ----------------------------------------------------------
# MODEL LOADING
with st.spinner("Loading Model..."):
    loader = ModelLoader()
    model = loader.load()

preprocessor = Preprocessor()
predictor = Predictor(model)
st.success("WELCOME TO CAB FARE PREDICTOR!")


# ----------------------------------------------------------
# TWO-SIDE LAYOUT
# ----------------------------------------------------------
left, right = st.columns(2)


# ----------------------------------------------------------
# LEFT SIDE — RIDE INPUTS
# ----------------------------------------------------------
with left:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("🚗 Ride Details")

    company = st.selectbox("Company", COMPANY_ENCODING.keys())
    ride_type = st.selectbox("Ride Type", UBER_RIDES if company == "Uber" else LYFT_RIDES)
    distance_km = st.number_input("Distance (km)", 0.1, 50.0, 2.0)
    pickup = st.selectbox("Pickup Location", LOCATION_ENCODING.keys())
    drop = st.selectbox("Drop Location", LOCATION_ENCODING.keys())

    st.subheader("⏱ Date & Time")
    now = datetime.now()
    date_input = st.date_input("Date", now.date())
    time_input = st.time_input("Time", now.time())

    dt = datetime.combine(date_input, time_input)
    hour, day, month, weekday = dt.hour, dt.day, dt.month, dt.weekday()
    weekend = 1 if weekday >= 5 else 0

    st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------------------------------------
# RIGHT SIDE — WEATHER INPUTS
# ----------------------------------------------------------
with right:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("🌤 Weather")

    temperature = st.number_input("Temperature (°F)", 0.0, 120.0, 60.0)
    pressure = st.number_input("Pressure (hPa)", 900.0, 1100.0, 1010.0)
    cloud = st.slider("Cloud Coverage (0–1)", 0.0, 1.0, 0.4)
    humidity = st.slider("Humidity (0–1)", 0.0, 1.0, 0.6)
    rainfall = st.number_input("Rainfall (inches)", 0.0, 20.0, 0.0)
    wind_speed = st.number_input("Wind Speed (mph)", 0.0, 60.0, 10.0)

    st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------------------------------------
# BOTTOM PREDICT BUTTON
# ----------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
predict_clicked = st.button("🔮 Predict Fare", use_container_width=True)


# ----------------------------------------------------------
# PREDICTION LOGIC
# ----------------------------------------------------------
if predict_clicked:
    try:
        inputs = {
            "distance_km": distance_km,
            "temperature": temperature,
            "cloud_coverage": cloud,
            "pressure": pressure,
            "rainfall": rainfall,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "hour": hour,
            "day": day,
            "month": month,
            "weekday": weekday,
            "weekend": weekend,
            "company": company,
            "ride_type": ride_type,
            "pickup": pickup,
            "drop": drop
        }

        row = preprocessor.transform(inputs)
        if not isinstance(row, pd.DataFrame):
            row = pd.DataFrame([row])

        fare = predictor.predict_row(row)
        fare = round(float(fare), 2)

        st.session_state.predicted_fare = fare

    except Exception as e:
        st.error(f"Error: {e}")


# ----------------------------------------------------------
# SHOW PREDICTION BOX AT BOTTOM
# ----------------------------------------------------------
if "predicted_fare" in st.session_state:
    st.markdown(
        f"""
        <div class='prediction-box'>
            💰 Estimated Fare: ${st.session_state.predicted_fare:.2f}
        </div>
        """,
        unsafe_allow_html=True
    )

