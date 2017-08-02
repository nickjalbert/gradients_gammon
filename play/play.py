import os
import time
import random

from learn.random_mover import RandomMover
from learn.neural_net import NeuralNetMover, DumbNeuralNetMover
from backgammon.boards import generate_next_boards
from backgammon.utility import (get_initial_board, roll_dice, black_wins, 
                                white_wins)

BLACK_SAVE_PATH = 'data/black_save_state_{}.pkl'
BLACK_LOAD_PATH = 'black_load_me.pkl'
WHITE_SAVE_PATH = 'data/white_save_state_{}.pkl'
WHITE_LOAD_PATH = 'white_load_me.pkl'

BLACK = 'black'
WHITE = 'white'

def play_games(count, black, white):
    print 'Playing {} games of backgammon...'.format(count)
    black_wins = 0
    white_wins = 0
    start_time = time.time()
    for i in range(count):
        black_won = play_game(black, white)
        black_wins += 1 if black_won else 0
        white_wins += 0 if black_won else 1
        if i % 100 == 99:
            black.save_state(BLACK_SAVE_PATH.format(i+1))
            white.save_state(WHITE_SAVE_PATH.format(i+1))
        if i % 10 == 9 or i == 0:
            elapsed_time = time.time() - start_time
            report_game_rate(i+1, elapsed_time)
    elapsed_time = time.time() - start_time
    report_game_rate(count, elapsed_time)
    report_win_results(black_wins, white_wins)
    return black_wins

def report_win_results(black_wins, white_wins):
    count = black_wins + white_wins
    print '\nBlack wins: {0} ({1:.2f}%)'.format(
            black_wins, float(black_wins)*100/count)
    print 'White wins: {0} ({1:.2f}%)'.format(
            white_wins, float(white_wins)*100/count)

def report_game_rate(games, elapsed):
    game_rate = games/elapsed
    description = "games per second"
    if game_rate < 1.0:
        game_rate = elapsed/games
        description = "seconds per game"
    print '\nRan {0} games in {1:.2f} sec ({2:.2f} {3})'.format(
            games, elapsed, game_rate, description)
 
def play_game(black, white):
    is_black_turn = random.choice([True, False])
    board = get_initial_board()
    while not black_wins(board) and not white_wins(board):
        roll = roll_dice()
        boards = generate_next_boards(board, is_black_turn, roll)
        if is_black_turn:
            board_index = black.move(is_black_turn, roll, board, boards)
        else: 
            board_index = white.move(is_black_turn, roll, board, boards)
        board = boards[board_index]
        black.save_move(is_black_turn, board)
        white.save_move(is_black_turn, board)
        is_black_turn = not is_black_turn
    black_won = black_wins(board)
    white_won = white_wins(board)
    assert black_won or white_won
    assert not (black_won and white_won)
    black.record_outcome(black_won)
    black.learn()
    white.record_outcome(black_won)
    white.learn()
    return black_wins(board)

def report_confidence_interval(games, wins, protag_desc, antag_desc):
    Z = 2.5759
    E = Z/(2*(games)**.5)
    observed_wins = float(wins)/games
    win_floor = max(0.0, observed_wins - E)
    win_ceil = min(1.0, observed_wins + E)
    print ('99% chance that the true win percentage of {0} against {1} is '
           'in interval [{2:.4f}, {3:.4f}]').format(
                   protag_desc, antag_desc, win_floor, win_ceil)

if __name__ == '__main__':
    black = RandomMover()
    if os.path.exists(BLACK_LOAD_PATH):
        print 'Loading black saved state found in {}'.format(BLACK_LOAD_PATH)
        black.load_state(BLACK_LOAD_PATH)
    white = NeuralNetMover()
    if os.path.exists(WHITE_LOAD_PATH):
        print 'Loading white saved state found in {}'.format(WHITE_LOAD_PATH)
        white.load_state(WHITE_LOAD_PATH)
    play_games(10000, black, white)
