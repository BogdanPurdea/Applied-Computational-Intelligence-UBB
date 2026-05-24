from models.coordinates import Coordinate
from typing import Dict, List

class Blackboard:
    """
    Shared communication model.
    Detectors write discovered high-density zones.
    Collectors read unharvested zones and mark them as harvested.
    """
    def __init__(self):
        # Stores coordinate mapping to a status: 'UNHARVESTED', 'IN_PROGRESS', 'HARVESTED'
        self.zones: Dict[Coordinate, str] = {}

    def write_zone(self, pos: Coordinate):
        """Detector writes a discovered zone."""
        if pos not in self.zones:
            self.zones[pos] = 'UNHARVESTED'

    def get_unharvested_zones(self) -> List[Coordinate]:
        """Collector reads available zones."""
        return [pos for pos, status in self.zones.items() if status == 'UNHARVESTED']

    def claim_zone(self, pos: Coordinate) -> bool:
        """Collector attempts to claim a zone to work on it."""
        if self.zones.get(pos) == 'UNHARVESTED':
            self.zones[pos] = 'IN_PROGRESS'
            return True
        return False

    def mark_harvested(self, pos: Coordinate):
        """Collector marks a zone as completely harvested."""
        if pos in self.zones:
            self.zones[pos] = 'HARVESTED'
