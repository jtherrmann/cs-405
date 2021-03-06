import unittest
from random import randint

from tic_tac_toe import core, minimax


DEPTH = 4


class TestMinimax(unittest.TestCase):

    def test_minimax(self):
        board = core.EMPTY_BOARD
        self._test_minimax(board)

        for _ in range(core.OFFSET):
            children = core.get_children(board)
            board = children[randint(0, len(children) - 1)]
            self._test_minimax(board)

    def _test_minimax(self, board):
        val = minimax.minimax(minimax.Node(board), minimax.Stats(), depth=DEPTH)
        self.assertEqual(minimax.test_minimax(board, DEPTH), val)
        # noinspection PyUnreachableCode
        if __debug__:
            print(f'Val: {val}')


if __name__ == '__main__':
    unittest.main()
