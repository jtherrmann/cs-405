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

        t1 = time()
        # noinspection PyUnusedLocal
        nodes_visited, nodes_created = minimax(self._root)
        t2 = time()

        # noinspection PyUnusedLocal
        total = round((t2 - t1) * 10 ** 3, ndigits=3)

        # noinspection PyUnreachableCode
        if __debug__:
            print(f'Nodes visited: {nodes_visited}')
            print(f'Nodes created: {nodes_created}')
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
    nodes_visited, nodes_created = 1, 0

    node.best_child = None
    node.val = core.check_outcome(node.board)  # TODO store outcome in node?

    if node.val is not None:
        return nodes_visited, nodes_created

    if depth == 0:
        node.val = eval_board(node.board)
        return nodes_visited, nodes_created

    if not node.children:
        node.children = [
            Node(board=core.add_move(index, node.board), move=index)
            for index in core.legal_moves(node.board)
        ]
        nodes_created += len(node.children)

    min_node = core.turn_bit(node.board)
    node.val, compare = (core.INF, lt) if min_node else (core.NEG_INF, gt)

    for child in node.children:
        result = minimax(child, depth - 1)
        nodes_visited += result[0]
        nodes_created += result[1]
        if compare(child.val, node.val):
            node.val = child.val
            node.best_child = child

    if node.best_child is None:
        node.best_child = node.children[0]
        assert node.val == node.best_child.val

    return nodes_visited, nodes_created
