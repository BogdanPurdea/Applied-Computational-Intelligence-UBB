import heapq
from models.coordinates import Coordinate
from typing import List, Optional


def get_neighbors(pos: Coordinate, width: int, height: int, env) -> List[Coordinate]:
    """
    Returns all valid traversable neighboring cells adjacent to the specified
    position.

    The function considers the four cardinal directions (north, south, east
    and west), ensures the resulting coordinates remain within environment
    boundaries and excludes cells marked as obstacles.

    Args:
        pos (Coordinate):
            The coordinate whose neighbors are being evaluated;
        width (int):
            Width of the environment grid;
        height (int):
            Height of the environment grid;
        env:
            Environment instance used to inspect cell properties.

    Returns:
        List[Coordinate]:
            A list of valid neighboring coordinates that can be traversed.
    """
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = pos.x + dx, pos.y + dy
        if 0 <= nx < width and 0 <= ny < height:
            if not env.get_cell(Coordinate(nx, ny)).is_obstacle:
                neighbors.append(Coordinate(nx, ny))
    return neighbors


def a_star_search(start: Coordinate, goal: Coordinate, env) -> Optional[List[Coordinate]]:
    """
    Computes the optimal path between two coordinates using the A* search
    algorithm.

    Movement cost is calculated as a base traversal cost of one unit plus a
    turbidity penalty derived from the destination cell. The heuristic function
    uses the coordinate distance to the goal, guiding the search toward the
    target while accounting for environmental traversal costs.

    Args:
        start (Coordinate):
            Starting coordinate of the path search;
        goal (Coordinate):
            Destination coordinate to reach;
        env:
            Environment instance containing grid dimensions and cell metadata.

    Returns:
        Optional[List[Coordinate]]:
            Ordered list of coordinates representing the path from the start
            position to the goal (excluding the starting coordinate) or None
            if no valid path exists.
    """
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
