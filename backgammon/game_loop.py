import random
from utility import get_initial_board

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
    game_loop()