import numpy as np

class LapSimulator:
    def __init__(self, track, driver):
        self.track = track
        self.driver = driver
        
    def calculate_lap_time(self, tire_wear=0, fuel_load=0):
        # Base time + driver skill adjustments
        base_time = self.driver["base_lap_time"]
        
        # Tire wear penalty (non-linear)
        wear_penalty = 0.5 * (tire_wear ** 1.5) * self.track["tire_wear_factor"]
        
        # Fuel load effect (kg → seconds)
        fuel_penalty = fuel_load * 0.03  
        
        # Driver skill modifiers
        driver_mod = (1 - self.driver["tire_management"] * 0.2) * wear_penalty
        
        return base_time + fuel_penalty + driver_mod