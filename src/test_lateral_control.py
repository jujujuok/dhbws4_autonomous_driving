from __future__ import annotations

import argparse

import cv2
import gymnasium as gym
import numpy as np

from lateral_control import LateralControl
from lane_detection import LaneDetection
from path_planning import PathPlanning
from env_wrapper import CarRacingEnvWrapper
from input_controller import InputController
from structs_and_configs import CarConst


def run(env, input_controller: InputController, lateral_control: LateralControl):
    lateral_control_instance = LateralControl()
    path_planning = PathPlanning()
    lane_detection = LaneDetection()
    seed = int(np.random.randint(0, int(1e6)))
    state_image, info = env.reset(seed=seed)
    total_reward = 0.0

    while not input_controller.quit:

        image = lane_detection.detect(state_image)
        front, longest_vector, longest_vector_true = path_planning.plan(image)

        if front is not None and longest_vector_true is not None and info['speed'] is not None:
            action = lateral_control.control(front, longest_vector, info['speed'])
        else:
            print("Fehlende Informationen in 'info'.")
            continue

        cv_image = np.asarray(state_image, dtype=np.uint8)

        for point in info['trajectory'][-20:]:
            if 0 < point[0] < 96 and 0 < point[1] < 84:
                cv_image[int(point[1]), int(point[0])] = [255, 255, 255]

                #print("point",point)



        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        print("long", longest_vector_true)
        cv_image = cv2.line(cv_image, [48, 64], [48, 64]+longest_vector, [255, 0, 0], 1)
        #cv_image = cv2.line(cv_image, [48, 64], [48, 64] +left, [255, 0, 0], 1)
        #cv_image = cv2.line(cv_image, [48, 64], [48, 64] +right, [255, 0, 0], 1)
        cv_image = cv2.resize(cv_image, (cv_image.shape[1] * 6, cv_image.shape[0] * 6))

        cv2.imshow('Car Racing - Lateral Control', cv_image)
        cv2.waitKey(1)

        input_controller.update()
        state_image, r, done, trunc, info = env.step(action)
        total_reward += r

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

    render_mode = 'rgb_array' if args.no_display else 'human'
    env = CarRacingEnvWrapper(gym.make("CarRacing-v2", render_mode=render_mode, domain_randomize=False))
    input_controller = InputController()




    lateral_control = LateralControl()
    run(env, input_controller, lateral_control)

    env.reset()

if __name__ == '__main__':
    main()