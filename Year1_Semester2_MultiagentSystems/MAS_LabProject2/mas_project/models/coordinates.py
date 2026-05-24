from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)
    
    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
