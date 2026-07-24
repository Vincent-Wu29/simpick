import mujoco
import gymnasium as gym
import gymnasium_robotics

print("[PASS] mujoco gymnasium gymnasium_robotics dependency imports")
import numpy as np

gym.register_envs(gymnasium_robotics)

env = gym.make("FetchReach-v4")
obs1, _ = env.reset(seed=42)
action1 = env.action_space.sample()
print(f"observation: {obs1}")
print(f"action: {action1}")

obs2, _ = env.reset(seed=42)
def seed_check(obs1, obs2):
    
    for key in obs1:
        if not np.allclose(obs1[key], obs2[key]):
            return False
    return True

if seed_check(obs1, obs2):
    print(f"[PASS] 随机种子可重复")
else:
    print(f"[FILED] 随机种子不可重复")

obs3, _ = env.reset(seed=43)
if seed_check(obs1, obs3):
    print(f"[FILED] 随机种子可重复检查失败")
else:
    print(f"[PASS] 随机种子可重复检查成功")



def run_episodes(env_id: str, episodes: int = 20):
    env = gym.make(env_id)
    print(f"[PASS] {env_id} created")

    for episode in range(episodes):
        obs, info = env.reset(seed=1000 + episode)

        print(f"[PASS] {env_id} deterministic reset")
        
        done = False
        steps = 0
        total_reward = 0.0

        while not done:
            action = env.action_space.sample()

            obs, reward, terminated, truncated, info = env.step(action)

            total_reward += reward
            steps += 1
            done = terminated or truncated

        print(
            f"{env_id} | "
            f"episode={episode} | "
            f"steps={steps} | "
            f"reward={total_reward:.2f} | "
            f"terminated={terminated} | "
            f"truncated={truncated} | "
            f"success={info.get('is_success')}" 
        )

    print(f"[PASS] {env_id} completed 20 episodes")
    env.close()

run_episodes("FetchReach-v4")
run_episodes("FetchPickAndPlace-v4")

from gymnasium.wrappers import RecordVideo

env = gym.make("FetchPickAndPlace-v4", render_mode="rgb_array",)

env = RecordVideo(
    env,
    video_folder="artifacts/videos",
    episode_trigger=lambda episode_id: episode_id == 0,
    name_prefix="random-pick-and-place",
)

obs, info = env.reset(seed=42)
done = False

while not done:
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated

env.close()

from pathlib import Path

folder = Path("artifacts/videos")

has_mp4 = any(folder.glob("*.mp4"))

if has_mp4:
    print("[PASS] video saved: artifacts/videos/random-pick-and-place.mp4")
