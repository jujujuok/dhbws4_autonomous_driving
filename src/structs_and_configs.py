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

    state_size: int = 6  # Number of features (current speed and distances to lanes)
    action_size: int = 3  # Number of actions (steering, gas, braking)

    num_episodes: int = 1000
    reward: int = 1


@dataclass
class CarConst:
    pos_w: int = 48
    pos_h: int = 80
    start_h: int = 65
    end_h: int = 78
    start_w: int = 44
    end_w: int = 51
