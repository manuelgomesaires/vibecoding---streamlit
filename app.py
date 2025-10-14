import streamlit as st
import pandas as pd

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

st.subheader("Map")
if st.session_state.spots:
  df = pd.DataFrame(st.session_state.spots)
  st.caption(f"Showing {len(df)} spot(s)")
  st.map(df, zoom=15)
else:
  st.info("No spots yet. Add one above or load demo spots.")
