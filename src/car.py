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

        # Führen Sie die Fahrspurerkennung durch
        lanes = self._lane_detection.detect(observation)

        # Führen Sie die Pfadplanung durch, um die Richtung und die längste erkannte Linie zu erhalten
        front, longest_vector = self._path_planning.plan(lanes)


        # Rufen Sie die longitudinale Steuerung auf, um Beschleunigung und Bremsen zu bestimmen
        acceleration, braking = self._longitudinal_control(front, longest_vector)

        # Rufen Sie die laterale Steuerung auf, um den Lenkwinkel zu bestimmen
        steering_angle = self._lateral_control(front, longest_vector)


        # Erstellen Sie eine Liste mit den Aktionen (Lenkung, Beschleunigung und Bremsen)
        action = [steering_angle, acceleration, braking]

        return action
