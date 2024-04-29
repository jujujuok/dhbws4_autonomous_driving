from __future__ import annotations
import numpy as np
from structs_and_configs import CarConst, ImageConfig, DistDir, State
from helper import show_plt_img_grey, vector_length


class PathPlanning:

    def sensor_application(self, image: np.ndarray) -> State:
        state = State()

        # front
        state.front = DistDir(-1, 0)
        state.right = DistDir(0, 1)
        state.left = DistDir(0, -1)
        state.front_left = DistDir(-1, -1)
        state.front_right = DistDir(-1, 1)

        dh = CarConst.pos_h
        while (
            dh < ImageConfig.height_cropped
            and dh > 0
            # find a 1 (= Lane)
            and image[dh][CarConst.pos_w] != 1
        ):
            dh = dh + state.front.h
            state.front.dist = state.front.dist + 1

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
                element.dist = element.dist + 1

                # mark the looked up ways for distances grey
                # image[dh][dw] = 0.5
            print(f"vector, {element.get_vector()}, length: {element.get_length()}")

        return state

    def plan(self, image: np.ndarray) -> list[float, np.ndarray]:
        state = self.sensor_application(image)

        lv = state.front

        for element in state.state_list():
            if element.dist > lv.dist:
                lv = element

        return state.front.dist, lv.get_vector()

    def reinforcement_path_planning(self, image: np.ndarray) -> State:

        return self.sensor_application(image)
