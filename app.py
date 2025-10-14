import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# --- Page setup ---
st.set_page_config(page_title="Parking Vacancy Probability", layout="wide")

st.title("🚗 Parking Vacancy Probability")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Filters & Settings")
    threshold = st.slider("Min vacancy probability", 0.0, 1.0, 0.3)
    area = st.selectbox("Area", ["Baixa", "Chiado", "Alfama", "Bairro Alto", "Belém"])
    time_of_day = st.slider("Time of day", 0, 23, 18)
    show_heatmap = st.checkbox("Show as heatmap", False)
    refresh = st.button("Refresh 🔄")

# --- Generate or Load Data (Simulated Example) ---
np.random.seed(42)
data = pd.DataFrame({
    "lat": np.random.uniform(38.70, 38.75, 50),
    "lon": np.random.uniform(-9.15, -9.10, 50),
    "prob_vacant": np.random.rand(50),
    "location_name": [f"Lisbon Spot {i}" for i in range(1, 51)]
})

# Filter by threshold
filtered = data[data["prob_vacant"] >= threshold]

# --- Summary statistics ---
total_spots = len(data)
avg_prob = data["prob_vacant"].mean()
best_area = "Chiado (72%)"  # placeholder; could be computed from data

# --- Map Visualization ---
if show_heatmap:
    layer = pdk.Layer(
        "HeatmapLayer",
        data=filtered,
        get_position=["lon", "lat"],
        get_weight="prob_vacant",
        radiusPixels=60,
    )
else:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered,
        get_position=["lon", "lat"],
        get_radius=60,
        get_fill_color=[
            "255 * (1 - prob_vacant)",
            "255 * prob_vacant",
            100,
            160
        ],
        pickable=True,
    )

view_state = pdk.ViewState(
    latitude=data["lat"].mean(),
    longitude=data["lon"].mean(),
    zoom=14
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{location_name}\nVacancy Probability: {prob_vacant}"}
)

# --- Layout: Map + Summary ---
col1, col2 = st.columns([2.5, 1])

with col1:
    st.pydeck_chart(r)

with col2:
    st.subheader("Summary")
    st.metric("Total Spots", total_spots)
    st.metric("Avg Vacancy Probability", f"{avg_prob:.2f}")
    st.metric("Best Area", best_area)

# --- Vacancy Trends ---
st.subheader("📈 Vacancy Trends")
hours = np.arange(0, 24)
trend_data = pd.DataFrame({
    "Hour": hours,
    "Vacancy Probability": np.clip(np.sin(hours / 3) * 0.3 + 0.5 + np.random.rand(24) * 0.1, 0, 1)
})
st.line_chart(trend_data, x="Hour", y="Vacancy Probability")

# --- Footer ---
st.caption("Lisbon parking vacancy probability based on car movement patterns.")
