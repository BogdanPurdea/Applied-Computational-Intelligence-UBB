from dataclasses import dataclass


@dataclass
class DetectorConfig:
    battery_capacity: int = 1000
    movement_speed: int = 1
    energy_cost_per_move: int = 1
    sensor_range: int = 1
    waste_detection_threshold: int = 5
    exploration_strategy: str = "Random"


@dataclass
class CollectorConfig:
    battery_capacity: int = 2000
    storage_capacity: int = 50
    movement_speed: int = 1
    energy_cost_per_move: int = 1
    harvest_rate: int = 5
    unload_location: str = "Barge"
    weight_waste_value: float = 1.0
    weight_distance_cost: float = 1.0
    weight_energy_cost: float = 1.0
