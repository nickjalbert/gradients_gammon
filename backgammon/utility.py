import random

BLACK_INDEX = 0
WHITE_INDEX = 1
BLACK_BAR_INDEX = 24
WHITE_BAR_INDEX = 25
BLACK_OFF_INDEX = 26
WHITE_OFF_INDEX = 27

def get_blank_board():
    """
    See README for explanation of the board data structure.
    """
    return ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0),
            (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0),
            (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0),
            (0,0))

def get_initial_board():
    board = list(get_blank_board())
    board[0]  = (0, 2)
    board[5]  = (5, 0)
    board[7]  = (3, 0)
    board[11]  = (0, 5)
    board[12]  = (5, 0)
    board[16]  = (0, 3)
    board[18]  = (0, 5)
    board[23]  = (2, 0)
    return tuple(board)

def black_wins(board):
    return board[BLACK_OFF_INDEX] == (15, 0)

def white_wins(board):
    return board[WHITE_OFF_INDEX] == (0, 15)

def is_valid_board(board):
    # count total whites
    assert sum(position[0] for position in board) == 15
    # count total blacks
    assert sum(position[1] for position in board) == 15
    assert board[BLACK_BAR_INDEX][WHITE_INDEX] == 0
    assert board[WHITE_BAR_INDEX][BLACK_INDEX] == 0
    assert board[BLACK_OFF_INDEX][WHITE_INDEX] == 0
    assert board[WHITE_OFF_INDEX][BLACK_INDEX] == 0
    for position in board:
        assert position[0] >= 0
        assert position[1] >= 0
        if position[0] > 0 and position[1] > 0:
            return False
    return True

def roll_dice():
    """
    Rolls two six sided die.  Returns a 2 element list (or 4 in the case of
    doubles).
    """
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)
    if dice1 == dice2:
        return [dice1, dice1, dice1, dice1]
    return [dice1, dice2]

def black_can_bear_off(board):
    """
    Black can only bear off if all pieces are in the upper right quadrant.
    """
    black_count = board[5][BLACK_INDEX]
    black_count += board[4][BLACK_INDEX]
    black_count += board[3][BLACK_INDEX]
    black_count += board[2][BLACK_INDEX]
    black_count += board[1][BLACK_INDEX]
    black_count += board[0][BLACK_INDEX]
    black_count += board[BLACK_OFF_INDEX][BLACK_INDEX]
    return black_count == 15

def white_can_bear_off(board):
    """
    White can only bear off if all pieces are in the bottom right quadrant.
    """
    white_count = board[18][WHITE_INDEX]
    white_count += board[19][WHITE_INDEX]
    white_count += board[20][WHITE_INDEX]
    white_count += board[21][WHITE_INDEX]
    white_count += board[22][WHITE_INDEX]
    white_count += board[23][WHITE_INDEX]
    white_count += board[WHITE_OFF_INDEX][WHITE_INDEX]
    return white_count == 15

def black_position_is_outer(board, position):
    """
    Returns boolean indicating whether <position> on the <board> is the most
    exterme point containing black pieces (i.e. furthest from the black home).
    """
    if board[position][BLACK_INDEX] == 0:
        return False
    if board[BLACK_BAR_INDEX][BLACK_INDEX] > 0:
        return False
    for i in range(position+1, len(board)):
        if i == BLACK_OFF_INDEX:
            continue
        if board[i][BLACK_INDEX] > 0:
            return False
    return True

def white_position_is_outer(board, position):
    """
    Returns boolean indicating whether <position> on the <board> is the most
    exterme point containing white pieces (i.e. furthest from the white home).
    """
    if board[position][WHITE_INDEX] == 0:
        return False
    if board[WHITE_BAR_INDEX][WHITE_INDEX] > 0:
        return False
    for i in range(position):
        if board[i][WHITE_INDEX] > 0:
            return False
    return True

