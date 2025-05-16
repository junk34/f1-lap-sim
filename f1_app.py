import streamlit as st
from src.simulator import LapSimulator
from src.strategy import RaceStrategy
import json
import os

# Title
st.title("🏁 F1 Lap Time Simulator")
st.subheader("Pick a driver and simulate a lap at Monaco")

# Get data path
def get_data_path(*args):
    return os.path.join("data", *args)

# Driver selection
driver_file = st.selectbox("Choose Driver", ["verstappen.json", "hamilton.json", "leclerc.json"])
track_file = "monaco.json"  # Static for now

# Load data
with open(get_data_path("drivers", driver_file)) as f:
    driver = json.load(f)

with open(get_data_path("tracks", track_file)) as f:
    track = json.load(f)

# Set parameters
fuel = st.slider("Fuel Load (kg)", 0, 100, 30)
wear = st.slider("Tire Wear (%)", 0, 100, 10)

# Run simulation
sim = LapSimulator(track, driver)
lap_time = sim.calculate_lap_time(tire_wear=wear, fuel_load=fuel)

st.metric("Simulated Lap Time", f"{lap_time:.3f} seconds")

# Strategy simulation
if st.button("Run Monte Carlo Strategy"):
    strategy = RaceStrategy(sim)
    results = strategy.monte_carlo()
    st.write(f"Best: {results['best']:.2f}s | Average: {results['avg']:.2f}s")

    from src.visualiser import plot_strategy
    import matplotlib.pyplot as plt
    import seaborn as sns

    st.pyplot(plt.gcf())  # Show last plot
