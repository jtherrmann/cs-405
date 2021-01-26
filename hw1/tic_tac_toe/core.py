def get_win_states(size):
    states = []
    for col in range(size):
        state = 1 << col
        for _ in range(size - 1):
            state <<= size
            state |= 1 << col
        states.append(state)

    mask = 2**size - 1
    for row in range(size):
        state = mask << (row * size)
        states.append(state)

    # TODO diagonals

    return states


def add_move(index, moveX, board, offset):
    if index is None:
        return None

    bit = 1 << index
    offset_bit = bit << offset
    if board & bit != 0 or board & offset_bit != 0:
        return None

    return board | bit if moveX else board | offset_bit


def check_outcome(board, offset, win_states):
    O_board = board >> offset
    for state in win_states:
        if board & state == state:
            return 1
        if O_board & state == state:
            return -1
    return 0 if is_full(board, offset) else None


def is_full(board, offset):
    count = 0
    while board != 0:
        count += board & 1
        board >>= 1
    return count == offset
