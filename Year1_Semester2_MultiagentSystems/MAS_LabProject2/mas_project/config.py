from models.agent_config import DetectorConfig, CollectorConfig

class Config:
    # Grid dimensions
    GRID_WIDTH = 20
    GRID_HEIGHT = 20

    # Agent counts
    NUM_DETECTORS = 2
    NUM_COLLECTORS = 2

    # Agent starting and drop-off point (central barge)
    BARGE_LOCATION = (10, 10)

    # Simulation settings
    MAX_STEPS = 500

    # Environmental generation settings
    WASTE_CLUSTERS = 5
    OBSTACLE_COUNT = 15
    MAX_TURBIDITY = 3
    
    # Default agent configs (used as initial values in GUI)
    DEFAULT_DETECTOR_CONFIG = DetectorConfig()
    DEFAULT_COLLECTOR_CONFIG = CollectorConfig()
