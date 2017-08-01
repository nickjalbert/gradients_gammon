class BasePlayer(object):
    def move(self, board_list):
        raise NotImplementedError('move() not implemented')

    def learn(self):
        raise NotImplementedError('learn() not implemented')


class BaseMoveTracker(object):
    def reset_move_tracking(self):
        self.black_moves = []
        self.white_moves = []
        self.black_payoff = 0
        self.white_payoff = 0

    def save_move(self, is_black_turn, board):
        if is_black_turn:
            self.black_moves.append(board) 
        else:
            self.white_moves.append(board)

    def record_outcome(self, black_won):
        self.black_payoff = 1 if black_won else -1
        self.white_payoff = 1 if not black_won else -1

    def assert_moves_were_tracked(self):
        assert len(self.black_moves) > 0
        assert len(self.white_moves) > 0
        assert self.black_payoff != 0
        assert self.white_payoff != 0
