from utility import (BLACK_INDEX, WHITE_INDEX, BLACK_BAR_INDEX,
                     WHITE_BAR_INDEX, BLACK_OFF_INDEX, WHITE_OFF_INDEX,
                     is_valid_board)


def visualize_board(board):
    """Prints ASCII visualization of the <board>."""
    assert is_valid_board(board)
    def _get_pos(board, position):
        tens = max(board[position][WHITE_INDEX]/10,
                   board[position][BLACK_INDEX]/10)
        zeros = max(board[position][WHITE_INDEX]%10,
                    board[position][BLACK_INDEX]%10)
        is_white = board[position][WHITE_INDEX] > board[position][BLACK_INDEX]
        color = 'W' if is_white else 'B'
        if (tens == 0) and (zeros == 0):
            zeros = ' '
            color = '_'
        if tens == 0:
            tens = ' '
        return tens, zeros, color

    tens0, ones0, color0 = _get_pos(board, 0)
    tens1, ones1, color1 = _get_pos(board, 1)
    tens2, ones2, color2 = _get_pos(board, 2)
    tens3, ones3, color3 = _get_pos(board, 3)
    tens4, ones4, color4 = _get_pos(board, 4)
    tens5, ones5, color5 = _get_pos(board, 5)
    tens6, ones6, color6 = _get_pos(board, 6)
    tens7, ones7, color7 = _get_pos(board, 7)
    tens8, ones8, color8 = _get_pos(board, 8)
    tens9, ones9, color9 = _get_pos(board, 9)
    tens10, ones10, color10 = _get_pos(board, 10)
    tens11, ones11, color11 = _get_pos(board, 11)
    tens12, ones12, color12 = _get_pos(board, 12)
    tens13, ones13, color13 = _get_pos(board, 13)
    tens14, ones14, color14 = _get_pos(board, 14)
    tens15, ones15, color15 = _get_pos(board, 15)
    tens16, ones16, color16 = _get_pos(board, 16)
    tens17, ones17, color17 = _get_pos(board, 17)
    tens18, ones18, color18 = _get_pos(board, 18)
    tens19, ones19, color19 = _get_pos(board, 19)
    tens20, ones20, color20 = _get_pos(board, 20)
    tens21, ones21, color21 = _get_pos(board, 21)
    tens22, ones22, color22 = _get_pos(board, 22)
    tens23, ones23, color23 = _get_pos(board, 23)
    tensbb, onesbb, colorbb = _get_pos(board, BLACK_BAR_INDEX)
    if tensbb == ' ' and onesbb == ' ':
        colorbb = ' '
    tenswb, oneswb, colorwb = _get_pos(board, WHITE_BAR_INDEX)
    if tenswb == ' ' and oneswb == ' ':
        colorwb = ' '
    tensbo, onesbo, colorbo = _get_pos(board, BLACK_OFF_INDEX)
    if tensbo == ' ' and onesbo == ' ':
        colorbo = ' '
    tenswo, oneswo, colorwo = _get_pos(board, WHITE_OFF_INDEX)
    if tenswo == ' ' and oneswo == ' ':
        colorwo = ' '
    print
    print '|  .  .  .  .  .  .  |   |  .  .  .  .  .  .  |'
    print '|  {}  {}  {}  {}  {}  {}  | {} |  {}  {}  {}  {}  {}  {}  | {}'.format(tens11,tens10,tens9,tens8,tens7,tens6,tensbb,tens5,tens4,tens3,tens2,tens1,tens0,tensbo)
    print '|  {}  {}  {}  {}  {}  {}  | {} |  {}  {}  {}  {}  {}  {}  | {}'.format(ones11,ones10,ones9,ones8,ones7,ones6,onesbb,ones5,ones4,ones3,ones2,ones1,ones0,onesbo)
    print '|  {}  {}  {}  {}  {}  {}  | {} |  {}  {}  {}  {}  {}  {}  | {}'.format(color11,color10,color9,color8,color7,color6,colorbb,color5,color4,color3,color2,color1,color0,colorbo)
    print '|                    |   |                    |'
    print '|                    |   |                    |'
    print '|  {}  {}  {}  {}  {}  {}  | {} |  {}  {}  {}  {}  {}  {}  | {}'.format(tens12,tens13,tens14,tens15,tens16,tens17,tenswb,tens18,tens19,tens20,tens21,tens22,tens23,tenswo)
    print '|  {}  {}  {}  {}  {}  {}  | {} |  {}  {}  {}  {}  {}  {}  | {}'.format(ones12,ones13,ones14,ones15,ones16,ones17,oneswb,ones18,ones19,ones20,ones21,ones22,ones23,oneswo)
    print '|  {}  {}  {}  {}  {}  {}  | {} |  {}  {}  {}  {}  {}  {}  | {}'.format(color12,color13,color14,color15,color16,color17,colorwb,color18,color19,color20,color21,color22,color23, colorwo)
    print '|  .  .  .  .  .  .  |   |  .  .  .  .  .  .  |'
    print


