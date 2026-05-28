import random
from dataclasses import dataclass
from models.coordinates import Coordinate
from config import Config
from state import State


@dataclass
class Cell:
    density: int = 0
    is_obstacle: bool = False
    turbidity: int = 0


class Environment:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self._state = State(grid=grid, step=0)
        self._generate_environment()

    @property
    def state(self) -> State:
        """The current PAGES environment state."""
        return self._state

    @property
    def grid(self):
        """Backward-compatible alias for self._state.grid."""
        return self._state.grid

    def _generate_environment(self):
        # Place barge (ensure it's clear)
        bx, by = Config.BARGE_LOCATION
        self._state.grid[by][bx].is_obstacle = False

        # Place obstacles
        obstacles_placed = 0
        while obstacles_placed < Config.OBSTACLE_COUNT:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if not self._state.grid[y][x].is_obstacle and (x, y) != Config.BARGE_LOCATION:
                self._state.grid[y][x].is_obstacle = True
                obstacles_placed += 1

        # Place waste clusters
        clusters_placed = 0
        while clusters_placed < Config.WASTE_CLUSTERS:
            cx = random.randint(0, self.width - 1)
            cy = random.randint(0, self.height - 1)
            if not self._state.grid[cy][cx].is_obstacle and (cx, cy) != Config.BARGE_LOCATION:
                # Add waste in a small radius around cluster center
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if not self._state.grid[ny][nx].is_obstacle and (nx, ny) != Config.BARGE_LOCATION:
                                density = random.randint(1, 10)
                                self._state.grid[ny][nx].density = density
                                # Also add turbidity near waste
                                self._state.grid[ny][nx].turbidity = random.randint(0, Config.MAX_TURBIDITY)
                clusters_placed += 1

    def get_cell(self, pos: Coordinate) -> Cell:
        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            return self._state.grid[pos.y][pos.x]
        return Cell(is_obstacle=True)  # Out of bounds is obstacle

    def update_cell_density(self, pos: Coordinate, new_density: int):
        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            self._state.grid[pos.y][pos.x].density = new_density

    def get_percept(self, pos: Coordinate):
        from models.percepts import Percept
        cell = self.get_cell(pos)
        adj = {}
        for dx, dy, d_name in [(0, -1, 'N'), (0, 1, 'S'), (1, 0, 'E'), (-1, 0, 'W')]:
            n_pos = Coordinate(pos.x + dx, pos.y + dy)
            n_cell = self.get_cell(n_pos)
            adj[d_name] = {'is_obstacle': n_cell.is_obstacle, 'density': n_cell.density}

        return Percept(
            current_position_density=cell.density,
            is_obstacle=cell.is_obstacle,
            turbidity=cell.turbidity,
            adjacent_cells=adj
        )
