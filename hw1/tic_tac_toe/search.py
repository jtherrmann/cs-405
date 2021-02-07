from dataclasses import dataclass
from time import time

from . import core
from .evaluate import eval_board


class Tree:

    def __init__(self):
        self._root = Node(core.EMPTY_BOARD)

    def get_next_board(self, board):
        self._update_root(board)

        stats = Stats()

        t1 = time()
        minimax(self._root, stats)
        t2 = time()

        # noinspection PyUnusedLocal
        total = round((t2 - t1) * 10 ** 3, ndigits=3)

        # noinspection PyUnreachableCode
        if __debug__:
            print(f'Nodes visited: {stats.visited}')
            print(f'Nodes created: {stats.created}')
            print(f'Search time: {total} ms\n')

        self._root = self._root.get_best_child()
        return self._root.get_board()

    def _update_root(self, board):
        if self._root.get_board() != board:
            for child in self._root.get_children():
                if child.get_board() == board:
                    self._root = child
                    return
            # noinspection PyUnreachableCode
            if __debug__:
                print('Replacing tree\n')
            self._root = Node(board)


class Node:

    def __init__(self, board):
        self._board = board

        self._val = core.check_outcome(self._board)
        self._leaf = self._val is not None

        self._children = ()

    def is_leaf(self):
        return self._leaf

    def is_max_node(self):
        return not core.turn_bit(self._board)

    def get_board(self):
        return self._board

    def get_val(self):
        return self._val

    def set_val(self, val):
        self._val = val

    def get_children(self):
        return self._children

    def create_children(self):
        if self._children:
            return 0
        self._children = [Node(board) for board in core.get_children(self._board)]
        return len(self._children)

    def get_best_child(self):
        for child in self._children:
            if child.get_val() == self._val:
                return child
        assert False


tree = Tree()


@dataclass
class Stats:
    visited = 0
    created = 0


def minimax(node: Node, stats: Stats, alpha=core.NEG_INF, beta=core.INF, depth=5):
    stats.visited += 1

    if node.is_leaf():
        return

    if depth == 0:
        node.set_val(eval_board(node.get_board()))
        return

    stats.created += node.create_children()

    if node.is_max_node():
        new_val = core.NEG_INF
        for child in node.get_children():
            minimax(child, stats, alpha, beta, depth - 1)
            new_val = max(new_val, child.get_val())
            alpha = max(alpha, new_val)
            # TODO
            # if alpha >= beta:
            #     break
    else:
        new_val = core.INF
        for child in node.get_children():
            minimax(child, stats, alpha, beta, depth - 1)
            new_val = min(new_val, child.get_val())
            beta = min(beta, new_val)
            # TODO
            # if alpha >= beta:
            #     break

    node.set_val(new_val)
