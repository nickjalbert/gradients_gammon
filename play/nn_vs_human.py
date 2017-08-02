'''
Pits a trained neural net against a random mover and reports 99% confidence
interval of true win rate of the neural net.

Pass in path to the NN state pickle.
'''

import os
import sys

from learn.random_mover import RandomMover
from learn.neural_net import DumbNeuralNetMover
from learn.human import HumanMover
from play import play_games, report_confidence_interval


if __name__ == '__main__':
    black = DumbNeuralNetMover()
    white = HumanMover()
    if not len(sys.argv) == 2:
        print 'Usage: python {} [path/to/NN.pkl]'.format(sys.argv[0])
        sys.exit(0)
    load_path = sys.argv[1]
    if os.path.exists(load_path):
        print 'Loading white saved state found in {}'.format(load_path)
        black.load_state(load_path)
    else:
        print 'Pickle file not found...'
        sys.exit(0)
    total_games = 1
    black_wins = play_games(total_games, black, white)
    white_wins = total_games - black_wins
    nn_desc = 'the NN Mover ({})'.format(load_path)
    random_desc = 'the Human'
    report_confidence_interval(total_games, white_wins, nn_desc, random_desc)


