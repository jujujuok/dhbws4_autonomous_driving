from __future__ import annotations
import numpy as np


class LongitudinalControl:
    def __init__(self, Kp: float = 0.1, Ki: float = 0.018, Kd: float = 0.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral_error = 0.1
        self.previous_error = 0.0

    def control(self, current_speed: float, target_speed: float, steer_input: float) -> tuple:
        error = target_speed - current_speed
        self.integral_error += error
        self.integral_error = max(min(self.integral_error, 10), -10)

        proportional_term = self.Kp * error
        integral_term = self.Ki * self.integral_error
        derivative_term = self.Kd * (error - self.previous_error)

        # Calculate acceleration and braking
        acceleration = max(0, proportional_term + integral_term + derivative_term)
        braking = max(0, -proportional_term - integral_term - derivative_term)

        self.previous_error = error

        if acceleration > 0 and braking > 0:
            if acceleration > braking:
                braking = 0
            else:
                acceleration = 0

        return acceleration, braking

    def predict_target_speed(self, angle: float, magnitude: float) -> float:
        base_speed = 39
        speed_adjustment = 2 * np.cos(angle)
        #print("speed_adjustment",speed_adjustment)
        magnitude_factor = 0.1 * magnitude
        magnitude_factor2 = -0.8 * (magnitude_factor - magnitude)/ 5
        #print("magnitude_factor2",magnitude_factor2)
        return max(10, base_speed + speed_adjustment + magnitude_factor + magnitude_factor2)
