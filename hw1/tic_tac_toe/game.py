from random import randint


class Game:
    def __init__(self, size, humanX, humanO):
        self._cell_count = size**2
        self._moveX_func = self._human_move_func if humanX else self._engine_move_func
        self._moveO_func = self._human_move_func if humanO else self._engine_move_func
        self._game = 0
        self._moveX = True
        self._human_move = None

    def set_human_move(self, move):
        self._human_move = move

    def make_move(self):
        move = self._moveX_func() if self._moveX else self._moveO_func()
        game = self._add_move(move, self._moveX, self._game, self._cell_count)

        if game is None:
            return None, None

        self._game = game
        char = 'X' if self._moveX else 'O'
        self._moveX = not self._moveX

        return move, char

    def _human_move_func(self):
        human_move = self._human_move
        self._human_move = None
        return human_move

    def _engine_move_func(self):
        return randint(0, self._cell_count - 1)

    @staticmethod
    def _add_move(move, moveX, game, offset):
        if move is None:
            return None

        bit = 1 << move
        offset_bit = bit << offset
        if game & bit != 0 or game & offset_bit != 0:
            return None

        return game | bit if moveX else game | offset_bit
