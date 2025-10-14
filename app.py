# ==============================================================
# 🚗 Lisbon Parking Vacancy Prediction App
# Uses historical EMEL-style data to predict free spots
# Works in Streamlit or Cursor IDE
# ==============================================================

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

# --------------------------------------------------------------
# 🧱 Page Configuration
# --------------------------------------------------------------
st.set_page_config(page_title="Lisbon Parking Prediction", layout="wide")
st.title("🚗 Lisbon Parking Vacancy Probability (EMEL Historical Data Demo)")

# --------------------------------------------------------------
# 📥 Load or Simulate EMEL Historical Datasets
# (replace with real CSVs from dados.gov.pt or EMEL portal)
# --------------------------------------------------------------

@st.cache_data
def load_emel_data():
    # Simulated parking locations
    locations = pd.DataFrame({
        "id": range(1, 51),
        "latitude": np.random.uniform(38.70, 38.76, 50),
        "longitude": np.random.uniform(-9.18, -9.10, 50),
        "capacity": np.random.randint(20, 100, 50),
        "zone_name": [f"Zona {i}" for i in range(1, 51)]
    })

    # Simulated occupancy history (3 days, hourly)
    records = []
    for _, row in locations.iterrows():
        for day in range(3):
            for hour in range(24):
                occupied = np.random.randint(0, row["capacity"])
                records.append({
                    "id": row["id"],
                    "timestamp": pd.Timestamp("2025-10-10") + pd.Timedelta(days=day, hours=hour),
                    "occupied": occupied,
                    "capacity": row["capacity"]
                })
    history = pd.DataFrame(records)
    return locations, history

locations, history = load_emel_data()

# --------------------------------------------------------------
# 🧮 Data Preprocessing
# --------------------------------------------------------------

history["timestamp"] = pd.to_datetime(history["timestamp"])
history["hour"] = history["timestamp"].dt.hour
history["weekday"] = history["timestamp"].dt.dayofweek
history["prob_vacant"] = (history["capacity"] - history["occupied"]) / history["capacity"]

# Merge with location info
data = history.merge(locations, on="id", how="left")

# Ensure capacity column exists (use capacity_x from history if capacity_y from locations is missing)
if 'capacity_y' in data.columns:
    data['capacity'] = data['capacity_y'].fillna(data['capacity_x'])
else:
    data['capacity'] = data['capacity_x']

# --------------------------------------------------------------
# 🧠 Train a Simple Prediction Model
# --------------------------------------------------------------

@st.cache_resource
def train_model():
    # Use the global data variable
    X = data[["hour", "weekday", "capacity"]]
    y = data["prob_vacant"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    return model, score, X_test, y_test

model, model_score, X_test, y_test = train_model()

# --------------------------------------------------------------
# 🎛️ User Controls
# --------------------------------------------------------------

with st.sidebar:
    st.header("Settings & Filters")
    selected_hour = st.slider("Hour of Day", 0, 23, 12)
    selected_weekday = st.selectbox("Day of Week", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    threshold = st.slider("Minimum Vacancy Probability", 0.0, 1.0, 0.3)

weekday_idx = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].index(selected_weekday)

# --------------------------------------------------------------
# 🔮 Predict Vacancy for Selected Time
# --------------------------------------------------------------

sample = pd.DataFrame({
    "hour": [selected_hour] * len(locations),
    "weekday": [weekday_idx] * len(locations),
    "capacity": locations["capacity"]
})

locations["pred_vacancy"] = model.predict(sample)
filtered = locations[locations["pred_vacancy"] >= threshold]

# --------------------------------------------------------------
# 🗺️ Map Visualization
# --------------------------------------------------------------

layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered,
    get_position=["longitude", "latitude"],
    get_radius=80,
    get_fill_color=[
        "255 * (1 - pred_vacancy)",
        "255 * pred_vacancy",
        50,
        200
    ],
    pickable=True
)

view_state = pdk.ViewState(
    latitude=38.7223,
    longitude=-9.1393,
    zoom=13
)

tooltip = {"text": "{zone_name}\nPredicted Vacancy: {pred_vacancy:.2f}"}

st.subheader("🗺️ Predicted Vacancy Map")
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip))

# --------------------------------------------------------------
# 📊 Summary & Model Metrics
# --------------------------------------------------------------

col1, col2, col3 = st.columns(3)
col1.metric("Total Parking Areas", len(locations))
col2.metric("Model R² Score", f"{model_score:.2f}")
col3.metric("Average Predicted Vacancy", f"{locations['pred_vacancy'].mean():.2f}")

# --------------------------------------------------------------
# 📈 Trend Visualization
# --------------------------------------------------------------

st.subheader("📈 Model Validation (Test Data)")
chart_data = pd.DataFrame({
    "Actual": y_test.reset_index(drop=True),
    "Predicted": model.predict(X_test)
})
st.line_chart(chart_data)

st.caption("Simulated EMEL data — replace with real CSVs for production use.")
