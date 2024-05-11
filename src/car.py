# car.py
from __future__ import annotations

import numpy as np
from lane_detection import LaneDetection
from lateral_control import LateralControl
from longitudinal_control import LongitudinalControl
from path_planning import PathPlanning

class Car:
    def __init__(self):
        # Initzialisierung aller notwendigen Objekte
        self._lane_detection = LaneDetection()
        self._path_planning = PathPlanning()
        self._lateral_control = LateralControl()
        self._longitudinal_control = LongitudinalControl()

    def next_action(self, observation: np.ndarray, info: dict[str, any]) -> list:
        """
        Defines the next action to take based on the current observation, reward, and other information.

        Args:
            observation (np.ndarray): The current observation of the environment.
            info (dict[str, Any]): Additional information about the environment.

        Returns:
            List: The action to take:
                0: steering, -1 is full left, +1 is full right
                1: gas, 0 is no gas, 1 is full gas
                2: breaking, 0 is no break, 1 is full break
        """

        # Detect lanes
        lanes = self._lane_detection.detect(observation)

        # Plan the path
        state, longest_vector = self._path_planning.plan(lanes)

        # Calculate steering angel
        steering_angle = self._lateral_control.control(longest_vector, state)

        # Determine the target speed
        front = state.front.get_vector()
        angle_between = np.arccos(np.dot(longest_vector, front) / (np.linalg.norm(longest_vector) * np.linalg.norm(front)))
        magnitude_of_front = np.linalg.norm(front)
        target_speed = self._longitudinal_control.predict_target_speed(angle_between, magnitude_of_front)

        # Calculate acceleration and braking
        acceleration, braking = self._longitudinal_control.control(info['speed'], target_speed, steering_angle)

        return [steering_angle, acceleration, braking]
