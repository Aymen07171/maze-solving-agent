# A* search (generator that yields steps for visualization)

import heapq

def manhattan(a, b):
    "Heuristic: Manhattan distance"
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_search(maze, heuristic=manhattan):
    start, goal = maze.start, maze.goal
    frontier = [(0, start)]
    came_from = {start: None}
    gscore = {start: 0}
    explored = set()

    while frontier:
        _, current = heapq.heappop(frontier)

        yield {"current": current, "explored": set(explored), "came_from": dict(came_from)}

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            yield {"path": path, "explored": set(explored)}
            return

        explored.add(current)

        for neighbor in maze.neighbors(current):
            new_cost = gscore[current] + 1
            if neighbor not in gscore or new_cost < gscore[neighbor]:
                gscore[neighbor] = new_cost
                fscore = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (fscore, neighbor))
                came_from[neighbor] = current

    yield {"path": None, "explored": set(explored)}