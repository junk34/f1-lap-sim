class LapSimulator:
    def __init__(self, track, driver):
        self.track = track
        self.driver = driver

    def calculate_lap_time(self, tire_wear=0, fuel_load=0, weather="dry"):
        base_time = float(self.driver["base_lap_time"])

        # Tire wear penalty
        tire_wear = max(0, float(tire_wear))
        wear_penalty = 0.5 * (tire_wear ** 1.5) * self.track["tire_wear_factor"]

        # Fuel load penalty
        fuel_penalty = float(fuel_load) * 0.03

        # Weather penalty
        weather_penalty = self._get_weather_penalty(weather)

        # Total lap time
        return float(base_time + wear_penalty + fuel_penalty + weather_penalty)

    def _get_weather_penalty(self, weather):
        """Returns a time penalty based on weather conditions."""
        weather = str(weather).lower()
        penalties = {
            "dry": 0.0,
            "wet": 2.5,
            "storm": 5.0,
            "fog": 1.5,
            "snow": 6.0
        }
        return penalties.get(weather, 0.0)  # default to 0 if unknown


        
