class LapSimulator:
    def __init__(self, track, driver):
        self.track = track
        self.driver = driver

    def calculate_lap_time(self, tire_wear=0, fuel_load=0):
        base_time = float(self.driver["base_lap_time"])
        
        # Make sure tire_wear is a real number and non-negative
        tire_wear = max(0, float(tire_wear))

        # Safe wear penalty calculation
        wear_penalty = 0.5 * (tire_wear ** 1.5) * self.track["tire_wear_factor"]

        # Fuel penalty (e.g., 0.03 seconds per unit of fuel)
        fuel_penalty = float(fuel_load) * 0.03

        # Return total lap time as a float
        return float(base_time + wear_penalty + fuel_penalty)

        
