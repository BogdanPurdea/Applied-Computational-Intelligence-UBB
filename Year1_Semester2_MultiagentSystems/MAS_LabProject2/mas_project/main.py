from config import Config
from environment import Environment
from blackboard import Blackboard
from utils.metrics import Metrics
from models.internal_state import InternalState
from models.coordinates import Coordinate
from agents.detector_agent import DetectorAgent
from agents.collector_agent import CollectorAgent
from simulation import Simulation

def main():
    print("Initializing Multi-Agent System...")

    # Initialize Environment
    env = Environment(Config.GRID_WIDTH, Config.GRID_HEIGHT)

    # Initialize Blackboard
    blackboard = Blackboard()

    # Initialize Metrics
    metrics = Metrics()

    # Initialize Agents
    agents = []
    
    barge_pos = Coordinate(Config.BARGE_LOCATION[0], Config.BARGE_LOCATION[1])
    
    for i in range(Config.NUM_DETECTORS):
        state = InternalState(
            position=Coordinate(barge_pos.x, barge_pos.y),
            battery=Config.DETECTOR_ENERGY_CAP,
        )
        detector = DetectorAgent(f"Detector-{i}", state)
        detector.set_blackboard(blackboard)
        agents.append(detector)
        
    for i in range(Config.NUM_COLLECTORS):
        state = InternalState(
            position=Coordinate(barge_pos.x, barge_pos.y),
            battery=Config.COLLECTOR_ENERGY_CAP,
            storage_capacity=Config.COLLECTOR_STORAGE_CAP
        )
        collector = CollectorAgent(f"Collector-{i}", state)
        collector.set_references(env, blackboard)
        agents.append(collector)

    # Initialize Simulation
    sim = Simulation(env, blackboard, agents, metrics)
    
    # Run
    sim.run()

if __name__ == "__main__":
    main()
