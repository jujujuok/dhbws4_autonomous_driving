from __future__ import annotations


class LongitudinalControl:
    def __init__(self):
        self.kp = 1.0
        self.ki = 0.1
        self.kd = 0.05
        self.set_speed = 30  # Zielgeschwindigkeit in km/h
        self.integral = 0
        self.last_error = 0

    def control(self, current_speed):
        error = self.set_speed - current_speed
        self.integral += error
        derivative = error - self.last_error

        # PID-Regelung für die Beschleunigung
        acceleration = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.last_error = error

        return acceleration