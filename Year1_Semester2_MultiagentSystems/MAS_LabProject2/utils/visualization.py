from models.coordinates import Coordinate

def print_grid(env, agents):
    grid = []
    for y in range(env.height):
        row = []
        for x in range(env.width):
            cell = env.get_cell(Coordinate(x, y))
            if cell.is_obstacle:
                row.append('X')
            elif cell.density > 0:
                row.append(str(cell.density))
            else:
                row.append('.')
        grid.append(row)

    # Overlay agents
    for agent in agents:
        x, y = agent.state.position.x, agent.state.position.y
        if agent.__class__.__name__ == 'DetectorAgent':
            grid[y][x] = 'D'
        elif agent.__class__.__name__ == 'CollectorAgent':
            grid[y][x] = 'C'

    # Overlay barge
    from config import Config
    bx, by = Config.BARGE_LOCATION
    grid[by][bx] = 'B'

    print("\nEnvironment State:")
    for row in grid:
        print(' '.join(row))
    print()
