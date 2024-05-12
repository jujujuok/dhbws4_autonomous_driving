import numpy as np
from helper import angle_of_vectors

from structs_and_configs import State

class LateralControl:
    def __init__(self):
        # Initialisiere Vektor, um eine Referenz zu haben
        self.last_vector: np.ndarray = np.array([-1,0])

    def control(self, longest_vector: np.ndarray, state: State) -> float:
        # Berechne die Norm von longest_vector
        norm = np.linalg.norm(longest_vector)
        if np.linalg.norm(self.last_vector) != norm:
            self.last_vector = longest_vector
        # Aktualisiere last_vector auf den neuen longest_vector

        # Wenn Longest Vektor nach voren Zeigt, übenimmt das auto keine Lenkanpassung
        if longest_vector[0] == 0 and longest_vector[1] == 0:
            return 0

        # Berechne den Winkel zwischen longest_vector und dem Richtungsvektor des Fahrzeuges
        angle = angle_of_vectors(longest_vector, np.array([0, -1]))
        # Normalisiere den Winkel zu einem Lenkbefehl
        angle = ((angle - 90) / 90)
        return angle
