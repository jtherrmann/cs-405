from operator import lt, gt
from time import time

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

        self._root = self._root.get_best_child()
        return self._root.get_move()

    def _update_root(self, board):
        if self._root.get_board() != board:
            for child in self._root.get_children():
                if child.get_board() == board:
                    self._root = child
                    return
            # noinspection PyUnreachableCode
            if __debug__:
                print('Replacing tree\n')
            self._root = Node(board=board)


# TODO refactor gui so do not have to store move
class Node:

    def __init__(self, board, move=None):
        self._board = board
        self._move = move

        self._val = core.check_outcome(self._board)
        self._leaf = self._val is not None

        self._children = ()

    def is_leaf(self):
        return self._leaf

    def is_min_node(self):
        return bool(core.turn_bit(self._board))

    def get_board(self):
        return self._board

    def get_move(self):
        return self._move

    def get_val(self):
        return self._val

    def set_val(self, val):
        self._val = val

    def get_children(self):
        return self._children

    def create_children(self):
        if self._children:
            return 0
        self._children = [
            Node(board=core.add_move(index, self._board), move=index)
            for index in core.legal_moves(self._board)
        ]
        return len(self._children)

    def get_best_child(self):
        for child in self._children:
            if child.get_val() == self._val:
                return child
        assert False


tree = Tree()


def minimax(node: Node, depth=5):
    nodes_visited, nodes_created = 1, 0

    if node.is_leaf():
        return nodes_visited, nodes_created

    if depth == 0:
        node.set_val(eval_board(node.get_board()))
        return nodes_visited, nodes_created

    nodes_created += node.create_children()

    if node.is_min_node():
        node.set_val(core.INF)
        compare = lt
    else:
        node.set_val(core.NEG_INF)
        compare = gt

    for child in node.get_children():
        result = minimax(child, depth - 1)
        nodes_visited += result[0]
        nodes_created += result[1]
        if compare(child.get_val(), node.get_val()):
            node.set_val(child.get_val())

    return nodes_visited, nodes_created
