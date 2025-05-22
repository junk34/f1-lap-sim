import streamlit as st
from src.simulator import LapSimulator
from src.strategy import RaceStrategy
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Custom CSS for F1-style
st.markdown("""
<style>
    .header-style {
        font-size: 28px;
        font-weight: bold;
        color: #E10600;  /* F1 Red */
        text-align: center;
        margin-bottom: 10px;
    }
    .subheader-style {
        font-size: 16px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-value {
        font-size: 28px !important;
        color: #E10600 !important;
    }
    .stSelectbox, .stSlider {
        background-color: #1E1E1E;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="header-style">🏎️ F1 LAP SIMULATOR</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader-style">Select driver and track to simulate lap times</p>', unsafe_allow_html=True)

# Helper to get data path
def get_data_path(*args):
    return os.path.join("data", *args)

# Load all driver and track data
@st.cache_data
def load_data():
    drivers = {}
    for f in sorted(os.listdir(get_data_path("drivers"))):
        if f.endswith(".json"):
            with open(get_data_path("drivers", f)) as file:
                drivers[f.replace(".json","")] = json.load(file)
    
    tracks = {}
    for f in sorted(os.listdir(get_data_path("tracks"))):
        if f.endswith(".json"):
            with open(get_data_path("tracks", f)) as file:
                tracks[f.replace(".json","")] = json.load(file)
    return drivers, tracks

drivers, tracks = load_data()

# Create two columns
col1, col2 = st.columns(2)

with col1:
    # Driver selection with profile display
    driver_name = st.selectbox("DRIVER", options=list(drivers.keys()))
    driver = drivers[driver_name]
    st.image(driver.get("image_path", "default_driver.png"), width=150)
    st.caption(f"Team: {driver['team']}")
    st.caption(f"Base Lap Time: {driver['base_time']}s")

with col2:
    # Track selection with info display
    track_name = st.selectbox("TRACK", options=list(tracks.keys()))
    track = tracks[track_name]
    st.image(track.get("image_path", "default_track.png"), width=200)
    st.caption(f"Length: {track['length']}km")
    st.caption(f"Corners: {track['corners']}")

# Simulation parameters
st.subheader("SIMULATION PARAMETERS")
fuel = st.slider("FUEL LOAD (kg)", 0, 100, 30, help="Higher fuel load increases lap time")
wear = st.slider("TIRE WEAR (%)", 0, 100, 10, help="Higher wear degrades performance")

# Run simulation
if st.button("SIMULATE LAP", type="primary"):
    sim = LapSimulator(track, driver)
    lap_time = sim.calculate_lap_time(tire_wear=wear, fuel_load=fuel)
    
    # Display result with F1 style
    st.markdown("---")
    st.markdown("### SIMULATION RESULT")
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("DRIVER", f"{driver_name.upper()}")
    with col_res2:
        st.metric("TRACK", f"{track_name.upper()}")
    
    st.metric("SIMULATED LAP TIME", 
              f"{lap_time:.3f} seconds",
              delta=f"{(driver['base_time'] - lap_time):.3f}s vs base",
              delta_color="inverse")

# Strategy simulation
st.markdown("---")
if st.button("RUN STRATEGY ANALYSIS", type="secondary"):
    sim = LapSimulator(track, driver)
    strategy = RaceStrategy(sim)
    results = strategy.monte_carlo()
    
    st.markdown("### STRATEGY ANALYSIS")
    cols = st.columns(3)
    cols[0].metric("Best Lap", f"{results['best']:.3f}s")
    cols[1].metric("Average", f"{results['avg']:.3f}s")
    cols[2].metric("Consistency", f"{results['std_dev']:.3f}s σ")
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(results["laps"], bins=20, kde=True, color="#E10600")
    ax.set_xlabel("Lap Time (seconds)")
    ax.set_title("Lap Time Distribution")
    st.pyplot(fig)
