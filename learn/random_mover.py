import random


class RandomMover(object):
    def __init__(self):
        self.black_moves = []
        self.white_moves = []
        self.black_payoff = 0
        self.white_payoff = 0

    def move(self, board_list):
        return random.choice(board_list)

    def save_move(self, is_black_turn, board):
        if is_black_turn:
            self.black_moves.append(board) 
        else:
            self.white_moves.append(board)

    def record_outcome(self, black_won):
        self.black_payoff = 1 if black_won else -1
        self.white_payoff = 1 if not black_won else -1

    def learn(self):
        assert len(self.black_moves) > 0
        assert len(self.white_moves) > 0
        assert self.black_payoff != 0
        assert self.white_payoff != 0
        self.black_moves = []
        self.white_moves = []
        self.black_payoff = 0
        self.white_payoff = 0

