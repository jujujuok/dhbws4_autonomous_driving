from dataclasses import dataclass
import numpy as np

FRONT_DIRECTION = np.array([-1, 0])


@dataclass
class ImageConfig:
    displaycrop: int = 14
    width: int = 96
    height: int = 96
    height_cropped = height - displaycrop


@dataclass
class ConfigLaneDetection:
    evaluate: bool = False
    debug: bool = False


@dataclass
class RLConfig:  # ReinforcementLearning
    train: bool = True
    test: bool = False

    state_size: int = 4  # Number of features (current speed and distances to lanes)
    action_size: int = 2  # Number of actions (steering, gas, braking)

    num_episodes: int = 1000
    # reward: int


class DistDir:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.dist = 0  # Initial distance set to 0

    def get_vector(self):
        return (self.w * self.dist, self.h * self.dist)

    def get_length(self):
        return np.sqrt((self.w * self.dist)**2 + (self.h * self.dist)**2)

    def reset_distance(self):
        self.dist = 0  # Reset the distance to 0



@dataclass
class RLAction:
    """
    - steering, -1 is full left, +1 is full right
    - gas, 0 is no gas, 1 is full gas
    - breaking, 0 is no break, 1 is full break
    """

    steering: float = 0  # [-1:1]
    acceleration: float = 0  # [-1:1] -> gas:[0,1]; breaking: [-1,0]
    action_size: int = 2


class State:
    def __init__(self):
        self.speed: float  # todo: needed?
        self.left: DistDir
        self.right: DistDir
        self.front: DistDir
        self.front_left: DistDir
        self.front_right: DistDir

    def state_list(self) -> list[DistDir]:

        return [self.left, self.right, self.front_left, self.front_right, self.front_left_l, self.front_right_r]



@dataclass
class CarConst:
    pos_w: int = 48
    pos_h: int = 64
    start_h: int = 65
    end_h: int = 78
    start_w: int = 44
    end_w: int = 51
