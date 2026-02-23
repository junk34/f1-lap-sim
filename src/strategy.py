from typing import Dict
import random
import numpy as np

class RaceStrategy:
    def __init__(self, simulator):
        self.sim = simulator

    def monte_carlo(self, laps: int = 50, n_sim: int = 1000, weather: str = "dry") -> Dict[str, float]:
        """
        Simulate race strategies using Monte Carlo method.

        Args:
            laps (int): Total number of laps in the race.
            n_sim (int): Number of simulations to run.
            weather (str): Weather condition affecting lap times.

        Returns:
            Dict[str, float]: Summary statistics of race times.
        """
        results = np.zeros(n_sim)

        for i in range(n_sim):
            total_time = 0.0
            tires = "soft"
            tire_life = self._get_tire_life(tires)
            fuel_load = 110.0

            for lap in range(laps):
                tire_wear = max(0, 20 - tire_life)
                lap_time = self.sim.calculate_lap_time(
                    tire_wear=tire_wear,
                    fuel_load=max(0.0, fuel_load),
                    weather=weather
                )
                total_time += lap_time
                fuel_load -= 2.0
                tire_life -= 1

                # Pit stop if tires are done
                if tire_life <= 0:
                    total_time += random.uniform(21.5, 23.5)
                    tires = random.choice(["medium", "hard"])
                    tire_life = self._get_tire_life(tires)

                # Safety car event (10% chance)
                if random.random() < 0.1:
                    total_time += random.uniform(14, 18)

            results[i] = total_time

        return {
            "best": float(np.min(results)),
            "avg": float(np.mean(results)),
            "p90": float(np.percentile(results, 90)),
            "worst": float(np.max(results))
        }

    def _get_tire_life(self, compound: str) -> int:
        """Returns tire life based on compound type."""
        return {
            "soft": 20,
            "medium": 25,
            "hard": 30
        }.get(compound, 20)
