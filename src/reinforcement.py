import numpy as np
from structs_and_configs import RLAction, State, state_to_index, rlaction_to_index


class QLearningAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate: float = 0.1
        self.discount_factor: float = 0.99
        self.exploration_rate: float = 1.0
        self.exploration_decay: float = 0.99
        self.exploration_min: float = 0.01
        self.q_table = np.zeros((state_size, action_size))

    def choose_action(self, state: State) -> RLAction:
        """
        gets the state and chooses how to steer 

        Args:
            state (State): (3 distances around the car to the lanes around 
                            it, front, right, left and the current speed)

        Returns:
            RLAction: 
                - steering: [-1:1] (right <-> left)
                - acceleration: [-1:1] -> gas:[0,1]; breaking: [-1,0]
        """
        if np.random.rand() < self.exploration_rate:  # Exploration: choose a random action
            a = RLAction
            a.steering = np.random.uniform(-1, 1)
            a.acceleration = np.random.uniform(0, 1)
            return a
        else:
            # Exploitation: choose the action with the highest Q-value
            state_index = state_to_index(state)
            action_index = np.argmax(self.q_table[state_index])
            steering = (action_index % self.action_size) / (self.action_size - 1) * 2 - 1
            acceleration = (action_index // self.action_size) / (self.action_size - 1)
            return RLAction(steering, acceleration)

    def update_q_table(self, state: State, action: RLAction, reward):
        """
        Updates the Q-table based on the observed transition.

        Args:
            state (State): The current state.
            action (RLAction): The chosen action.
            reward (float): The observed reward.
        """
        state_index = state_to_index(state)
        action_index = rlaction_to_index(action)
        
        # Q-learning update rule
        self.q_table[state_index, action_index] += self.learning_rate * (
            reward + self.discount_factor * np.max(self.q_table[state_index]) - self.q_table[state_index, action_index]
        )

        # Decay exploration rate
        self.exploration_rate = max(self.exploration_min, self.exploration_rate * self.exploration_decay)

    # After training, you can use the Q-learning agent to drive the car in the environment
    # by choosing actions based on the learned Q-values

    # todo, front_left and front_right)
