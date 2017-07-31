# Positions counter clockwise from top right
# Each element (black pieces, white pieces)
# White is trying to exit bottom right
# Black is trying to exit top right

# Board index:
#
# |  1  1  9  8  7  6  |   |  5  4  3  2  1  0  | Black Off: 26
# |  1  0              |   |                    | Black Bar: 24
# |                    |   |                    |
# |  _  _  _  _  _  _  |   |  _  _  _  _  _  _  |
# |                    |   |                    |
# |                    |   |                    |
# |  1  1  1  1  1  1  |   |  1  1  2  2  2  2  |
# |  2  3  4  5  6  7  |   |  8  9  0  1  2  3  | White Off: 27
# |  _  _  _  _  _  _  |   |  _  _  _  _  _  _  | White Bar: 25
# |  .  .  .  .  .  .  |   |  .  .  .  .  .  .  |

import random
import copy
import pprint

BLACK_INDEX = 0
WHITE_INDEX = 1
BLACK_BAR_INDEX = 24
WHITE_BAR_INDEX = 25
BLACK_OFF_INDEX = 26
WHITE_OFF_INDEX = 27


def get_blank_board():
    return ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0),
            (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0),
            (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0))

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
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)
    if dice1 == dice2:
        return [dice1, dice1, dice1, dice1]
    return [dice1, dice2]

def black_can_bear_off(board):
    black_count = board[5][BLACK_INDEX]
    black_count += board[4][BLACK_INDEX]
    black_count += board[3][BLACK_INDEX]
    black_count += board[2][BLACK_INDEX]
    black_count += board[1][BLACK_INDEX]
    black_count += board[0][BLACK_INDEX]
    black_count += board[BLACK_OFF_INDEX][BLACK_INDEX]
    return black_count == 15

def white_can_bear_off(board):
    white_count = board[18][WHITE_INDEX]
    white_count += board[19][WHITE_INDEX]
    white_count += board[20][WHITE_INDEX]
    white_count += board[21][WHITE_INDEX]
    white_count += board[22][WHITE_INDEX]
    white_count += board[23][WHITE_INDEX]
    white_count += board[WHITE_OFF_INDEX][WHITE_INDEX]
    return white_count == 15

def black_position_is_outer(board, position):
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
    if board[position][WHITE_INDEX] == 0:
        return False
    if board[WHITE_BAR_INDEX][WHITE_INDEX] > 0:
        return False
    for i in range(position):
        if board[i][WHITE_INDEX] > 0:
            return False
    return True

def _get_all_boards_black(board, roll):
    if board[BLACK_BAR_INDEX][BLACK_INDEX] > 0:
        new_board = list(copy.deepcopy(board))
        black_bar_count, white_bar_count = new_board[BLACK_BAR_INDEX]
        new_board[BLACK_BAR_INDEX] = (black_bar_count - 1, white_bar_count)
        target_index = 24 - roll
        black_target_count, white_target_count = new_board[target_index]
        if white_target_count == 1:
            new_board[target_index] = (black_target_count+1, 0)
            white_bar_black, white_bar_white = new_board[WHITE_BAR_INDEX]
            new_board[WHITE_BAR_INDEX] = (white_bar_black, white_bar_white+1)
        else:
            new_board[target_index] = (black_target_count+1, white_target_count)
        if is_valid_board(new_board):
            return [tuple(new_board)]
        return []
    all_boards = []
    for position, (black_count, white_count) in enumerate(board):
        if position == BLACK_OFF_INDEX:
            continue
        if black_count == 0:
            continue
        target = position - roll
        if target < 0 and black_can_bear_off(board) and black_position_is_outer(board, position):
            target = BLACK_OFF_INDEX
        if target == -1 and black_can_bear_off(board):
            target = BLACK_OFF_INDEX
        if target < 0: 
            continue
        new_board = list(copy.deepcopy(board))
        new_board[position] = (black_count-1, white_count)
        if new_board[target][WHITE_INDEX] == 1: # hit
            new_board[target] = (1, 0)
            new_board[WHITE_BAR_INDEX] = (0, new_board[WHITE_BAR_INDEX][WHITE_INDEX]+1)
        else:
            new_board[target] = (new_board[target][BLACK_INDEX]+1,
                                 new_board[target][WHITE_INDEX])
        new_board = tuple(new_board)
        if is_valid_board(new_board):
            all_boards.append(new_board)
    return all_boards

def _get_all_boards_white(board, roll):
    if board[WHITE_BAR_INDEX][WHITE_INDEX] > 0:
        new_board = list(copy.deepcopy(board))
        black_bar_count, white_bar_count = new_board[WHITE_BAR_INDEX]
        new_board[WHITE_BAR_INDEX] = (black_bar_count, white_bar_count - 1)
        target_index = -1 + roll
        black_target_count, white_target_count = new_board[target_index]
        if black_target_count == 1:
            new_board[target_index] = (0, white_target_count+1)
            black_bar_black, black_bar_white =  new_board[BLACK_BAR_INDEX]
            new_board[BLACK_BAR_INDEX] = (black_bar_black+1, black_bar_white)
        else:
            new_board[target_index] = (black_target_count, white_target_count+1)
        if is_valid_board(new_board):
            return [tuple(new_board)]
        return []
    all_boards = []
    for position, (black_count, white_count) in enumerate(board):
        if position == WHITE_OFF_INDEX:
            continue
        if white_count == 0:
            continue
        target = position + roll
        if target > 23 and white_can_bear_off(board) and white_position_is_outer(board, position):
            target = WHITE_OFF_INDEX
        elif target == 24 and white_can_bear_off(board):
            target = WHITE_OFF_INDEX
        elif target > 23:
            continue
        new_board = list(copy.deepcopy(board))
        new_board[position] = (black_count, white_count-1)
        if new_board[target][BLACK_INDEX] == 1: # hit
            new_board[target] = (0, 1)
            new_board[BLACK_BAR_INDEX] = (new_board[BLACK_BAR_INDEX][BLACK_INDEX]+1, 0)
        else:
            new_board[target] = (new_board[target][BLACK_INDEX],
                                 new_board[target][WHITE_INDEX]+1)
        new_board = tuple(new_board)
        if is_valid_board(new_board):
            all_boards.append(new_board)
    return all_boards


def visualize_board(board):
    assert is_valid_board(board)
    def _get_pos(board, position):
        tens = max(board[position][WHITE_INDEX]/10, board[position][BLACK_INDEX]/10)
        zeros = max(board[position][WHITE_INDEX]%10, board[position][BLACK_INDEX]%10)
        color = 'W' if board[position][WHITE_INDEX] > board[position][BLACK_INDEX] else 'B'
        if (tens == 0) and (zeros == 0):
            zeros = ' '
            color = '_'
        if tens == 0:
            tens = ' '
        return tens, zeros, color

    tens0, ones0, color0 = _get_pos(board, 0)
    tens1, ones1, color1 = _get_pos(board, 1)
    tens2, ones2, color2 = _get_pos(board, 2)
    tens3, ones3, color3 = _get_pos(board, 3)
    tens4, ones4, color4 = _get_pos(board, 4)
    tens5, ones5, color5 = _get_pos(board, 5)
    tens6, ones6, color6 = _get_pos(board, 6)
    tens7, ones7, color7 = _get_pos(board, 7)
    tens8, ones8, color8 = _get_pos(board, 8)
    tens9, ones9, color9 = _get_pos(board, 9)
    tens10, ones10, color10 = _get_pos(board, 10)
    tens11, ones11, color11 = _get_pos(board, 11)
    tens12, ones12, color12 = _get_pos(board, 12)
    tens13, ones13, color13 = _get_pos(board, 13)
    tens14, ones14, color14 = _get_pos(board, 14)
    tens15, ones15, color15 = _get_pos(board, 15)
    tens16, ones16, color16 = _get_pos(board, 16)
    tens17, ones17, color17 = _get_pos(board, 17)
    tens18, ones18, color18 = _get_pos(board, 18)
    tens19, ones19, color19 = _get_pos(board, 19)
    tens20, ones20, color20 = _get_pos(board, 20)
    tens21, ones21, color21 = _get_pos(board, 21)
    tens22, ones22, color22 = _get_pos(board, 22)
    tens23, ones23, color23 = _get_pos(board, 23)
    tensbb, onesbb, colorbb = _get_pos(board, BLACK_BAR_INDEX)
    if tensbb == ' ' and onesbb == ' ':
        colorbb = ' '
    tenswb, oneswb, colorwb = _get_pos(board, WHITE_BAR_INDEX)
    if tenswb == ' ' and oneswb == ' ':
        colorwb = ' '
    tensbo, onesbo, colorbo = _get_pos(board, BLACK_OFF_INDEX)
    if tensbo == ' ' and onesbo == ' ':
        colorbo = ' '
    tenswo, oneswo, colorwo = _get_pos(board, WHITE_OFF_INDEX)
    if tenswo == ' ' and oneswo == ' ':
        colorwo = ' '
    print
    print '|  .  .  .  .  .  .  |   |  .  .  .  .  .  .  |'
    print '|  {}  {}  {}  {}  {}  {}  | {} |  {}  {}  {}  {}  {}  {}  | {}'.format(tens11,tens10,tens9,tens8,tens7,tens6,tensbb,tens5,tens4,tens3,tens2,tens1,tens0,tensbo)
    print '|  {}  {}  {}  {}  {}  {}  | {} |  {}  {}  {}  {}  {}  {}  | {}'.format(ones11,ones10,ones9,ones8,ones7,ones6,onesbb,ones5,ones4,ones3,ones2,ones1,ones0,onesbo)
    print '|  {}  {}  {}  {}  {}  {}  | {} |  {}  {}  {}  {}  {}  {}  | {}'.format(color11,color10,color9,color8,color7,color6,colorbb,color5,color4,color3,color2,color1,color0,colorbo)
    print '|                    |   |                    |'
    print '|                    |   |                    |'
    print '|  {}  {}  {}  {}  {}  {}  | {} |  {}  {}  {}  {}  {}  {}  | {}'.format(tens12,tens13,tens14,tens15,tens16,tens17,tenswb,tens18,tens19,tens20,tens21,tens22,tens23,tenswo)
    print '|  {}  {}  {}  {}  {}  {}  | {} |  {}  {}  {}  {}  {}  {}  | {}'.format(ones12,ones13,ones14,ones15,ones16,ones17,oneswb,ones18,ones19,ones20,ones21,ones22,ones23,oneswo)
    print '|  {}  {}  {}  {}  {}  {}  | {} |  {}  {}  {}  {}  {}  {}  | {}'.format(color12,color13,color14,color15,color16,color17,colorwb,color18,color19,color20,color21,color22,color23, colorwo)
    print '|  .  .  .  .  .  .  |   |  .  .  .  .  .  .  |'
    print

def generate_next_boards(board, is_black_turn, rolls):
    final_boards = []
    search_stack = []
    # [board, rolls, rolls_used]
    search_stack.append([tuple(copy.deepcopy(board)), copy.deepcopy(rolls), []])
    while search_stack:
        board, rolls, used_rolls = search_stack.pop()
        if not rolls:
            final_boards.append((board, tuple(used_rolls)))
            continue
        for i, roll in enumerate(rolls):
            if is_black_turn:
                next_boards = _get_all_boards_black(board, roll)
            else:
                next_boards = _get_all_boards_white(board, roll)
            if not next_boards:
                next_rolls = copy.deepcopy(rolls)
                next_rolls.pop(i)
                search_stack.append((board, next_rolls, used_rolls))
            for next_board in next_boards:
                next_rolls = copy.deepcopy(rolls)
                tmp_used_rolls = copy.deepcopy(used_rolls)
                tmp_used_rolls.append(next_rolls.pop(i))
                search_stack.append((next_board, next_rolls, tmp_used_rolls))
            if len(set(rolls)) == 1: # optimize for doubles
                break
    max_moves = max(len(used_rolls) for (board, used_rolls) in final_boards)
    filtered_final_boards = [(board, used_rolls)
                             for (board, used_rolls) in final_boards 
                             if len(used_rolls) == max_moves]
    if max_moves == 1:
        max_roll = max(max(used_rolls) 
                       for (board, used_rolls) 
                       in filtered_final_boards)
        filtered_final_boards = [(board, used_rolls)
                                 for (board, used_rolls) in filtered_final_boards
                                 if max(used_rolls) == max_roll]
    return list(set([board for (board, used_rolls) in filtered_final_boards]))



def test_move_prioritization():
    """
    Ensure that we don't return:
        board[2] = (0,15)       
        board[4] = (15,0)       
    as a next board because it doesn't use all rolls
    """
    board = list(get_blank_board())
    board[1] = (0,1)
    board[2] = (0,14)
    board[4] = (15,0)
    assert is_valid_board(board)
    roll = [2,1]
    next_boards = generate_next_boards(board, False, roll)
    visualize_board(board)
    for nboard in next_boards:
        visualize_board(nboard)

    assert len(next_boards) == 2
    board1 = list(get_blank_board())
    board1[2]= (0,13)
    board1[3]= (0,2)
    board1[4]= (15,0)
    board1 = tuple(board1)
    assert board1 in next_boards
    board2 = list(get_blank_board())
    board2[1]= (0,1)
    board2[2]= (0,13)
    board2[4]= (15,0)
    board2[5]= (0,1)
    board2 = tuple(board2)
    assert board2 in next_boards

def test_black_enter_from_bar():
    board = list(get_blank_board())
    board[BLACK_BAR_INDEX] = (15, 0)
    board[23] = (0, 15)
    assert is_valid_board(board)
    roll = [2,1]
    next_boards = generate_next_boards(board, True, roll)
    assert len(next_boards) == 1
    assert next_boards[0][BLACK_BAR_INDEX] == (14, 0)
    assert next_boards[0][23] == (0, 15)
    assert next_boards[0][22] == (1, 0)
    roll = [1,1,1,1]
    next_boards = generate_next_boards(board, True, roll)
    assert len(next_boards) == 1
    assert next_boards[0][BLACK_BAR_INDEX] == (15, 0)
    assert next_boards[0][23] == (0, 15)

def test_white_enter_from_bar():
    board = list(get_blank_board())
    board[WHITE_BAR_INDEX] = (0, 15)
    board[0] = (15, 0)
    assert is_valid_board(board)
    roll = [2,1]
    next_boards = generate_next_boards(board, False, roll)
    assert len(next_boards) == 1
    assert next_boards[0][WHITE_BAR_INDEX] == (0, 14)
    assert next_boards[0][0] == (15, 0)
    assert next_boards[0][1] == (0, 1)
    roll = [1,1,1,1]
    next_boards = generate_next_boards(board, False, roll)
    assert len(next_boards) == 1
    assert next_boards[0][WHITE_BAR_INDEX] == (0, 15)
    assert next_boards[0][0] == (15, 0)

def test_white_hit():
    board = list(get_blank_board())
    board[23] = (1,0)
    board[22] = (0,15)
    board[3] = (14,0)
    roll = [1,1,1,1]
    next_boards = generate_next_boards(board, False, roll)
    assert len(next_boards) == 3
    for next_board in next_boards:
        assert next_board[BLACK_BAR_INDEX] == (1,0)

def test_black_hit():
    board = list(get_blank_board())
    board[1] = (0,1)
    board[2] = (15,0)
    board[3] = (0,14)
    roll = [1,1,1,1]
    next_boards = generate_next_boards(board, True, roll)
    assert len(next_boards) == 4
    for next_board in next_boards:
        assert next_board[WHITE_BAR_INDEX] == (0,1)

def test_no_move():
    board = list(get_blank_board())
    board[1] = (0,15)
    board[2] = (15,0)
    roll = [1,1,1,1]
    next_boards = generate_next_boards(board, True, roll)
    assert len(next_boards) == 1
    assert next_boards[0][1] == (0,15)
    assert next_boards[0][2] == (15,0)

def test_black_bear_off():
    board = list(get_blank_board())
    board[10] = (15,0)
    board[1] = (0,15)
    assert is_valid_board(board)
    assert not black_can_bear_off(board)
    board[10] = (0,0)
    board[0] = (15,0)
    assert black_can_bear_off(board)
    roll = [1]
    next_boards = generate_next_boards(board, True, roll)
    assert len(next_boards) == 1
    assert next_boards[0][0] == (14, 0)
    assert next_boards[0][BLACK_OFF_INDEX] == (1, 0)
    roll = [2]
    next_boards = generate_next_boards(board, True, roll)
    assert len(next_boards) == 1
    assert next_boards[0][0] == (14, 0)
    assert next_boards[0][BLACK_OFF_INDEX] == (1, 0)
    board = list(get_blank_board())
    board[10] = (0,15)
    board[1] = (15,0)
    roll = [3,1]
    next_boards = generate_next_boards(board, True, roll)
    assert len(next_boards) == 1
    assert next_boards[0][0] == (1, 0)
    assert next_boards[0][1] == (13, 0)
    assert next_boards[0][BLACK_OFF_INDEX] == (1, 0)

def test_white_bear_off():
    board = list(get_blank_board())
    board[10] = (15,0)
    board[15] = (0,15)
    assert is_valid_board(board)
    assert not white_can_bear_off(board)
    board[15] = (0,0)
    board[23] = (0,15)
    assert white_can_bear_off(board)
    roll = [1]
    next_boards = generate_next_boards(board, False, roll)
    assert len(next_boards) == 1
    assert next_boards[0][23] == (0, 14)
    assert next_boards[0][WHITE_OFF_INDEX] == (0, 1)
    roll = [2]
    next_boards = generate_next_boards(board, False, roll)
    assert len(next_boards) == 1
    assert next_boards[0][23] == (0, 14)
    assert next_boards[0][WHITE_OFF_INDEX] == (0, 1)
    board = list(get_blank_board())
    board[10] = (15,0)
    board[22] = (0,15)
    roll = [3,1]
    next_boards = generate_next_boards(board, False, roll)
    assert len(next_boards) == 1
    assert next_boards[0][23] == (0, 1)
    assert next_boards[0][22] == (0, 13)
    assert next_boards[0][WHITE_OFF_INDEX] == (0, 1)
 
def test_utility_functions():
    board = list(get_blank_board())
    board[0] = (15,0)
    board[1] = (0,15)
    assert is_valid_board(board)
    board = list(get_blank_board())
    board[0] = (15,15)
    assert not is_valid_board(board)
    assert is_valid_board(get_initial_board())
    assert roll_dice()
    assert not black_wins(get_initial_board())
    assert not white_wins(get_initial_board())
    board = list(get_blank_board())
    board[BLACK_OFF_INDEX] = (15, 0)
    board[1] = (0, 15)
    assert black_wins(board)
    assert not white_wins(board)
    board = list(get_blank_board())
    board[WHITE_OFF_INDEX] = (0, 15)
    board[1] = (15, 0)
    assert not black_wins(board)
    assert white_wins(board)

def test_hit_from_bear_on_white():
    board = list(get_blank_board())
    board[WHITE_BAR_INDEX] = (0,15)
    board[1] = (1,0)
    board[3] = (14,0)
    roll = [2,2,2,2]
    next_boards = generate_next_boards(board, False, roll)
    board[WHITE_BAR_INDEX] = (0,11)
    board[1] = (0,4)
    board[BLACK_BAR_INDEX] = (1,0)
    board = tuple(board)
    assert board in next_boards

def test_hit_from_bear_on_black():
    board = list(get_blank_board())
    board[BLACK_BAR_INDEX] = (15,0)
    board[23] = (0,1)
    board[0] = (0,14)
    roll = [1,1,1,1]
    next_boards = generate_next_boards(board, True, roll)
    board[BLACK_BAR_INDEX] = (11,0)
    board[23] = (4,0)
    board[WHITE_BAR_INDEX] = (0,1)
    board = tuple(board)
    assert board in next_boards

def test_use_larger():
    board = list(get_blank_board())
    board[11] = (2,0)
    board[10] = (2,0)
    board[9] = (2,0)
    board[8] = (2,0)
    board[7] = (2,0)
    board[6] = (3,0)
    board[5] = (0,14)
    board[4] = (1,0)
    board[3] = (1,0)
    board[1] = (0,1)
    roll = [2,3]
    next_boards = generate_next_boards(board, False, roll)
    assert len(next_boards) == 1
    board[1] = (0,0)
    board[4] = (0,1)
    board[BLACK_BAR_INDEX] = (1,0)
    board = tuple(board)
    assert board in next_boards

def test():
    test_utility_functions()
    test_move_prioritization()
    test_black_enter_from_bar()
    test_white_enter_from_bar()
    test_white_hit()
    test_black_hit()
    test_no_move()
    test_black_bear_off()
    test_white_bear_off()
    test_hit_from_bear_on_white()
    test_hit_from_bear_on_black()
    test_use_larger()


def do_black_turn(board):
    roll = roll_dice()
    next_boards = generate_next_boards(board, True, roll)
    print 'Black rolls {}'.format(roll)
    next_board = random.choice(next_boards)
    visualize_board(next_board)
    raw_input()
    print
    return next_board, (black_wins(next_board) or white_wins(next_board))

def do_white_turn(board):
    roll = roll_dice()
    next_boards = generate_next_boards(board, False, roll)
    print 'White rolls {}'.format(roll)
    for i, next_board in enumerate(next_boards):
        print
        print '{}.'.format(i)
        visualize_board(next_board)

    choice = raw_input()
    if choice:
        try:
            choice = int(choice)
        except ValueError:
            choice = None

    if choice and 0 <= choice < len(next_boards):
        next_board = next_boards[choice]
    else:
        next_board = random.choice(next_boards)
    print 
    print
    visualize_board(next_board)
    print
    return next_board, (black_wins(next_board) or white_wins(next_board))

def game_loop():
    board = get_initial_board()
    is_black_turn = random.randint(0,1)
    finished = False
    while not finished:
        if is_black_turn:
            board, finished = do_black_turn(board)
            is_black_turn = False
        else:
            board, finished = do_white_turn(board)
            is_black_turn = True
    message = 'Black WINS!' if black_wins(board) else 'White WINS!'
    print message


if __name__ == "__main__":
    test()
    game_loop()
