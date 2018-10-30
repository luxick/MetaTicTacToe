import copy


class WrongBoardError(Exception):
    pass


class FieldTakenError(Exception):
    pass


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

        if self.assert_board_winner(bd, br):
            # The Board has already finished
            raise WrongBoardError

        if self._state[bd][br][fd][fr]:
            # The field is already taken
            raise FieldTakenError

        self._state[bd][br][fd][fr] = marker
        self._next = (fd, fr)

        if self.assert_board_winner(bd, br):
            # The board was finished by this mark
            self._next = None

        if self.assert_board_winner(fd, fr):
            # The next player would have to play in a finished board
            self._next = None

        return self._next

    def assert_board_winner(self, bd, br):
        board = self._state[bd][br]
        if type(board) is not list:
            return board

        winner = self._assert_board(board)
        if winner:
            self._state[bd][br] = winner
        return winner

    def assert_meta_winner(self):
        board = copy.deepcopy(self._state)
        for x in range(3):
            for y in range(3):
                winner = self.assert_board_winner(x, y)
                board[x][y] = winner
        return self._assert_board(board)

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
    def _assert_row(board):
        for row in board:
            if len(set(row)) == 1 and None not in set(row):
                return row[0]
        return None

    @staticmethod
    def _assert_diagonals(board):
        if len(set([board[i][i] for i in range(len(board))])) == 1:
            return board[0][0]
        if len(set([board[i][len(board) - i - 1] for i in range(len(board))])) == 1:
            return board[0][len(board) - 1]
        return None

    def _assert_board(self, board):
        # Transposition to check rows, then columns
        for newBoard in [board, zip(*board)]:
            result = self._assert_row(newBoard)
            if result:
                return result
        return self._assert_diagonals(board)

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
