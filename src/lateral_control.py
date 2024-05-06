import numpy as np
from helper import angle_of_vectors
from structs_and_configs import State


class LateralControl:
    def __init__(self):
        self.k = 0.7
        self.max_steering_angle = 80

    def control(self, longest_vector, state: State) -> float:
        # Berechne den Betrag des Richtungsvektors
        Betrag = np.linalg.norm(longest_vector)

        if Betrag < 30:
            return 0

            # Berechnung des Zielwinkels
        target_angle = -angle_of_vectors(longest_vector, np.array([-1, 0]))
        print(f"Target angle: {target_angle}, magnitude: {Betrag}")

        # Richtung des Zielwinkels korrigieren, um sicherzustellen, dass er im Bereich [-90, 90] Grad liegt
        if target_angle > 90:
            target_angle -= 180
        elif target_angle < -90:
            target_angle += 180

        if -20 <= target_angle <= 20:
            return 0

        # Stanley-Regelung
        # Der Lenkwinkel wird angepasst, um den Zielwinkel zu erreichen
        steering_angle = target_angle * self.k

        # Skalierung des Lenkwinkels auf [-1, 1]
        norm_steering = steering_angle / self.max_steering_angle
        # Klemmen des Werts, um sicherzustellen, dass er innerhalb von [-1, 1] bleibt
        norm_steering = np.clip(norm_steering, -1, 1)

        return norm_steering
