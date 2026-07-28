from enum import Enum, auto

class PickState(Enum):
    APPROACH_ABOVE = auto()
    DESCEND_TO_GRASP = auto()
    CLOSE_GRIPPER = auto()
    LIFT_OBJECT = auto()
    MOVE_ABOVE_GOAL = auto()
    DESCEND_TO_GOAL = auto()
    RELEASE_OBJECT = auto()
    SUCCEDD = auto()
    FAILURE = auto()

class PickPlaceFSM:
    def __init__(self, config) -> None:
        self.config = config
        self.state = PickState.APPROACH_ABOVE
        self.state_steps = 0
        self.retries = 0
        self.failure_reason = None

    def reset(self):
        self.state = PickState.APPROACH_ABOVE
        self.state_steps = 0
        self.retries = 0
        