import copy

from utility import (BLACK_INDEX, WHITE_INDEX, BLACK_BAR_INDEX,
                     WHITE_BAR_INDEX, BLACK_OFF_INDEX, WHITE_OFF_INDEX,
                     get_blank_board, get_initial_board, black_wins,
                     white_wins, is_valid_board, roll_dice,
                     black_can_bear_off, white_can_bear_off,
                     black_position_is_outer, white_position_is_outer)


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


