# Jake Herrmann
# CS 405
#
# core.py
# Core tic-tac-toe game logic.

SIZE = 4
OFFSET = SIZE * SIZE
EMPTY_BOARD = 0

INF = float('inf')
NEG_INF = -INF


def mid_index():
    mid_coord = (SIZE - 1) // 2
    return SIZE * mid_coord + mid_coord


MID_INDEX = mid_index()


def get_win_states():
    states = []

    # Rows
    row_mask = 2**SIZE - 1
    for row in range(SIZE):
        state = row_mask << (row * SIZE)
        states.append(state)

    # Columns
    for col in range(SIZE):
        col_bit = 1 << col
        state = col_bit
        for _ in range(SIZE - 1):
            state <<= SIZE
            state |= col_bit
        states.append(state)

    # Upper-left diagonal
    state = 1
    for _ in range(SIZE - 1):
        state <<= (SIZE + 1)
        state |= 1
    states.append(state)

    # Upper-right diagonal
    top_right_bit = 1 << (SIZE - 1)
    state = top_right_bit
    for _ in range(SIZE - 1):
        state <<= (SIZE - 1)
        state |= top_right_bit
    states.append(state)

    return states


WIN_STATES = get_win_states()


def print_win_states():
    print('Win states:\n')
    for state in WIN_STATES:
        print_win_state(state, SIZE)
        print()
    print('(End win states)\n')


def print_win_state(state, size):
    for _ in range(size):
        rowstr = ''
        for _ in range(size):
            rowstr += '# ' if state & 1 else '. '
            state >>= 1
        print(rowstr)
    assert state == 0


# noinspection PyUnreachableCode
if __debug__:
    print_win_states()


def add_move(index, board):
    move_bit = 0b10 << index
    move_bit <<= (OFFSET * turn_bit(board))
    return (board ^ 1) | move_bit


def turn_bit(board):
    return board & 1


def legal_moves(board):
    moves = []
    pieces, O_pieces = split_board(board)
    pieces |= O_pieces
    for i in range(OFFSET):
        if not (pieces & 1):
            moves.append(i)
        pieces >>= 1
    return moves


def get_children(board):
    return [add_move(index, board) for index in legal_moves(board)]


def check_outcome(board):
    pieces, O_pieces = split_board(board)
    for state in WIN_STATES:
        if pieces & state == state:
            return INF
        if O_pieces & state == state:
            return NEG_INF
    return 0 if count_bits(pieces) == OFFSET else None


def count_bits(num):
    count = 0
    while num != 0:
        count += num & 1
        num >>= 1
    return count


def split_indices(board):
    pieces, O_pieces = split_board(board)
    return get_indices(pieces), get_indices(O_pieces)


def get_indices(pieces):
    for i in range(OFFSET):
        if pieces & 1:
            yield i
        pieces >>= 1


def split_board(board):
    pieces = board >> 1
    return pieces, pieces >> OFFSET
