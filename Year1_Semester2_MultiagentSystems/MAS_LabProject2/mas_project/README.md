# Multi-Agent System: Underwater Environmental Cleanup

This project simulates a Multi-Agent System (MAS) for an underwater environmental cleanup mission, utilizing Autonomous Underwater Vehicles (AUVs).

## Architecture

The project implements two types of agents:
- **DetectorAgent**: A reactive/reflex agent that explores the grid, finds high-density waste zones, and posts them to a shared Blackboard.
- **CollectorAgent**: A utility-based deliberative agent that evaluates unharvested zones on the Blackboard, plans optimal paths using A* search, collects the waste, and returns it to a central barge.

The agents communicate via a shared **Blackboard** and act in a discrete deterministic **Environment** represented by a 2D grid.

## Project Structure

- `main.py`: The entry point that initializes the environment, blackboard, agents, and starts the simulation.
- `config.py`: Configuration settings for grid size, agent energy, thresholds, etc.
- `simulation.py`: The main simulation loop orchestrating agent turns and tracking metrics.
- `environment.py`: Represents the physical grid, including waste density, obstacles, and turbidity.
- `blackboard.py`: Shared memory structure for agent communication.
- `state.py`: Global state of the simulation.
- `agents/`: Contains the base and specialized agent implementations.
- `models/`: Data structures representing coordinates, percepts, internal states, and actions.
- `utils/`: Helper functions for metrics tracking, pathfinding (A*), and terminal visualization.

## Running the Simulation

Ensure you have Python 3.7+ installed. No external dependencies are required.

Run the simulation via the terminal:

```bash
python main.py
```

The terminal will output the environment grid periodically and display final metrics upon completion.
