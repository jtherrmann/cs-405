from . import core
from .evaluate import eval_board


def minimax(board, depth=5, get_val=True):
    outcome = core.check_outcome(board)
    if outcome is not None:
        return outcome

    if depth == 0:
        return eval_board(board)

    moves = core.legal_moves(board)
    vals = [minimax(core.add_move(index, board), depth - 1) for index in moves]

    result = min(vals) if core.turn_bit(board) else max(vals)
    if get_val:
        return result

    return moves[vals.index(result)]
