from dataclasses import dataclass
import numpy as np

@dataclass
class FetchState():
    ee_pos: np.ndarray
    object_ops: np.ndarray
    goal_pos: np.ndarray
    object_relative_pos: np.ndarray
    gripper_state: np.ndarray

def parse_fetch_pick_and_place_observation(obs: dict) -> FetchState:
    raw = obs["observation"]

    if raw.shape[0] < 11:
        raise ValueError(
            f"Unexpected observation shape: {raw.shape}"
        )

    return FetchState(
        ee_pos=raw[0:3].copy(),
        object_ops=raw[3:6].copy(),
        object_relative_pos=raw[6:9].copy(),
        gripper_state=raw[9:11].copy(),
        goal_pos=obs["desired_goal"].copy()
    )



def grasp_error(state: FetchState):
    return np.linalg.norm(
        state.ee_pos - state.object_ops
    )

def place_error(state: FetchState):
    return np.linalg.norm(
        state.object_ops - state.goal_pos
    )