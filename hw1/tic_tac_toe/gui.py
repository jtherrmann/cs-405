import json
import os
import tkinter
import tkinter.messagebox
from datetime import datetime, timezone
from random import randint

from . import core, debug


# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

CELL_SIZE = 100
CANVAS_SIZE = core.SIZE * CELL_SIZE

BG = 'black'
FG = 'white'

HISTORY_DIR = 'game-history'


# ----------------------------------------------------------------------
# Game
# ----------------------------------------------------------------------

class Game:
    HUMAN = 'Human'
    RANDOM = 'Random moves'

    move_funcs = {
        HUMAN: '_human_move_func',
        RANDOM: '_random_move_func'
    }

    def _get_move_func(self, name):
        return getattr(self, Game.move_funcs[name])

    def _human_move_func(self):
        if self._human_move is not None:
            human_move = self._human_move
            self._human_move = None
            if human_move in core.legal_moves(self._current_board()):
                return human_move

    def _random_move_func(self):
        moves = core.legal_moves(self._current_board())
        return moves[randint(0, len(moves) - 1)]

    def __init__(self):
        self._game_active = False
        self._Xmover = None
        self._Omover = None
        self._outcome = None
        self._human_move = None
        self._boards = []
        self._history_index = 0

        self._moveX_func = None
        self._moveO_func = None

    def _set_game_fields(self, game_active, Xmover, Omover, outcome, human_move, boards, history_index):
        self._game_active = game_active
        self._Xmover = Xmover
        self._Omover = Omover
        self._outcome = outcome
        self._human_move = human_move
        self._boards = boards
        self._history_index = history_index

        self._moveX_func = self._get_move_func(Xmover)
        self._moveO_func = self._get_move_func(Omover)

    def active(self):
        return self._game_active

    def handle_click(self, event):
        if self._history_index == len(self._boards) - 1:
            self._human_move = point_to_index(event.x, event.y)

    def inc_history_index(self):
        if self._history_index < len(self._boards) - 1:
            self._history_index += 1
            self._refresh_display()

    def dec_history_index(self):
        if self._history_index > 0:
            self._history_index -= 1
            self._refresh_display()

    def make_move(self):
        index = self._moveX_func() if core.turn_X(self._current_board()) else self._moveO_func()

        if index is not None:
            assert index in core.legal_moves(self._current_board())
            self._boards.append(core.add_move(index, self._current_board()))
            self._outcome = core.check_outcome(self._current_board(), core.WIN_STATES)
            self._history_index = len(self._boards) - 1
            self._refresh_display()

            if self._outcome is not None:
                self._game_active = False
                self._save_summary()

    def new_game(self, Xmover, Omover):
        self._set_game_fields(
            game_active=True,
            Xmover=Xmover,
            Omover=Omover,
            outcome=None,
            human_move=None,
            boards=[1],
            history_index=0
        )
        self._refresh_display()
        timer()

    def load_old_game(self, name):
        with open(os.path.join(HISTORY_DIR, name), 'r') as f:
            summary = json.loads(f.read())

        if summary['size'] == core.SIZE:
            self._set_game_fields(
                game_active=False,
                Xmover=summary['X player'],
                Omover=summary['O player'],
                outcome=summary['outcome'],
                human_move=None,
                boards=summary['history'],
                history_index=len(summary['history']) - 1
            )
            self._refresh_display()
        else:
            tkinter.messagebox.showerror(message='Selected game used a different board size')

    def _save_summary(self):
        summary = json.dumps(
            {'X player': self._Xmover,
             'O player': self._Omover,
             'outcome': self._outcome,
             'size': core.SIZE,
             'history': self._boards}
        )
        with open(os.path.join(HISTORY_DIR, datetime.now(timezone.utc).isoformat() + '.json'), 'w') as f:
            f.write(summary)

    def _current_board(self):
        return self._boards[-1]

    def _refresh_display(self):
        draw_board(self._boards[self._history_index])
        status_line['text'] = self._get_status()

    def _get_status(self):
        return f'{self._Xmover} (X) vs. {self._Omover} (O)\nResult: {self._outcome}\nMove: {self._history_index}'


# ----------------------------------------------------------------------
# Global objects
# ----------------------------------------------------------------------

root = tkinter.Tk()
canvas = tkinter.Canvas(root, bg=BG, width=CANVAS_SIZE, height=CANVAS_SIZE)
status_line = tkinter.Label(root)
game = Game()


# ----------------------------------------------------------------------
# Timer
# ----------------------------------------------------------------------

def timer():
    if game.active():
        game.make_move()
        root.after(50, timer)


# ----------------------------------------------------------------------
# Widget functions
# ----------------------------------------------------------------------

def new_game_command():
    def _new_game():
        window.destroy()
        game.new_game(Xmover=Xmover.get(), Omover=Omover.get())

    window = tkinter.Toplevel()
    window.geometry('300x150')
    window.wm_title('New game')

    Xmover = tkinter.StringVar(window, value=Game.HUMAN)
    Omover = tkinter.StringVar(window, value=Game.RANDOM)

    Xmover_label = tkinter.Label(window, text='X player:')
    Omover_label = tkinter.Label(window, text='O player:')

    Xmover_menu = tkinter.OptionMenu(window, Xmover, *Game.move_funcs.keys())
    Omover_menu = tkinter.OptionMenu(window, Omover, *Game.move_funcs.keys())

    button = tkinter.Button(window, text='Play', command=_new_game)

    Xmover_label.grid(row=0, column=0)
    Xmover_menu.grid(row=0, column=1)

    Omover_label.grid(row=1, column=0)
    Omover_menu.grid(row=1, column=1)

    button.grid(row=2, column=0)


def history_command():
    def _replay_game():
        window.destroy()
        game.load_old_game(selection.get())

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
# Drawing functions
# ----------------------------------------------------------------------

def draw_board(board):
    canvas.delete('all')
    draw_grid()
    draw_pieces(board)


def draw_grid():
    for cell in range(core.SIZE):
        pos = cell * CELL_SIZE
        canvas.create_line(pos, 0, pos, CANVAS_SIZE, fill=FG)
        canvas.create_line(0, pos, CANVAS_SIZE, pos, fill=FG)


def draw_pieces(board):
    # TODO move bitwise logic to core
    pieces, O_pieces = core.split_board(board)
    for i in range(core.OFFSET):
        if pieces & 1:
            assert not (O_pieces & 1)
            draw_piece(i, 'X')
        elif O_pieces & 1:
            draw_piece(i, 'O')
        pieces >>= 1
        O_pieces >>= 1


def draw_piece(index, char):
    x, y = index_to_point(index)
    canvas.create_text(x, y, text=char, font='Mono 32', fill=FG)


# ----------------------------------------------------------------------
# Coordinate conversion functions
# ----------------------------------------------------------------------

def point_to_index(x, y):
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return core.SIZE * row + col


def index_to_point(index):
    row, col = divmod(index, core.SIZE)
    return center_coord(col), center_coord(row)


def center_coord(row_or_col):
    return row_or_col * CELL_SIZE + CELL_SIZE // 2


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main(args):
    if args.debug:
        debug.print_win_states(core.WIN_STATES, core.SIZE)

    if not os.path.isdir(HISTORY_DIR):
        os.mkdir(HISTORY_DIR)

    root.title('Tic-tac-toe')
    root.resizable(False, False)

    canvas.bind('<Button-1>', game.handle_click)

    new_game_button = tkinter.Button(root, text='New game', command=new_game_command)
    history_button = tkinter.Button(root, text='History', command=history_command)
    history_dec_button = tkinter.Button(root, text='<-', command=game.dec_history_index)
    history_inc_button = tkinter.Button(root, text='->', command=game.inc_history_index)

    canvas.pack()
    status_line.pack()
    new_game_button.pack(side=tkinter.LEFT)
    history_button.pack(side=tkinter.LEFT)
    history_dec_button.pack(side=tkinter.LEFT)
    history_inc_button.pack(side=tkinter.LEFT)

    root.mainloop()
