import tkinter

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
# Setup
# ----------------------------------------------------------------------

root = tkinter.Tk()
canvas = tkinter.Canvas(root, bg=BG, width=CANVAS_SIZE, height=CANVAS_SIZE)


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

def click_handler(game):

    def handler(event):
        move = point_to_move(event.x, event.y)
        game.set_human_move(move)

    return handler


# ----------------------------------------------------------------------
# Timer loop
# ----------------------------------------------------------------------

def start_timer(game):

    def timer():
        outcome = make_move(game)
        if outcome is None:
            root.after(TIMER_MS, timer)
        else:
            print(f'Outcome: {outcome}')  # TODO: display in gui

    timer()


def make_move(game):
    move, char = game.make_move()
    if move is not None:
        x, y = move_to_point(move)
        draw_move(x, y, char)
        return game.get_outcome()
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
    root.title('Tic-tac-toe')
    canvas.pack()
    draw_grid()
    game = Game(SIZE, humanX=True, humanO=True, debugOn=args.debug)
    root.bind('<Button-1>', click_handler(game))
    start_timer(game)
    root.mainloop()
