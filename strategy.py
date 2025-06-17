import numpy as np

class RaceStrategy:
    def __init__(self, simulator):
        self.simulator = simulator

    def monte_carlo(self, simulations=500):
        laps = []
        for _ in range(simulations):
            lap = self.simulator.calculate_lap_time(
                tire_wear=np.random.uniform(0, 100),
                fuel_load=np.random.uniform(0, 100),
                weather="Clear"
            )
            laps.append(lap)
        return {
            "laps": laps,
            "best": min(laps),
            "avg": sum(laps) / len(laps),
            "std_dev": np.std(laps)
        }
