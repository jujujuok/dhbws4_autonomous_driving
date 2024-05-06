from __future__ import annotations

import argparse

import gymnasium as gym
import cv2
import numpy as np

from env_wrapper import CarRacingEnvWrapper
from input_controller import InputController
from lane_detection import LaneDetection
from path_planning import PathPlanning
from reinforcement import QLearningAgent
from structs_and_configs import RLConfig, CarConst


def visualize(image, state_image):
    cv_image = np.asarray(image, dtype=np.uint8)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
    cv_image = cv2.resize(cv_image, np.asarray(state_image.shape[:2]) * 6)
    cv2.imshow("Car Racing - Lane Detection", cv_image)
    cv2.waitKey(1)


def run(env: CarRacingEnvWrapper, total_reward):

    DONE = False

    lane_detection = LaneDetection()
    path_planning = PathPlanning()

    agent = QLearningAgent(RLConfig.state_size, RLConfig.action_size)

    state_image, info = env.reset(seed=int(np.random.randint(0, int(1e6))))

    while not DONE:
        
        # returns an image with 0s for the path and 1s where its offroad --> penalty
        image = lane_detection.reinforcement_lane_detection(state_image)
    
        visualize(image * 255, state_image)

        # calculates the distances around the car, to offroad
        state = path_planning.reinforcement_path_planning(image)

        state.speed = info["speed"]
        
        DONE = (  # todo if car offroad -> DONE = 1
            image[CarConst.start_h][CarConst.start_w] == 1
            and image[CarConst.end_h][CarConst.start_w] == 1
            and image[CarConst.start_h][CarConst.end_w] == 1
            and image[CarConst.end_h][CarConst.end_w] == 1
        )
        if DONE: print("DONE, Offroad!! ")

        a = agent.choose_action(state)
        action = [a.steering, a.acceleration, 0] if a.acceleration > 0 else [a.steering, 0, -a.acceleration]

        state_image, reward, _, _, info = env.step(action)

        # calculate the agents reward based on speed and score
        # r = reward -*+/ time

        agent.update_q_table(state=state, action=action, reward=reward)# ,next_state???)

        total_reward += reward




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_display", action="store_true", default=False)
    args = parser.parse_args()

    render_mode = "rgb_array" if args.no_display else "human"
    env = CarRacingEnvWrapper(
        gym.make("CarRacing-v2", render_mode=render_mode, domain_randomize=False)
    )
    env.reset()

    for episode in range(RLConfig.num_episodes):
        reward = 0
        run(env, reward)
        env.reset()

    print(
        f"Episode {episode + 1}/{RLConfig.num_episodes}, Total Reward: {total_reward}"
    )


if __name__ == "__main__":
    main()
