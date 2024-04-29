import numpy as np
from helper import angle_of_vectors
from structs_and_configs import FRONT_DIRECTION
import math


class LateralControl:
    def __init__(self):
        self._car_position = np.array([48, 64])

    def control(self, front: float, longest_vector: np.ndarray, speed: float) -> list:

        angle = angle_of_vectors(longest_vector, FRONT_DIRECTION)

        print(angle)

        if angle < 0:
            angle = 0
        elif angle > 90:
            angle = 90

        mapped_value = sigmoid(angle / 90.0)

        return angle


def sigmoid(x):
    return 1 / (1 + math.exp(-x))
