from dataclasses import dataclass
import numpy as np


@dataclass
class ConfigLaneDetection:
    carmask: np.ndarray 
    displaycrop: int = 100
    evaluate: bool = False
    debug: bool = False
    
@dataclass
class Distances:
    front: int
    right: int
    left: int
    front_left: int
    front_right: int
