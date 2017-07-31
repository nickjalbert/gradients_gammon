### Backgammon

### Commands

* Run a game loop: ```python game_loop.py```
* Run the tests: ```python test.py```

### Tour

This subproject enumerates all legal next states given a backgammon board, dice
roll, and player's turn.  This is accomplished in ```boards.py``` by the
```generate_all_boards``` method.

Example of usage:

```python
from boards import generate_next_boards
from utility import get_initial_board
board = get_initial_board()
is_black_turn = False
roll = [3,1]
next_boards = generate_next_boards(board, is_black_turn, roll)
```

You can use ASCII to visualize a backgammon board as follows:

```python
from visualize import visualize_board
visualize_board(next_boards[0])
```

You can run a game loop from the command line and play against black:

```
python game_loop.py
```

You select your move from the menu printed above the depiction of the current board state.  If you do not select a move, one will be automatically selected.

### Board Representation

We represent the backgammon board as a 28 element list of 2-tuples.  List
indices 0 through 23 represent each point on the board.  The first element of
each 2-tuple is the number of black pieces on the point.  The second element
of each 2-tuple is the number of white pieces on the point.

List index 24 is the tuple representing the bar where black pieces go when
hit.

List index 25 is the tuple representing the bar where white pieces go when
hit.

List index 26 is the tuple representing the the area where born off black
pieces reside.

List index 27 is the tuple representing the the area where born off white
pieces reside.

White moves counter-clockwise and bears off to the bottom right.  Black moves
clockwise and bears off to the top right.

Illustration of the list indices and their correspondence to the board:

```

 |  1  1  9  8  7  6  |   |  5  4  3  2  1  0  | Black Off: 26
 |  1  0              |   |                    | Black Bar: 24
 |                    |   |                    |
 |  _  _  _  _  _  _  |   |  _  _  _  _  _  _  |
 |                    |   |                    |
 |                    |   |                    |
 |  1  1  1  1  1  1  |   |  1  1  2  2  2  2  |
 |  2  3  4  5  6  7  |   |  8  9  0  1  2  3  | White Off: 27
 |  _  _  _  _  _  _  |   |  _  _  _  _  _  _  | White Bar: 25
 |  .  .  .  .  .  .  |   |  .  .  .  .  .  .  |
```

### State Enumeration

To enumerate all legal next states, we apply each dice roll one at a time to
each point on the board in ```generate_next_boards```.  The generation
strategy could be better optimized to prune equivalent subtrees from the
generation space.

### Test
```
python test.py
```

### Bugs

```

```


