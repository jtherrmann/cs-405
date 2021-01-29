SIZE = 4
OFFSET = SIZE * SIZE


def get_win_states():
    states = []
    for col in range(SIZE):
        state = 1 << col
        for _ in range(SIZE - 1):
            state <<= SIZE
            state |= 1 << col
        states.append(state)

    mask = 2**SIZE - 1
    for row in range(SIZE):
        state = mask << (row * SIZE)
        states.append(state)

    # TODO diagonals

    return states


WIN_STATES = get_win_states()


def add_move(index, board):
    move_bit = 0b10 << index
    if not turn_X(board):
        move_bit <<= OFFSET
    return (board ^ 1) | move_bit


def turn_X(board):
    return bool(board & 1)


def legal_moves(board):
    # TODO refactor?
    moves = []
    pieces, O_pieces = split_board(board)
    for i in range(OFFSET):
        if not ((pieces & 1) | (O_pieces & 1)):
            moves.append(i)
        pieces >>= 1
        O_pieces >>= 1
    return moves


def check_outcome(board, win_states):
    pieces, O_pieces = split_board(board)
    for state in win_states:
        if pieces & state == state:
            return 1
        if O_pieces & state == state:
            return -1
    return 0 if is_full(pieces) else None


def is_full(pieces):
    count = 0
    while pieces != 0:
        count += pieces & 1
        pieces >>= 1
    return count == OFFSET


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
