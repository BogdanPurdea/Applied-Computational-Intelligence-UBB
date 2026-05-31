import sys
import os
sys.path.append(os.path.abspath('.'))

from models.coordinates import Coordinate
from config import Config
from environment import Environment
from utils.pathfinding import a_star_search

env = Environment(Config.GRID_WIDTH, Config.GRID_HEIGHT)
start = Coordinate(10, 10)
goal = Coordinate(11, 10)
env.get_cell(goal).is_obstacle = False # Ensure not obstacle

path = a_star_search(start, goal, env)
print("Path found:", path)
