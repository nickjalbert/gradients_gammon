'''
Pits the random mover against a trained neural net and reports 99% confidence
interval of true win rate of the neural net.
'''

import os
import sys

from learn.random_mover import RandomMover
from learn.neural_net import DumbNeuralNetMover
from play import play_games


if __name__ == '__main__':
    black = RandomMover()
    white = DumbNeuralNetMover()
    if not len(sys.argv) == 2:
        print 'Usage: python {} [path/to/NN.pkl]'.format(sys.argv[0])
        sys.exit(0)
    load_path = sys.argv[1]
    if os.path.exists(load_path):
        print 'Loading white saved state found in {}'.format(load_path)
        white.load_state(load_path)
    else:
        print 'Pickle file not found...'
        sys.exit(0)
    total_games = 100
    black_wins = play_games(total_games, black, white)
    Z = 2.5759
    E = Z/(2*(total_games)**.5)
    observed_wins = float(total_games - black_wins)/total_games
    win_floor = max(0.0, observed_wins - E)
    win_ceil = min(1.0, observed_wins + E)
    print '99% chance that the true win percentage of the NN against a random mover is in interval [{0:.4f}, {1:.4f}]'.format(win_floor, win_ceil)

