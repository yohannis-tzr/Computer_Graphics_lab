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