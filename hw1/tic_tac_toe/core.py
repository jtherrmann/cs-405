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


def add_move(index, moveX, board):
    if index is None:
        return None

    bit = 1 << index
    offset_bit = bit << OFFSET
    if board & bit != 0 or board & offset_bit != 0:
        return None

    return board | bit if moveX else board | offset_bit


def check_outcome(board, win_states):
    O_board = board >> OFFSET
    for state in win_states:
        if board & state == state:
            return 1
        if O_board & state == state:
            return -1
    return 0 if is_full(board) else None


def is_full(board):
    count = 0
    while board != 0:
        count += board & 1
        board >>= 1
    return count == OFFSET
