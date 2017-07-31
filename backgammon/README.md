### Backgammon

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


### Bugs

```

```


