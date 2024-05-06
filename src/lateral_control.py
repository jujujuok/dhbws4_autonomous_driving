import numpy as np
from helper import angle_of_vectors
from structs_and_configs import FRONT_DIRECTION
import math
from structs_and_configs import State


class LateralControl:

    def __init__(self):
        self.last_vector: np.ndarray = np.array([-1,0])

    def control(self, longest_vector:np.ndarray, state: State) -> float:

        norm = np.linalg.norm(longest_vector)
        if np.linalg.norm(self.last_vector) != norm:
            self.last_vector = longest_vector
            

        if longest_vector[0] == 0 and longest_vector[1] == 0:
            return 0 # drive forwards
                
        print(f"longest vector: {longest_vector}")
        
        angle = angle_of_vectors(longest_vector, np.array([0, -1]))

        angle = (angle - 90) / 90

        print(f"Angle: {angle}")

        return angle