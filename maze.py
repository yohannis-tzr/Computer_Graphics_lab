import pygame
import random
import sys
from collections import deque

CELL_SIZE = 20
WALL_THICK = 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

class Maze:
    def __init__(self, rows, cols, extra_walls=False):
        self.rows = rows
        self.cols = cols
        self.extra_walls = extra_walls
        self.north = [[1 for _ in range(cols)] for _ in range(rows)]
        self.east = [[1 for _ in range(cols)] for _ in range(rows)]
        self.vis = [[False for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.end = None
        self.path = []
        self.dead = []

class Game:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cell = 20
        self.w = cols * 20 + 1
        self.h = rows * 20 + 1
        pygame.init()
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Maze")
        self.clock = pygame.time.Clock()
        self.running = True
        self.maze = None
    
    def draw_cell(self, r, c, color=None):
        x = c * self.cell
        y = r * self.cell
        if color:
            pygame.draw.rect(self.screen, color, (x, y, self.cell, self.cell))
        if self.maze.north[r][c]:
            pygame.draw.line(self.screen, BLACK, (x, y), (x + self.cell, y), 2)
        if self.maze.east[r][c]:
            pygame.draw.line(self.screen, BLACK, (x + self.cell, y), (x + self.cell, y + self.cell), 2)
        if c == 0:
            pygame.draw.line(self.screen, BLACK, (x, y), (x, y + self.cell), 2)
        if r == self.rows - 1:
            pygame.draw.line(self.screen, BLACK, (x, y + self.cell), (x + self.cell, y + self.cell), 2)
        def get_nb(self, row, col):
        n = []
        if row > 0 and not self.vis[row-1][col]:
            n.append((row-1, col, 'n'))
        if row < self.rows - 1 and not self.vis[row+1][col]:
            n.append((row+1, col, 's'))
        if col > 0 and not self.vis[row][col-1]:
            n.append((row, col-1, 'w'))
        if col < self.cols - 1 and not self.vis[row][col+1]:
            n.append((row, col+1, 'e'))
        return n
    
    def eat(self, r1, c1, r2, c2, d):
        if d == 'n':
            self.north[r1][c1] = 0
        elif d == 's':
            self.north[r2][c2] = 0
        elif d == 'w':
            self.east[r1][c1-1] = 0
        elif d == 'e':
            self.east[r1][c1] = 0
    
    def generate_stack(self, delay=None):
        for i in range(self.rows):
            for j in range(self.cols):
                self.north[i][j] = 1
                self.east[i][j] = 1
                self.vis[i][j] = False
        
        sr = random.randint(0, self.rows-1)
        sc = random.randint(0, self.cols-1)
        stack = [(sr, sc)]
        self.vis[sr][sc] = True
        
        if delay:
            if not delay():
                return False
        
        while stack:
            r, c = stack[-1]
            nb = self.get_nb(r, c)
            if nb:
                nr, nc, d = random.choice(nb)
                self.eat(r, c, nr, nc, d)
                self.vis[nr][nc] = True
                stack.append((nr, nc))
                if delay:
                    if not delay():
                        return False
            else:
                stack.pop()
                if delay:
                    if not delay():
                        return False
        
        self.pick_start_end()
        self.reset_vis()
        return True
    
    def generate_queue(self, delay=None):
        for i in range(self.rows):
            for j in range(self.cols):
                self.north[i][j] = 1
                self.east[i][j] = 1
                self.vis[i][j] = False
        
        sr = random.randint(0, self.rows-1)
        sc = random.randint(0, self.cols-1)
        queue = deque()
        queue.append((sr, sc))
        self.vis[sr][sc] = True
        
        if delay:
            if not delay():
                return False
        
        while queue:
            r, c = queue.popleft()
            nb = self.get_nb(r, c)
            if nb:
                nr, nc, d = random.choice(nb)
                self.eat(r, c, nr, nc, d)
                self.vis[nr][nc] = True
                queue.append((nr, nc))
                if delay:
                    if not delay():
                        return False
        
        self.pick_start_end()
        self.reset_vis()
        return True
    
    def pick_start_end(self):
        self.start = (random.randint(0, self.rows-1), 0)
        self.east[self.start[0]][0] = 0
        self.end = (random.randint(0, self.rows-1), self.cols-1)
    
    def reset_vis(self):
        self.vis = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        def add_cycles_targeting_end(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < 0.05:
                    if i > 0 and self.north[i][j] == 1:
                        self.north[i][j] = 0
                if random.random() < 0.05:
                    if j < self.cols - 1 and self.east[i][j] == 1:
                        self.east[i][j] = 0
        
        end_r, end_c = self.end if self.end else (self.rows//2, self.cols-1)
        for _ in range(3):
            r = max(0, min(self.rows-1, end_r + random.randint(-2, 2)))
            c = max(0, min(self.cols-1, end_c + random.randint(-2, 2)))
            if r > 0 and self.north[r][c] == 1:
                self.north[r][c] = 0
            if c < self.cols - 1 and self.east[r][c] == 1:
                self.east[r][c] = 0
    
    def solve_backtrack(self, delay=None):
        stack = [(self.start[0], self.start[1], [])]
        self.vis[self.start[0]][self.start[1]] = True
        self.dead = []
        
        while stack:
            r, c, p = stack.pop()
            cur = p + [(r, c)]
            
            if delay:
                if not delay(cur, self.vis, self.dead):
                    return None
            
            if (r, c) == self.end:
                self.path = cur
                return cur
            
            dirs = ['n', 's', 'w', 'e']
            random.shuffle(dirs)
            
            for d in dirs:
                nr, nc = r, c
                ok = False
                if d == 'n' and r > 0 and self.north[r][c] == 0:
                    nr, nc = r-1, c
                    ok = True
                elif d == 's' and r < self.rows-1 and self.north[r+1][c] == 0:
                    nr, nc = r+1, c
                    ok = True
                elif d == 'w' and c > 0 and self.east[r][c-1] == 0:
                    nr, nc = r, c-1
                    ok = True
                elif d == 'e' and c < self.cols-1 and self.east[r][c] == 0:
                    nr, nc = r, c+1
                    ok = True
                
                if ok and not self.vis[nr][nc]:
                    self.vis[nr][nc] = True
                    stack.append((nr, nc, cur))
            
            has_unvisited = False
            for d in ['n', 's', 'w', 'e']:
                nr, nc = r, c
                ok = False
                if d == 'n' and r > 0 and self.north[r][c] == 0:
                    nr, nc = r-1, c
                    ok = True
                elif d == 's' and r < self.rows-1 and self.north[r+1][c] == 0:
                    nr, nc = r+1, c
                    ok = True
                elif d == 'w' and c > 0 and self.east[r][c-1] == 0:
                    nr, nc = r, c-1
                    ok = True
                elif d == 'e' and c < self.cols-1 and self.east[r][c] == 0:
                    nr, nc = r, c+1
                    ok = True
                if ok and not self.vis[nr][nc]:
                    has_unvisited = True
                    break
            
            if not has_unvisited and (r, c) != self.end and (r, c) not in self.dead:
                self.dead.append((r, c))
                if delay:
                    delay(cur, self.vis, self.dead)
        
        return None
    
    def solve_shoulder(self, delay=None):
        r, c = self.start
        facing = 'e'
        path = [(r, c)]
        visited = set()
        visited.add((r, c))
        stuck = 0
        
        while (r, c) != self.end and stuck < 5000:
            if delay:
                if not delay(path, visited, []):
                    return None
            
            order = ['left', 'forward', 'right', 'back']
            
            for turn in order:
                if facing == 'n':
                    if turn == 'left':
                        dr, dc, new_facing = 0, -1, 'w'
                    elif turn == 'forward':
                        dr, dc, new_facing = -1, 0, 'n'
                    elif turn == 'right':
                        dr, dc, new_facing = 0, 1, 'e'
                    else:
                        dr, dc, new_facing = 1, 0, 's'
                elif facing == 's':
                    if turn == 'left':
                        dr, dc, new_facing = 0, 1, 'e'
                    elif turn == 'forward':
                        dr, dc, new_facing = 1, 0, 's'
                    elif turn == 'right':
                        dr, dc, new_facing = 0, -1, 'w'
                    else:
                        dr, dc, new_facing = -1, 0, 'n'
                elif facing == 'w':
                    if turn == 'left':
                        dr, dc, new_facing = 1, 0, 's'
                    elif turn == 'forward':
                        dr, dc, new_facing = 0, -1, 'w'
                    elif turn == 'right':
                        dr, dc, new_facing = -1, 0, 'n'
                    else:
                        dr, dc, new_facing = 0, 1, 'e'
                else:
                    if turn == 'left':
                        dr, dc, new_facing = -1, 0, 'n'
                    elif turn == 'forward':
                        dr, dc, new_facing = 0, 1, 'e'
                    elif turn == 'right':
                        dr, dc, new_facing = 1, 0, 's'
                    else:
                        dr, dc, new_facing = 0, -1, 'w'
                
                nr, nc = r + dr, c + dc
                
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    blocked = False
                    if new_facing == 'n' and self.north[nr][nc] == 1:
                        blocked = True
                    elif new_facing == 's' and self.north[r][c] == 1:
                        blocked = True
                    elif new_facing == 'w' and self.east[nr][nc-1] == 1:
                        blocked = True
                    elif new_facing == 'e' and self.east[r][c] == 1:
                        blocked = True
                    
                    if not blocked:
                        r, c, facing = nr, nc, new_facing
                        if (r, c) not in path:
                            path.append((r, c))
                        stuck = 0
                        break
            else:
                stuck += 1
        
        self.path = path
        return path if (r, c) == self.end else None