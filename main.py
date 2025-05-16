from src.simulator import LapSimulator
from src.strategy import RaceStrategy
from src.visualiser import plot_strategy
import json
import os
import sys

# Add 'src' directory to the Python module search path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Get absolute path to data files
def get_data_path(*args):
    return os.path.join(os.path.dirname(__file__), 'data', *args)

def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found - {path}")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON - {path}")
        exit(1)

def main():
    # Load data
    driver = load_json(get_data_path('drivers', 'verstappen.json'))
    track = load_json(get_data_path('tracks', 'monaco.json'))

    # Run simulation
    sim = LapSimulator(track, driver)
    strategy = RaceStrategy(sim)
    results = strategy.monte_carlo()

    print(f"\n--- Simulation Results ---")
    print(f"Best Case:   {results['best']:.2f} s")
    print(f"Average:     {results['avg']:.2f} s")

    # Optional visualization
    if 'all' in results:
        plot_strategy(results['all'])

if __name__ == "__main__":
    main()
