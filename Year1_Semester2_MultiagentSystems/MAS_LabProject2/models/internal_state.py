from dataclasses import dataclass, field
from typing import List, Optional
from .coordinates import Coordinate


@dataclass
class InternalState:
    position: Coordinate
    battery: int
    storage_capacity: int = 0
    current_storage: int = 0
    trajectory: List[Coordinate] = field(default_factory=list)
    current_target: Optional[Coordinate] = None
    
    def record_move(self, pos: Coordinate):
        self.trajectory.append(self.position)
        self.position = pos
