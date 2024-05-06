import numpy as np
from helper import angle_of_vectors
from structs_and_configs import FRONT_DIRECTION
import math
from structs_and_configs import State


class LateralControl:

    def __init__(self) -> None:
        self.step = 0

    def control(self, longest_vector, state: State) -> float:

        if self.step<10: 
            self.step += 1 
            return 0

        if longest_vector[0] == 0 and longest_vector[1] == 0:
            return 0 # drive forwards
        
        # todo check bounds 
        #  -> dont let the car drive completely at the right/left the whole time
        # if state.left.dist < 2:
        #     print("too much left")
        #     return 0.2
        # if state.right.dist <2:
        #     print("too much right")
        #     return -0.2
        
        print(f"longest vector: {longest_vector}")
        
        angle = angle_of_vectors(longest_vector, np.array([0, -1]))

        angle = (angle - 90) / 90

        print(f"Angle: {angle}")

        return angle