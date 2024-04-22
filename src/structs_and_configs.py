from dataclasses import dataclass
import numpy as np


@dataclass
class ImageConfig:
    displaycrop: int = 14
    width: int = 96
    height: int = 96
    height_cropped = height - displaycrop


@dataclass
class ConfigLaneDetection:
    evaluate: bool = False
    debug: bool = True


@dataclass
class CarConst:
    pos_w: int = 48
    pos_h: int = 80
    start_h: int = 65
    end_h: int = 78
    start_w: int = 44
    end_w: int = 51
