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
        self.maze = Maze(rows, cols)
    
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
    
    def draw(self, path=None, vis=None, dead=None):
        self.screen.fill(WHITE)
        for i in range(self.rows):
            for j in range(self.cols):
                color = None
                if (i, j) == self.maze.start:
                    color = GREEN
                elif (i, j) == self.maze.end:
                    color = RED
                elif dead and (i, j) in dead:
                    color = BLUE
                elif path and (i, j) in path and (i, j) not in [self.maze.start, self.maze.end]:
                    color = RED
                elif vis and vis[i][j] and (i, j) not in [self.maze.start, self.maze.end]:
                    color = GRAY
                self.draw_cell(i, j, color)
        pygame.display.flip()
    
    def get_nb(self, row, col):
        n = []
        if row > 0 and not self.maze.vis[row-1][col]:
            n.append((row-1, col, 'n'))
        if row < self.rows - 1 and not self.maze.vis[row+1][col]:
            n.append((row+1, col, 's'))
        if col > 0 and not self.maze.vis[row][col-1]:
            n.append((row, col-1, 'w'))
        if col < self.cols - 1 and not self.maze.vis[row][col+1]:
            n.append((row, col+1, 'e'))
        return n
    
    def eat(self, r1, c1, r2, c2, d):
        if d == 'n':
            self.maze.north[r1][c1] = 0
        elif d == 's':
            self.maze.north[r2][c2] = 0
        elif d == 'w':
            self.maze.east[r1][c1-1] = 0
        elif d == 'e':
            self.maze.east[r1][c1] = 0
    
    def generate_stack(self, delay=None):
        for i in range(self.rows):
            for j in range(self.cols):
                self.maze.north[i][j] = 1
                self.maze.east[i][j] = 1
                self.maze.vis[i][j] = False
        
        sr = random.randint(0, self.rows-1)
        sc = random.randint(0, self.cols-1)
        stack = [(sr, sc)]
        self.maze.vis[sr][sc] = True
        
        if delay:
            if not delay():
                return False
        
        while stack:
            r, c = stack[-1]
            nb = self.get_nb(r, c)
            if nb:
                nr, nc, d = random.choice(nb)
                self.eat(r, c, nr, nc, d)
                self.maze.vis[nr][nc] = True
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
    
    def pick_start_end(self):
        self.maze.start = (random.randint(0, self.rows-1), 0)
        self.maze.east[self.maze.start[0]][0] = 0
        self.maze.end = (random.randint(0, self.rows-1), self.cols-1)
    
    def reset_vis(self):
        self.maze.vis = [[False for _ in range(self.cols)] for _ in range(self.rows)]
    
    def solve_backtrack(self, delay=None):
        stack = [(self.maze.start[0], self.maze.start[1], [])]
        self.maze.vis[self.maze.start[0]][self.maze.start[1]] = True
        self.maze.dead = []
        
        while stack:
            r, c, p = stack.pop()
            cur = p + [(r, c)]
            
            if delay:
                if not delay(cur, self.maze.vis, self.maze.dead):
                    return None
            
            if (r, c) == self.maze.end:
                self.maze.path = cur
                return cur
            
            dirs = ['n', 's', 'w', 'e']
            random.shuffle(dirs)
            
            for d in dirs:
                nr, nc = r, c
                ok = False
                if d == 'n' and r > 0 and self.maze.north[r][c] == 0:
                    nr, nc = r-1, c
                    ok = True
                elif d == 's' and r < self.rows-1 and self.maze.north[r+1][c] == 0:
                    nr, nc = r+1, c
                    ok = True
                elif d == 'w' and c > 0 and self.maze.east[r][c-1] == 0:
                    nr, nc = r, c-1
                    ok = True
                elif d == 'e' and c < self.cols-1 and self.maze.east[r][c] == 0:
                    nr, nc = r, c+1
                    ok = True
                
                if ok and not self.maze.vis[nr][nc]:
                    self.maze.vis[nr][nc] = True
                    stack.append((nr, nc, cur))
            
            has_unvisited = False
            for d in ['n', 's', 'w', 'e']:
                nr, nc = r, c
                ok = False
                if d == 'n' and r > 0 and self.maze.north[r][c] == 0:
                    nr, nc = r-1, c
                    ok = True
                elif d == 's' and r < self.rows-1 and self.maze.north[r+1][c] == 0:
                    nr, nc = r+1, c
                    ok = True
                elif d == 'w' and c > 0 and self.maze.east[r][c-1] == 0:
                    nr, nc = r, c-1
                    ok = True
                elif d == 'e' and c < self.cols-1 and self.maze.east[r][c] == 0:
                    nr, nc = r, c+1
                    ok = True
                if ok and not self.maze.vis[nr][nc]:
                    has_unvisited = True
                    break
            
            if not has_unvisited and (r, c) != self.maze.end and (r, c) not in self.maze.dead:
                self.maze.dead.append((r, c))
                if delay:
                    delay(cur, self.maze.vis, self.maze.dead)
        
        return None
    
    def animate_gen(self):
        def step():
            self.draw()
            self.clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return False
            return True
        
        self.generate_stack(step)
        self.draw()
    
    def animate_solve(self):
        self.maze.vis = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        sol = []
        
        def step(path, vis, dead):
            nonlocal sol
            sol = path
            self.draw(path, vis, dead)
            self.clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return False
            return True
        
        self.solve_backtrack(step)
        for _ in range(60):
            self.draw(sol, None, None)
            self.clock.tick(30)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return
    
    def wait_space(self):
        waiting = True
        while waiting and self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                    return False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        waiting = False
                    if e.key == pygame.K_ESCAPE:
                        self.running = False
                        return False
            self.clock.tick(30)
        return True
    
    def run(self):
        print("Press SPACE to generate maze")
        if not self.wait_space():
            return
        self.animate_gen()
        print("Press SPACE to solve maze")
        if not self.wait_space():
            return
        self.animate_solve()
        print("Done! Press ESC to quit")
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.running = False
            self.clock.tick(30)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game(21, 31)
    game.run()