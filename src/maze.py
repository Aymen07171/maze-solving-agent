# Maze loader & random generator

import random

class Maze:
    def __init__(self, grid, start=None, goal=None):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0
        self.start = start
        self.goal = goal

    @classmethod
    def from_file(cls, path):
        lines = []
        with open(path, 'r', encoding='utf-8') as f:
            for ln in f:
                if ln.strip() == '':
                    continue
                lines.append(ln.rstrip('\n'))

        if not lines:
            raise ValueError("Maze file empty")

        width = max(len(l) for l in lines)
        grid = []
        start = None
        goal = None

        for r, line in enumerate(lines):
            row = []
            for c in range(width):
                ch = line[c] if c < len(line) else '#'
                if ch in ('#', '1'):
                    row.append(1)
                elif ch in ('S', 's'):
                    row.append(0)
                    start = (r, c)
                elif ch in ('G', 'g'):
                    row.append(0)
                    goal = (r, c)
                else:
                    row.append(0)
            grid.append(row)

        if start is None:
            start = (0, 0)
        if goal is None:
            goal = (len(grid) - 1, len(grid[0]) - 1)

        return cls(grid, start, goal)

    def in_bounds(self, pos):
        r, c = pos
        return 0 <= r < self.height and 0 <= c < self.width

    def passable(self, pos):
        r, c = pos
        return self.grid[r][c] == 0

    def neighbors(self, pos):
        r, c = pos
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if self.in_bounds((nr, nc)) and self.passable((nr, nc)):
                yield (nr, nc)

    def change_dimensions(self, new_width, new_height):
        """Change the maze dimensions, resizing the grid"""
        old_height, old_width = self.height, self.width
        new_grid = []
        
        for r in range(new_height):
            row = []
            for c in range(new_width):
                if r < old_height and c < old_width:
                    row.append(self.grid[r][c])
                else:
                    row.append(1)  # Fill new cells with walls
            new_grid.append(row)
        
        self.grid = new_grid
        self.height = new_height
        self.width = new_width
        
        # Ensure start and goal are within bounds
        if self.start:
            sr, sc = self.start
            if sr >= new_height or sc >= new_width:
                self.start = (0, 0)
        
        if self.goal:
            gr, gc = self.goal
            if gr >= new_height or gc >= new_width:
                self.goal = (new_height - 1, new_width - 1)

    def change_goal(self, new_goal):
        """Change the goal position"""
        r, c = new_goal
        if self.in_bounds((r, c)) and self.passable((r, c)):
            self.goal = (r, c)
            return True
        return False

    def add_obstacle(self, row, col):
        """Add an obstacle (wall) at the specified position"""
        if self.in_bounds((row, col)):
            # Don't add obstacle at start or goal
            if (row, col) != self.start and (row, col) != self.goal:
                self.grid[row][col] = 1
                return True
        return False

    def remove_obstacle(self, row, col):
        """Remove an obstacle (wall) at the specified position"""
        if self.in_bounds((row, col)):
            self.grid[row][col] = 0
            return True
        return False

    def add_random_obstacles(self, count):
        """Add random obstacles (walls) to the maze"""
        added = 0
        attempts = 0
        max_attempts = count * 10
        
        while added < count and attempts < max_attempts:
            r = random.randint(0, self.height - 1)
            c = random.randint(0, self.width - 1)
            if self.grid[r][c] == 0 and (r, c) != self.start and (r, c) != self.goal:
                self.grid[r][c] = 1
                added += 1
            attempts += 1
        return added

    def remove_random_obstacles(self, count):
        """Remove random obstacles (walls) from the maze"""
        removed = 0
        attempts = 0
        max_attempts = count * 10
        
        # Get all wall positions
        walls = []
        for r in range(self.height):
            for c in range(self.width):
                if self.grid[r][c] == 1:
                    walls.append((r, c))
        
        if not walls:
            return 0
        
        random.shuffle(walls)
        for r, c in walls[:min(count, len(walls))]:
            self.grid[r][c] = 0
            removed += 1
        
        return removed

    def reset_to_initial(self, initial_grid, initial_start, initial_goal):
        """Reset the maze to its initial state"""
        # Deep copy the initial grid
        self.grid = [row[:] for row in initial_grid]
        self.height = len(initial_grid)
        self.width = len(initial_grid[0]) if self.height > 0 else 0
        self.start = initial_start
        self.goal = initial_goal