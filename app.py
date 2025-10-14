import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

st.set_page_config(page_title="Parking Vacancy Map", layout="wide")

st.title("🚗 Parking Vacancy Probability Map")

# --- Simulated Data ---
np.random.seed(42)
data = pd.DataFrame({
    "lat": np.random.uniform(37.77, 37.79, 50),
    "lon": np.random.uniform(-122.42, -122.40, 50),
    "prob_vacant": np.random.rand(50),
    "location_name": [f"Spot {i}" for i in range(1, 51)]
})

# --- Controls ---
threshold = st.slider("Minimum Vacancy Probability", 0.0, 1.0, 0.3)
filtered = data[data["prob_vacant"] >= threshold]

# --- Map Layer ---
layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered,
    get_position=["lon", "lat"],
    get_radius=50,
    get_fill_color=[
        "255 * (1 - prob_vacant)",  # Red when low
        "255 * prob_vacant",        # Green when high
        100,
        160
    ],
    pickable=True
)

# --- View ---
view_state = pdk.ViewState(
    latitude=data["lat"].mean(),
    longitude=data["lon"].mean(),
    zoom=14
)

# --- Render ---
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{location_name}\nVacancy Probability: {prob_vacant}"}
)

st.pydeck_chart(r)

st.write(f"Showing {len(filtered)} of {len(data)} locations (≥ {threshold:.2f} probability).")
