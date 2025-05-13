from src.simulator import LapSimulator
from src.strategy import RaceStrategy
import json

# Load data
with open("data/drivers/verstappen.json") as f:
    driver = json.load(f)
    
with open("data/tracks/monaco.json") as f:
    track = json.load(f)

# Run simulation
sim = LapSimulator(track, driver)
strategy = RaceStrategy(sim)
results = strategy.monte_carlo()

print(f"Best Case: {results['best']:.2f}s")
print(f"Average: {results['avg']:.2f}s")