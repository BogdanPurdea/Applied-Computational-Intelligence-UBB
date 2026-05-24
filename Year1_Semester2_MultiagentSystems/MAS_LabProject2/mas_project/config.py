class Config:
    # Grid dimensions
    GRID_WIDTH = 20
    GRID_HEIGHT = 20

    # Agent counts
    NUM_DETECTORS = 2
    NUM_COLLECTORS = 2

    # Agent starting and drop-off point (central barge)
    BARGE_LOCATION = (10, 10)

    # Agent constraints
    DETECTOR_ENERGY_CAP = 1000
    COLLECTOR_ENERGY_CAP = 2000
    COLLECTOR_STORAGE_CAP = 50

    # Simulation settings
    MAX_STEPS = 500
    WASTE_DENSITY_THRESHOLD = 5  # Density above this is reported by detectors

    # Environmental generation settings
    WASTE_CLUSTERS = 5
    OBSTACLE_COUNT = 15
    MAX_TURBIDITY = 3
