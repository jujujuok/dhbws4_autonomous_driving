from __future__ import annotations
import numpy as np
from structs_and_configs import CarConst, ImageConfig, DistDir, State
from helper import show_plt_img_grey, vector_length

class PathPlanning1:

    def __init__(self):
        # Initialize directions
        self.directions = {
            'front': DistDir(-1, 0),
            'right': DistDir(0, 1),
            'left': DistDir(0, -1),
            'front_left': DistDir(-1, -1),
            'front_right': DistDir(-1, 1)
        }

    def sensor_application(self, image: np.ndarray) -> State:
        if image.shape != (ImageConfig.height_cropped, ImageConfig.width):
            raise ValueError("Incorrect image dimensions")

        state = State()

        # Set state directions
        for key, direction in self.directions.items():
            setattr(state, key, direction)

        # Process each direction
        for key, element in self.directions.items():
            dw, dh = CarConst.pos_w, CarConst.pos_h

            while self._within_bounds(dw + element.w, dh + element.h, image):
                dh += element.h
                dw += element.w
                if image[dh][dw] == 1:
                    break
                element.dist += 1

            print(f"{key} vector: {element.get_vector()}, length: {element.get_length()}")

        return state

    def _within_bounds(self, dw, dh, image):
        """Check if coordinates are within image boundaries."""
        return 0 <= dw < ImageConfig.width and 0 <= dh < ImageConfig.height_cropped

    def plan(self, image: np.ndarray) -> tuple[State, np.ndarray]:
        """
        Args:
            image (np.ndarray): lanes detected by the LaneDetection class

        Returns:
            tuple[State, np.ndarray]: the state and the longest vector detected by the sensors around the car
        """
        state = self.sensor_application(image)
        lv = max(state.state_list(), key=lambda x: x.dist)

        return state, lv.get_vector()

    def get_state(self, image) -> State:
        """Return the sensor state for a given image."""
        return self.sensor_application(image)

    def reinforcement_path_planning(self, image: np.ndarray) -> State:
        """Apply reinforcement learning for path planning."""
        return self.sensor_application(image)

