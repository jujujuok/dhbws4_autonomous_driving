from __future__ import annotations
import numpy as np
from structs_and_configs import CarConst, ImageConfig
from helper import show_plt_img_grey, vector_length


class DistDir:
    def __init__(self, label: str, h: int, w: int):
        self.label = label
        self.dist: float = 0
        self.h = h
        self.w = w

    def get_vector(self) -> np.ndarray:
        return np.array([self.w, self.h]) * self.dist

    def get_length(self) -> float:
        return np.linalg.norm(self.get_vector())


class PathPlanning:

    def __init__(self):
        self.front = DistDir("front", -1, 0)
        self.dist_dir = [
            DistDir("right", 0, 1),
            DistDir("left", 0, -1),
        ]

    def sensor_application(self, image: np.ndarray):
        # front
        dh = CarConst.pos_h
        self.front.dist = 1
        while (
            dh < ImageConfig.height_cropped
            and dh > 0
            # find a 1 (= Lane)
            and image[dh][CarConst.pos_w] != 1
        ):
            dh = dh + self.front.h
            self.front.dist = self.front.dist + 1

        # sides etc
        for element in self.dist_dir:
            dw = CarConst.pos_w
            dh = CarConst.pos_h
            element.dist = 1

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

        # i = image * 255
        # show_plt_img_grey(i)

        #lv = self.front

        # get longest vector
        #for element in self.dist_dir:
        #    if element.dist > lv.dist:
        #        lv = element

        # interpolate direction by adding all three vectors
        #interpolated_dir = self.front.get_vector()
        #for element in self.dist_dir:
        #    np.add(interpolated_dir, element.get_vector())

        interpolated_dir = self.front.get_vector()
        longest_vector = None
        longest_distance = 0
        for element in self.dist_dir:
            if element.dist > longest_distance:
                longest_distance = element.dist
                longest_vector = element

        print("distances", [self.front.dist, self.dist_dir[0].dist, self.dist_dir[1].dist])
        print("intpltd", interpolated_dir)
        print("longest", longest_vector)
        #return self.front.dist, lv.get_vector()
        print("add",interpolated_dir)
        print("rechts",self.dist_dir)
        return self.front.dist, interpolated_dir, self.dist_dir[0],

