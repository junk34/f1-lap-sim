from typing import List
import random
import numpy as np

class RaceStrategy:
    def __init__(self, simulator):
        self.sim = simulator
        
    def monte_carlo(self, laps: int = 50, n_sim: int = 1000) -> dict:
        """
        Run Monte Carlo simulation of race strategies
        
        Args:
            laps: Number of laps in the race
            n_sim: Number of simulations to run
            
        Returns:
            Dictionary with:
            - 'best': Best case race time (seconds)
            - 'avg': Average race time
            - 'p90': 90th percentile race time
        """
        results = []
        
        for _ in range(n_sim):
            total_time = 0.0  # Initialize as float
            tires = "soft"
            tire_life = 20
            fuel_load = 110.0  # Starting fuel (kg)
            
            for lap in range(laps):
                # Calculate lap time with type safety
                lap_time = float(self.sim.calculate_lap_time(
                    tire_wear=max(0, 20 - tire_life),  # Ensure non-negative
                    fuel_load=max(0.0, fuel_load)      # Ensure non-negative float
                ))
                total_time += lap_time
                fuel_load -= 2.0  # Fuel consumption per lap
                
                # Pit stop logic
                if tire_life <= 0:
                    total_time += random.uniform(21.5, 23.5)  # Realistic pit time variance
                    tires = random.choice(["medium", "hard"])
                    tire_life = 30 if tires == "hard" else 20
                
                tire_life -= 1
                
                # Random safety car (10% chance)
                if random.random() < 0.1:
                    total_time += random.uniform(14, 18)  # SC duration variance
            
            results.append(float(total_time))
        
        return {
            "best": float(np.min(results)),
            "avg": float(np.mean(results)),
            "p90": float(np.percentile(results, 90)),
            "worst": float(np.max(results))  # Added for completeness
        }