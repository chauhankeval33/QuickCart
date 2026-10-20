"""Page 1: delivery-time estimator (Part D model)."""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

MODELS = Path(__file__).resolve().parents[1] / "models"
NUM = ["distance_km", "items_count", "store_open_orders", "basket_value", "discount_amt", "hour_sin", "hour_cos"]
CAT = ["payment_method", "city"]
PEAK_HOURS = [8, 9, 19, 20, 21]                       # same definition as 02_delivery_regression.ipynb


@st.cache_resource                                    # the model is loaded once, not on every click
def load_model(filename):
    path = MODELS / filename
    return joblib.load(path) if path.exists() else None


st.title("Delivery time estimator")
model = load_model("delivery_model.joblib")
if model is None:
    st.error("Model file app/models/delivery_model.joblib not found. Save it from 02_delivery_regression.ipynb.")
    st.stop()
promise_model = load_model("delivery_q90_model.joblib")           # optional 90th-percentile model

# Typical values for inputs that are not in the form, taken from the fitted pipeline itself.
pre = model.named_steps["pre"]
cities = sorted(pre.named_transformers_["cat"].named_steps["oh"].categories_[1])
typical = dict(zip(NUM, pre.named_transformers_["num"].named_steps["imp"].statistics_))
payment = pre.named_transformers_["cat"].named_steps["imp"].statistics_[0]

with st.form("estimate"):
    distance = st.number_input("Distance (km)", value=2.5, step=0.1)
    items = st.number_input("Items in the order", value=5, step=1)
    load = st.number_input("Store load (open orders at the store now)", value=15, step=1)
    rain = st.checkbox("It is raining")
    hour = st.slider("Hour of day (0-23)", 0, 23, 12)
    city = st.selectbox("City", cities)
    submitted = st.form_submit_button("Estimate delivery time")

if submitted:
    errors = []
    if distance < 0:
        errors.append(f"Distance cannot be negative (you entered {distance} km). Enter a value above 0.")
    elif not 0 < distance <= 50:
        errors.append("Distance must be above 0 and at most 50 km.")
    if items != int(items) or not 1 <= items <= 100:
        errors.append("Items must be a whole number between 1 and 100.")
    if load != int(load) or not 0 <= load <= 200:
        errors.append("Store load must be a whole number between 0 and 200.")
    for message in errors:
        st.error(message)
    if not errors:
        row = pd.DataFrame([{
            "distance_km": distance, "items_count": items, "store_open_orders": load,
            "basket_value": typical["basket_value"], "discount_amt": typical["discount_amt"],
            "hour_sin": np.sin(2 * np.pi * hour / 24), "hour_cos": np.cos(2 * np.pi * hour / 24),
            "is_raining": int(rain), "is_peak_hour": int(hour in PEAK_HOURS), "is_weekend": 0,
            "payment_method": payment, "city": city}])
        minutes = max(1.0, float(model.predict(row)[0]))
        st.metric("Predicted delivery time", f"{minutes:.0f} minutes")
        if promise_model is not None:
            st.metric("Safe promise to show the customer (90th percentile)",
                      f"{max(minutes, float(promise_model.predict(row)[0])):.0f} minutes")
        st.caption("Typical error is about 3 minutes. Basket value, discount, payment method and weekday "
                   "are set to typical values because they barely change the prediction.")
