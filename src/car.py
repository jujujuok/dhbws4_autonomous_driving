from __future__ import annotations

import numpy as np

from lane_detection import LaneDetection
from lateral_control import LateralControl
from longitudinal_control import LongitudinalControl
from path_planning import PathPlanning

class Car:

    def __init__(self):
        self._lane_detection = LaneDetection()
        self._path_planning = PathPlanning()
        self._lateral_control = LateralControl()
        self._longitudinal_control = LongitudinalControl()

    def next_action(self, observation: np.ndarray, info: dict[str, any]) -> list:
        """Defines the next action to take based on the current observation, reward, and other information.

        Args:
            observation (np.ndarray): The current observation of the environment.
            info (dict[str, Any]): Additional information about the environment.

        Returns:
            List: The action to take:
                0: steering, -1 is full left, +1 is full right
                1: gas, 0 is no gas, 1 is full gas
                2: breaking, 0 is no break, 1 is full break
        """

        lanes = self._lane_detection.detect(observation)
        front, longest_vector = self._path_planning.plan(lanes)
         
        acceleration, braking = self._longitudinal_control.control(front, longest_vector, info['speed'])
        steering_angle = self._lateral_control.control(front, longest_vector, info['speed'])

        action = [steering_angle, acceleration, braking]

        return action
