from random import randint

from . import debug


class Game:
    HUMAN = 'Human'
    RANDOM = 'Random moves'

    move_funcs = {
        HUMAN: '_human_move_func',
        RANDOM: '_random_move_func'
    }

    def _get_move_func(self, name):
        return getattr(self, Game.move_funcs[name])

    def __init__(self, size, Xmover, Omover, debugOn):
        self._debugOn = debugOn

        self._size = size
        self._offset = self._size * self._size
        self._win_states = get_win_states(self._size)

        self._moveX_func = self._get_move_func(Xmover)
        self._moveO_func = self._get_move_func(Omover)

        self._moveX = True
        self._human_move = None

        self._board = 0
        self._outcome = None

        if self._debugOn:
            debug.print_win_states(self._win_states, self._size)

    def set_human_move(self, index):
        self._human_move = index

    def get_board(self):
        return self._board

    def get_outcome(self):
        return self._outcome

    def make_move(self):
        index = self._moveX_func() if self._moveX else self._moveO_func()
        board = add_move(index, self._moveX, self._board, self._offset)

        if board is not None:
            self._board = board
            self._outcome = check_outcome(self._board, self._offset, self._win_states)
            self._moveX = not self._moveX
            return True
        return False

    def _human_move_func(self):
        human_move = self._human_move
        self._human_move = None
        return human_move

    def _random_move_func(self):
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


def add_move(index, moveX, board, offset):
    if index is None:
        return None

    bit = 1 << index
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
