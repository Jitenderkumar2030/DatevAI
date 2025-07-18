import pandas as pd
from stable_baselines3 import A2C
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np

class SimpleFinanceEnv(Env):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.action_space = Discrete(3)  # 0: hold, 1: spend, 2: save
        self.observation_space = Box(low=0, high=1, shape=(len(df.columns),), dtype=np.float32)
        self.current_step = 0

    def reset(self):
        self.current_step = 0
        return self._next_observation()

    def _next_observation(self):
        obs = self.df.iloc[self.current_step].values
        return obs / np.max(obs)

    def step(self, action):
        reward = np.random.rand()  # Mock reward; later: use real metrics
        self.current_step += 1
        done = self.current_step >= len(self.df) - 1
        return self._next_observation(), reward, done, {}

def train_agent(df):
    env = SimpleFinanceEnv(df)
    model = A2C("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=1000)
    return model

def get_finrl_recommendation(model, df):
    obs = df.iloc[-1].values / np.max(df.values)
    action, _ = model.predict(obs)
    return ["Hold", "Spend", "Save"][action]
