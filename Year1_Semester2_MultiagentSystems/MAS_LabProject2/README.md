# Multi-Agent System: Autonomous Plastic Collection Simulation

## 1. Project Overview
This project implements a Multi-Agent System (MAS) designed to autonomously detect and collect plastic waste from a simulated aquatic environment. The system features a graphical user interface (GUI) and consists of two distinct agent types that collaborate to achieve a global objective: **Detector Agents** and **Collector Agents**.

---

## 2. Environment Design (PEAS)
The environment is formalized using the **PEAS** (Performance measure, Environment, Actuators, Sensors) framework:

- **Performance Measure**: 
  - Maximize the total amount of plastic waste harvested.
  - Minimize the energy consumed by the agents (movement and collection costs).
  - Clear the environment as quickly as possible (time/steps).
- **Environment**: 
  - A discrete 2D grid representing an aquatic region.
  - Contains dynamic features: Water (empty cells), Obstacles (impassable), Plastic Waste clusters (variable density), and a Central Barge (drop-off and recharge point).
  - Episodic, fully observable by the simulation, but *partially observable* by individual agents.
- **Actuators**: 
  - Movement capabilities (North, South, East, West).
  - Waste harvesting mechanisms (Collect).
  - Drop-off mechanisms (Unload at the barge).
- **Sensors**: 
  - Local cell sensors for reading the current position's waste density.
  - Adjacent cell sensors for detecting obstacles (North, South, East, West).
  - Blackboard access for reading/writing global discoveries.

---

## 3. Agent Design (PAGE)
The agents are structured using the **PAGE** (Percepts, Actions, Goals, Environment) architecture. There is a clear heterogeneous divide in the agent roles:

### 3.1. Detector Agent (Reactive/Reflex Agent)
Detectors are lightweight, exploratory agents. Their sole purpose is to map the environment and report high-density waste clusters.

- **Percepts**: Current cell waste density, adjacent obstacle status.
- **Actions**: `MOVE` (randomly to an unvisited/adjacent non-obstacle cell), `IDLE`.
- **Goals**: Explore the grid extensively. Report any cell with waste density $\ge$ Threshold to the Blackboard.
- **Environment**: Operates on the grid, oblivious to other agents, relies entirely on local perception.

**Code Implementation (Detector):**
```python
class DetectorAgent(Agent):
    def next(self):
        # Reflex behavior: if current cell has high density, write to blackboard
        if self.current_percept and self.current_percept.current_position_density >= self.config.waste_detection_threshold:
            if self.last_blackboard:
                self.last_blackboard.write_zone(self.state.position)

    def action(self) -> Action:
        # Reflex behavior: pick a random adjacent cell that is not an obstacle
        valid_moves = []
        if self.current_percept:
            for d_name, info in self.current_percept.adjacent_cells.items():
                if not info['is_obstacle']:
                    # ... calculate target_pos ...
                    valid_moves.append(target_pos)

        if valid_moves:
            return Action(type=ActionType.MOVE, target=random.choice(valid_moves))
        return Action(type=ActionType.IDLE)
```

### 3.2. Collector Agent (Utility-Based Deliberative Agent)
Collectors are heavy-duty agents that act on the intelligence gathered by the Detectors. They evaluate objectives and pathfind intelligently.

- **Percepts**: Current cell waste density, adjacent obstacle status, global list of unharvested zones from the Blackboard.
- **Actions**: `MOVE` (via A* pathfinding), `COLLECT` (harvest waste), `DROP` (unload at barge).
- **Goals**: Maintain battery/storage capacity, select the most optimal waste zone based on a multi-objective utility function (distance cost vs. waste value), and transport waste to the barge.
- **Environment**: Needs global knowledge from the Blackboard to plan paths (using A*) across the grid.

**Code Implementation (Collector Utility Evaluation):**
```python
    def _evaluate_zones(self):
        """Utility function: find the best zone based on distance (energy cost) vs waste value."""
        zones = self.blackboard_ref.get_unharvested_zones()
        best_zone, min_cost = None, float('inf')
        
        for zone in zones:
            path = a_star_search(self.state.position, zone, self.environment_ref)
            if path is not None:
                waste_density = self.environment_ref.get_cell(zone).density
                
                # Multi-objective utility calculation
                distance_cost = len(path) * self.config.weight_distance_cost
                waste_value = waste_density * self.config.weight_waste_value
                total_cost = distance_cost - waste_value
                
                if total_cost < min_cost:
                    min_cost = total_cost
                    best_zone = zone
                    
        return best_zone
```

---

## 4. Communication Method: The Blackboard Architecture
To decouple the agents and prevent complex direct messaging (e.g., FIPA ACL overhead for simple mapping), the MAS utilizes a **Blackboard pattern**. 

The Blackboard serves as a shared knowledge base. It handles the synchronization between the exploratory phase of the Detectors and the exploitative phase of the Collectors.

- **Write Operations**: Detectors post the coordinates of `UNHARVESTED` zones.
- **Read/Claim Operations**: Collectors query the board for available zones. To prevent two collectors from targeting the same cluster, the Blackboard uses a mutex-like state transition (`UNHARVESTED` $\rightarrow$ `IN_PROGRESS`).
- **Update Operations**: Once a collector finishes cleaning a zone, it updates the status to `HARVESTED`.

**Code Implementation (Blackboard):**
```python
class Blackboard:
    def __init__(self):
        # Maps Coordinate -> 'UNHARVESTED', 'IN_PROGRESS', 'HARVESTED'
        self.zones: Dict[Coordinate, str] = {}

    def write_zone(self, pos: Coordinate):
        """Detector writes a discovered zone."""
        if pos not in self.zones:
            self.zones[pos] = 'UNHARVESTED'

    def get_unharvested_zones(self) -> List[Coordinate]:
        """Collector reads available zones."""
        return [pos for pos, status in self.zones.items() if status == 'UNHARVESTED']

    def claim_zone(self, pos: Coordinate) -> bool:
        """Collector attempts to claim a zone."""
        if self.zones.get(pos) == 'UNHARVESTED':
            self.zones[pos] = 'IN_PROGRESS'
            return True
        return False
```

## 5. Conclusion
This architecture successfully demonstrates the principles of Multi-Agent Systems. By separating concerns—using reactive agents for cheap, wide-spread exploration, and utility-based deliberative agents for resource-intensive harvesting—the system optimizes global performance metrics while remaining modular and scalable.
