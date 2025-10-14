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
    # Simulated EMEL parking locations (based on real EMEL structure)
    locations = pd.DataFrame({
        "id_parque": range(1, 51),
        "nome_parque": [f"Parque {i}" for i in range(1, 51)],
        "zona": [f"Zona {np.random.randint(1, 6)}" for _ in range(50)],
        "latitude": np.random.uniform(38.70, 38.76, 50),
        "longitude": np.random.uniform(-9.18, -9.10, 50),
        "lugares_totais": np.random.randint(20, 100, 50),
        "preco_hora": np.random.uniform(0.5, 2.5, 50).round(2),
        "tipo_parque": np.random.choice(["Superfície", "Subterrâneo", "Misto"], 50)
    })

    # Simulated EMEL occupancy history (3 days, hourly)
    records = []
    for _, row in locations.iterrows():
        for day in range(3):
            for hour in range(24):
                # Simulate realistic occupancy patterns (higher during day, lower at night)
                base_occupancy = 0.3 + 0.4 * np.sin((hour - 6) * np.pi / 12)  # Peak around 12-14h
                base_occupancy = max(0.1, min(0.9, base_occupancy))  # Keep between 10-90%
                
                occupied = int(row["lugares_totais"] * base_occupancy + np.random.normal(0, 0.1))
                occupied = max(0, min(row["lugares_totais"], occupied))  # Ensure valid range
                
                records.append({
                    "id_parque": row["id_parque"],
                    "data": (pd.Timestamp("2025-10-10") + pd.Timedelta(days=day)).strftime("%Y-%m-%d"),
                    "hora": hour,
                    "lugares_totais": row["lugares_totais"],
                    "lugares_ocupados": occupied,
                    "lugares_livres": row["lugares_totais"] - occupied,
                    "taxa_ocupacao": round((occupied / row["lugares_totais"]) * 100, 2)
                })
    history = pd.DataFrame(records)
    return locations, history

locations, history = load_emel_data()

# --------------------------------------------------------------
# 🧮 Data Preprocessing
# --------------------------------------------------------------

# Create timestamp from data and hora columns
history["timestamp"] = pd.to_datetime(history["data"] + " " + history["hora"].astype(str) + ":00:00")
history["hour"] = history["hora"]
history["weekday"] = history["timestamp"].dt.dayofweek
history["prob_vacant"] = history["lugares_livres"] / history["lugares_totais"]

# Merge with location info
data = history.merge(locations, on="id_parque", how="left")

# Use the correct capacity column name
data['capacity'] = data['lugares_totais_x']

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
    "capacity": locations["lugares_totais"]
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

tooltip = {"text": "{nome_parque}\nZona: {zona}\nPredicted Vacancy: {pred_vacancy:.2f}"}

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
