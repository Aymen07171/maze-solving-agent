# Maze loader & random generator

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