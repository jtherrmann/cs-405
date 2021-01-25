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

        self._Xmover = tkinter.StringVar(root)
        self._Omover = tkinter.StringVar(root)

        self._Xmover.set(Game.HUMAN)
        self._Omover.set(Game.RANDOM)

        self._debugOn = False

    def set_debug(self, debugOn):
        self._debugOn = debugOn

    def new_game(self):
        self.game = Game(SIZE, Xmover=self._Xmover.get(), Omover=self._Omover.get(), debugOn=self._debugOn)
        canvas.delete('all')
        draw_grid()
        timer()

    def new_game_options(self):
        window = tkinter.Toplevel()
        window.geometry('300x150')
        window.wm_title('Options')

        Xmover_label = tkinter.Label(window, text='X player:')
        Omover_label = tkinter.Label(window, text='O player:')

        Xmover_menu = tkinter.OptionMenu(window, self._Xmover, *Game.move_funcs.keys())
        Omover_menu = tkinter.OptionMenu(window, self._Omover,  *Game.move_funcs.keys())

        close_button = tkinter.Button(window, text='Close', command=window.destroy)

        Xmover_label.grid(row=0, column=0)
        Xmover_menu.grid(row=0, column=1)

        Omover_label.grid(row=1, column=0)
        Omover_menu.grid(row=1, column=1)

        close_button.grid(row=2, column=0)


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


def draw_move(move, char):
    x, y = move_to_point(move)
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
    move, char, outcome = gamewrapper.game.make_move()
    if move is not None:
        draw_move(move, char)
    return outcome


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
    root.resizable(False, False)
    root.bind('<Button-1>', click_handler)

    new_game_button = tkinter.Button(root, text='New game', command=gamewrapper.new_game)
    options_button = tkinter.Button(root, text='Options', command=gamewrapper.new_game_options)

    canvas.pack()
    new_game_button.pack(side=tkinter.LEFT)
    options_button.pack(side=tkinter.LEFT)

    root.mainloop()
