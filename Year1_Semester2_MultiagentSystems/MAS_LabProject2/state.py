from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Environment
    from blackboard import Blackboard
    from agents.base_agent import Agent


@dataclass
class State:
    """
    The PAGES environment state.

    Captures the mutable world at a single simulation step.
    Transitions from one step to the next through agent actions:
      - grid: the 2D cell array (densities, obstacles, turbidity)
      - step: the current simulation step counter
    """
    grid: List[List]  # List[List[Cell]] — Cell defined in environment.py
    step: int = 0


class SimulationState:
    """
    Simulation-level aggregate: ties together the environment, blackboard,
    all live agents, and provides cross-cutting queries for the GUI.

    This is a representation of the simulation parameters and live references;
    it is not modified by agent actions.
    """
    def __init__(self, environment: "Environment", blackboard: "Blackboard", agents: List["Agent"]):
        self.environment = environment
        self.blackboard = blackboard
        self.agents = agents

    def get_agent_positions(self):
        return {agent.id: agent.state.position for agent in self.agents}
