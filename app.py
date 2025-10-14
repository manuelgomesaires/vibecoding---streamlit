import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Parking Map")

st.title("Empty Parking Spaces Map")

# Initialize storage for parking spots in session
if "spots" not in st.session_state:
  st.session_state.spots = []  # list of {"lat": float, "lon": float}

with st.expander("Add parking spot"):
  c1, c2, c3 = st.columns([1,1,1])
  with c1:
    lat = st.number_input("Latitude", value=38.7223, format="%.6f")
  with c2:
    lon = st.number_input("Longitude", value=-9.1393, format="%.6f")
  with c3:
    if st.button("Add spot"):
      st.session_state.spots.append({"lat": float(lat), "lon": float(lon)})

c4, c5 = st.columns([1,1])
with c4:
  if st.button("Load demo spots"):
    # Simple demo set (around Lisbon). Replace with real data later.
    st.session_state.spots = [
      {"lat": 38.7223, "lon": -9.1393},
      {"lat": 38.7230, "lon": -9.1400},
      {"lat": 38.7215, "lon": -9.1385},
    ]
with c5:
  if st.button("Clear spots"):
    st.session_state.spots = []

st.subheader("Recommendations")
with st.expander("Load most probable spots"):
  top_n = st.slider("How many spots?", 1, 20, 5)
  center_lat = st.number_input("Center latitude", value=38.7223, format="%.6f")
  center_lon = st.number_input("Center longitude", value=-9.1393, format="%.6f")
  if st.button("Generate recommendations"):
    # Mock: generate 50 candidates around the center with random probability
    candidates = []
    for _ in range(50):
      dlat = random.uniform(-0.01, 0.01)
      dlon = random.uniform(-0.01, 0.01)
      prob = random.random()
      candidates.append({"lat": center_lat + dlat, "lon": center_lon + dlon, "prob": prob})
    # Pick top-N by probability
    candidates.sort(key=lambda x: x["prob"], reverse=True)
    selected = [{"lat": c["lat"], "lon": c["lon"]} for c in candidates[:top_n]]
    # Merge into current spots
    st.session_state.spots.extend(selected)
    st.success(f"Loaded {len(selected)} recommended spot(s)")

st.subheader("Map")
if st.session_state.spots:
  df = pd.DataFrame(st.session_state.spots)
  st.caption(f"Showing {len(df)} spot(s)")
  st.map(df, zoom=15)
else:
  st.info("No spots yet. Add one above or load demo spots.")
