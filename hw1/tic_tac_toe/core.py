SIZE = 4
OFFSET = SIZE * SIZE
TURN_BIT = 1 << (OFFSET * 2)


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
    move_bit = 1 << index
    if not turn_X(board):
        move_bit <<= OFFSET
    return (board ^ TURN_BIT) | move_bit


def turn_X(board):
    return bool(board & TURN_BIT)


def legal_moves(board):
    moves = []
    O_board = board >> OFFSET
    for i in range(OFFSET):
        if not ((board & 1) | (O_board & 1)):
            moves.append(i)
        board >>= 1
        O_board >>= 1
    return moves


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
