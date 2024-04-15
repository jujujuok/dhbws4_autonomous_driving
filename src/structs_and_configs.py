from dataclasses import dataclass
import numpy as np


@dataclass
class ConfigLaneDetection:
    carmask: np.ndarray 
    window_w: int
    window_h: int
    displaycrop: int = 105
    evaluate: bool = False
    debug: bool = False

    
@dataclass
class CarConst:
    pos_w: int = 48
    pos_h: int = 85
    start_h: int = 700
    end_h: int = 802
    start_w: int = 592
    end_w: int = 660
    
    
@dataclass
class Distances:
    front: int
    right: int
    left: int
    front_left: int
    front_right: int


@dataclass
class CarVectors:
    front: float
    longest_vector: list[int, int] # h & w
