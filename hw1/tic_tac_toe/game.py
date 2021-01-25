from random import randint


class Game:
    def __init__(self, size, humanX, humanO):
        self._size = size
        self._offset = self._size**2
        self._win_states = get_win_states(self._size)
        self._moveX_func = self._human_move_func if humanX else self._engine_move_func
        self._moveO_func = self._human_move_func if humanO else self._engine_move_func
        self._board = 0
        self._moveX = True
        self._human_move = None

    def set_human_move(self, move):
        self._human_move = move

    def make_move(self):
        move = self._moveX_func() if self._moveX else self._moveO_func()
        board = add_move(move, self._moveX, self._board, self._offset)

        if board is None:
            return None, None

        self._board = board
        char = 'X' if self._moveX else 'O'
        self._moveX = not self._moveX

        return move, char

    def get_outcome(self):
        return check_outcome(self._board, self._offset, self._win_states)

    def _human_move_func(self):
        human_move = self._human_move
        self._human_move = None
        return human_move

    def _engine_move_func(self):
        return randint(0, self._offset - 1)


def get_win_states(size):
    states = []
    for col in range(size):
        state = 1 << col
        for _ in range(size - 1):
            state <<= size
            state |= 1 << col
        states.append(state)

    mask = 2**size - 1
    for row in range(size):
        state = mask << (row * size)
        states.append(state)

    # TODO diagonals

    return states


def add_move(move, moveX, board, offset):
    if move is None:
        return None

    bit = 1 << move
    offset_bit = bit << offset
    if board & bit != 0 or board & offset_bit != 0:
        return None

    return board | bit if moveX else board | offset_bit


def check_outcome(board, offset, win_states):
    O_board = board >> offset
    for state in win_states:
        if board & state == state:
            return 1
        if O_board & state == state:
            return -1
    return 0 if is_full(board, offset) else None


def is_full(board, offset):
    count = 0
    while board != 0:
        count += board & 1
        board >>= 1
    return count == offset
