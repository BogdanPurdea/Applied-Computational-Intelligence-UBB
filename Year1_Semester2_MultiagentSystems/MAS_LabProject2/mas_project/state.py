from environment import Environment
from blackboard import Blackboard
from typing import List
from agents.base_agent import Agent

class GlobalState:
    """
    Represents the complete state of the simulation at a point in time.
    """
    def __init__(self, environment: Environment, blackboard: Blackboard, agents: List[Agent]):
        self.environment = environment
        self.blackboard = blackboard
        self.agents = agents
        
    def get_agent_positions(self):
        return {agent.id: agent.state.position for agent in self.agents}
