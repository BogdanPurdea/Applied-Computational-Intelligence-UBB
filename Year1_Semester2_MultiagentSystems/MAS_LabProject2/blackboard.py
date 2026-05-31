from models.coordinates import Coordinate
from typing import Dict, List

class Blackboard:
    """
    Shared coordination mechanism used by agents to exchange information about
    detected waste zones.

    Detector agents publish newly discovered high-density waste locations,
    while collector agents retrieve, claim, and update the processing status
    of those locations. This prevents multiple collectors from working on the
    same zone simultaneously and provides a centralized view of collection
    progress.

    Zone lifecycle:
        UNHARVESTED -> IN_PROGRESS -> HARVESTED
    """

    def __init__(self):
        """
        Initializes an empty blackboard containing no registered waste zones.

        The blackboard maintains a mapping between zone coordinates and their
        current processing status.
        """
        # Stores coordinate mapping to a status: 'UNHARVESTED', 'IN_PROGRESS', 'HARVESTED'
        self.zones: Dict[Coordinate, str] = {}

    def write_zone(self, pos: Coordinate):
        """
        Registers a newly detected waste zone on the blackboard.

        If the zone has already been registered, the existing entry remains
        unchanged.

        Args:
            pos (Coordinate):
                Coordinate of the detected waste zone.
        """
        if pos not in self.zones:
            self.zones[pos] = 'UNHARVESTED'

    def get_unharvested_zones(self) -> List[Coordinate]:
        """
        Retrieves all zones currently available for collection.

        Returns:
            List[Coordinate]:
                Collection of coordinates whose status is UNHARVESTED.
        """
        return [pos for pos, status in self.zones.items() if status == 'UNHARVESTED']

    def claim_zone(self, pos: Coordinate) -> bool:
        """
        Attempts to reserve a zone for processing by a collector agent.

        If the zone is currently unharvested, its status is changed to
        IN_PROGRESS and the claim succeeds.

        Args:
            pos (Coordinate):
                Coordinate of the zone to claim.

        Returns:
            bool:
                True if the claim was successful; otherwise False.
        """
        if self.zones.get(pos) == 'UNHARVESTED':
            self.zones[pos] = 'IN_PROGRESS'
            return True
        return False

    def mark_harvested(self, pos: Coordinate):
        """
        Marks a zone as fully processed and collected.

        Args:
            pos (Coordinate):
                Coordinate of the harvested zone.
        """
        if pos in self.zones:
            self.zones[pos] = 'HARVESTED'
