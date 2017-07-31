import unittest

from utility import (BLACK_INDEX, WHITE_INDEX, BLACK_BAR_INDEX,
                     WHITE_BAR_INDEX, BLACK_OFF_INDEX, WHITE_OFF_INDEX,
                     get_blank_board, get_initial_board, black_wins,
                     white_wins, is_valid_board, roll_dice,
                     can_bear_off, position_is_outer, swap_colors)
from boards import generate_next_boards


class TestUtilities(unittest.TestCase):
    def test_get_blank_board(self):
        board = get_blank_board()
        board[0] = (15,0)
        board[1] = (0,15)
        self.assertTrue(is_valid_board(board))
        board = get_blank_board()
        board[0] = (15,15)
        self.assertFalse(is_valid_board(board))

    def test_get_initial_board(self):
        self.assertTrue(is_valid_board(get_initial_board()))

    def test_black_wins(self):
        self.assertFalse(black_wins(get_initial_board()))
        board = get_blank_board()
        board[BLACK_OFF_INDEX] = (15, 0)
        board[1] = (0, 15)
        self.assertTrue(black_wins(board))
        self.assertFalse(white_wins(board))

    def test_white_wins(self):
        self.assertFalse(white_wins(get_initial_board()))
        board = get_blank_board()
        board[WHITE_OFF_INDEX] = (0, 15)
        board[1] = (15, 0)
        self.assertTrue(white_wins(board))
        self.assertFalse(black_wins(board))

    def test_roll_dice(self):
        self.assertIsNotNone(roll_dice())

    def test_can_bear_off(self):
        board = get_blank_board()
        board[10] = (15,0)
        board[15] = (0,15)
        self.assertTrue(is_valid_board(board))
        self.assertFalse(can_bear_off(board))
        board[15] = (0,0)
        board[23] = (0,15)
        self.assertTrue(can_bear_off(board))

    def test_position_is_outer(self):
        board = get_blank_board()
        board[10] = (15,0)
        board[15] = (0,13)
        board[16] = (0,2)
        self.assertTrue(is_valid_board(board))
        self.assertFalse(position_is_outer(board, 16))
        self.assertTrue(position_is_outer(board, 15))


class TestBackgammonRules(unittest.TestCase):
    def test_move_prioritization(self):
        """
        Ensure we don't return:
            board[2] = (0,15)
            board[4] = (15,0)
        as a next board because you must use the max number of rolls possible.
        """
        board = get_blank_board()
        board[1] = (0,1)
        board[2] = (0,14)
        board[4] = (15,0)
        self.assertTrue(is_valid_board(board))
        roll = [2,1]
        next_boards = generate_next_boards(board, False, roll)
        self.assertEqual(len(next_boards), 2)
        board1 = get_blank_board()
        board1[2]= (0,13)
        board1[3]= (0,2)
        board1[4]= (15,0)
        self.assertIn(board1, next_boards)
        board2 = get_blank_board()
        board2[1]= (0,1)
        board2[2]= (0,13)
        board2[4]= (15,0)
        board2[5]= (0,1)
        self.assertIn(board2, next_boards)

    def test_black_enter_from_bar(self):
        board = get_blank_board()
        board[BLACK_BAR_INDEX] = (15, 0)
        board[23] = (0, 15)
        self.assertTrue(is_valid_board(board))
        roll = [2,1]
        next_boards = generate_next_boards(board, True, roll)
        self.assertEqual(len(next_boards), 1)
        self.assertEqual(next_boards[0][BLACK_BAR_INDEX], (14, 0))
        self.assertEqual(next_boards[0][23], (0, 15))
        self.assertEqual(next_boards[0][22], (1, 0))
        roll = [1,1,1,1]
        next_boards = generate_next_boards(board, True, roll)
        self.assertEqual(len(next_boards), 1)
        self.assertEqual(next_boards[0][BLACK_BAR_INDEX], (15, 0))
        self.assertEqual(next_boards[0][23], (0, 15))

    def test_white_enter_from_bar(self):
        board = get_blank_board()
        board[WHITE_BAR_INDEX] = (0, 15)
        board[0] = (15, 0)
        self.assertTrue(is_valid_board(board))
        roll = [2,1]
        next_boards = generate_next_boards(board, False, roll)
        self.assertEqual(len(next_boards), 1)
        self.assertEqual(next_boards[0][WHITE_BAR_INDEX], (0, 14))
        self.assertEqual(next_boards[0][0], (15, 0))
        self.assertEqual(next_boards[0][1], (0, 1))
        roll = [1,1,1,1]
        next_boards = generate_next_boards(board, False, roll)
        self.assertEqual(len(next_boards), 1)
        self.assertEqual(next_boards[0][WHITE_BAR_INDEX], (0, 15))
        self.assertEqual(next_boards[0][0], (15, 0))

    def test_white_hit(self):
        board = get_blank_board()
        board[23] = (1,0)
        board[22] = (0,15)
        board[3] = (14,0)
        roll = [1,1,1,1]
        next_boards = generate_next_boards(board, False, roll)
        self.assertEqual(len(next_boards), 3)
        for next_board in next_boards:
            self.assertEqual(next_board[BLACK_BAR_INDEX], (1,0))

    def test_black_hit(self):
        board = get_blank_board()
        board[1] = (0,1)
        board[2] = (15,0)
        board[3] = (0,14)
        roll = [1,1,1,1]
        next_boards = generate_next_boards(board, True, roll)
        self.assertEqual(len(next_boards), 4)
        for next_board in next_boards:
            self.assertEqual(next_board[WHITE_BAR_INDEX], (0,1))

    def test_no_move(self):
        board = get_blank_board()
        board[1] = (0,15)
        board[2] = (15,0)
        roll = [1,1,1,1]
        next_boards = generate_next_boards(board, True, roll)
        self.assertEqual(len(next_boards), 1)
        self.assertEqual(next_boards[0][1], (0,15))
        self.assertEqual(next_boards[0][2], (15,0))

    def test_black_bear_off(self):
        board = get_blank_board()
        board[1] = (0,15)
        board[0] = (15,0)
        self.assertTrue(is_valid_board(board))
        roll = [1]
        next_boards = generate_next_boards(board, True, roll)
        self.assertEqual(len(next_boards), 1)
        self.assertEqual(next_boards[0][0], (14, 0))
        self.assertEqual(next_boards[0][BLACK_OFF_INDEX], (1, 0))
        roll = [2]
        next_boards = generate_next_boards(board, True, roll)
        self.assertEqual(len(next_boards), 1)
        self.assertEqual(next_boards[0][0], (14, 0))
        self.assertEqual(next_boards[0][BLACK_OFF_INDEX], (1, 0))
        board = get_blank_board()
        board[10] = (0,15)
        board[1] = (15,0)
        roll = [3,1]
        next_boards = generate_next_boards(board, True, roll)
        self.assertEqual(len(next_boards), 1)
        self.assertEqual(next_boards[0][0], (1, 0))
        self.assertEqual(next_boards[0][1], (13, 0))
        self.assertEqual(next_boards[0][BLACK_OFF_INDEX], (1, 0))

    def test_white_bear_off(self):
        board = get_blank_board()
        board[10] = (15,0)
        board[15] = (0,0)
        board[23] = (0,15)
        self.assertTrue(is_valid_board(board))
        roll = [1]
        next_boards = generate_next_boards(board, False, roll)
        self.assertEqual(len(next_boards), 1)
        self.assertEqual(next_boards[0][23], (0, 14))
        self.assertEqual(next_boards[0][WHITE_OFF_INDEX], (0, 1))
        roll = [2]
        next_boards = generate_next_boards(board, False, roll)
        self.assertEqual(len(next_boards), 1)
        self.assertEqual(next_boards[0][23], (0, 14))
        self.assertEqual(next_boards[0][WHITE_OFF_INDEX], (0, 1))
        board = get_blank_board()
        board[10] = (15,0)
        board[22] = (0,15)
        roll = [3,1]
        next_boards = generate_next_boards(board, False, roll)
        self.assertEqual(len(next_boards), 1)
        self.assertEqual(next_boards[0][23], (0, 1))
        self.assertEqual(next_boards[0][22], (0, 13))
        self.assertEqual(next_boards[0][WHITE_OFF_INDEX], (0, 1))

    def test_hit_from_bear_on_white(self):
        board = get_blank_board()
        board[WHITE_BAR_INDEX] = (0,15)
        board[1] = (1,0)
        board[3] = (14,0)
        roll = [2,2,2,2]
        next_boards = generate_next_boards(board, False, roll)
        board[WHITE_BAR_INDEX] = (0,11)
        board[1] = (0,4)
        board[BLACK_BAR_INDEX] = (1,0)
        self.assertIn(board, next_boards)

    def test_hit_from_bear_on_black(self):
        board = get_blank_board()
        board[BLACK_BAR_INDEX] = (15,0)
        board[23] = (0,1)
        board[0] = (0,14)
        roll = [1,1,1,1]
        next_boards = generate_next_boards(board, True, roll)
        board[BLACK_BAR_INDEX] = (11,0)
        board[23] = (4,0)
        board[WHITE_BAR_INDEX] = (0,1)
        self.assertIn(board, next_boards)

    def test_use_larger(self):
        board = get_blank_board()
        board[11] = (2,0)
        board[10] = (2,0)
        board[9] = (2,0)
        board[8] = (2,0)
        board[7] = (2,0)
        board[6] = (3,0)
        board[5] = (0,14)
        board[4] = (1,0)
        board[3] = (1,0)
        board[1] = (0,1)
        roll = [2,3]
        next_boards = generate_next_boards(board, False, roll)
        self.assertEqual(len(next_boards), 1)
        board[1] = (0,0)
        board[4] = (0,1)
        board[BLACK_BAR_INDEX] = (1,0)
        self.assertIn(board, next_boards)

    def test_swap_colors(self):
        board = list(get_initial_board())
        board[0] = (0,0)
        board[1] = (1,0)
        board[5] = (4,0)
        board[WHITE_BAR_INDEX] = (0,2)
        board[23] = (0,0)
        board[BLACK_OFF_INDEX] = (2,0)
        self.assertTrue(is_valid_board(board))
        board = swap_colors(board)
        self.assertEqual(board[0], (0,0))
        self.assertEqual(board[1], (0,0))
        self.assertEqual(board[2], (0,0))
        self.assertEqual(board[3], (0,0))
        self.assertEqual(board[4], (0,0))
        self.assertEqual(board[5], (5,0))
        self.assertEqual(board[6], (0,0))
        self.assertEqual(board[7], (3,0))
        self.assertEqual(board[8], (0,0))
        self.assertEqual(board[9], (0,0))
        self.assertEqual(board[10], (0,0))
        self.assertEqual(board[11], (0,5))
        self.assertEqual(board[12], (5,0))
        self.assertEqual(board[13], (0,0))
        self.assertEqual(board[14], (0,0))
        self.assertEqual(board[15], (0,0))
        self.assertEqual(board[16], (0,3))
        self.assertEqual(board[17], (0,0))
        self.assertEqual(board[18], (0,4))
        self.assertEqual(board[19], (0,0))
        self.assertEqual(board[20], (0,0))
        self.assertEqual(board[21], (0,0))
        self.assertEqual(board[22], (0,1))
        self.assertEqual(board[23], (0,0))
        self.assertEqual(board[WHITE_BAR_INDEX], (0,0))
        self.assertEqual(board[BLACK_BAR_INDEX], (2,0))
        self.assertEqual(board[WHITE_OFF_INDEX], (0,2))
        self.assertEqual(board[BLACK_OFF_INDEX], (0,0))


if __name__ == '__main__':
    unittest.main()
