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
    def __init__(self, h: int, w: int):
        self.dist: float = 0
        self.h = h
        self.w = w

    def get_vector(self) -> np.ndarray:
        return np.array([self.h, self.w]) * self.dist

    def get_length(self) -> float:
        return np.linalg.norm(self.get_vector())


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




@dataclass
class State:
    speed: float
    left: DistDir
    right: DistDir
    front: DistDir
    # front_left: DistDir
    # front_right: DistDir


@dataclass
class CarConst:
    pos_w: int = 48
    pos_h: int = 80
    start_h: int = 65
    end_h: int = 78
    start_w: int = 44
    end_w: int = 51
