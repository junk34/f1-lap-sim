class Driver:
    """
    Represents a racing driver with performance traits.

    Attributes:
    - name (str): Driver's name
    - base_lap_time (float): Baseline lap time in seconds
    - consistency (float): Modifies lap variability (1.0 = neutral)
    - aggression (float): Affects strategy/risk (1.0 = neutral)
    """

    def __init__(self, name: str, base_lap_time: float, consistency: float = 1.0, aggression: float = 1.0):
        if base_lap_time <= 0:
            raise ValueError("base_lap_time must be a positive number.")
        if not (0.0 <= consistency <= 2.0):
            raise ValueError("consistency must be between 0.0 and 2.0.")
        if not (0.0 <= aggression <= 2.0):
            raise ValueError("aggression must be between 0.0 and 2.0.")

        self.name = name.strip() or "Unknown"
        self.base_lap_time = float(base_lap_time)
        self.consistency = float(consistency)
        self.aggression = float(aggression)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "base_lap_time": self.base_lap_time,
            "consistency": self.consistency,
            "aggression": self.aggression,
        }

    @classmethod
    def from_dict(cls, data: dict):
        try:
            return cls(
                name=data.get("name", "Unknown"),
                base_lap_time=float(data["base_lap_time"]),
                consistency=float(data.get("consistency", 1.0)),
                aggression=float(data.get("aggression", 1.0))
            )
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"Invalid driver data: {e}")

    def __repr__(self) -> str:
        return (f"Driver(name='{self.name}', base_lap_time={self.base_lap_time}, "
                f"consistency={self.consistency}, aggression={self.aggression})")
