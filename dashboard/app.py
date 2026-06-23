import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mock_data import generate_mock_dem, generate_mock_radar
from src.radar_engine import compute_cpr_dop
from src.terrain_engine import compute_slope
from src.ml_engine import train_and_predict_ice

st.set_page_config(page_title="LunaIceNet Dashboard", layout="wide")

st.title("🌙 LunaIceNet MVP Dashboard")
st.markdown("**Subsurface Ice Detection in Doubly-Shadowed Lunar Craters**")

@st.cache_data
def load_data():
    dem = generate_mock_dem((200, 200))
    hh, hv, vv = generate_mock_radar((200, 200))
    return dem, hh, hv, vv

dem, hh, hv, vv = load_data()

# Processing
cpr, dop = compute_cpr_dop(hh, hv, vv)
slope = compute_slope(dem)
ice_prob = train_and_predict_ice(cpr, dop, slope)

tab1, tab2, tab3 = st.tabs(["Terrain & Radar", "Derived Metrics", "Ice Classification"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Simulated DEM (Elevation)")
        fig, ax = plt.subplots()
        im = ax.imshow(dem, cmap='terrain')
        plt.colorbar(im, ax=ax, label='Elevation (m)')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Simulated Radar (HH Channel)")
        fig, ax = plt.subplots()
        im = ax.imshow(hh, cmap='gray')
        plt.colorbar(im, ax=ax, label='Backscatter')
        st.pyplot(fig)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Circular Polarization Ratio (CPR)")
        st.write("Bright areas indicate multiple scattering (Ice or Rocks).")
        fig, ax = plt.subplots()
        im = ax.imshow(cpr, cmap='jet', vmin=0, vmax=2)
        plt.colorbar(im, ax=ax, label='CPR')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Terrain Slope")
        st.write("Steep slopes (crater rims) are rocky and unsafe.")
        fig, ax = plt.subplots()
        im = ax.imshow(slope, cmap='magma')
        plt.colorbar(im, ax=ax, label='Slope (Degrees)')
        st.pyplot(fig)

with tab3:
    st.subheader("Machine Learning Ice Probability Map")
    st.write("The RF model uses CPR, DOP, and Slope to filter out the rocky crater rims and highlight flat, radar-bright ice deposits.")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(ice_prob, cmap='Blues', vmin=0, vmax=1)
    plt.colorbar(im, ax=ax, label='Probability of Ice')
    
    # Overlay contours of the crater rim for context
    ax.contour(dem, levels=[0], colors='red', alpha=0.5, linewidths=1)
    st.pyplot(fig)

st.sidebar.title("Mission Controls")
st.sidebar.info("This MVP uses synthetically generated radar and DEM matrices to simulate the lunar environment.")
if st.sidebar.button("Regenerate Synthetic Data"):
    st.cache_data.clear()
    st.rerun()
