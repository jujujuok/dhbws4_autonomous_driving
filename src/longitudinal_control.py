from __future__ import annotations
import numpy as np


class LongitudinalControl:
    # Initialisiesirung PID-Reglerparameter
    def __init__(self, Kp: float = 0.1, Ki: float = 0.015, Kd: float = 0.0):
        self.Kp = Kp  # Proportionalbeiwert
        self.Ki = Ki  # Integralbeiwert
        self.Kd = Kd  # Differentialbeiwert
        self.integral_error = 0.1  # Startwert Fehlerintegration
        self.previous_error = 0.0  # Startwert vorherigen Fehlers

    # Berechnet Beschleunigung und Bremsung
    # basierend auf der aktuellen gewünschten Geschwindigkeit
    def control(
        self, current_speed: float, target_speed: float, steer_input: float
    ) -> tuple:
        # Fehler berechnen
        error = target_speed - current_speed
        self.integral_error += error
        # Begrenzung der Fehlerintegration
        self.integral_error = max(min(self.integral_error, 10), -10)

        # PID-Terme berechnen
        proportional_term = self.Kp * error
        integral_term = self.Ki * self.integral_error
        derivative_term = self.Kd * (error - self.previous_error)

        # Berechne Beschleunigung und Bremsung
        acceleration = max(0, proportional_term + integral_term + derivative_term)
        braking = max(0, -proportional_term - integral_term - derivative_term)

        self.previous_error = error  # Aktualisiere den vorherigen Fehler

        # Verhindere, dass sowohl Beschleunigung als auch Bremsung zur gliechen Zeit
        if acceleration > 0 and braking > 0:
            if acceleration > braking:
                braking = 0
            else:
                acceleration = 0

        return acceleration, braking

    # berechnung Zielgeschwindigkeit basierend auf Lenkwinkel und Betrag Longest Vektor
    def predict_target_speed(self, angle: float, magnitude: float) -> float:
        base_speed = 33  # Basisgeschwindigkeit
        speed_adjustment = 1.5 * np.cos(
            angle
        )  # Geschwindigkeitsanpassung durch cos des Winkels
        # print(speed_adjustment)
        magnitude_factor = 0.1 * magnitude  # Faktor basierend auf der Lenkintensität
        # Zusätzliche Anpassung
        magnitude_factor2 = -1 * (magnitude_factor - magnitude) / 6
        # Geschwindigkeitsberechnung kombiniert
        # return max(10, base_speed + magnitude_factor + magnitude_factor2 + speed_adjustment)

        # Falls etwas agresiver gefahren werden soll, kann aber aß der Kurve Fliegen
        return (
            max(
                10, base_speed + magnitude_factor + magnitude_factor2 + speed_adjustment
            )
            * 1.2
        )
