from .base_agent import Agent
from models.actions import Action, ActionType
from models.coordinates import Coordinate
from utils.pathfinding import a_star_search
from config import Config


class CollectorAgent(Agent):
    """
    Deliberative Agent (Architecture):
    Utility-based deliberative agent that maximizes waste collected while minimizing energy.
    Reads Blackboard, selects optimal zones, collects and returns to barge.
    """

    def __init__(self, agent_id: str, initial_state, config):
        """
        Initializes the collector agent with its runtime state, navigation path,
        barge reference position and external system references required for
        environment-aware decision-making and pathfinding.
        """
        super().__init__(agent_id, initial_state, config)
        self.current_path = []
        self.barge_pos = Coordinate(Config.BARGE_LOCATION[0], Config.BARGE_LOCATION[1])
        self.environment_ref = None  # Needed for pathfinding
        self.blackboard_ref = None

    def set_references(self, env, blackboard):
        """
        Assigns external references required by the agent to inspect the
        environment and coordinate zone ownership through the shared blackboard.
        """
        self.environment_ref = env
        self.blackboard_ref = blackboard

    def _evaluate_zones(self):
        """
        Evaluates all currently unharvested zones and selects the most valuable
        reachable target based on a utility cost function that balances travel
        distance against expected waste density.

        Returns:
            Coordinate | None: The best target zone to pursue or None if no
            reachable unharvested zones are available.
        """

        zones = self.blackboard_ref.get_unharvested_zones()
        if not zones:
            return None

        best_zone = None
        min_cost = float('inf')

        for zone in zones:
            path = a_star_search(self.state.position, zone, self.environment_ref)
            if path is not None:
                # Get waste density for utility calculation
                waste_density = self.environment_ref.get_cell(zone).density

                # Calculate utility-based cost
                distance_cost = len(path) * self.config.weight_distance_cost
                waste_value = waste_density * self.config.weight_waste_value
                total_cost = distance_cost - waste_value

                if total_cost < min_cost:
                    min_cost = total_cost
                    best_zone = zone

        return best_zone

    def next(self):
        """
        Performs the deliberative decision phase for the agent.

        Determines the next operational goal based on battery level, storage
        capacity, current target status, blackboard availability, and pathfinding
        feasibility. The agent prioritizes returning to the barge when storage is
        full or battery is low, otherwise it selects and claims an optimal waste
        zone.
        """

        # 1. If storage is full or battery is low, goal is barge
        if self.state.current_storage >= self.state.storage_capacity or self.state.battery < self.state.position.distance(
                self.barge_pos) + 20:
            if self.state.current_target != self.barge_pos:
                self.state.current_target = self.barge_pos
                self.current_path = a_star_search(self.state.position, self.barge_pos, self.environment_ref)
            return

        # 2. If at target zone, we will act to collect (handled in action)
        if self.state.current_target and self.state.position == self.state.current_target:
            if self.state.current_target != self.barge_pos:
                # Target was a waste zone, we have arrived
                return
            else:
                # At barge. If empty, clear target to find new zones.
                if self.state.current_storage == 0:
                    self.state.current_target = None
                else:
                    return

        # 3. If no target or finished previous target, find a new one
        if not self.state.current_target or self.current_path is None or len(self.current_path) == 0:
            best_zone = self._evaluate_zones()
            if best_zone and self.blackboard_ref.claim_zone(best_zone):
                # print(f"[{self.id}] Claimed zone {best_zone}")
                self.state.current_target = best_zone
                self.current_path = a_star_search(self.state.position, best_zone, self.environment_ref)
            else:
                # No zones available, wait or move towards barge
                if self.state.position != self.barge_pos:
                    self.state.current_target = self.barge_pos
                    self.current_path = a_star_search(self.state.position, self.barge_pos, self.environment_ref)
                else:
                    self.state.current_target = None  # Stay idle, wait for zones

    def action(self) -> Action:
        """
        Selects and returns the next executable action based on the agent's
        current state and previously deliberated target.

        The agent drops collected waste at the barge, collects waste when located
        on a valid target zone, marks depleted zones as harvested, follows its
        planned path when movement is required, or remains idle when no action is
        currently applicable.

        Returns:
            Action: The next action to be executed by the simulation runtime.
        """

        # Are we at the barge and need to drop?
        if self.state.position == self.barge_pos and self.state.current_storage > 0:
            return Action(type=ActionType.DROP)

        # Are we at a waste target?
        if self.state.current_target and self.state.position == self.state.current_target and self.state.current_target != self.barge_pos:
            if self.current_percept and self.current_percept.current_position_density > 0:
                return Action(type=ActionType.COLLECT)
            else:
                # Cleaned up, mark as harvested
                self.blackboard_ref.mark_harvested(self.state.current_target)
                self.state.current_target = None
                return Action(type=ActionType.IDLE)

        # Follow path
        if self.current_path and len(self.current_path) > 0:
            next_step = self.current_path.pop(0)
            return Action(type=ActionType.MOVE, target=next_step)

        return Action(type=ActionType.IDLE)