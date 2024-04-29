from __future__ import annotations

import argparse

import cv2
import gymnasium as gym
import numpy as np

from env_wrapper import CarRacingEnvWrapper
from input_controller import InputController
from lateral_control import LateralControl
from path_planning import PathPlanning
from lane_detection import LaneDetection
from structs_and_configs import CarConst
from time import time


def run(env, input_controller: InputController):
    t = time()
    lateral_control = LateralControl()
    path_planning = PathPlanning()
    lane_detection = LaneDetection()

    seed = int(np.random.randint(0, int(1e6)))
    state_image, info = env.reset(seed=seed)
    total_reward = 0.0

    while not input_controller.quit:
        if t < 3:
            continue

        image = lane_detection.detect(state_image)

        state, longest_vector = path_planning.plan(image)

        angle = lateral_control.control(longest_vector, state)
        
        # ----------- visualization -----------

        cv_image = image * 255

        cv_image = np.asarray(cv_image, dtype=np.uint8)

        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

        # for vec in [state.front]:
        #     pos = (CarConst.pos_h, CarConst.pos_w)
        #     end_w = CarConst.pos_w + vec.w
        #     end_h = CarConst.pos_h + vec.h
        #     cv_image = cv2.line(cv_image, pos, (end_h, end_w), [255, 0, 0], 1)

        cv_image = cv2.resize(cv_image, (cv_image.shape[1] * 6, cv_image.shape[0] * 6))

        cv2.imshow("Car Racing - Lateral Control", cv_image)
        cv2.waitKey(1)

        # ------------

        # Step the environment
        input_controller.update()
        a = [angle, input_controller.accelerate, input_controller.brake]
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
