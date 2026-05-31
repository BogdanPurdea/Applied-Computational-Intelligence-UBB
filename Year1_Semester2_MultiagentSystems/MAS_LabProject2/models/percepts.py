from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Percept:
    """
        What the agent can see at its current location
    """
    current_position_density: int
    is_obstacle: bool
    turbidity: int
    adjacent_cells: Dict[str, Any]  # e.g., {'N': {'is_obstacle': False, 'density': 2}, ...}
