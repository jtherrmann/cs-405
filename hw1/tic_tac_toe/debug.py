def print_game(game, size, offset):
    Oboard = game >> offset
    for _ in range(size):
        rowstr = ''
        for _ in range(size):
            if game & 1:
                assert Oboard & 1 == 0
                rowstr += 'X '
            elif Oboard & 1:
                rowstr += 'O '
            else:
                rowstr += '. '
            game >>= 1
            Oboard >>= 1
        print(rowstr)


def print_win_states(win_states, size):
    for state in win_states:
        print_win_state(state, size)
        print()


def print_win_state(state, size):
    for _ in range(size):
        rowstr = ''
        for _ in range(size):
            rowstr += '# ' if state & 1 else '. '
            state >>= 1
        print(rowstr)
    assert state == 0
