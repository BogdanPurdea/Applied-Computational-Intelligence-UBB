import random
from .base_agent import Agent
from models.actions import Action, ActionType
from models.coordinates import Coordinate


class DetectorAgent(Agent):
    """
    Reactive Agent (Architecture):
    Reactive/reflex agent that explores the grid, detects high-density waste zones
    and writes their coordinates to a shared Blackboard.
    """

    def __init__(self, agent_id: str, initial_state, config):
        """
        Initializes the detector agent with its runtime state, configuration, and
        exploration metadata required for randomized grid traversal and blackboard
        reporting.
        """
        super().__init__(agent_id, initial_state, config)
        # Random walk for exploration
        self.explore_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.last_blackboard = None  # Reference kept to write to it during next()

    def set_blackboard(self, blackboard):
        """
        Stores a reference to the shared blackboard so detected waste zones can be
        reported during the agent's decision phase.
        """
        self.last_blackboard = blackboard

    def next(self):
        """
        Performs the agent's reflex decision phase.

        If the current percept indicates that the agent is located on a cell whose
        waste density meets or exceeds the configured detection threshold, the
        cell position is written to the shared blackboard for collector agents to
        process.
        """
        # Reflex behavior: if current cell has high density, write to blackboard
        if self.current_percept and self.current_percept.current_position_density >= self.config.waste_detection_threshold:
            if self.last_blackboard:
                self.last_blackboard.write_zone(self.state.position)

    def action(self) -> Action:
        """
        Selects the next movement action using a reactive random-walk strategy.

        The agent evaluates adjacent cells from its current percept, filters out
        obstacles, converts valid cardinal directions into target coordinates, and
        randomly chooses one reachable neighboring cell. If no valid movement is
        available, the agent remains idle.

        Returns:
            Action: A MOVE action targeting a valid adjacent cell, or an IDLE
            action when movement is not possible.
        """
        # Reflex behavior: pick a random adjacent cell that is not an obstacle
        valid_moves = []
        if self.current_percept:
            for d_name, info in self.current_percept.adjacent_cells.items():
                if not info['is_obstacle']:
                    # Map N, S, E, W to coordinates
                    dx, dy = 0, 0
                    if d_name == 'N':
                        dy = -1
                    elif d_name == 'S':
                        dy = 1
                    elif d_name == 'E':
                        dx = 1
                    elif d_name == 'W':
                        dx = -1

                    target_pos = Coordinate(self.state.position.x + dx, self.state.position.y + dy)
                    valid_moves.append(target_pos)

        if valid_moves:
            return Action(type=ActionType.MOVE, target=random.choice(valid_moves))
        return Action(type=ActionType.IDLE)
