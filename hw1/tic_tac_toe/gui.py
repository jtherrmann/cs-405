import tkinter
from typing import Optional

from .game import Game


# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

SIZE = 4
CELL_SIZE = 100
CANVAS_SIZE = SIZE * CELL_SIZE

BG = 'black'
FG = 'white'

TIMER_MS = 50


# ----------------------------------------------------------------------
# Game wrapper
# ----------------------------------------------------------------------

class GameWrapper:
    def __init__(self):
        self.game: Optional[Game] = None
        self._debugOn = False

    def set_debug(self, debugOn):
        self._debugOn = debugOn

    def new_game(self):
        self.game = Game(SIZE, humanX=True, humanO=True, debugOn=self._debugOn)
        canvas.delete('all')
        draw_grid()
        timer()


# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

root = tkinter.Tk()
canvas = tkinter.Canvas(root, bg=BG, width=CANVAS_SIZE, height=CANVAS_SIZE)
gamewrapper = GameWrapper()


# ----------------------------------------------------------------------
# Drawing functions
# ----------------------------------------------------------------------

def draw_grid():
    for cell in range(SIZE):
        pos = cell * CELL_SIZE
        canvas.create_line(pos, 0, pos, CANVAS_SIZE, fill=FG)
        canvas.create_line(0, pos, CANVAS_SIZE, pos, fill=FG)


def draw_move(x, y, char):
    canvas.create_text(x, y, text=char, font='Mono 32', fill=FG)


# ----------------------------------------------------------------------
# Event handlers
# ----------------------------------------------------------------------

def click_handler(event):
    if gamewrapper.game:
        move = point_to_move(event.x, event.y)
        gamewrapper.game.set_human_move(move)


# ----------------------------------------------------------------------
# Timer loop
# ----------------------------------------------------------------------

def timer():
    outcome = make_move()
    if outcome is None:
        root.after(TIMER_MS, timer)
    else:
        print(f'Outcome: {outcome}')  # TODO: display in gui


def make_move():
    move, char = gamewrapper.game.make_move()
    if move is not None:
        x, y = move_to_point(move)
        draw_move(x, y, char)
        return gamewrapper.game.get_outcome()
    return None


# ----------------------------------------------------------------------
# Coordinate conversion functions
# ----------------------------------------------------------------------

def point_to_move(x, y):
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return SIZE * row + col


def move_to_point(move):
    row, col = divmod(move, SIZE)
    return center_coord(col), center_coord(row)


def center_coord(row_or_col):
    return row_or_col * CELL_SIZE + CELL_SIZE // 2


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main(args):
    gamewrapper.set_debug(args.debug)
    root.title('Tic-tac-toe')
    root.bind('<Button-1>', click_handler)
    button = tkinter.Button(root, text='New game', command=gamewrapper.new_game)
    canvas.pack()
    button.pack()
    root.mainloop()
