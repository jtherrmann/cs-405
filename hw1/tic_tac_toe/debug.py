def print_board(board, size, offset):
    O_board = board >> offset
    for _ in range(size):
        rowstr = ''
        for _ in range(size):
            if board & 1:
                assert O_board & 1 == 0
                rowstr += 'X '
            elif O_board & 1:
                rowstr += 'O '
            else:
                rowstr += '. '
            board >>= 1
            O_board >>= 1
        print(rowstr)


def print_win_states(win_states, size):
    print('Win states:\n')
    for state in win_states:
        print_win_state(state, size)
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
