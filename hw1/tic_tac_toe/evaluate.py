from . import core


def eval_board(board):
    return eval_turn(board) + eval_max_connected(board)


def eval_turn(board):
    turn = core.turn_bit(board)
    if turn:
        return -1
    return 1


def eval_max_connected(board):
    pieces, O_pieces = core.split_board(board)
    return max_connected(pieces) - max_connected(O_pieces)


def max_connected(pieces):
    # TODO don't count a sequence if it includes an enemy piece
    return max(core.count_bits(pieces & state) for state in core.WIN_STATES)
