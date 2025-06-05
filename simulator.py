def calculate_lap_time(self, tire_wear=0, fuel_load=0, weather="Clear"):
    base_time = float(self.driver.get('base_time', 90.0))
    track_factor = 1 + (float(self.track.get('difficulty', 50)) / 100)

    time = base_time * track_factor
    time += fuel_load * 0.03
    time += tire_wear * 0.02

    # Skill impact
    skill_factor = 1 - (float(self.driver.get('skill', 50)) / 500)
    time *= skill_factor

    # Weather penalty
    weather_impact = {
        "Clear": 0.0,
        "Cloudy": 0.2,
        "Wet": 1.0,
        "Rain": 2.0,
        "Storm": 3.0
    }
    time += weather_impact.get(weather, 0.0)

    # Random variation
    import random
    time += random.uniform(-0.5, 0.5)

    return round(time, 3)

