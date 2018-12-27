import copy
from enum import IntEnum
from dataclasses import dataclass
from queue import Queue


class WrongBoardError(Exception):
    pass


class FieldTakenError(Exception):
    pass


class Result(IntEnum):
    Draw = 0,
    PlayerOne = 1,
    PlayerTwo = 2,
    Ongoing = 3


@dataclass
class Player:
    """
    Class to hold player data and the mark symbol used in the game logic
    """
    name: str
    mark: int
    time: float = 0.0

    def __init__(self, name):
        self.name = name


@dataclass
class State:
    """State object to hold the complete state of the game"""
    board: list
    current_player: Player
    players: Queue
    next_board: tuple = None
    play_time: int = 0
    result: Result = Result.Ongoing

    def __init__(self, board: list, player1: Player, player2: Player):
        self.board = board
        player1.mark = 1
        player2.mark = 2
        self.players = Queue(2)
        self.players.put(player2)
        self.current_player = player1


class Logic:
    @staticmethod
    def mark(state: State,
             board_x: int, board_y: int,
             field_x: int, field_y: int):

        if state.next_board and state.next_board != (board_x, board_y):
            # Player not checking in the right board
            raise WrongBoardError

        result = Game.check_board(state.board[board_x][board_y])
        if result is not Result.Ongoing:
            # The Board has already finished
            raise WrongBoardError

        if state.board[board_x][board_y][field_x][field_y]:
            # The field is already taken
            raise FieldTakenError

        marker = state.current_player.mark
        state.board[board_x][board_y][field_x][field_y] = marker
        state.next_board = (field_x, field_y)

        # Check if the next field mark is free choice
        result = Game.check_board(state.board[field_x][field_y])
        if result is not Result.Ongoing:
            state.next_board = None

        return state.next_board

    @staticmethod
    def check_meta_board(state: State) -> Result:
        meta = copy.deepcopy(state.board)
        for x in range(3):
            for y in range(3):
                board = meta[x][y]
                result = Game.check_board(board)
                if result == Result.Ongoing:
                    result = None
                meta[x][y] = result
        return Logic.check_board(meta)

    @staticmethod
    def check_board(board: list) -> Result:
        # Transposition to check rows, then columns
        for newBoard in [board, zip(*board)]:
            winner = Logic.check_row(newBoard)
            if winner:
                return winner
        winner = Logic.check_diagonals(board)
        if winner:
            return Result(winner)
        # No more 'None' entries left -> board is a drawexcecute
        still_open = set([y for x in board for y in x if y is None])
        if not still_open:
            return Result.Draw
        return Result.Ongoing

    @staticmethod
    def check_row(board: list):
        for row in board:
            if len(set(row)) == 1 and None not in set(row):
                return row[0]
        return None

    @staticmethod
    def check_diagonals(board: list):
        if len(set([board[i][i] for i in range(len(board))])) == 1:
            return board[0][0]
        if len(set([board[i][len(board) - i - 1] for i in
                    range(len(board))])) == 1:
            return board[0][len(board) - 1]
        return None

    @staticmethod
    def create_board():
        return [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    @staticmethod
    def create_metaboard():
        board = Logic.create_board()
        for row in board:
            for i in range(len(row)):
                row[i] = Logic.create_board()
        return board


class Game(Logic):
    """Main game class. Use this class to execute the game logic"""
    def __init__(self, state: State):
        self.state = state

    def reset_board(self):
        self.state.board = self.create_metaboard()

    def mark(self,
             board_x: int, board_y: int,
             field_x: int, field_y: int) -> tuple:
        return super().mark(self.state, board_x, board_y, field_x, field_y)

    def check_board_by_idx(self, board_x: int, board_y: int):
        return super().check_board(self.state.board[board_x][board_y])

    def check_meta_board(self) -> Result:
        return super().check_meta_board(self.state)

    def current_player(self) -> Player:
        return self.state.current_player

    def next_player(self) -> Player:
        self.state.players.put(self.state.current_player)
        nxt = self.state.players.get()
        self.state.current_player = nxt
        return nxt


