import random
from learn.basic import BaseMoveTracker, BasePlayer


class RandomMover(BaseMoveTracker, BasePlayer):
    def __init__(self):
        self.reset_move_tracking()

    def move(self, board_list):
        return random.choice(board_list)

    def learn(self):
        self.assert_moves_were_tracked()
        self.reset_move_tracking()

