import numpy as np
from helper import angle_of_vectors
from structs_and_configs import FRONT_DIRECTION



class LateralControl:
    def __init__(self):
        self._car_position = np.array([48, 64])

    def control(self, front: float, longest_vector: np.ndarray, speed: float) -> list:
        # Berechnen des Winkels

        angle = angle_of_vectors(longest_vector, FRONT_DIRECTION) -90
        #print(longest_vector)
        print(angle)



        # Umrechnung Winkle in Radiant
        angle_rad = np.deg2rad(angle)



        # Berechnnug Lenkwinkels
        steering_angle = -np.sin(
            angle_rad)
        # Negative Sinus, da eine Korrektur

        # Normalisieren des Lenkwinkels
        steering_angle = np.clip(steering_angle, -1, 1)


        #konst speed
        speed = 0.02

        # Geschwindigkeit beibehalten, kein Bremsen
        return [steering_angle, speed, 0]