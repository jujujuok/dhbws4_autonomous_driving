import numpy as np
from helper import angle_of_vectors
from structs_and_configs import FRONT_DIRECTION
import math


class LateralControl:

    def control(self, longest_vector: np.ndarray) -> float:

        angle = angle_of_vectors(longest_vector, np.array([-1, 0]))

        angle = (angle - 90) / 90

        print(f"Angle: {angle}")

        return angle