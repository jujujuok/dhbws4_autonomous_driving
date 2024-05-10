import numpy as np
from helper import angle_of_vectors
from structs_and_configs import FRONT_DIRECTION
import math
from structs_and_configs import State


class LateralControl:

    def control(self, longest_vector, state: State) -> float:

        if longest_vector[0] == 0 and longest_vector[1] == 0:
            return 0 # drive forwards

        if longest_vector[1] > 0:
            longest_vector[1] += 15
        elif longest_vector[1] < 0:
            longest_vector[1] -= 15

        angle = angle_of_vectors(longest_vector, np.array([0, -1]))
        angle = ((angle - 90) / 90) * 1.7
        return angle





