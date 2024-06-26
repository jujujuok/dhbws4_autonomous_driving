from __future__ import annotations
import numpy as np
from structs_and_configs import CarConst, ImageConfig, DistDir, State

DEBUG = False


class PathPlanning:

    def sensor_application(self, image: np.ndarray) -> State:
        state = State()

        # front
        state.front = DistDir(-1, 0)
        state.right = DistDir(0, 1)
        state.left = DistDir(0, -1)
        state.front_left = DistDir(-1, -1)
        state.front_right = DistDir(-1, 1)
        state.front_right_r = DistDir(-2, 1)
        state.front_left_l = DistDir(-2, -1)

        dh = CarConst.pos_h
        while (
            dh < ImageConfig.height_cropped
            and dh > 0
            # find a 1 (= Lane)
            and image[dh][CarConst.pos_w] != 1
        ):
            dh = dh + state.front.h
            state.front.dist = state.front.dist + 1

        if DEBUG:
            print(
                f"\n\nfront: {state.front.get_vector()}, \t length: {state.front.get_length()}"
            )

        for element in state.state_list():
            dw = CarConst.pos_w
            dh = CarConst.pos_h

            while (
                # dw and dh must remain inside the boundaries of the image
                dw > 0
                and dw < ImageConfig.width
                and dh > 0
                and dh < ImageConfig.height_cropped
                # find a 1 (= Lane)
                and image[dh][dw] != 1
            ):
                dh = dh + element.h
                dw = dw + element.w
                added_length = np.linalg.norm(
                    [element.w, element.h]
                )  # ! changed distance calculation
                element.dist = element.dist + added_length

            if DEBUG:
                print(
                    f"vector: {element.get_vector()} , \t length: {element.get_length()}"
                )

        return state

    def plan(self, image: np.ndarray) -> list[State, np.ndarray]:
        """
        Args:
            image (np.ndarray): lanes detected by the LaneDetection class

        Returns:
            np.ndarray: the longest vector detected by the sensors around the car
        """
        state = self.sensor_application(image)

        lv = state.front

        for element in state.state_list():
            if element.dist > lv.dist and element.dist < CarConst.pos_h * 1.1:  # !
                lv = element

        return state, lv.get_vector()

    def get_state(self, image) -> State:
        return self.sensor_application(image)

    def reinforcement_path_planning(self, image: np.ndarray) -> State:
        return self.sensor_application(image)
