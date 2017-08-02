'''
Pits a random mover against another random mover and reports 99% confidence
interval of true win rate of the neural net.
'''

import os
import sys

from learn.random_mover import RandomMover
from learn.neural_net import DumbNeuralNetMover
from play import play_games, report_confidence_interval


if __name__ == '__main__':
    black = RandomMover()
    white = RandomMover()
    total_games = 1024
    black_wins = play_games(total_games, black, white)
    white_wins = total_games - black_wins
    nn_desc = 'Random Mover 1'
    random_desc = 'Random Mover 2'
    report_confidence_interval(total_games, white_wins, nn_desc, random_desc)


