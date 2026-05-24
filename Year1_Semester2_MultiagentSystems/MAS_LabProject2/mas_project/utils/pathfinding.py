import heapq
from models.coordinates import Coordinate
from typing import List, Optional

def get_neighbors(pos: Coordinate, width: int, height: int, env) -> List[Coordinate]:
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = pos.x + dx, pos.y + dy
        if 0 <= nx < width and 0 <= ny < height:
            if not env.get_cell(Coordinate(nx, ny)).is_obstacle:
                neighbors.append(Coordinate(nx, ny))
    return neighbors

def a_star_search(start: Coordinate, goal: Coordinate, env) -> Optional[List[Coordinate]]:
    width = env.width
    height = env.height
    
    frontier = []
    heapq.heappush(frontier, (0, id(start), start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, _, current = heapq.heappop(frontier)

        if current.x == goal.x and current.y == goal.y:
            break

        for next_node in get_neighbors(current, width, height, env):
            # Cost to move to adjacent cell is 1 + turbidity penalty (simplified)
            turbidity_penalty = env.get_cell(next_node).turbidity
            new_cost = cost_so_far[current] + 1 + turbidity_penalty
            
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + next_node.distance(goal)
                heapq.heappush(frontier, (priority, id(next_node), next_node))
                came_from[next_node] = current

    if goal not in came_from:
        return None  # No path found

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
