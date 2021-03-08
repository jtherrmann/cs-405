# Jake Herrmann
# CS 405
#
# mcts.py
# Monte Carlo tree search (MCTS).

from dataclasses import dataclass
from math import sqrt, log
from random import randint
from time import time

from . import core


# TODO review code


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
        self._root = mcts(self._root, stats)
        t2 = time()

        # noinspection PyUnusedLocal
        total = (t2 - t1) * 10 ** 3

        # noinspection PyUnreachableCode
        if __debug__:
            print('MCTS')
            print(f'Nodes visited: {stats.visited}')
            print(f'Search time: {total:.3f} ms')
            print(f'Rate: {(stats.visited / total):.1f} nodes visited / ms')
            print()

        return self._root.board()

    def _update_root(self, board):
        if self._root.board() != board:
            for child in self._root.children():
                if child.board() == board:
                    self._root = child
                    return
            # noinspection PyUnreachableCode
            if __debug__:
                print('MCTS: Replacing tree\n')
            self._root = Node(board)


# ----------------------------------------------------------------------
# Node
# ----------------------------------------------------------------------

# TODO try different values (including 0)
UCT_PARAM = sqrt(2)


class Node:

    def __init__(self, board):
        self._board = board
        self._outcome = core.check_outcome(self._board)
        self._children = []
        self._unvisited_children = []
        self._wins = 0
        self._simulations = 0

    def board(self):
        return self._board

    def children(self):
        return self._children

    def outcome(self):
        return self._outcome

    def has_outcome(self):
        return self._outcome is not None

    def wins(self):
        return self._wins

    def simulations(self):
        return self._simulations

    def win_ratio(self):
        return self._wins / self._simulations

    def is_X_child(self):
        # If it is O's turn to move, then this node is a child of an X node.
        return bool(core.turn_bit(self._board))

    def fully_expanded(self):
        if self.has_outcome():
            return False
        self._create_children()
        return not self._unvisited_children

    def _create_children(self):
        assert not self.has_outcome()
        if not self._children:
            assert not self._unvisited_children
            self._children = [Node(board) for board in core.get_children(self._board)]
            self._unvisited_children = self._children.copy()

    def max_uct_child(self):
        logN = log(self._simulations)
        return max(self._children, key=lambda child: child.uct(logN))

    def uct(self, logN):
        # https://en.wikipedia.org/wiki/Monte_Carlo_tree_search#Exploration_and_exploitation
        return self._wins / self._simulations + UCT_PARAM * sqrt(logN / self._simulations)

    def get_unvisited_child(self):
        assert not self.has_outcome()
        return self._unvisited_children.pop()

    def random_child(self):
        self._create_children()
        return self._children[randint(0, len(self._children) - 1)]

    def get_best_child(self):
        # TODO try other methods

        # https://ai.stackexchange.com/a/17713
        best_child = max(self._children, key=lambda child: child.simulations())

        # noinspection PyUnreachableCode
        if __debug__:
            print_children_stats(self._children, best_child)

        return best_child

    def update_stats(self, win):
        self._wins += win
        self._simulations += 1


def print_children_stats(children, best_child):
    # TODO print data in tabular format
    # TODO mark the rows with max wins, max simulations, and max ratio

    print('MCTS children (wins / simulations):')
    for child in children:
        marker = ''
        if child is best_child:
            marker = ' (best child)'
        print(f'{child.wins()} / {child.simulations()} = {child.win_ratio():.3f} {marker}')
    print()


# ----------------------------------------------------------------------
# MCTS
# ----------------------------------------------------------------------

# TODO: how to handle terminal nodes?

@dataclass
class Stats:
    visited = 0


def mcts(root: Node, stats: Stats):
    stop_time = get_time() + 10
    while get_time() < stop_time:
        path = get_child(root)
        outcome = rollout(path[-1])
        backpropagate(path, outcome)
        stats.visited += len(path) - 1
    return root.get_best_child()


def get_child(node: Node):
    path = [node]
    while node.fully_expanded():
        node = node.max_uct_child()
        path.append(node)
    if not node.has_outcome():
        path.append(node.get_unvisited_child())
    return path


def rollout(node: Node):
    while not node.has_outcome():
        node = node.random_child()
    return node.outcome()


def backpropagate(path, outcome):
    if outcome is core.INF:
        X_win, O_win = 1, 0
    elif outcome is core.NEG_INF:
        X_win, O_win = 0, 1
    else:
        assert outcome == 0
        X_win = O_win = 0.5

    if path[0].is_X_child():
        curr_win, next_win = X_win, O_win
    else:
        curr_win, next_win = O_win, X_win

    for node in path:
        node.update_stats(curr_win)
        curr_win, next_win = next_win, curr_win


def get_time():
    return round(time())


# ----------------------------------------------------------------------
# Global tree object
# ----------------------------------------------------------------------

tree = Tree()
