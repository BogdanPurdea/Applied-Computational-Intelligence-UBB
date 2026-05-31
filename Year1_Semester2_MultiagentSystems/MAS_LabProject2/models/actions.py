from enum import Enum, auto
from dataclasses import dataclass
from .coordinates import Coordinate

class ActionType(Enum):
    MOVE = auto()
    COLLECT = auto()
    DROP = auto()
    IDLE = auto()

@dataclass(frozen=True)
class Action:
    type: ActionType
    target: Coordinate = None  # Relevant for MOVE
