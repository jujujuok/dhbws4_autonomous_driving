from __future__ import annotations

import argparse

import cv2
import gymnasium as gym
import numpy as np

from env_wrapper import CarRacingEnvWrapper
from input_controller import InputController
from path_planning import PathPlanning
from lane_detection import LaneDetection
from utils import test_visualize
from time import time


def run(env, input_controller: InputController):
    t = time()
    lane_detection = LaneDetection()
    path_planning = PathPlanning()

    seed = int(np.random.randint(0, int(1e6)))
    state_image, info = env.reset(seed=seed)
    total_reward = 0.0

    if t>3: print("start")
    while not input_controller.quit and t>3:
        image = lane_detection.detect(state_image)

        test_visualize(image)

        state, longest_vector = path_planning.plan(image)

        print(f"distance front: {state.front.dist}, longest_vector: {longest_vector}")

        # visualize

        # Step the environment
        input_controller.update()
        a = [
            input_controller.steer,
            input_controller.accelerate,
            input_controller.brake,
        ]
        state_image, r, done, trunc, info = env.step(a)
        total_reward += r

        # Reset environment if the run is skipped
        input_controller.update()
        if done or input_controller.skip:
            print(f"seed: {seed:06d}     reward: {total_reward:06.2F}")

            input_controller.skip = False
            seed = int(np.random.randint(0, int(1e6)))
            state_image, info = env.reset(seed=seed)
            total_reward = 0.0


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
