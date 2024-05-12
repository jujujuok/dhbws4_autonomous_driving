from __future__ import annotations

import argparse
import cv2

import gymnasium as gym
import numpy as np
from matplotlib import pyplot as plt

from env_wrapper import CarRacingEnvWrapper
from input_controller import InputController
from longitudinal_control import LongitudinalControl
from lateral_control import LateralControl
from path_planning import PathPlanning
from lane_detection import LaneDetection
from time import time

fig = plt.figure()
plt.ion()
plt.show()


def run(env, input_controller: InputController):
    # Initialisierung
    lateral_control = LateralControl()
    path_planning = PathPlanning()
    lane_detection = LaneDetection()
    longitudinal_control = LongitudinalControl()

    seed = int(np.random.randint(0, int(1e6)))
    # Zurücksetzen der Umgebung auf den Anfangszustand
    state_image, info = env.reset(seed=seed)
    total_reward = 0.0

    # -------------------------------------
    # Initialisierung einer Liste zur Speicherung der Geschwindigkeitshistorie
    speed_history = []
    # Initialisierung einer Liste zur Speicherung der Zielgeschwindigkeitshistorie
    target_speed_history = []
    # ------------------------------------

    while not input_controller.quit:
        target_speed = 20

        image = lane_detection.detect(state_image)
        state, longest_vector = path_planning.plan(image)
        angle = lateral_control.control(longest_vector, state)
        front = state.front.get_vector()

        print("longest_vector", longest_vector, "angle", angle, "front", front)

        cv_image = image * 255
        cv_image = np.asarray(cv_image, dtype=np.uint8)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

        angle_between = np.arccos(
            np.dot(longest_vector, front)
            / (np.linalg.norm(longest_vector) * np.linalg.norm(front))
        )
        magnitude_of_front = np.linalg.norm(front)

        target_speed = (
            longitudinal_control.predict_target_speed(angle_between, magnitude_of_front)
            * 0.8
        )

        angle = lateral_control.control(longest_vector, state)

        acceleration, braking = longitudinal_control.control(
            info["speed"], target_speed, input_controller.steer
        )

        speed_history.append(info["speed"])
        target_speed_history.append(target_speed)

        plt.gcf().clear()
        plt.plot(speed_history, c="green")
        plt.plot(target_speed_history)
        try:
            fig.canvas.flush_events()
        except:
            pass

        input_controller.update()
        a = [angle, acceleration, braking]
        state_image, r, done, trunc, info = env.step(a)
        total_reward += r

        input_controller.update()
        if done or input_controller.skip:
            print(f"seed: {seed:06d}     reward: {total_reward:06.2F}")

            input_controller.skip = False
            seed = int(np.random.randint(0, int(1e6)))
            state_image, info = env.reset(seed=seed)
            total_reward = 0.0

            speed_history = []
            target_speed_history = []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_display", action="store_true", default=False)
    args = parser.parse_args()

    render_mode = "rgb_array" if args.no_display else "human"
    env = CarRacingEnvWrapper(
        gym.make("CarRacing-v2", render_mode=render_mode, domain_randomize=False)
    )
    input_controller = InputController()

    run(env, input_controller)
    env.reset()


if __name__ == "__main__":
    main()
