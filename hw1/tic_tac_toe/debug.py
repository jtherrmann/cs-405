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
