class LapSimulator:
    def __init__(self, track, driver):
        self.track = track
        self.driver = driver

    def calculate_lap_time(self, tire_wear, fuel_load, weather="Clear"):
        # Safely get base lap time with fallback
        base_time = self.driver.get("base_lap_time", self.driver.get("base_time", 90))
        time = base_time

        # Apply fuel and tire wear penalties
        time += fuel_load * 0.035
        time += tire_wear * 0.04

        # Normalize weather input
        weather = weather.strip().capitalize()

        # Apply weather impact
        weather_penalty = {
            "Clear": 0.0,
            "Cloudy": 0.5,
            "Wet": 2.5,
            "Rain": 4.0,
            "Storm": 6.0
        }
        time += weather_penalty.get(weather, 0.0)

        return round(time, 3)

