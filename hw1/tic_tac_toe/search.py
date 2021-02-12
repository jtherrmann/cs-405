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

        if not self._leaf:
            self._val = eval_board(self._board)

        self._children = []

    def is_leaf(self):
        return self._leaf

    def is_max_node(self):
        return not core.turn_bit(self._board)

    def get_board(self):
        return self._board

    def get_val(self):
        return self._val

    def get_children(self):
        return self._children

    def create_children(self):
        if self._children:
            return 0
        self._children = [Node(board) for board in core.get_children(self._board)]
        self._children.sort(key=lambda child: child.get_val(), reverse=self.is_max_node())
        return len(self._children)


# ----------------------------------------------------------------------
# Minimax
# ----------------------------------------------------------------------

@dataclass
class Stats:
    visited = 0
    created = 0


def minimax(node: Node, stats: Stats, alpha=core.NEG_INF, beta=core.INF, depth=8, get_best_child=False):
    stats.visited += 1

    if node.is_leaf() or depth == 0:
        return node.get_val()

    stats.created += node.create_children()

    best_child = None
    if node.is_max_node():
        val = core.NEG_INF
        for child in node.get_children():
            child_val = minimax(child, stats, alpha, beta, depth - 1)
            if child_val > val:
                val = child_val
                best_child = child
            alpha = max(alpha, val)
            if alpha >= beta:
                break
    else:
        val = core.INF
        for child in node.get_children():
            child_val = minimax(child, stats, alpha, beta, depth - 1)
            if child_val < val:
                val = child_val
                best_child = child
            beta = min(beta, val)
            if alpha >= beta:
                break

    if get_best_child:
        # TODO I think this assertion should fail if all children are
        #  -inf (if max node) or inf (if min node), so the solution
        #  would be to just return any child in that case
        assert best_child is not None
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
