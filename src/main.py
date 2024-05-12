from __future__ import annotations

import argparse

import gymnasium as gym

import numpy as np
from car import Car
from env_wrapper import CarRacingEnvWrapper

import multiprocessing as multi


def evaluate(env, seed, eval_length=600):
    state_image, info = env.reset(seed=seed)

    car = Car()

    reward = 0
    for t in range(eval_length):
        action = car.next_action(state_image, info)

        state_image, r, done, trunc, info = env.step(action)
        reward += r

        if done or trunc:
            print(f'seed: {seed}, reward: {reward}');
            return reward


def start(args):
    cli, seed = args

    render_mode = 'rgb_array' if cli.no_display else 'human'
    env = CarRacingEnvWrapper(
        gym.make(
            "CarRacing-v2", 
            render_mode=render_mode, 
            domain_randomize=cli.domain_randomize
        )
    )

    reward = evaluate(env, seed, eval_length=1000)

    env.reset()
    return reward

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_display", action="store_true", default=False)
    parser.add_argument("--domain_randomize", action="store_true", default=False)
    args = parser.parse_args()

    episodes = 50
    parameters = []

    for i in range(episodes):
        seed = int(np.random.randint(0, int(1e6)))
        parameters.append((args, seed))

    parallel = multi.cpu_count() - 1    # one less to keep the system responsive
    rewards = []

    with multi.Pool(parallel) as p:
        rewards += p.map(start, parameters)

    print(rewards)
    rewards = np.array(rewards)

    print('---------------------------')
    print(' avg score: %f' % (np.mean(np.asarray(rewards))))
    print(' std diff:  %f' % (np.std(np.asarray(rewards))))
    print(' max score: %f' % (np.max(np.asarray(rewards))))
    print(' min score: %f' % (np.min(np.asarray(rewards))))
    print('---------------------------')
    print(' top 5 avg score: %f' % (np.mean(np.sort(np.asarray(rewards))[-5:])))
    print(' low 5 avg score: %f' % (np.mean(np.sort(np.asarray(rewards))[:5])))
    print('---------------------------')

if __name__ == "__main__":
    main()
