import numpy as np
from helper import angle_of_vectors
from structs_and_configs import FRONT_DIRECTION
import math


class LateralControl:

    def control(self, longest_vector: np.ndarray) -> float:

        if longest_vector[0] == 0 and longest_vector[1] == 0:
            return 0 # drive forwards
        
        # todo check bounds 
        #  -> dont let the car drive completely at the right/left the whole time
        
        print(f"longest vector: {longest_vector}")
        
        angle = angle_of_vectors(longest_vector, np.array([-1, 0]))

        angle = (angle - 90) / 90

        print(f"Angle: {angle}")

        return angle