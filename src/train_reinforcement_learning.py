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
from structs_and_configs import RLConfig

DONE = False

def visualize(image, state_image):
    cv_image = np.asarray(image, dtype=np.uint8)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
    cv_image = cv2.resize(cv_image, np.asarray(state_image.shape[:2]) * 6)
    cv2.imshow('Car Racing - Lane Detection', cv_image)
    cv2.waitKey(1)


def run(env: CarRacingEnvWrapper):
    lane_detection = LaneDetection()
    path_planning = PathPlanning()

    agent = QLearningAgent(RLConfig.state_size, RLConfig.action_size)

    seed = int(np.random.randint(0, int(1e6)))
    state_image, info = env.reset(seed=seed)
    total_reward = 0.0

    while not DONE:
        image = lane_detection.reinforcement_lane_detection(state_image)
        
        visualize(image*255, state_image)

        state = path_planning.reinforcement_path_planning(image)

        state.speed = info['speed'] 
        

        # Step the environment
                # input_controller.update()
                # a = [input_controller.steer, input_controller.accelerate, input_controller.brake]
                # state_image, r, done, trunc, info = env.step(a)

        
        # state: RLState

        #a = [input_controller.steer, input_controller.accelerate, input_controller.brake]
        
        
        action = agent.choose_action(state)

        state_image, reward, done, trunc, info = env.step(action)

        total_reward += reward

        action = agent.choose_action(state=state)

        # agent.update_q_table(state, action, reward, next_state)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_display", action="store_true", default=False)
    args = parser.parse_args()

    render_mode = 'rgb_array' if args.no_display else 'human'
    env = CarRacingEnvWrapper(gym.make("CarRacing-v2", render_mode=render_mode, domain_randomize=False))
    input_controller = InputController()

    for episode in range(RLConfig.num_episodes):
        total_reward = 0
        run(env, input_controller)
        env.reset()
        
    
    print(f"Episode {episode + 1}/{RLConfig.num_episodes}, Total Reward: {total_reward}")
    


if __name__ == '__main__':
    main()
