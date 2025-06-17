class LapSimulator:
    def __init__(self, track, driver):
        self.track = track
        self.driver = driver

    def calculate_lap_time(self, tire_wear, fuel_load, weather="Clear"):
        base_time = self.driver.get("base_lap_time", 90)
        time = base_time
        time += fuel_load * 0.035
        time += tire_wear * 0.04
        if weather == "Cloudy":
            time += 0.5
        elif weather == "Wet":
            time += 2.5
        elif weather == "Rain":
            time += 4.0
        elif weather == "Storm":
            time += 6.0
        return time

