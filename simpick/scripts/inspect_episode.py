import sys
import os

curretn_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(curretn_dir)

sys.path.insert(0, parent_dir)


from fetch_state import FetchState, parse_fetch_pick_and_place_observation, grasp_error, place_error
import gymnasium as gym
import gymnasium_robotics
import numpy as np

gym.register_envs(gymnasium_robotics)



def run_one_epoisde():
    env = gym.make("FetchPickAndPlace-v4")
    obs, _ = env.reset(seed=42)
    action = env.action_space.sample()

    done = False
    step = 0
    while not done:
        obs, reward, terminated, truncated, info = env.step(action)
        state = parse_fetch_pick_and_place_observation(obs)

        print(f"step:{step} grasp_error={grasp_error(state):.2f}m place_error={place_error(state):.2f}m")

        step += 1
        done = terminated or truncated
    env.close()
#run_one_epoisde()

def run_action(action):
    env = gym.make("FetchPickAndPlace-v4")
    obs, _ = env.reset(seed=42)
    state_old = parse_fetch_pick_and_place_observation(obs)

    obs, reward, terminated, truncated, info = env.step(action)

    state_new = parse_fetch_pick_and_place_observation(obs)
    env.close()
    print(f"末端位置变化:{state_new.ee_pos - state_old.ee_pos}")

actions = {
    "positive_x": np.array([1.0, 0.0, 0.0, 0.0]),
    "positive_y": np.array([0.0, 1.0, 0.0, 0.0]),
    "positive_z": np.array([0.0, 0.0, 1.0, 0.0]),
    "negative_x": np.array([-1.0, 0.0, 0.0, 0.0]),
}

for k, v in actions.items():
    print(k)
    run_action(v)
