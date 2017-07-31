import random
import time

from learn import random_mover
from backgammon.boards import generate_next_boards
from backgammon.utility import (get_initial_board, roll_dice, black_wins, 
                                white_wins)

def play_games(count, black, white):
    print 'Playing {} games of backgammon...'.format(count)
    black_wins = 0
    white_wins = 0
    start_time = time.time()
    for i in range(count):
        black_won = play_game(black, white)
        black_wins += 1 if black_won else 0
        white_wins += 0 if black_won else 1
        if i % 10 == 0:
            elapsed_time = time.time() - start_time
            print 'Ran {0} games in {1:.2f} sec ({2:.2f} games/sec)'.format(
                    i, elapsed_time, i/elapsed_time)

    print
    print 'Black win percentage: {0:.2f}%'.format(float(black_wins)*100/count)
    print 'White win percentage: {0:.2f}%'.format(float(white_wins)*100/count)
    elapsed_time = time.time() - start_time
    print 'Total runtime: {0:.2f} sec ({1:.2f} games/sec)'.format(
            elapsed_time, count/elapsed_time)


def play_game(black, white):
    is_black_turn = random.choice([True, False])
    board = get_initial_board()
    while not black_wins(board) and not white_wins(board):
        roll = roll_dice()
        boards = generate_next_boards(board, is_black_turn, roll)
        board = black.move(boards) if is_black_turn else white.move(boards)
        is_black_turn = not is_black_turn
    assert black_wins(board) or white_wins(board)
    assert not (black_wins(board) and white_wins(board))
    return black_wins(board)

if __name__ == '__main__':
    play_games(100, random_mover, random_mover)
