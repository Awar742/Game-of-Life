from nodebox.graphics import *
import random

CELL_SIZE = 10
GRID_WIDTH = 50
GRID_HEIGHT = 50

A = set()

def neighbours(x, y):
    O = {(x+dx, y+dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)}
    return {(a.x, a.y) for a in A if (a.x, a.y) in O}

def exist(x, y):
    return any((a.x, a.y) == (x, y) for a in A)

class CA:
    def __init__(self, x, y, live=True):
        self.x = x
        self.y = y
        self.live = live

    def draw(self):
        fill(self.y / float(GRID_HEIGHT), 0, self.x / float(GRID_WIDTH), 1)
        rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    def rule(self):
        x, y = self.x, self.y
        if (x in range(10, 15) and y == 30) or \
           (x in range(15, 20) and y == 20) or \
           (x in range(25, 28) and y == 10):
            return set()

        possible_moves = [(x + dx, y - 1) for dx in [-2, -1, 0, 1, 2]]
        for nx, ny in possible_moves:
            if 0 < nx < GRID_WIDTH and 0 < ny < GRID_HEIGHT and not exist(nx, ny):
                self.live = False
                return {(nx, ny)}

        return set()

def drawGrid():
    stroke(0, 0.1)
    for i in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
        line(i, 0, i, GRID_HEIGHT * CELL_SIZE)
        line(0, i, GRID_WIDTH * CELL_SIZE, i)

def draw(canvas):
    global step, pause
    if canvas.keys.char == " ":
        pause = not pause

    if canvas.mouse.button == LEFT:
        x, y = canvas.mouse.x // CELL_SIZE, canvas.mouse.y // CELL_SIZE
        if not exist(x, y):
            A.add(CA(x, y))

    canvas.clear()
    drawGrid()
    text(f"Step {step}\n\nCells {len(A)}", GRID_WIDTH * CELL_SIZE + 10, 450)

    for a in A:
        a.draw()

    if canvas.frame % 2 == 0 and not pause:
        step += 1
        new_cells = set()
        for a in list(A):
            new_cells.update(a.rule())

        A.difference_update({a for a in A if not a.live})

        for i, j in new_cells:
            if 0 < i < GRID_WIDTH and 0 < j < GRID_HEIGHT:
                A.add(CA(i, j))

A.update({CA(10, 10), CA(11, 10), CA(12, 10)})
step = 0
pause = False
canvas.size = GRID_WIDTH * CELL_SIZE + 150, GRID_HEIGHT * CELL_SIZE
canvas.run(draw)
