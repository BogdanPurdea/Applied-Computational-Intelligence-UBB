from abc import ABC, abstractmethod
from models.internal_state import InternalState
from models.percepts import Percept
from models.actions import Action

class Agent(ABC):
    def __init__(self, agent_id: str, initial_state: InternalState):
        self.id = agent_id
        self.state = initial_state
        self.current_percept = None

    def see(self, percept: Percept):
        """Update the agent's internal state based on what it perceives."""
        self.current_percept = percept

    @abstractmethod
    def next(self):
        """Process the percept and update internal beliefs/targets. Deliberation phase."""
        pass

    @abstractmethod
    def action(self) -> Action:
        """Select the next action to perform based on the internal state."""
        pass

    def act(self, env, blackboard, metrics) -> bool:
        """
        Execute the cycle. Returns False if the agent cannot act (e.g., out of battery).
        """
        if self.state.battery <= 0:
            return False

        # 1. Perception phase is handled externally by the simulation providing `see(percept)`
        # before calling `act()`. Or we can just assume `see()` was called.

        # 2. Deliberation
        self.next()

        # 3. Action selection
        chosen_action = self.action()

        # 4. Action Execution (the environment/simulation should actually process this, 
        # but for simplicity we will handle state changes here and return the action)
        return chosen_action
