# entry point + pygame visualizer + CLI

import os, pygame, time
from maze import Maze
from astar import astar_search

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WALL = (0, 255, 0)  # Green color for barriers
START = (0, 200, 0)  # Darker green for start
GOAL = (255, 0, 0)
PATH = (255, 215, 0)
EXPLORED = (100, 149, 237)
AGENT = (255, 0, 255)

CELL_SIZE = 30


def draw_maze(screen, maze, state=None, agent_pos=None):
    maze_offset_x = 0
    
    for r in range(maze.height):
        for c in range(maze.width):
            rect = pygame.Rect(maze_offset_x + c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze.grid[r][c] == 1:
                pygame.draw.rect(screen, WALL, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

    
    if state:
        for r, c in state.get("explored", []):
            rect = pygame.Rect(maze_offset_x + c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, EXPLORED, rect)

       
        if "path" in state and state["path"]:
            for r, c in state["path"]:
                rect = pygame.Rect(maze_offset_x + c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, PATH, rect)

    
    if agent_pos:
        r, c = agent_pos
        center_x = maze_offset_x + c * CELL_SIZE + CELL_SIZE // 2
        center_y = r * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        pygame.draw.circle(screen, AGENT, (center_x, center_y), radius)

    
    sr, sc = maze.start
    gr, gc = maze.goal
    pygame.draw.rect(screen, START, (maze_offset_x + sc*CELL_SIZE, sr*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, GOAL, (maze_offset_x + gc*CELL_SIZE, gr*CELL_SIZE, CELL_SIZE, CELL_SIZE))



def main():

    maze_dir = os.path.join(os.path.dirname(__file__), "..", "mazes")
    maze_file = os.path.join(maze_dir, "example_maze.txt")
    
    if not os.path.exists(maze_file):
        print(f"Maze file not found: {maze_file}")
        return
    
    maze = Maze.from_file(maze_file)
    generator = None

    pygame.init()
    screen = pygame.display.set_mode((maze.width*CELL_SIZE, maze.height*CELL_SIZE))
    pygame.display.set_caption("Maze Solver with A* (Animated)")
    clock = pygame.time.Clock()

    state = None
    agent_pos = maze.start
    path = None
    animating_path = False
    path_index = 0
    paused = False

    def restart_search():
        nonlocal generator, state, agent_pos, path, animating_path, path_index
        generator = astar_search(maze)
        state = None
        agent_pos = maze.start
        path = None
        animating_path = False
        path_index = 0

    restart_search()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart_search()
                elif event.key == pygame.K_p:
                    paused = not paused

        if not paused and not animating_path:
            try:
                if generator:
                    state = next(generator)
                    if "current" in state:
                        agent_pos = state["current"]
                    if "path" in state:
                        path = state["path"]
                        animating_path = True
                        path_index = 0
                        time.sleep(0.15)
            except StopIteration:
                pass
        elif not paused and animating_path:
            if path and path_index < len(path):
                agent_pos = path[path_index]
                path_index += 1
                time.sleep(0.5)
            else:
                animating_path = False

        
        screen.fill(BLACK)
        draw_maze(screen, maze, state, agent_pos)
        pygame.display.flip()
        clock.tick(10)  

    pygame.quit()

if __name__ == "__main__":
    main()