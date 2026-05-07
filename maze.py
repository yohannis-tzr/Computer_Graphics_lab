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