from __future__ import annotations
import numpy as np


class LongitudinalControl:
    def __init__(self, Kp: float = 0.1, Ki: float = 0.01, Kd: float = 0.05):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral_error = 0.0
        self.previous_error = 0.0

    def control(self, current_speed: float, target_speed: float, steer_input: float) -> tuple:
        error = target_speed - current_speed
        self.integral_error += error
        proportional_term = self.Kp * error
        integral_term = self.Ki * self.integral_error
        derivative_term = self.Kd * (error - self.previous_error)
        acceleration = max(0, proportional_term + integral_term + derivative_term)
        braking = max(0, -proportional_term - integral_term - derivative_term)
        self.previous_error = error  # Aktualisierung des vorherigen Fehlers für die nächste Iteration
        return acceleration, braking

    def predict_target_speed(self, angle: float, magnitude: float) -> float:
        base_speed = 40  # Basisgeschwindigkeit
        speed_adjustment = 3.5 * np.cos(angle)  # Geschwindigkeitsanpassung basierend auf dem Winkel
        magnitude_factor = 0.1 * magnitude  # Einfluss des Betrags
        return max(0, base_speed + speed_adjustment + magnitude_factor)