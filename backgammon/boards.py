import copy

from utility import (BLACK_INDEX, WHITE_INDEX, BLACK_BAR_INDEX,
                     WHITE_BAR_INDEX, BLACK_OFF_INDEX, WHITE_OFF_INDEX,
                     get_blank_board, get_initial_board, black_wins,
                     white_wins, is_valid_board, roll_dice,
                     can_bear_off, position_is_outer, swap_colors)


def generate_next_boards(board, is_black_turn, rolls):
    """ 
    Returns a list of all legal board transitions given the initial
    <board> and a list of rolls.
    """
    if is_black_turn:
        board = swap_colors(board)
    final_boards = []
    search_stack = []
    # [board, rolls, rolls_used]
    search_stack.append((board[:], rolls[:], []))
    while search_stack:
        board, rolls, used_rolls = search_stack.pop()
        # Check to see if we're at a leaf node
        if not rolls:
            final_boards.append((board, used_rolls))
            continue
        # For each roll, get all possible boards
        for i, roll in enumerate(rolls):
            next_boards = _get_all_boards(board, roll)
            next_rolls = rolls[:]
            next_rolls.pop(i)
            # Drop roll if it gives us no moves 
            if not next_boards:
                search_stack.append((board, next_rolls, used_rolls[:]))
            # Explore all states after this roll with remaning rolls
            for next_board in next_boards:
                next_used_rolls = used_rolls[:]
                next_used_rolls.append(roll)
                search_stack.append((next_board, next_rolls, next_used_rolls))
            # Don't explore all equivalent subtrees of doubles
            if len(set(rolls)) == 1:
                break
    final_boards = _choose_maximal_moves(final_boards)
    final_boards = _filter_equivalent_boards(final_boards)
    if is_black_turn:
        final_boards = [swap_colors(board) for board in final_boards]
    return final_boards


def _choose_maximal_moves(final_boards):
    """
    Filters out illegal transitions that are disallowed because they do not
    use the maximum number of moves.
    """
    # You are forced to use the maximum number of dies as possible
    max_moves = max(len(used_rolls) for (board, used_rolls) in final_boards)
    final_boards = [(board, used_rolls)
                    for (board, used_rolls) in final_boards
                    if len(used_rolls) == max_moves]
    # If you can choose between which die to use, you must use the greatest
    if max_moves == 1:
        max_roll = max(max(used_rolls)
                       for (board, used_rolls)
                       in final_boards)
        final_boards = [(board, used_rolls)
                        for (board, used_rolls) in final_boards
                        if max(used_rolls) == max_roll]
    return final_boards

def _filter_equivalent_boards(final_boards):
    """
    Filters out duplicate boards.
    """
    final_boards = set(tuple(board) for (board, used_rolls) in final_boards)
    return [list(board) for board in final_boards]

def _get_all_boards(board, roll):
    """
    Generates a list of all legal next boards given <board> and a roll. 
    Always assumes white is moving (swap_colors as necessary).
    """
    if board[WHITE_BAR_INDEX][WHITE_INDEX] > 0:
        return _handle_bar_pieces(board, roll)
    all_boards = []
    for position, (black_count, white_count) in enumerate(board):
        if position < 0 or position > 23:
            continue
        if white_count == 0:
            continue
        target = position + roll
        if (target > 23 and 
                can_bear_off(board) and position_is_outer(board, position)):
            target = WHITE_OFF_INDEX
        elif target == 24 and can_bear_off(board):
            target = WHITE_OFF_INDEX
        elif target > 23:
            continue
        new_board = _move_to_board_position(board, position, target)
        if is_valid_board(new_board):
            all_boards.append(new_board)
    return all_boards

def _handle_bar_pieces(board, roll):
    target_index = -1 + roll
    board = _move_to_board_position(board, WHITE_BAR_INDEX, target_index)
    if is_valid_board(board):
        return [board]
    return []

def _move_to_board_position(board, start, end):
    board = board[:]
    black_count, white_count = board[start]
    board[start] = (black_count, white_count - 1)
    black_end_count, white_end_count = board[end]
    if black_end_count == 1:
        board[end] = (0, white_end_count + 1)
        bar_black_count, bar_white_count = board[BLACK_BAR_INDEX]
        board[BLACK_BAR_INDEX] = (bar_black_count + 1, bar_white_count)
    else:
        board[end] = (black_end_count, white_end_count + 1)
    return board

