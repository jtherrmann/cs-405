from dataclasses import dataclass
from operator import lt, gt
from time import time
from typing import List, Any

from . import core
from .evaluate import eval_board


class Tree:

    def __init__(self):
        self._root = Node(board=core.EMPTY_BOARD)

    def get_move(self, board):
        self._update_root(board)

        # noinspection PyUnreachableCode
        if __debug__:
            # noinspection PyUnusedLocal
            t1 = time()

        minimax(self._root)

        # noinspection PyUnreachableCode
        if __debug__:
            t2 = time()
            total = round((t2 - t1) * 10**3, ndigits=3)
            print(f'Search time: {total} ms\n')

        self._root = self._root.best_child
        return self._root.move

    def _update_root(self, board):
        if self._root.board != board:
            for child in self._root.children:
                if child.board == board:
                    self._root = child
                    return
            # noinspection PyUnreachableCode
            if __debug__:
                print('Replacing tree\n')
            self._root = Node(board=board)


# TODO refactor gui so do not have to store move
@dataclass
class Node:
    board: int
    move: int = None
    val: float = None
    children: List = ()
    best_child: Any = None  # TODO don't store this in node?


tree = Tree()


def minimax(node: Node, depth=5):
    node.best_child = None
    node.val = core.check_outcome(node.board)  # TODO store outcome in node?

    if node.val is not None:
        return

    if depth == 0:
        node.val = eval_board(node.board)
        return

    if not node.children:
        node.children = [
            Node(board=core.add_move(index, node.board), move=index)
            for index in core.legal_moves(node.board)
        ]

    min_node = core.turn_bit(node.board)
    node.val, compare = (core.INF, lt) if min_node else (core.NEG_INF, gt)

    for child in node.children:
        minimax(child, depth - 1)
        if compare(child.val, node.val):
            node.val = child.val
            node.best_child = child

    if node.best_child is None:
        node.best_child = node.children[0]
        assert node.val == node.best_child.val
