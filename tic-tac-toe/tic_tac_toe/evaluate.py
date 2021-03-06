# Jake Herrmann
# CS 405
#
# evaluate.py
# Tic-tac-toe board evaluation.

from . import core


# ----------------------------------------------------------------------
# Main eval function
# ----------------------------------------------------------------------

def eval_board(board):
    return eval_turn(board) + eval_max_connected(board)


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------

def eval_turn(board):
    return -1 if core.turn_bit(board) else 1


def eval_max_connected(board):
    pieces, O_pieces = core.split_board(board)
    return max_connected(pieces, O_pieces) - max_connected(O_pieces, pieces)


def max_connected(pieces, enemy_pieces):
    return max(count_connected(pieces, enemy_pieces, state) for state in core.WIN_STATES)


def count_connected(pieces, enemy_pieces, win_state):
    count = core.count_bits(pieces & win_state)
    if not (enemy_pieces & win_state):
        return count
    return 0
