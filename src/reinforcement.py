import numpy as np


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

    def choose_action(self, state) -> np.ndarray:
        if np.random.rand() < self.exploration_rate:
            return np.random.randint(self.action_size)
        return np.argmax(self.q_table[state, :])

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state, :])
        td_target = (
            reward + self.discount_factor * self.q_table[next_state, best_next_action]
        )
        td_error = td_target - self.q_table[state, action]
        self.q_table[state, action] += self.learning_rate * td_error

        self.exploration_rate = max(
            self.exploration_min, self.exploration_rate * self.exploration_decay
        )

if __name__ == "__main__":

    # Define state and action spaces
    state_size = 6  # Number of features (current speed and distances to lanes)
    action_size = 3  # Number of actions (steering, gas, braking)

    # Initialize Q-learning agent
    agent = QLearningAgent(state_size, action_size)

# Training loop
num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()  # Reset the environment to start a new episode
    done = False
    total_reward = 0

    while not done:
        # Choose action
        action = agent.choose_action(state)

        # Take action and observe next state and reward
        next_state, reward, done = env.step(action)

        # Update Q-table
        agent.update_q_table(state, action, reward, next_state)

        state = next_state
        total_reward += reward

    print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}")

# After training, you can use the Q-learning agent to drive the car in the environment
# by choosing actions based on the learned Q-values
