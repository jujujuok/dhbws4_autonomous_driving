from dataclasses import dataclass
import numpy as np


@dataclass
class ConfigLaneDetection:
    displaycrop: int = 100
    carmask: np.ndarray
    evaluate: bool = False
    debug: bool = False
    
@dataclass
class Distances:
    front: int
    right: int
    left: int
    front_left: int
    front_right: int
