Maze Generator & Solver

Overview
This program generates a random maze and finds a path from the left edge (green) to the right edge (red) using a stack-based DFS backtracking algorithm.

How It Works

**Generation (Stack-based DFS "Mouse" Logic)**
- Mouse starts in a random cell
- Eats through walls to unvisited neighbors
- Pushes current cell onto a stack
- When trapped, pops from stack to backtrack
- Repeats until all cells are visited

**Solving**
- Red dot = current path
- Blue cells = dead ends
- Backtracking finds the exit

Data Structure
- `northWall[r][c]` - 1 = wall exists, 0 = wall eaten
- `eastWall[r][c]` - 1 = wall exists, 0 = wall eaten

Controls
| Key | Action |
|-----|--------|
| SPACE | Generate / Solve |
| ESC | Exit |

