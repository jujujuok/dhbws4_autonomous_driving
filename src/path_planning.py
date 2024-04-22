from __future__ import annotations
import numpy as np
from structs_and_configs import CarConst, ImageConfig, DistDir, State
from helper import show_plt_img_grey, vector_length


class PathPlanning:

    def __init__(self):
        self.state = State

        self.state.front = DistDir(-1, 0)
        self.state.right = DistDir(0, 1)
        self.state.left = DistDir(0, -1)

    def get_state_list(self):
        return [self.state.front, self.state.right, self.state.left]

    def sensor_application(self, image: np.ndarray):
        # front
        dh = CarConst.pos_h
        while (
            dh < ImageConfig.height_cropped
            and dh > 0
            # find a 1 (= Lane)
            and image[dh][CarConst.pos_w] != 1
        ):
            dh = dh + self.front.h
            self.state.front.dist = self.state.front.dist + 1

        # sides etc
        for element in self.get_state_list():
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

    def plan(self, image: np.ndarray) -> list[float, np.ndarray]:
        self.sensor_application(image)

        lv = self.state.front

        for element in self.get_state_list():
            if element.dist > lv.dist:
                lv = element

        return self.state.front.dist, lv.get_vector()

    def reinforcement_path_planning(self, image:np.ndarray) -> State:
        
        self.sensor_application(image)

        return self.state
        


