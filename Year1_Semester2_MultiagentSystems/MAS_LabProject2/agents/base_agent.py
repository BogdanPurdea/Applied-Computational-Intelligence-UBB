from abc import ABC, abstractmethod
from models.internal_state import InternalState
from models.percepts import Percept
from models.actions import Action


class Agent(ABC):

    def __init__(self, agent_id: str, initial_state: InternalState, config=None):
        """
        Initializes the base agent with a unique identifier, internal runtime
        state, optional configuration and an empty percept reference.
        """
        self.id = agent_id
        self.state = initial_state
        self.config = config
        self.current_percept = None

    def see(self, percept: Percept):
        """
        Updates the agent's current percept with the latest environmental
        observation provided by the simulation.
        """
        self.current_percept = percept

    @abstractmethod
    def next(self):
        """
        Executes the agent's deliberation phase.

        Subclasses must implement this method to process the current percept,
        update internal beliefs, select targets or prepare any decision context
        required before choosing an action.
        """
        pass

    @abstractmethod
    def action(self) -> Action:
        """
        Selects the next action the agent intends to perform.

        Subclasses must implement this method to convert the current internal
        state and decision context into an executable simulation action.

        Returns:
            Action: The action selected by the concrete agent implementation.
        """
        pass

    def act(self, env, blackboard, metrics) -> bool:
        """
        Runs one complete agent decision cycle.

        The method validates whether the agent still has available battery,
        executes the deliberation phase, selects the next action and returns
        that action to the simulation runtime for processing.

        Args:
            - env: The environment instance associated with the current simulation.
            - blackboard: The shared coordination structure used by agents.
            - metrics: The metrics collector used by the simulation runtime.

        Returns:
            Action | bool: The selected action when the agent can act or False
            when the agent has no remaining battery.
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
