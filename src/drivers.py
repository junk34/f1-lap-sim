class Driver:
    def __init__(self, name, base_lap_time, consistency=1.0, aggression=1.0):
        """
        Initializes a Driver object.

        Parameters:
        - name (str): Driver name
        - base_lap_time (float): Baseline lap time (in seconds)
        - consistency (float): Modifies lap variability (1.0 = neutral)
        - aggression (float): Affects strategy/risk (1.0 = neutral)
        """
        self.name = name
        self.base_lap_time = float(base_lap_time)
        self.consistency = float(consistency)
        self.aggression = float(aggression)

    def to_dict(self):
        return {
            "name": self.name,
            "base_lap_time": self.base_lap_time,
            "consistency": self.consistency,
            "aggression": self.aggression,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", "Unknown"),
            base_lap_time=data["base_lap_time"],
            consistency=data.get("consistency", 1.0),
            aggression=data.get("aggression", 1.0)
        )
