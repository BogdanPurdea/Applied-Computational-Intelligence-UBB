from typing import List
from models.actions import ActionType
from agents.base_agent import Agent
from environment import Environment
from blackboard import Blackboard
from utils.metrics import Metrics
from utils.visualization import print_grid
from state import GlobalState
from config import Config
import time

class Simulation:
    def __init__(self, environment: Environment, blackboard: Blackboard, agents: List[Agent], metrics: Metrics):
        self.environment = environment
        self.blackboard = blackboard
        self.agents = agents
        self.metrics = metrics
        self.global_state = GlobalState(environment, blackboard, agents)

    def step(self, current_step: int) -> bool:
        self.metrics.increment_time()
        active_agents = 0
        
        for agent in self.agents:
            # 1. Perception
            percept = self.environment.get_percept(agent.state.position)
            agent.see(percept)
            
            # 2 & 3. Deliberation & Action Selection (act returns Action)
            action = agent.act(self.environment, self.blackboard, self.metrics)
            
            if action is False: # Agent is dead/out of battery
                continue
            
            active_agents += 1
            
            # 4. Action Execution
            if action.type == ActionType.MOVE:
                # Validate move (no obstacle)
                target_cell = self.environment.get_cell(action.target)
                if not target_cell.is_obstacle:
                    # Energy cost: 1 base + turbidity
                    energy_cost = 1 + target_cell.turbidity
                    if agent.state.battery >= energy_cost:
                        agent.state.record_move(action.target)
                        agent.state.battery -= energy_cost
                        self.metrics.add_energy(energy_cost)
            
            elif action.type == ActionType.COLLECT:
                cell = self.environment.get_cell(agent.state.position)
                if cell.density > 0 and agent.state.current_storage < agent.state.storage_capacity:
                    collected = min(cell.density, agent.state.storage_capacity - agent.state.current_storage)
                    self.environment.update_cell_density(agent.state.position, cell.density - collected)
                    agent.state.current_storage += collected
                    
                    # Energy cost for collecting
                    energy_cost = 5
                    agent.state.battery -= energy_cost
                    self.metrics.add_energy(energy_cost)

            elif action.type == ActionType.DROP:
                # Drop at barge
                if agent.state.position.x == Config.BARGE_LOCATION[0] and agent.state.position.y == Config.BARGE_LOCATION[1]:
                    self.metrics.add_harvested(agent.state.current_storage)
                    agent.state.current_storage = 0
                    # Recharging at barge (optional, assuming infinite energy at barge or just dropping off)
                    # Let's say dropping costs 2 energy
                    agent.state.battery -= 2
                    self.metrics.add_energy(2)
                    
        if active_agents == 0:
            print(f"Simulation ended early at step {current_step}: All agents out of energy.")
            return False
            
        # Check if all waste is cleared - simple check
        total_waste = sum(cell.density for row in self.environment.grid for cell in row)
        if total_waste == 0:
            print(f"Simulation ended early at step {current_step}: All waste cleared!")
            return False
            
        return True

    def run(self):
        print("Starting Simulation...")
        for step in range(Config.MAX_STEPS):
            # Print grid every 50 steps
            if step % 50 == 0:
                print(f"\n--- Step {step} ---")
                print_grid(self.environment, self.agents)
            
            if not self.step(step):
                break
                
        print("\nSimulation Finished!")
        self.metrics.discovered_zones_count = len(self.blackboard.zones)
        self.metrics.harvested_zones_count = len([z for z, status in self.blackboard.zones.items() if status == 'HARVESTED'])
        self.metrics.display()
        print_grid(self.environment, self.agents)
