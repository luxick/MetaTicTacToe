import copy
from enum import Enum


class WrongBoardError(Exception):
    pass


class FieldTakenError(Exception):
    pass


class GameResult(Enum):
    Draw = 0,
    Won = 1


class MetaTicTacToe:
    _next = None

    def __init__(self, board=None):
        if board:
            self._state = board
        else:
            self._state = self._make_metaboard()

    def mark(self, marker: str, bd: int, br: int, fd: int, fr: int):
        if self._next and self._next != (bd, br):
            # Player not checking in the right board
            raise WrongBoardError

        if self.check_board_winner(bd, br):
            # The Board has already finished
            raise WrongBoardError

        if self._state[bd][br][fd][fr]:
            # The field is already taken
            raise FieldTakenError

        self._state[bd][br][fd][fr] = marker
        self._next = (fd, fr)

        # Check if the board was finished with this mark
        self.check_board_winner(bd, br)

        if self.check_board_winner(fd, fr):
            # The next player would have to play in a finished board
            self._next = None

        return self._next

    def check_board_winner(self, bd, br):

        # If the state is a single value, the board has already finished
        state = self._state[bd][br]
        if type(state) is not list:
            return state

        winner = self._check_board(state)
        if winner:
            self._state[bd][br] = winner
        return winner

    def check_meta_winner(self):
        board = copy.deepcopy(self._state)
        for x in range(3):
            for y in range(3):
                winner = self.check_board_winner(x, y)
                board[x][y] = winner
        return self._check_board(board)

    @staticmethod
    def _make_board():
        return [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def _make_metaboard(self):
        board = self._make_board()
        for row in board:
            for i in range(len(row)):
                row[i] = self._make_board()
        return board

    @staticmethod
    def _check_row(board):
        for row in board:
            if len(set(row)) == 1 and None not in set(row):
                return row[0]
        return None

    @staticmethod
    def _check_diagonals(board):
        if len(set([board[i][i] for i in range(len(board))])) == 1:
            return board[0][0]
        if len(set([board[i][len(board) - i - 1] for i in range(len(board))])) == 1:
            return board[0][len(board) - 1]
        return None

    def _check_board(self, board):
        # Transposition to check rows, then columns
        for newBoard in [board, zip(*board)]:
            winner = self._check_row(newBoard)
            if winner:
                return winner
        winner = self._check_diagonals(board)
        if winner:
            return winner
        # No more 'None' entries left -> board is a draw
        still_open = set([y for x in board for y in x if y is None])
        if not still_open:
            return 'draw'
        return None

    def __getitem__(self, item):
        return self._state[item]

    def __str__(self):
        out = ''
        for x in range(3):
            out += ' ' + ' -------' * 3 + '\n'
            for z in range(3):
                out += ' | '
                for y in range(3):
                    out += ' '.join([x if x is not None else ' ' for x in self._state[x][y][z]])
                    out += ' | '
                out += '\n'
        out += ' ' + ' -------' * 3 + '\n'
        return out

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._state)
