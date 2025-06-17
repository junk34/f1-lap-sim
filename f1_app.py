import streamlit as st
from src.simulator import LapSimulator
from src.strategy import RaceStrategy
import json
import os
import matplotlib.pyplot as plt

# Custom CSS for F1-style
st.markdown("""
<style>
    .header-style {
        font-size: 28px;
        font-weight: bold;
        color: #E10600;
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
    .error-box {
        background-color: #2D0000;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="header-style">🏎️ F1 LAP SIMULATOR</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader-style">Select driver and track to simulate lap times</p>', unsafe_allow_html=True)

# Helper to get data path with verification
def get_data_path(*args):
    path = os.path.join("data", *args)
    if not os.path.exists(path):
        st.markdown(f'<div class="error-box">Error: Path not found - {path}</div>', unsafe_allow_html=True)
    return path

# JSON file validation
def validate_json_folder(folder_path, label):
    issues = []
    if os.path.exists(folder_path):
        for f in sorted(os.listdir(folder_path)):
            if f.endswith(".json"):
                filepath = os.path.join(folder_path, f)
                try:
                    if os.path.getsize(filepath) == 0:
                        issues.append(f"[{label}] Empty file: {f}")
                    else:
                        with open(filepath, "r") as file:
                            json.load(file)
                except json.JSONDecodeError as e:
                    issues.append(f"[{label}] Invalid JSON in {f}: {str(e)}")
                except Exception as e:
                    issues.append(f"[{label}] Error reading {f}: {str(e)}")
    return issues

driver_issues = validate_json_folder(get_data_path("drivers"), "Driver")
track_issues = validate_json_folder(get_data_path("tracks"), "Track")
for issue in driver_issues + track_issues:
    st.warning(issue)

# Load data
@st.cache_data
def load_data():
    def load_json_data(folder):
        data = {}
        if os.path.exists(folder):
            for f in sorted(os.listdir(folder)):
                if f.endswith(".json"):
                    filepath = os.path.join(folder, f)
                    try:
                        with open(filepath, 'r') as file:
                            content = file.read()
                            if not content.strip():
                                st.warning(f"Empty file: {f}")
                                continue
                            data[f.replace(".json", "")] = json.loads(content)
                    except json.JSONDecodeError as e:
                        st.error(f"Invalid JSON in {f}: {str(e)}")
                    except Exception as e:
                        st.error(f"Error loading {f}: {str(e)}")
        else:
            st.error(f"Directory not found: {folder}")
        return data

    drivers = load_json_data(get_data_path("drivers"))
    tracks = load_json_data(get_data_path("tracks"))
    return drivers, tracks

try:
    drivers, tracks = load_data()
except Exception as e:
    st.error(f"Failed to load data: {str(e)}")
    st.stop()

with st.expander("Debug: View Loaded Data"):
    st.write("Drivers loaded:", list(drivers.keys()))
    st.write("Tracks loaded:", list(tracks.keys()))

# Layout
col1, col2 = st.columns(2)

with col1:
    if drivers:
        driver_name = st.selectbox("DRIVER", options=list(drivers.keys()))
        driver = drivers[driver_name]
        st.image(driver.get("image_path", "default_driver.png"), width=150,
                 caption=f"{driver_name} - {driver.get('team', 'Unknown Team')}")
        st.caption(f"Base Lap Time: {driver.get('base_time', driver.get('base_lap_time', 'N/A'))}s")
    else:
        st.error("No driver data available")

with col2:
    if tracks:
        track_name = st.selectbox("TRACK", options=list(tracks.keys()))
        track = tracks[track_name]
        st.image(track.get("image_path", "default_track.png"), width=200,
                 caption=f"{track_name} - {track.get('location', 'Unknown Location')}")
        st.caption(f"Length: {track.get('lap_distance', track.get('length', 'N/A'))}km")
        st.caption(f"Corners: {track.get('corners', 'N/A')}")
    else:
        st.error("No track data available")

# Parameters
st.subheader("SIMULATION PARAMETERS")
fuel = st.slider("FUEL LOAD (kg)", 0, 100, 30)
wear = st.slider("TIRE WEAR (%)", 0, 100, 10)
weather = st.selectbox(
    "WEATHER CONDITIONS",
    options=["☀️ Clear", "⛅ Cloudy", "🌧️ Wet", "🌧️ Rain", "⛈️ Storm"]
).split(" ", 1)[-1]

# Simulate
if st.button("SIMULATE LAP", type="primary"):
    if not drivers or not tracks:
        st.error("Cannot simulate - missing driver or track data")
    else:
        try:
            sim = LapSimulator(track, driver)
            lap_time = sim.calculate_lap_time(tire_wear=wear, fuel_load=fuel, weather=weather)

            st.markdown("---")
            st.markdown("### SIMULATION RESULT")
            col_res1, col_res2 = st.columns(2)
            col_res1.metric("DRIVER", driver_name.upper())
            col_res2.metric("TRACK", track_name.upper())

            base_time = driver.get('base_time', driver.get('base_lap_time', lap_time))
            delta = float(base_time) - lap_time if isinstance(base_time, (int, float)) else 0

            st.metric("SIMULATED LAP TIME",
                      f"{lap_time:.3f} seconds",
                      delta=f"{delta:.3f}s vs base",
                      delta_color="inverse")
        except Exception as e:
            st.error(f"Simulation failed: {str(e)}")

# Strategy
st.markdown("---")
if st.button("RUN STRATEGY ANALYSIS", type="secondary"):
    if not drivers or not tracks:
        st.error("Cannot analyze strategy - missing driver or track data")
    else:
        try:
            sim = LapSimulator(track, driver)
            strategy = RaceStrategy(sim)
            results = strategy.monte_carlo()

            st.markdown("### STRATEGY ANALYSIS")
            cols = st.columns(3)
            cols[0].metric("Best Lap", f"{results['best']:.3f}s")
            cols[1].metric("Average", f"{results['avg']:.3f}s")
            cols[2].metric("Consistency", f"{results['std_dev']:.3f}s σ")

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.hist(results["laps"], bins=20, color="#E10600", edgecolor='black')
            ax.set_xlabel("Lap Time (seconds)")
            ax.set_ylabel("Frequency")
            ax.set_title("Lap Time Distribution")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Strategy analysis failed: {str(e)}")
