import json
import os
import tkinter
import tkinter.messagebox
from datetime import datetime, timezone
from typing import Optional

from .game import Game


# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

SIZE = 4
OFFSET = SIZE * SIZE
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
        self._game: Optional[Game] = None
        self._Xmover = None
        self._Omover = None
        self._outcome = None
        self._boards = []
        self._history_index = 0
        self._debugOn = False

    def set_debug(self, debugOn):
        self._debugOn = debugOn

    def inc_history_index(self):
        if self._history_index < len(self._boards) - 1:
            self._history_index += 1
            self._draw_board()

    def dec_history_index(self):
        if self._history_index > 0:
            self._history_index -= 1
            self._draw_board()

    def make_move(self):
        if self._game.make_move():
            self._boards.append(self._game.get_board())
            self._history_index = len(self._boards) - 1
            self._outcome = self._game.get_outcome()
            self._draw_board()

            if self._outcome is not None:
                self._game = None
                self._save_summary()

    def new_game(self, Xmover, Omover):
        self._boards = [0]
        self._history_index = 0
        self._Xmover = Xmover
        self._Omover = Omover
        self._outcome = None
        self._game = Game(SIZE, Xmover=Xmover, Omover=Omover, debugOn=self._debugOn)
        self._draw_board()
        timer()

    def load_old_game(self, name):
        with open(os.path.join(HISTORY_DIR, name), 'r') as f:
            summary = json.loads(f.read())

        self._game = None
        self._Xmover = summary['X player']
        self._Omover = summary['O player']
        self._outcome = summary['outcome']
        self._boards = summary['history']
        self._history_index = len(self._boards) - 1
        self._draw_board()

    def has_game(self):
        return self._game is not None

    def handle_click(self, event):
        if self.has_game():
            index = point_to_index(event.x, event.y)
            self._game.set_human_move(index)

    def _draw_board(self):
        draw_board(self._boards[self._history_index], OFFSET)
        status_line['text'] = self._get_status()

    def _get_status(self):
        return f'{self._Xmover} (X) vs. {self._Omover} (O)\nResult: {self._outcome}\nMove: {self._history_index}'

    def _save_summary(self):
        summary = json.dumps(
            {'X player': self._Xmover, 'O player': self._Omover, 'outcome': self._outcome, 'history': self._boards}
        )
        with open(os.path.join(HISTORY_DIR, datetime.now(timezone.utc).isoformat() + '.json'), 'w') as f:
            f.write(summary)


# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

root = tkinter.Tk()
canvas = tkinter.Canvas(root, bg=BG, width=CANVAS_SIZE, height=CANVAS_SIZE)
status_line = tkinter.Label(root)
gamewrapper = GameWrapper()


# ----------------------------------------------------------------------
# Drawing functions
# ----------------------------------------------------------------------


def draw_board(board, offset):
    canvas.delete('all')
    draw_grid()
    draw_pieces(board, offset)


def draw_grid():
    for cell in range(SIZE):
        pos = cell * CELL_SIZE
        canvas.create_line(pos, 0, pos, CANVAS_SIZE, fill=FG)
        canvas.create_line(0, pos, CANVAS_SIZE, pos, fill=FG)


def draw_pieces(board, offset):
    O_board = board >> offset
    for i in range(offset):
        if board & 1:
            draw_piece(i, 'X')
        if O_board & 1:
            draw_piece(i, 'O')
        board >>= 1
        O_board >>= 1


def draw_piece(index, char):
    x, y = index_to_point(index)
    canvas.create_text(x, y, text=char, font='Mono 32', fill=FG)


# ----------------------------------------------------------------------
# Widget functions
# ----------------------------------------------------------------------

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
        window.destroy()
        gamewrapper.load_old_game(selection.get())

    names = sorted((name for name in os.listdir(HISTORY_DIR) if name.endswith('.json')), reverse=True)

    if names:
        window = tkinter.Toplevel()
        window.wm_title('History')

        label = tkinter.Label(window, text='Game:')
        selection = tkinter.StringVar(window, value=names[0])
        menu = tkinter.OptionMenu(window, selection, *names)
        button = tkinter.Button(window, text='Replay', command=_replay_game)

        label.pack()
        menu.pack()
        button.pack()
    else:
        tkinter.messagebox.showerror(message='No previous games')


# ----------------------------------------------------------------------
# Timer loop
# ----------------------------------------------------------------------

def timer():
    if gamewrapper.has_game():
        gamewrapper.make_move()
        root.after(TIMER_MS, timer)


# ----------------------------------------------------------------------
# Coordinate conversion functions
# ----------------------------------------------------------------------

def point_to_index(x, y):
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return SIZE * row + col


def index_to_point(index):
    row, col = divmod(index, SIZE)
    return center_coord(col), center_coord(row)


def center_coord(row_or_col):
    return row_or_col * CELL_SIZE + CELL_SIZE // 2


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main(args):
    gamewrapper.set_debug(args.debug)

    if not os.path.isdir(HISTORY_DIR):
        os.mkdir(HISTORY_DIR)

    root.title('Tic-tac-toe')
    root.resizable(False, False)

    canvas.bind('<Button-1>', gamewrapper.handle_click)

    new_game_button = tkinter.Button(root, text='New game', command=new_game_command)
    history_button = tkinter.Button(root, text='History', command=history_command)
    history_dec_button = tkinter.Button(root, text='<-', command=gamewrapper.dec_history_index)
    history_inc_button = tkinter.Button(root, text='->', command=gamewrapper.inc_history_index)

    canvas.pack()
    status_line.pack()
    new_game_button.pack(side=tkinter.LEFT)
    history_button.pack(side=tkinter.LEFT)
    history_dec_button.pack(side=tkinter.LEFT)
    history_inc_button.pack(side=tkinter.LEFT)

    root.mainloop()
