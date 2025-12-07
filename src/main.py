# entry point + pygame visualizer + CLI

import sys, os, pygame, time, random
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
CONTROL_PANEL_WIDTH = 250  # Space for controls sidebar

def change_maze_dimensions(maze, new_width, new_height):
    """Function to change maze dimensions"""
    maze.change_dimensions(new_width, new_height)
    return maze

def change_goal_position(maze, new_goal_row, new_goal_col):
    """Function to change the goal position"""
    return maze.change_goal((new_goal_row, new_goal_col))

def add_obstacle(maze, row, col):
    """Function to add an obstacle at a specific position"""
    return maze.add_obstacle(row, col)

def remove_obstacle(maze, row, col):
    """Function to remove an obstacle at a specific position"""
    return maze.remove_obstacle(row, col)

def augment_obstacles(maze, count):
    """Function to add random obstacles (augment)"""
    return maze.add_random_obstacles(count)

def reduce_obstacles(maze, count):
    """Function to remove random obstacles (reduce)"""
    return maze.remove_random_obstacles(count)

def get_available_mazes():
    """Get list of available maze files"""
    maze_dir = os.path.join(os.path.dirname(__file__), "..", "mazes")
    maze_files = []
    if os.path.exists(maze_dir):
        for file in os.listdir(maze_dir):
            if file.endswith('.txt'):
                maze_files.append(file)
    maze_files.sort()
    return maze_files

def draw_maze(screen, maze, state=None, agent_pos=None, show_controls=True, current_maze_name=None, available_mazes=None):
    # Draw control panel sidebar
    control_panel_rect = pygame.Rect(0, 0, CONTROL_PANEL_WIDTH, screen.get_height())
    pygame.draw.rect(screen, (30, 30, 30), control_panel_rect)
    pygame.draw.line(screen, (100, 100, 100), (CONTROL_PANEL_WIDTH, 0), (CONTROL_PANEL_WIDTH, screen.get_height()), 2)
    
    # Draw controls in sidebar
    if show_controls:
        try:
            font = pygame.font.Font(None, 24)
            title_font = pygame.font.Font(None, 28)
            controls = [
                ("Controls:", title_font),
                ("", None),
                ("Mouse:", title_font),
                ("Left Click - Add", font),
                ("Right Click - Remove", font),
                ("", None),
                ("Keyboard:", title_font),
                ("1-4 - Select Maze", font),
                ("I - Initial Maze", font),
                ("R - Reset & Resize", font),
                ("G - Change Goal", font),
                ("A - Add obstacles", font),
                ("D - Remove obstacles", font),
                ("Space - Restart", font),
                ("H - Hide/Show", font),
                ("P - Pause", font)
            ]
            y_offset = 20
            for text, text_font in controls:
                if text_font:
                    text_surface = text_font.render(text, True, (255, 255, 255))
                    screen.blit(text_surface, (15, y_offset))
                y_offset += 30
            
            # Show current maze and available mazes
            if current_maze_name and available_mazes:
                y_offset += 10
                maze_title = title_font.render("Mazes:", True, (255, 255, 255))
                screen.blit(maze_title, (15, y_offset))
                y_offset += 30
                for i, maze_file in enumerate(available_mazes[:4], 1):  # Show first 4 mazes
                    prefix = "> " if maze_file == current_maze_name else f"{i}. "
                    maze_text = f"{prefix}{maze_file.replace('.txt', '')}"
                    color = (255, 255, 0) if maze_file == current_maze_name else (200, 200, 200)
                    maze_surface = font.render(maze_text, True, color)
                    screen.blit(maze_surface, (15, y_offset))
                    y_offset += 25
        except:
            pass
    
    # Draw maze offset to the right of control panel
    maze_offset_x = CONTROL_PANEL_WIDTH
    
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
    
    # Get available mazes
    available_mazes = get_available_mazes()
    if not available_mazes:
        print("No maze files found!")
        return
    
    # Start with first maze
    current_maze_index = 0
    maze_dir = os.path.join(os.path.dirname(__file__), "..", "mazes")
    maze_file = os.path.join(maze_dir, available_mazes[current_maze_index])
    maze = Maze.from_file(maze_file)
    current_maze_name = available_mazes[current_maze_index]
    
    # Store initial maze state for reset
    import copy
    initial_grid = copy.deepcopy(maze.grid)
    initial_start = maze.start
    initial_goal = maze.goal

    generator = None
    show_controls = True
    
    def load_maze(maze_filename):
        """Load a maze file and update initial state"""
        nonlocal maze, initial_grid, initial_start, initial_goal, current_maze_name
        maze_path = os.path.join(maze_dir, maze_filename)
        if os.path.exists(maze_path):
            maze = Maze.from_file(maze_path)
            current_maze_name = maze_filename
            initial_grid = copy.deepcopy(maze.grid)
            initial_start = maze.start
            initial_goal = maze.goal
            return True
        return False

    pygame.init()
    screen = pygame.display.set_mode((maze.width*CELL_SIZE + CONTROL_PANEL_WIDTH, maze.height*CELL_SIZE))
    pygame.display.set_caption("Maze Solver with A* (Animated) - Press H to toggle controls")
    clock = pygame.time.Clock()

    state = None
    agent_pos = maze.start
    path = None
    animating_path = False
    path_index = 0
    paused = False
    mouse_drawing = False
    last_mouse_cell = None

    def restart_search():
        nonlocal generator, state, agent_pos, path, animating_path, path_index
        generator = astar_search(maze)
        state = None
        agent_pos = maze.start
        path = None
        animating_path = False
        path_index = 0

    restart_search()

    def get_cell_from_pos(pos):
        """Convert mouse position to maze cell coordinates"""
        x, y = pos
        if x < CONTROL_PANEL_WIDTH:
            return None  # Clicked on control panel
        col = (x - CONTROL_PANEL_WIDTH) // CELL_SIZE
        row = y // CELL_SIZE
        if 0 <= row < maze.height and 0 <= col < maze.width:
            return (row, col)
        return None

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cell = get_cell_from_pos(event.pos)
                if cell:
                    row, col = cell
                    if event.button == 1:  # Left click - add obstacle
                        if add_obstacle(maze, row, col):
                            restart_search()
                    elif event.button == 3:  # Right click - remove obstacle
                        if remove_obstacle(maze, row, col):
                            restart_search()
                    last_mouse_cell = cell
                    mouse_drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_drawing = False
                last_mouse_cell = None
            elif event.type == pygame.MOUSEMOTION:
                if mouse_drawing:
                    cell = get_cell_from_pos(event.pos)
                    if cell and cell != last_mouse_cell:
                        row, col = cell
                        if mouse_buttons[0]:  # Left button held - add
                            if add_obstacle(maze, row, col):
                                restart_search()
                        elif mouse_buttons[2]:  # Right button held - remove
                            if remove_obstacle(maze, row, col):
                                restart_search()
                        last_mouse_cell = cell
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    show_controls = not show_controls
                elif event.key == pygame.K_1 and len(available_mazes) > 0:
                    if load_maze(available_mazes[0]):
                        screen = pygame.display.set_mode((maze.width*CELL_SIZE + CONTROL_PANEL_WIDTH, maze.height*CELL_SIZE))
                        restart_search()
                elif event.key == pygame.K_2 and len(available_mazes) > 1:
                    if load_maze(available_mazes[1]):
                        screen = pygame.display.set_mode((maze.width*CELL_SIZE + CONTROL_PANEL_WIDTH, maze.height*CELL_SIZE))
                        restart_search()
                elif event.key == pygame.K_3 and len(available_mazes) > 2:
                    if load_maze(available_mazes[2]):
                        screen = pygame.display.set_mode((maze.width*CELL_SIZE + CONTROL_PANEL_WIDTH, maze.height*CELL_SIZE))
                        restart_search()
                elif event.key == pygame.K_4 and len(available_mazes) > 3:
                    if load_maze(available_mazes[3]):
                        screen = pygame.display.set_mode((maze.width*CELL_SIZE + CONTROL_PANEL_WIDTH, maze.height*CELL_SIZE))
                        restart_search()
                elif event.key == pygame.K_i:
                    # Reset to initial maze state
                    maze.reset_to_initial(initial_grid, initial_start, initial_goal)
                    screen = pygame.display.set_mode((maze.width*CELL_SIZE + CONTROL_PANEL_WIDTH, maze.height*CELL_SIZE))
                    restart_search()
                elif event.key == pygame.K_r:
                    # Reset and resize to 20x15
                    change_maze_dimensions(maze, 20, 15)
                    screen = pygame.display.set_mode((maze.width*CELL_SIZE + CONTROL_PANEL_WIDTH, maze.height*CELL_SIZE))
                    restart_search()
                elif event.key == pygame.K_g:
                    # Change goal to a random passable position
                    attempts = 0
                    while attempts < 100:
                        r = random.randint(0, maze.height - 1)
                        c = random.randint(0, maze.width - 1)
                        if change_goal_position(maze, r, c):
                            restart_search()
                            break
                        attempts += 1
                elif event.key == pygame.K_a:
                    # Add obstacles (augment)
                    added = augment_obstacles(maze, 10)
                    print(f"Added {added} obstacles")
                    restart_search()
                elif event.key == pygame.K_d:
                    # Remove obstacles (reduce)
                    removed = reduce_obstacles(maze, 10)
                    print(f"Removed {removed} obstacles")
                    restart_search()
                elif event.key == pygame.K_SPACE:
                    # Restart search
                    restart_search()
                elif event.key == pygame.K_p:
                    paused = not paused

        # Handle continuous mouse drawing
        if mouse_drawing and (mouse_buttons[0] or mouse_buttons[2]):
            cell = get_cell_from_pos(mouse_pos)
            if cell and cell != last_mouse_cell:
                row, col = cell
                if mouse_buttons[0]:  # Left button - add
                    if add_obstacle(maze, row, col):
                        restart_search()
                elif mouse_buttons[2]:  # Right button - remove
                    if remove_obstacle(maze, row, col):
                        restart_search()
                last_mouse_cell = cell

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
        draw_maze(screen, maze, state, agent_pos, show_controls, current_maze_name, available_mazes)
        pygame.display.flip()
        clock.tick(10)  

    pygame.quit()

if __name__ == "__main__":
    main()