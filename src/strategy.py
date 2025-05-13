from typing import List
import random

class RaceStrategy:
    def __init__(self, simulator):
        self.sim = simulator
        
    def monte_carlo(self, laps=50, n_sim=1000):
        results = []
        for _ in range(n_sim):
            total_time = 0
            tires = "soft"
            tire_life = 20
            
            for lap in range(laps):
                # Simulate random safety car (10% chance)
                if random.random() < 0.1:
                    total_time += 15  # Slow laps under SC
                
                # Pit stop logic
                if tire_life <= 0:
                    total_time += 22  # Pit stop time
                    tires = random.choice(["medium", "hard"])
                    tire_life = 30 if tires == "hard" else 20
                
                # Calculate lap time
                lap_time = self.sim.calculate_lap_time(
                    tire_wear=20 - tire_life,
                    fuel_load=max(0, 110 - lap*2))  # Fuel burn
                
                total_time += lap_time
                tire_life -= 1
            
            results.append(total_time)
        
        return {
            "best": min(results),
            "avg": sum(results)/len(results),
            "p90": np.percentile(results, 90)
        }