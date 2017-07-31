import unittest
from utility import (BLACK_INDEX, WHITE_INDEX, BLACK_BAR_INDEX,
                     WHITE_BAR_INDEX, BLACK_OFF_INDEX, WHITE_OFF_INDEX,
                     get_blank_board, get_initial_board, black_wins,
                     white_wins, is_valid_board, roll_dice, 
                     black_can_bear_off, white_can_bear_off, 
                     black_position_is_outer, white_position_is_outer)
                     

class TestUtilities(unittest.TestCase):
    def test_get_blank_board(self):
        board = list(get_blank_board())
        board[0] = (15,0)
        board[1] = (0,15)
        self.assertTrue(is_valid_board(board))
        board = list(get_blank_board())
        board[0] = (15,15)
        self.assertFalse(is_valid_board(board))

    def test_get_initial_board(self):
        self.assertTrue(is_valid_board(get_initial_board()))

    def test_black_wins(self):
        self.assertFalse(black_wins(get_initial_board()))
        board = list(get_blank_board())
        board[BLACK_OFF_INDEX] = (15, 0)
        board[1] = (0, 15)
        self.assertTrue(black_wins(board))
        self.assertFalse(white_wins(board))

    def test_white_wins(self):
        self.assertFalse(white_wins(get_initial_board()))
        board = list(get_blank_board())
        board[WHITE_OFF_INDEX] = (0, 15)
        board[1] = (15, 0)
        self.assertTrue(white_wins(board))
        self.assertFalse(black_wins(board))

    def test_roll_dice(self):
        self.assertIsNotNone(roll_dice())

    def test_black_can_bear_off(self):
        board = list(get_blank_board())
        board[10] = (15,0)
        board[1] = (0,15)
        self.assertTrue(is_valid_board(board))
        self.assertFalse(black_can_bear_off(board))
        board[10] = (0,0)
        board[0] = (15,0)
        self.assertTrue(black_can_bear_off(board))

    def test_white_can_bear_off(self):
        board = list(get_blank_board())
        board[10] = (15,0)
        board[15] = (0,15)
        self.assertTrue(is_valid_board(board))
        self.assertFalse(white_can_bear_off(board))
        board[15] = (0,0)
        board[23] = (0,15)
        self.assertTrue(white_can_bear_off(board))

    def test_black_position_is_outer(self):
        board = list(get_blank_board())
        board[10] = (12,0)
        board[9] = (3,0)
        board[1] = (0,15)
        self.assertTrue(is_valid_board(board))
        self.assertFalse(black_position_is_outer(board, 9))
        self.assertTrue(black_position_is_outer(board, 10))

    def test_white_position_is_outer(self):
        board = list(get_blank_board())
        board[10] = (15,0)
        board[15] = (0,13)
        board[16] = (0,2)
        self.assertTrue(is_valid_board(board))
        self.assertFalse(white_position_is_outer(board, 16))
        self.assertTrue(white_position_is_outer(board, 15))

if __name__ == '__main__':
    unittest.main()
