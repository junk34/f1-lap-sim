import math

class CarPhysics:
    def __init__(self, car_mass, engine_power, drag_coeff, frontal_area, tyre_mu):
        self.mass = car_mass
        self.power = engine_power
        self.Cd = drag_coeff
        self.A = frontal_area
        self.mu = tyre_mu
        self.rho = 1.225  # air density

    def drag_force(self, speed):
        return 0.5 * self.rho * self.Cd * self.A * speed**2

    def rolling_resistance(self):
        return 0.015 * self.mass * 9.81

    def max_accel(self, speed):
        F_engine = min(self.power / max(speed, 1), 15000)
        F_drag = self.drag_force(speed)
        F_roll = self.rolling_resistance()
        return (F_engine - F_drag - F_roll) / self.mass

    def corner_speed(self, radius):
        return math.sqrt(self.mu * 9.81 * radius)
