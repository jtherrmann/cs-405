# Tic-tac-toe

Jake Herrmann\
CS 405

## Usage

Known to work with Python 3.8.6 on Linux.

Run the game:

```
python3 -m tic_tac_toe
```

Run the game with optimizations (no assertions or debugging output):

```
python3 -O -m tic_tac_toe
```

## Known issues

* The minimax search blocks GUI events (e.g. button presses).
* The minimax search sometimes blocks the board display from refreshing, so during human vs. engine games, your move may not appear until after the engine calculates its reply.
