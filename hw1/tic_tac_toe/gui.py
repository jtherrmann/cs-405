import json
import os
import tkinter
from datetime import datetime, timezone
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

HISTORY_DIR = 'game-history'


# ----------------------------------------------------------------------
# Game wrapper
# ----------------------------------------------------------------------

class GameWrapper:
    def __init__(self):
        self.game: Optional[Game] = None
        self._debugOn = False

    def set_debug(self, debugOn):
        self._debugOn = debugOn

    def new_game(self, Xmover, Omover):
        self.game = Game(SIZE, Xmover=Xmover, Omover=Omover, debugOn=self._debugOn)
        reset_grid()
        timer()

    def stop_game(self):
        self.game = None
        reset_grid()


# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

root = tkinter.Tk()
canvas = tkinter.Canvas(root, bg=BG, width=CANVAS_SIZE, height=CANVAS_SIZE)
gamewrapper = GameWrapper()


# ----------------------------------------------------------------------
# Drawing functions
# ----------------------------------------------------------------------

def reset_grid():
    canvas.delete('all')
    draw_grid()


def draw_grid():
    for cell in range(SIZE):
        pos = cell * CELL_SIZE
        canvas.create_line(pos, 0, pos, CANVAS_SIZE, fill=FG)
        canvas.create_line(0, pos, CANVAS_SIZE, pos, fill=FG)


def draw_move(move, char):
    x, y = move_to_point(move)
    canvas.create_text(x, y, text=char, font='Mono 32', fill=FG)


# ----------------------------------------------------------------------
# Widget functions
# ----------------------------------------------------------------------

def click_handler(event):
    if gamewrapper.game:
        move = point_to_move(event.x, event.y)
        gamewrapper.game.set_human_move(move)


def new_game_command():
    def _new_game():
        window.destroy()
        gamewrapper.new_game(Xmover=Xmover.get(), Omover=Omover.get())

    window = tkinter.Toplevel()
    window.geometry('300x150')
    window.wm_title('New game')

    Xmover = tkinter.StringVar(window, value=Game.HUMAN)
    Omover = tkinter.StringVar(window, value=Game.RANDOM)

    Xmover_label = tkinter.Label(window, text='X player:')
    Omover_label = tkinter.Label(window, text='O player:')

    Xmover_menu = tkinter.OptionMenu(window, Xmover, *Game.move_funcs.keys())
    Omover_menu = tkinter.OptionMenu(window, Omover,  *Game.move_funcs.keys())

    button = tkinter.Button(window, text='Play', command=_new_game)

    Xmover_label.grid(row=0, column=0)
    Xmover_menu.grid(row=0, column=1)

    Omover_label.grid(row=1, column=0)
    Omover_menu.grid(row=1, column=1)

    button.grid(row=2, column=0)


def history_command():
    def _replay_game():
        name = selection.get()
        if name:
            replay_game(name)

    names = [name for name in os.listdir(HISTORY_DIR) if name.endswith('.json')]

    window = tkinter.Toplevel()
    window.wm_title('History')

    label = tkinter.Label(window, text='Game:')
    selection = tkinter.StringVar(window)
    menu = tkinter.OptionMenu(window, selection, *names)
    button = tkinter.Button(window, text='Replay', command=_replay_game)

    label.pack()
    menu.pack()
    button.pack()


def replay_game(name):
    gamewrapper.stop_game()
    with open(os.path.join(HISTORY_DIR, name), 'r') as f:
        summary = json.loads(f.read())
    print(summary)  # TODO: display in gui


# ----------------------------------------------------------------------
# Timer loop
# ----------------------------------------------------------------------

def timer():
    if gamewrapper.game is not None:
        outcome = make_move()
        if outcome is None:
            root.after(TIMER_MS, timer)
        else:
            print(f'Outcome: {outcome}')  # TODO: display in gui
            save_summary()


def make_move():
    move, char, outcome = gamewrapper.game.make_move()
    if move is not None:
        draw_move(move, char)
    return outcome


def save_summary():
    summary = json.dumps(gamewrapper.game.get_summary())

    if not os.path.isdir(HISTORY_DIR):
        os.mkdir(HISTORY_DIR)

    with open(os.path.join(HISTORY_DIR, datetime.now(timezone.utc).isoformat() + '.json'), 'w') as f:
        f.write(summary)


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

    canvas.bind('<Button-1>', click_handler)

    new_game_button = tkinter.Button(root, text='New game', command=new_game_command)
    history_button = tkinter.Button(root, text='History', command=history_command)

    canvas.pack()
    new_game_button.pack(side=tkinter.LEFT)
    history_button.pack(side=tkinter.LEFT)

    root.mainloop()
