import unittest
from random import randint

from tic_tac_toe import core, search


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
        node = search.Node(board)
        search.minimax(node, search.Stats(), depth=DEPTH)
        self.assertEqual(search.test_minimax(board, DEPTH), node.get_val())
        # noinspection PyUnreachableCode
        if __debug__:
            print(f'Val: {node.get_val()}')


if __name__ == '__main__':
    unittest.main()
