from __future__ import annotations

import argparse
import cv2

import gymnasium as gym
import numpy as np
import neat

from env_wrapper import CarRacingEnvWrapper
from input_controller import InputController
from path_planning import PathPlanning
from lane_detection_helper import detect_green_pixels

# https://neat-python.readthedocs.io/en/latest/neat_overview.html


@staticmethod
def visualize(image: np.ndarray):
    cv_image = image * 255
    cv_image = np.asarray(cv_image, dtype=np.uint8)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

    cv_image = cv2.resize(cv_image, (cv_image.shape[1] * 6, cv_image.shape[0] * 6))
    cv2.imshow("Car Racing - Lateral Control", cv_image)
    cv2.waitKey(1)


@staticmethod
def load_config():
    # Load Config
    config_path = "rl_config.txt"
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    return config


class RLCar:
    """
    every car runs in its own environment with the same seed as long as it is alive
    """

    def __init__(self):
        self.alive = True
        self.env = CarRacingEnvWrapper(
            gym.make(
                "CarRacing-v2", render_mode=self.render_mode, domain_randomize=False
            )
        )
        self.visualize = True

    def drive(self, seed=42):
        path_planning = PathPlanning()

        # seed = int(np.random.randint(0, int(1e6))) # todo with random seeds to test ?

        # Zurücksetzen der Umgebung auf den Anfangszustand
        state_image, info = self.env.reset(seed=seed)
        total_reward = 0.0

        while not self.input_controller.quit:
            image = detect_green_pixels(state_image)
            if self.visualize:
                visualize(image)

            state, longest_vector = path_planning.plan(image)

            a = [0, 0, 0]
            state_image, r, done, trunc, info = self.env.step(a)
            total_reward += r

            # if round is finished or skipped
            if done or self.input_controller.skip:
                print(f"seed: {seed:06d}     reward: {total_reward:06.2F}")

                self.input_controller.skip = False
                seed = int(np.random.randint(0, int(1e6)))
                state_image, info = self.env.reset(seed=seed)
                total_reward = 0.0


class RL:
    """
    class for Reinforcement Learning with NEAT algorithm

    car is alive as long as its on path
    """

    def __init__(self, render_mode):
        self.batch_size = 10

        self.cars: list[RLCar] = []
        self.input_controller = InputController()
        self.nets = []
        self.genomes = []

        self.current_generation = 0

        self.running_time = 60  # in seconds

    def run(self):
        """
        creates multiple cars at the same seed
        """
        config = 0  # todo

        for i, g in self.genomes:
            self.nets.append(neat.nn.FeedForwardNetwork.create(g, config))
            g.fitness = 0

            self.cars.append(RLCar())

        self.current_generation += 1

        for i, car in enumerate(self.cars):
            car.drive(self.nets[i].activate(car.get_data()))


if __name__ == "__main__":
    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_display", action="store_true", default=False)
    args = parser.parse_args()

    render_mode = "rgb_array" if args.no_display else "human"

    # neat setup
    config = load_config()
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    rl = RL(render_mode)

    population.run(rl.run(), 100)  # Run Simulation For A Maximum of 100 Generations
