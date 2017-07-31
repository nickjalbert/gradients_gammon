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
    return [(0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0),
            (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0),
            (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0),
            (0,0)]

def get_initial_board():
    board = get_blank_board()
    board[0]  = (0, 2)
    board[5]  = (5, 0)
    board[7]  = (3, 0)
    board[11]  = (0, 5)
    board[12]  = (5, 0)
    board[16]  = (0, 3)
    board[18]  = (0, 5)
    board[23]  = (2, 0)
    return board

def black_wins(board):
    return board[BLACK_OFF_INDEX] == (15, 0)

def white_wins(board):
    return board[WHITE_OFF_INDEX] == (0, 15)

def is_valid_board(board):
    assert sum(position[WHITE_INDEX] for position in board) == 15
    assert sum(position[BLACK_INDEX] for position in board) == 15
    assert board[BLACK_BAR_INDEX][WHITE_INDEX] == 0
    assert board[WHITE_BAR_INDEX][BLACK_INDEX] == 0
    assert board[BLACK_OFF_INDEX][WHITE_INDEX] == 0
    assert board[WHITE_OFF_INDEX][BLACK_INDEX] == 0
    for position in board:
        assert position[WHITE_INDEX] >= 0
        assert position[BLACK_INDEX] >= 0
        if position[WHITE_INDEX] > 0 and position[BLACK_INDEX] > 0:
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

def can_bear_off(board):
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

def position_is_outer(board, position):
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

def swap_colors(board):
    """
    Returns a new board in which white is in an identical position to black on
    the old board (and vice versa).
    """
    def _in_place_swap(board, i, j):
        tmp0, tmp1 = board[i]
        board[i] = (board[j][1], board[j][0])
        board[j] = (tmp1, tmp0)
    board = board[:]
    _in_place_swap(board, 0, 23)
    _in_place_swap(board, 1, 22)
    _in_place_swap(board, 2, 21)
    _in_place_swap(board, 3, 20)
    _in_place_swap(board, 4, 19)
    _in_place_swap(board, 5, 18)
    _in_place_swap(board, 6, 17)
    _in_place_swap(board, 7, 16)
    _in_place_swap(board, 8, 15)
    _in_place_swap(board, 9, 14)
    _in_place_swap(board, 10, 13)
    _in_place_swap(board, 11, 12)
    _in_place_swap(board, BLACK_BAR_INDEX, WHITE_BAR_INDEX)
    _in_place_swap(board, BLACK_OFF_INDEX, WHITE_OFF_INDEX)
    return board

