# Jake Herrmann
# CS 405
#
# search.py
# Minimax search tree.

from dataclasses import dataclass
from time import time

from . import core
from .evaluate import eval_board


# ----------------------------------------------------------------------
# Tree
# ----------------------------------------------------------------------

class Tree:

    def __init__(self):
        self._root = Node(core.EMPTY_BOARD)

    def get_next_board(self, board):
        self._update_root(board)

        stats = Stats()

        t1 = time()
        self._root = minimax(self._root, stats, get_best_child=True)
        t2 = time()

        # noinspection PyUnusedLocal
        total = (t2 - t1) * 10 ** 3

        # noinspection PyUnreachableCode
        if __debug__:
            print(f'Nodes visited: {stats.visited}')
            print(f'Nodes created: {stats.created}')
            print(f'Search time: {total:.3f} ms')
            print(f'Rate: {(stats.visited / total):.1f} nodes visited / ms')
            print()

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


# ----------------------------------------------------------------------
# Node
# ----------------------------------------------------------------------

class Node:

    def __init__(self, board):
        self._board = board

        self._val = core.check_outcome(self._board)
        self._leaf = self._val is not None

        self._children = []

    def is_leaf(self):
        return self._leaf

    def is_max_node(self):
        return not core.turn_bit(self._board)

    def get_board(self):
        return self._board

    def get_val(self):
        return self._val

    def set_val(self, val):
        assert not self.is_leaf()
        self._val = val

    def get_children(self):
        return self._children

    def create_children(self):
        if self._children:
            return 0
        self._children = [Node(board) for board in core.get_children(self._board)]
        return len(self._children)


# ----------------------------------------------------------------------
# Minimax
# ----------------------------------------------------------------------

@dataclass
class Stats:
    visited = 0
    created = 0


def minimax(node: Node, stats: Stats, depth=5, get_best_child=False):
    stats.visited += 1

    if node.is_leaf():
        return node.get_val()

    if depth == 0:
        val = eval_board(node.get_board())
        node.set_val(val)
        return val

    stats.created += node.create_children()

    best_child = None
    if node.is_max_node():
        val = core.NEG_INF
        for child in node.get_children():
            child_val = minimax(child, stats, depth - 1)
            if child_val > val:
                val = child_val
                best_child = child
    else:
        val = core.INF
        for child in node.get_children():
            child_val = minimax(child, stats, depth - 1)
            if child_val < val:
                val = child_val
                best_child = child

    node.set_val(val)

    if get_best_child:
        # TODO this should fail if all children were -inf (if max node) or inf (if min node)
        assert best_child is not None
        assert best_child.get_val() == val
        return best_child

    return val


def test_minimax(board, depth):
    # Minimax with no caching or pruning, for testing purposes.

    outcome = core.check_outcome(board)
    if outcome is not None:
        return outcome

    if depth == 0:
        return eval_board(board)

    vals = [test_minimax(child, depth - 1) for child in core.get_children(board)]
    if not core.turn_bit(board):
        return max(core.NEG_INF, *vals)
    return min(core.INF, *vals)


# ----------------------------------------------------------------------
# Global tree object
# ----------------------------------------------------------------------

tree = Tree()
