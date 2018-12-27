import copy
import unittest

from mttt import Game


class TikTakToeTester(unittest.TestCase):
    p1 = "X"
    p2 = "O"

    b00 = [[None, None, None],
           [None, None, None],
           [None, None, None]]

    b01 = [[None, None, None],
           [None, None, None],
           [None, None, None]]

    b02 = [[None, None, None],
           [None, None, None],
           [None, None, None]]

    b10 = [[None, None, None],
           [None, None, None],
           [None, None, None]]

    b20 = [[None, None, None],
           [None, None, None],
           [None, None, None]]

    b11 = [[None, None, None],
           [None, None, None],
           [None, None, None]]

    b12 = [[None, None, None],
           [None, None, None],
           [None, None, None]]

    b21 = [[None, None, None],
           [None, None, None],
           [None, None, None]]

    b22 = [[None, None, None],
           [None, None, None],
           [None, None, None]]

    test_board = [[b00, b01, b02],
                  [b10, b11, b12],
                  [b20, b21, b22]]

    def test_create_board(self):
        # Set up empty game board
        game = Game()
        self.assertEqual(self.test_board, game._state)

    def test_wrong_board(self):
        """
        A player must check in the correct board corresponding to the field checked by the last player
        """
        game = Game()
        game.mark(self.p1, 0, 0, 1, 1)
        res = game.mark(self.p2, 2, 2, 1, 1, )
        self.assertEqual('Invalid Move', res)

    def test_victory_column(self):
        board = copy.deepcopy(self.test_board)
        board[0][0] = [["X", None, None],
                       ["X", None, None],
                       ["X", None, None]]
        game = Game(board)
        self.assertEqual("X", game.check_board_winner(0, 0))

    def test_victory_row(self):
        board = copy.deepcopy(self.test_board)
        board[0][0] = [[None, None, None],
                       ["X", "X", "X"],
                       [None, None, None]]
        game = Game(board)
        self.assertEqual("X", game.check_board_winner(0, 0))

    def test_victory_diagonal(self):
        board = copy.deepcopy(self.test_board)
        board[0][0] = [[None, None, "X"],
                       [None, "X", None],
                       ["X", None, None]]
        game = Game(board)
        self.assertEqual("X", game.check_board_winner(0, 0))

        board[0][0] = [["X", None, None],
                       [None, "X", None],
                       [None, None, "X"]]
        game = Game(board)
        self.assertEqual("X", game.check_board_winner(0, 0))

    def test_meta_victory(self):
        board = copy.deepcopy(self.test_board)
        # Player X wins board 0-0 and 0-1
        board[0][0] = [[None, None, None],
                       ["X", "X", "X"],
                       [None, None, None]]
        board[0][1] = [[None, None, None],
                       ["X", "X", "X"],
                       [None, None, None]]
        game = Game(board)
        self.assertIsNone(game.check_meta_board())

        # Player X finishes by winning board 0-2
        game._state[0][2] = [[None, None, None],
                             ["X", "X", "X"],
                             [None, None, None]]

        self.assertEqual("X", game.check_meta_board())
        pass


if __name__ == '__main__':
    unittest.main()
