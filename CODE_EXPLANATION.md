# 🧠 Maze Solving Agent - Complete Code Explanation
## A Beginner-Friendly Guide to Understanding the Code

---

## 📚 Table of Contents
1. [What is This Project?](#what-is-this-project)
2. [Project Structure](#project-structure)
3. [Understanding Python Basics Used](#understanding-python-basics-used)
4. [File-by-File Explanation](#file-by-file-explanation)
5. [How Everything Works Together](#how-everything-works-together)
6. [Step-by-Step Code Walkthrough](#step-by-step-code-walkthrough)

---

## 🎯 What is This Project?

This project creates a **maze-solving robot** that uses artificial intelligence to find the shortest path from a starting point to a goal. Think of it like a robot in a maze trying to find the exit!

### Key Concepts:
- **Maze**: A grid with walls (obstacles) and open paths
- **Agent**: The robot that moves through the maze
- **A* Algorithm**: A smart search algorithm that finds the best path
- **Visualization**: We use Pygame to see the robot moving in real-time

---

## 📁 Project Structure

```
maze-solving-agent/
├── src/
│   ├── main.py      # Main program with graphics and controls
│   ├── maze.py      # Maze class - handles maze data
│   └── astar.py     # A* algorithm - finds the path
├── mazes/
│   ├── example_maze.txt
│   ├── small_maze.txt
│   └── ... (more maze files)
└── requirements.txt
```

---

## 🐍 Understanding Python Basics Used

Before diving into the code, let's understand some Python concepts:

### 1. **Variables**
```python
CELL_SIZE = 30  # A constant value
maze = Maze.from_file(file)  # A variable that stores a maze object
```

### 2. **Lists and Tuples**
```python
# List: can change
colors = [255, 255, 255]

# Tuple: cannot change (immutable)
position = (5, 10)  # row 5, column 10
```

### 3. **Functions**
```python
def function_name(parameter):
    # Do something
    return result
```

### 4. **Classes**
```python
class Maze:
    def __init__(self, grid):
        self.grid = grid  # 'self' refers to the object itself
```

### 5. **Loops**
```python
# For loop - repeat for each item
for row in range(10):
    print(row)

# While loop - repeat while condition is true
while running:
    # Do something
```

---

## 📄 File-by-File Explanation

### File 1: `maze.py` - The Maze Class

This file defines what a maze is and what it can do.

#### **What is a Class?**
A class is like a blueprint. Think of it as a cookie cutter - you can make many cookies (objects) from one cutter (class).

#### **The Maze Class Structure:**

```python
class Maze:
    def __init__(self, grid, start=None, goal=None):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0
        self.start = start
        self.goal = goal
```

**Explanation:**
- `__init__` is a special function called when you create a new maze
- `self.grid`: The maze layout (0 = open path, 1 = wall)
- `self.height`: Number of rows
- `self.width`: Number of columns
- `self.start`: Starting position (row, column)
- `self.goal`: Goal position (row, column)

#### **Key Methods Explained:**

**1. `from_file(cls, path)` - Loading a Maze from File**
```python
@classmethod
def from_file(cls, path):
    lines = []
    with open(path, 'r', encoding='utf-8') as f:
        for ln in f:
            if ln.strip() == '':
                continue
            lines.append(ln.rstrip('\n'))
```

**What it does:**
- Opens a text file
- Reads each line
- Converts characters to numbers:
  - `#` or `1` → wall (1)
  - `.` or space → open path (0)
  - `S` → start position
  - `G` → goal position

**2. `neighbors(self, pos)` - Finding Adjacent Cells**
```python
def neighbors(self, pos):
    r, c = pos
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if self.in_bounds((nr, nc)) and self.passable((nr, nc)):
            yield (nr, nc)
```

**What it does:**
- Takes a position (row, column)
- Checks 4 directions: up, down, left, right
- Returns only valid, passable neighbors
- `yield` is like `return`, but for generators (more efficient)

**3. `add_obstacle` and `remove_obstacle` - Modifying the Maze**
```python
def add_obstacle(self, row, col):
    if self.in_bounds((row, col)):
        if (row, col) != self.start and (row, col) != self.goal:
            self.grid[row][col] = 1
            return True
    return False
```

**What it does:**
- Checks if position is valid
- Makes sure we don't block start or goal
- Changes grid cell to 1 (wall)

---

### File 2: `astar.py` - The A* Search Algorithm

This is the "brain" that finds the best path!

#### **What is A* Algorithm?**
A* (A-star) is a pathfinding algorithm that:
1. Explores possible paths
2. Uses a "heuristic" (educated guess) to prioritize promising paths
3. Always finds the shortest path if one exists

#### **The Algorithm Step-by-Step:**

```python
def astar_search(maze, heuristic=manhattan):
    start, goal = maze.start, maze.goal
    frontier = [(0, start)]  # Priority queue: (priority, position)
    came_from = {start: None}  # Track where we came from
    gscore = {start: 0}  # Cost to reach each position
    explored = set()  # Positions we've already checked
```

**Key Variables:**
- `frontier`: Positions to explore next (like a to-do list)
- `came_from`: Remembers the path (like breadcrumbs)
- `gscore`: Actual cost to reach each position
- `explored`: Positions we've already visited

**The Main Loop:**
```python
while frontier:
    _, current = heapq.heappop(frontier)  # Get best position
    
    if current == goal:  # Found the goal!
        # Reconstruct path
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
    
    explored.add(current)
    
    # Check neighbors
    for neighbor in maze.neighbors(current):
        new_cost = gscore[current] + 1
        if neighbor not in gscore or new_cost < gscore[neighbor]:
            gscore[neighbor] = new_cost
            fscore = new_cost + heuristic(neighbor, goal)
            heapq.heappush(frontier, (fscore, neighbor))
            came_from[neighbor] = current
```

**How it works:**
1. Start with the starting position
2. Check all neighbors (up, down, left, right)
3. Calculate cost: actual distance + estimated distance to goal
4. Add promising positions to frontier
5. Repeat until goal is found

**Manhattan Distance (Heuristic):**
```python
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
```

This calculates the straight-line distance (like city blocks - can't go diagonally).

---

### File 3: `main.py` - The Main Program

This file handles:
- Graphics (drawing the maze)
- User input (keyboard and mouse)
- Animation (showing the robot move)

#### **Color Constants:**
```python
WHITE = (255, 255, 255)  # RGB color values
WALL = (0, 255, 0)       # Green for walls
START = (0, 200, 0)      # Darker green for start
GOAL = (255, 0, 0)       # Red for goal
PATH = (255, 215, 0)     # Gold for path
EXPLORED = (100, 149, 237)  # Blue for explored cells
AGENT = (255, 0, 255)    # Magenta for the robot
```

**RGB Colors:** Each color is represented by three numbers (0-255):
- Red, Green, Blue
- (255, 0, 0) = Pure Red
- (0, 255, 0) = Pure Green
- (0, 0, 255) = Pure Blue

#### **The `draw_maze` Function:**

This function draws everything on the screen:

```python
def draw_maze(screen, maze, state=None, agent_pos=None, ...):
    # 1. Draw control panel (sidebar)
    control_panel_rect = pygame.Rect(0, 0, CONTROL_PANEL_WIDTH, screen.get_height())
    pygame.draw.rect(screen, (30, 30, 30), control_panel_rect)
    
    # 2. Draw the maze grid
    for r in range(maze.height):
        for c in range(maze.width):
            rect = pygame.Rect(maze_offset_x + c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze.grid[r][c] == 1:
                pygame.draw.rect(screen, WALL, rect)  # Draw wall
            else:
                pygame.draw.rect(screen, WHITE, rect)  # Draw open path
    
    # 3. Draw explored cells (blue)
    if state:
        for r, c in state.get("explored", []):
            rect = pygame.Rect(...)
            pygame.draw.rect(screen, EXPLORED, rect)
    
    # 4. Draw the path (gold)
    if "path" in state and state["path"]:
        for r, c in state["path"]:
            pygame.draw.rect(screen, PATH, rect)
    
    # 5. Draw the agent (robot) as a circle
    if agent_pos:
        r, c = agent_pos
        center_x = maze_offset_x + c * CELL_SIZE + CELL_SIZE // 2
        center_y = r * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        pygame.draw.circle(screen, AGENT, (center_x, center_y), radius)
    
    # 6. Draw start and goal
    pygame.draw.rect(screen, START, ...)  # Green square
    pygame.draw.rect(screen, GOAL, ...)   # Red square
```

#### **The `main` Function - The Game Loop:**

This is the heart of the program. It runs continuously:

```python
def main():
    # 1. Load the maze
    maze = Maze.from_file(maze_file)
    
    # 2. Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    
    # 3. Create the A* search generator
    generator = astar_search(maze)
    
    # 4. Main game loop
    running = True
    while running:
        # Handle events (keyboard, mouse, window close)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Handle keyboard input
                if event.key == pygame.K_a:
                    # Add obstacles
                elif event.key == pygame.K_d:
                    # Remove obstacles
        
        # Update the search (get next step)
        if not paused and not animating_path:
            try:
                state = next(generator)  # Get next step from A*
                agent_pos = state["current"]
            except StopIteration:
                pass  # Search finished
        
        # Draw everything
        screen.fill(BLACK)
        draw_maze(screen, maze, state, agent_pos, ...)
        pygame.display.flip()  # Update the screen
        clock.tick(10)  # Limit to 10 frames per second
```

**Key Concepts:**

**1. Event Loop:**
- Continuously checks for user input
- Updates the game state
- Redraws the screen

**2. Generator:**
```python
generator = astar_search(maze)
state = next(generator)  # Get next step
```
- A generator yields values one at a time
- Perfect for animation (shows each step)

**3. Mouse Input:**
```python
def get_cell_from_pos(pos):
    x, y = pos
    if x < CONTROL_PANEL_WIDTH:
        return None  # Clicked on control panel
    col = (x - CONTROL_PANEL_WIDTH) // CELL_SIZE
    row = y // CELL_SIZE
    return (row, col)
```

**What it does:**
- Converts screen coordinates (pixels) to grid coordinates
- Example: Click at (300, 150) → Cell (5, 2)

---

## 🔄 How Everything Works Together

### The Flow:

1. **Program Starts** → `main()` function runs
2. **Load Maze** → Reads from text file
3. **Initialize Graphics** → Creates Pygame window
4. **Start A* Search** → Creates generator
5. **Game Loop Begins:**
   - Check for user input
   - Get next step from A* algorithm
   - Draw everything on screen
   - Repeat
6. **User Interacts:**
   - Presses keys or clicks mouse
   - Maze changes
   - Search restarts
7. **Path Found:**
   - A* returns the path
   - Robot animates along the path
   - Done!

### Data Flow:

```
Maze File (text)
    ↓
Maze Class (converts to grid)
    ↓
A* Algorithm (finds path)
    ↓
Main Program (displays on screen)
    ↓
User sees animation
```

---

## 📖 Step-by-Step Code Walkthrough

### Example: What happens when you press 'A'?

1. **User presses 'A' key**
   ```python
   elif event.key == pygame.K_a:
   ```

2. **Add random obstacles**
   ```python
   added = augment_obstacles(maze, 10)
   ```
   - Calls `maze.add_random_obstacles(10)`
   - Randomly picks 10 empty cells
   - Changes them to walls (1)

3. **Restart search**
   ```python
   restart_search()
   ```
   - Creates new A* generator
   - Resets agent position
   - Starts fresh search

4. **Screen updates**
   - New obstacles appear (green)
   - Search begins again
   - New path is found

### Example: How A* finds a path

**Initial State:**
```
Start: (0, 0)
Goal: (5, 5)
Frontier: [(0, (0, 0))]
```

**Step 1:**
- Pop (0, (0, 0)) from frontier
- Check neighbors: (0, 1), (1, 0)
- Add to frontier with costs

**Step 2:**
- Pop best position
- Check its neighbors
- Continue...

**Final Step:**
- Reach goal (5, 5)
- Reconstruct path using `came_from`
- Return path: [(0,0), (0,1), (1,1), ..., (5,5)]

---

## 🎓 Key Python Concepts Explained

### 1. **Lists vs Tuples**
```python
# List - can modify
my_list = [1, 2, 3]
my_list.append(4)  # OK

# Tuple - cannot modify
my_tuple = (1, 2, 3)
my_tuple.append(4)  # ERROR!
```

### 2. **Dictionaries**
```python
came_from = {start: None}
came_from[(1, 2)] = (0, 0)  # Store value
position = came_from[(1, 2)]  # Retrieve value
```

### 3. **Sets**
```python
explored = set()
explored.add((1, 2))  # Add item
if (1, 2) in explored:  # Check if exists
    print("Found!")
```

### 4. **Generators (yield)**
```python
def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()
print(next(gen))  # Prints 1
print(next(gen))  # Prints 2
```

### 5. **List Comprehensions**
```python
# Instead of:
new_list = []
for item in old_list:
    new_list.append(item * 2)

# You can write:
new_list = [item * 2 for item in old_list]
```

### 6. **Lambda Functions (not used here, but good to know)**
```python
# Short function
square = lambda x: x * x
print(square(5))  # Prints 25
```

---

## 🎮 Controls Explained

### Keyboard Controls:
- **1-4**: Select different maze files
- **I**: Reset to initial maze state
- **R**: Reset and resize to 20x15
- **G**: Change goal to random position
- **A**: Add 10 random obstacles
- **D**: Remove 10 random obstacles
- **Space**: Restart the search
- **H**: Hide/show control panel
- **P**: Pause/unpause animation

### Mouse Controls:
- **Left Click**: Add obstacle at clicked cell
- **Right Click**: Remove obstacle at clicked cell
- **Click and Drag**: Draw obstacles continuously

---

## 🐛 Common Questions

### Q: What is `self`?
**A:** `self` refers to the object itself. When you call `maze.add_obstacle(5, 10)`, `self` is the `maze` object.

### Q: What is `nonlocal`?
**A:** Used in nested functions to modify variables from the outer function:
```python
def outer():
    x = 5
    def inner():
        nonlocal x
        x = 10  # Modifies outer x
```

### Q: Why use `yield` instead of `return`?
**A:** `yield` creates a generator that can be paused and resumed. Perfect for animations!

### Q: What is `heapq`?
**A:** A priority queue - always gives you the smallest item first. Perfect for A* algorithm!

---

## 🚀 Next Steps for Learning

1. **Modify colors** - Change the RGB values
2. **Add new maze files** - Create your own mazes
3. **Change cell size** - Make cells bigger/smaller
4. **Add new controls** - Implement your own features
5. **Try different algorithms** - BFS, DFS, Dijkstra

---

## 📝 Summary

This project demonstrates:
- **Object-Oriented Programming** (Classes)
- **Algorithm Implementation** (A* search)
- **Game Development** (Pygame)
- **File I/O** (Reading maze files)
- **Event Handling** (Keyboard/Mouse)
- **Animation** (Step-by-step visualization)

**The Big Picture:**
1. Load a maze from a file
2. Use A* algorithm to find the best path
3. Display everything with Pygame
4. Allow user interaction
5. Animate the solution

---

## 💡 Tips for Beginners

1. **Start Small**: Understand one function at a time
2. **Print Statements**: Add `print()` to see what's happening
3. **Modify Values**: Change numbers and see what happens
4. **Read Error Messages**: They tell you what's wrong!
5. **Practice**: Try modifying the code yourself

---

**Happy Coding! 🎉**

If you have questions, try:
- Adding print statements to see values
- Reading Python documentation
- Experimenting with small changes

