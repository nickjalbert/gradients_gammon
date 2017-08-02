import random
from learn.basic import BaseMoveTracker, BasePlayer
from backgammon.visualize import visualize_board


class HumanMover(BaseMoveTracker, BasePlayer):
    def __init__(self):
        self.reset_move_tracking()

    def move(self, is_black_turn, roll, current_board, board_list):
        for i, board in enumerate(board_list):
            print "{}.".format(i)
            visualize_board(board)
        print
        print '-------'
        print 'Roll is {}'.format(roll)
        visualize_board(current_board)
        choice = raw_input('Move? ')
        try:
            choice = int(choice)
        except ValueError:
            choice = None
        if (choice is None) or (choice < 0) or (choice >= len(board_list)):
            return random.choice(range(len(board_list)))
        return choice

    def learn(self):
        self.assert_moves_were_tracked()
        self.reset_move_tracking()

    def save_state(self, path):
        pass
    
    def load_state(self, path):
        pass

