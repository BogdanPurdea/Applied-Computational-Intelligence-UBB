from typing import List
from models.actions import ActionType
from agents.base_agent import Agent
from environment import Environment
from blackboard import Blackboard
from utils.metrics import Metrics
from utils.visualization import print_grid
from state import SimulationState
from config import Config


class Simulation:
    """
    Central simulation controller responsible for coordinating the interaction
    between agents, the environment, the blackboard and performance metrics.

    The simulation follows a perception-deliberation-action cycle for each
    agent and applies the resulting actions to the environment until a
    termination condition is reached.
    """

    def __init__(self,
        environment: Environment,
        blackboard: Blackboard,
        agents: List[Agent],
        metrics: Metrics
    ):
        """
        Initializes the simulation and registers all participating components.

        Args:
            environment (Environment):
                Environment containing the simulation grid and world state;
            blackboard (Blackboard):
                Shared coordination mechanism used by agents;
            agents (List[Agent]):
                Collection of participating agents;
            metrics (Metrics):
                Metrics collector used to monitor simulation performance.
        """
        self.environment = environment
        self.blackboard = blackboard
        self.agents = agents
        self.metrics = metrics
        self.global_state = SimulationState(environment, blackboard, agents)

    def step(self, current_step: int) -> bool:
        """
        Executes a single simulation step.

        During each step, every active agent performs the following cycle:
            1. Perceives the environment;
            2. Updates its internal state;
            3. Selects an action;
            4. Executes the selected action.

        The simulation also updates energy consumption, waste collection
        statistics and evaluates termination conditions.

        Args:
            current_step (int):
                Current simulation iteration number.
        Returns:
            bool:
                True if the simulation should continue;
                False if a termination condition has been reached.
        """
        self.environment.state.step = current_step
        self.metrics.increment_time()
        active_agents = 0

        for agent in self.agents:

            # 1. Perception
            percept = self.environment.get_percept(agent.state.position)
            agent.see(percept)

            # 2 & 3. Deliberation and action selection
            action = agent.act(
                self.environment,
                self.blackboard,
                self.metrics
            )

            if action is False:
                # Agent is out of battery and can no longer participate.
                continue

            active_agents += 1

            # 4. Action Execution
            if action.type == ActionType.MOVE:

                # Validate destination before moving.
                target_cell = self.environment.get_cell(action.target)

                if not target_cell.is_obstacle:

                    # Movement cost depends on base energy consumption
                    # and local turbidity conditions.
                    energy_cost = (agent.config.energy_cost_per_move+ target_cell.turbidity)

                    if agent.state.battery >= energy_cost:
                        agent.state.record_move(action.target)
                        agent.state.battery -= energy_cost
                        self.metrics.add_energy(energy_cost)

            elif action.type == ActionType.COLLECT:

                cell = self.environment.get_cell(agent.state.position)

                if (cell.density > 0
                    and agent.state.current_storage
                    < agent.state.storage_capacity
                ):

                    # Determine maximum collection amount.
                    if hasattr(agent.config, 'harvest_rate'):
                        harvest_limit = agent.config.harvest_rate
                    else:
                        harvest_limit = cell.density

                    collected = min(
                        cell.density,
                        agent.state.storage_capacity
                        - agent.state.current_storage,
                        harvest_limit
                    )

                    self.environment.update_cell_density(agent.state.position, cell.density - collected)

                    agent.state.current_storage += collected

                    # Collection operations are more expensive than movement.
                    energy_cost = agent.config.energy_cost_per_move * 5

                    agent.state.battery -= energy_cost
                    self.metrics.add_energy(energy_cost)

            elif action.type == ActionType.DROP:

                # Waste can only be unloaded at the barge location.
                if (agent.state.position.x == Config.BARGE_LOCATION[0]
                    and agent.state.position.y == Config.BARGE_LOCATION[1]
                ):
                    self.metrics.add_harvested(agent.state.current_storage)

                    agent.state.current_storage = 0

                    # Energy cost associated with unloading.
                    agent.state.battery -= 2
                    self.metrics.add_energy(2)

        # Termination Condition 1: No agents remain operational.
        if active_agents == 0:
            print(f"Simulation ended early at step " f"{current_step}: All agents out of energy.")
            return False

        # Termination Condition 2: All waste has been collected.
        total_waste = sum(cell.density for row in self.environment.grid for cell in row)

        if total_waste == 0:
            print(f"Simulation ended early at step "f"{current_step}: All waste cleared!")
            return False

        return True

    def run(self):
        """
        Executes the complete simulation lifecycle.

        The simulation repeatedly advances through discrete time steps until
        one of the following conditions occurs:
            - Maximum simulation steps are reached;
            - All agents run out of energy;
            - All waste has been collected.

        At completion, summary statistics are calculated and displayed,
        followed by a final visualization of the environment state.
        """
        print("Starting Simulation...")

        for step in range(Config.MAX_STEPS):
            # Periodically display simulation progress.
            if step % 50 == 0:
                print(f"\n--- Step {step} ---")
                print_grid(self.environment, self.agents)
            if not self.step(step):
                break

        print("\nSimulation Finished!")

        self.metrics.discovered_zones_count = len(self.blackboard.zones)
        self.metrics.harvested_zones_count = len(
            [
                z
                for z, status in self.blackboard.zones.items()
                if status == 'HARVESTED'
            ]
        )
        self.metrics.display()

        print_grid(self.environment, self.agents)   # Display final environment state.
