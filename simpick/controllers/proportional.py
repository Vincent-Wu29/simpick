import numpy as np
def position_action(
        current_pos: np.ndarray,
        target_pos: np.ndarray,
        gripper_command: float,
        kp: float = 10.0,
):
    error = target_pos - current_pos
    action_xyz = np.clip(error * kp, -1.0, 1.0)

    action = np.concatenate([
        action_xyz,
        np.array([gripper_command])
    ])

    return action