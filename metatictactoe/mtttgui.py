import arcade
import sys
import os

from enum import Enum
from queue import Queue

from start_screen import SetupScreen
from mttt import MetaTicTacToe, WrongBoardError, FieldTakenError

VERSION = 1.0

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

MIN_WIDTH = 800
MIN_HEIGHT = 550

MARGIN = 30

COLOR_VALID = 242, 250, 234
COLOR_INVALID = 250, 234, 234

COLOR_PANEL_BG = 226, 226, 226, 255


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class GameState(Enum):
    Setup = 0
    Running = 1
    Finished = 2


class GameResult(Enum):
    Draw = 0,
    Won = 1


class Player:
    def __init__(self, name, mark):
        self.name = name
        self.mark = mark
        self.play_time = 0.0


class GameUI(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, f'Meta Tic Tac Toe v{VERSION}', resizable=True)
        self.set_min_size(MIN_WIDTH, MIN_HEIGHT)
        self.background = None
        self.total_time = 0.0

        self.mttt_board = None
        self.player_1 = None
        self.player_2 = None
        self.play_queue = None
        self.active_player = None

        self.game_state = GameState.Setup
        self.game_result = None

        self.nxt_legal = None

        self.meta_x = 0
        self.meta_y = 0
        self.meta_size = 0

        self.panel_x = 0
        self.panel_y = 0
        self.panel_width = 0
        self.panel_height = 0

        self.setup_screen = SetupScreen(self)

    def setup(self):
        # Create your sprites and sprite lists here
        bg_path = resource_path('resources/background.jpg')
        self.background = arcade.load_texture(bg_path)

        self.mttt_board = MetaTicTacToe()
        self.player_1 = Player('Player 1', 'X')
        self.player_2 = Player('Player 2', 'O')
        self.play_queue = Queue(2)
        self.play_queue.put(self.player_1)
        self.play_queue.put(self.player_2)

        self.active_player = self.play_queue.get()

        self.game_state = GameState.Setup
        self.setup_screen.setup()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.setup_screen.on_resize(width, height)

        self.meta_size = round(min(width, height)) - 2 * MARGIN

        overlap = self.width - self.meta_size - self.meta_size // 2 - 2 * MARGIN
        if overlap < 0:
            self.meta_size = self.meta_size + overlap

        self.panel_width = self.meta_size // 2
        self.panel_height = self.meta_size

        # horizontally center game area
        abs_width = self.meta_size + self.panel_width + MARGIN
        free_space = self.width - abs_width
        self.panel_x = free_space // 2
        self.meta_x = self.panel_x + self.panel_width + MARGIN

        self.meta_y = self.height - self.meta_size - MARGIN
        self.panel_y = self.meta_y

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Draw the background
        arcade.draw_texture_rectangle(center_x=self.width // 2,
                                      center_y=self.height // 2,
                                      width=self.width,
                                      height=self.height,
                                      texture=self.background,
                                      repeat_count_x=1,
                                      repeat_count_y=1)

        if self.game_state == GameState.Setup:
            self.setup_screen.on_draw()
            return

        # Draw the game result, if finished
        if self.game_state == GameState.Finished:
            if self.game_result == GameResult.Won:
                arcade.draw_text(text=f'Player "{self.active_player.name}" won the game!',
                                 start_x=self.width // 2,
                                 start_y=self.height // 2,
                                 color=arcade.color.BLACK,
                                 font_size=30,
                                 align="center",
                                 anchor_x="center",
                                 anchor_y="center")
            elif self.game_result == GameResult.Draw:
                arcade.draw_text(text=f'The game is a draw!',
                                 start_x=self.width // 2,
                                 start_y=self.height // 2,
                                 color=arcade.color.BLACK,
                                 font_size=30,
                                 align="center",
                                 anchor_x="center",
                                 anchor_y="center")
            return

        # Draw the game area
        if self.game_state == GameState.Running:
            # In case the game is open
            self.draw_game_area()
            self.draw_panel_bg()
            self.draw_panel_items()

    def draw_panel_bg(self):
        arcade.draw_rectangle_filled(center_x=self.panel_x + self.panel_width // 2,
                                     center_y=self.panel_y + self.panel_height // 2,
                                     width=self.panel_width,
                                     height=self.panel_height,
                                     color=COLOR_PANEL_BG)
        arcade.draw_rectangle_outline(center_x=self.panel_x + self.panel_width // 2,
                                      center_y=self.panel_y + self.panel_height // 2,
                                      width=self.panel_width,
                                      height=self.panel_height,
                                      color=arcade.color.BLACK,
                                      border_width=2)

    def draw_panel_items(self):
        item_height = 40
        item_width = self.panel_width
        item_x = self.panel_x + self.panel_width // 2
        item_y = self.panel_y + self.panel_height - item_height // 2

        # Game time display
        text = 'Game Time'
        self.draw_time_display(center_x=item_x,
                               center_y=item_y,
                               width=item_width,
                               height=item_height,
                               text=text,
                               time=self.total_time)
        # Player 1 time
        item_y = item_y - item_height
        self.draw_time_display(center_x=item_x,
                               center_y=item_y,
                               width=item_width,
                               height=item_height,
                               text=self.player_1.name,
                               time=self.player_1.play_time)
        # Player 2 time
        item_y = item_y - item_height
        self.draw_time_display(center_x=item_x,
                               center_y=item_y,
                               width=item_width,
                               height=item_height,
                               text=self.player_2.name,
                               time=self.player_2.play_time)

    @staticmethod
    def draw_time_display(center_x, center_y, width, height, text, time,
                          text_color=arcade.color.BLACK, background_color=arcade.color.LIGHT_BLUE):
        arcade.draw_rectangle_filled(center_x, center_y, width, height, background_color)
        arcade.draw_rectangle_outline(center_x, center_y, width, height, arcade.color.BLACK)
        arcade.draw_text(text=f'{text}:',
                         start_x=center_x,
                         start_y=center_y,
                         width=width * 0.8,
                         align='left',
                         anchor_x='center',
                         anchor_y='center',
                         color=text_color)
        minutes = int(time) // 60
        seconds = int(time) % 60
        time_string = '{:02}:{:02}'.format(minutes, seconds)
        arcade.draw_text(text=time_string,
                         start_x=center_x,
                         start_y=center_y,
                         width=width * 0.8,
                         align='right',
                         anchor_x='center',
                         anchor_y='center',
                         color=text_color)

    def draw_game_area(self):
        # Draw the board outlines
        board_size = self.meta_size // 3
        for num_x in range(0, 3):
            for num_y in range(0, 3):
                x = self.meta_x + num_x * board_size
                y = self.meta_y + num_y * board_size

                bd, br, fd, fr = self.get_grid_coordinates(x, y)
                color = self.board_color(bd, br)

                # Check if the board was finished
                winner = self.mttt_board.check_board_winner(bd, br)
                if winner:
                    arcade.draw_rectangle_filled(x + board_size // 2,
                                                 y + board_size // 2,
                                                 board_size, board_size,
                                                 arcade.color.WHITE)
                    self.draw_player_mark(winner, x, y, board_size)
                    # Exit early if this board was already finished
                    continue

                # Draw field outlines
                self.draw_board(x, y, board_size, arcade.color.GRAY_BLUE, color, line_padding=0.03)

                field_size = board_size // 3
                # Draw field contents
                for num_fx in range(0, 3):
                    for num_fy in range(0, 3):
                        fx = x + num_fx * field_size
                        fy = y + num_fy * field_size
                        fx_center = fx + field_size // 2
                        fy_center = fy + field_size // 2
                        a, b, c, d = self.get_grid_coordinates(fx_center, fy_center)
                        content = self.mttt_board[a][b][c][d]
                        if content:
                            self.draw_player_mark(content, fx, fy, field_size)

        # Draw the meta board
        self.draw_board(self.meta_x, self.meta_y, self.meta_size, arcade.color.BLACK, border_width=2)

        # Draw an outline around the game area
        arcade.draw_rectangle_outline(center_x=self.meta_x + self.meta_size / 2,
                                      center_y=self.meta_y + self.meta_size / 2,
                                      width=self.meta_size,
                                      height=self.meta_size,
                                      color=arcade.color.BLACK,
                                      border_width=2)

    def board_color(self, bd, br):
        if not self.nxt_legal or self.nxt_legal == (bd, br):
            return COLOR_VALID
        return COLOR_INVALID

    @staticmethod
    def draw_player_mark(mark, x, y, size):
        if mark == 'X':

            x_left = x + size * 0.125
            x_right = x_left + size * 0.75
            y_low = y + size * 0.125
            y_high = y_low + size * 0.75
            arcade.draw_line(start_x=x_left,
                             end_x=x_right,
                             start_y=y_low,
                             end_y=y_high,
                             border_width=4,
                             color=arcade.color.BLACK)

            arcade.draw_line(start_x=x_left,
                             end_x=x_right,
                             start_y=y_high,
                             end_y=y_low,
                             border_width=4,
                             color=arcade.color.BLACK)
        if mark == 'O':
            arcade.draw_circle_outline(center_x=x + size // 2,
                                       center_y=y + size // 2,
                                       radius=size * 0.4375,
                                       border_width=3,
                                       color=arcade.color.BLACK)

        if mark == 'draw':
            arcade.draw_rectangle_filled(center_x=x + size // 2,
                                         center_y=y + size // 2,
                                         width=size,
                                         height=size,
                                         color=arcade.color.LIGHT_GRAY)

    @staticmethod
    def draw_board(pos_x, pos_y, size, color, bg_color=None, line_padding=0.0, border_width=1):
        # Draw background
        if bg_color:
            arcade.draw_rectangle_filled(pos_x + size // 2,
                                         pos_y + size // 2,
                                         size, size, bg_color)
        # Draw vertical lines
        sub_size = size // 3
        for num_x in range(0, 3):
            x = pos_x + num_x * sub_size
            arcade.draw_line(start_x=x,
                             end_x=x,
                             start_y=pos_y + size * line_padding,
                             end_y=pos_y + size - (size * line_padding),
                             color=color,
                             border_width=border_width)
        # Draw horizontal lines
        for num_y in range(0, 3):
            y = pos_y + num_y * sub_size
            arcade.draw_line(start_x=pos_x + size * line_padding,
                             start_y=y,
                             end_x=pos_x + size - (size * line_padding),
                             end_y=y,
                             color=arcade.color.GRAY_BLUE,
                             border_width=border_width)

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.game_state != GameState.Running:
            return

        self.total_time += delta_time
        self.active_player.play_time += delta_time

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if self.game_state == GameState.Setup:
            self.setup_screen.on_mouse_press(x, y, button, key_modifiers)

        if not self.game_area_hit(x, y) or self.game_state != GameState.Running:
            return

        cords = self.get_grid_coordinates(x, y)

        try:
            nxt = self.mttt_board.mark(self.active_player.mark, *cords)
        except WrongBoardError:
            print(f'Must play in board: {self.nxt_legal}')
            return
        except FieldTakenError:
            print(f'Field {self.nxt_legal} id already marked')
            return

        # Check if the game has ended
        finished = self.mttt_board.check_meta_winner()
        if finished == "draw":
            self.game_state = GameState.Finished
            self.game_result = GameResult.Draw
            return
        elif finished:
            self.game_state = GameState.Finished
            self.game_result = GameResult.Won
            return

        # Prepare next turn
        self.nxt_legal = nxt
        self.play_queue.put(self.active_player)
        self.active_player = self.play_queue.get()

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        if self.game_state == GameState.Setup:
            self.setup_screen.on_mouse_release(x, y, button, key_modifiers)
            return

    def game_area_hit(self, x, y):
        if x < self.meta_x or x > self.meta_x + self.meta_size:
            return False
        if y < self.meta_y or y > self.meta_y + self.meta_size:
            return False
        return True

    def get_grid_coordinates(self, x, y):
        # Get board
        board_size = self.meta_size // 3
        column, row = self.get_cell_from_coordinates(x, y,
                                                     self.meta_x, self.meta_y,
                                                     board_size)
        # Get Field
        board_x = self.meta_x + column * board_size
        board_y = self.meta_y + (self.meta_size - board_size) - row * board_size
        field_column, field_row = self.get_cell_from_coordinates(x, y,
                                                                 board_x, board_y,
                                                                 board_size // 3)
        return row, column, field_row, field_column

    @staticmethod
    def get_cell_from_coordinates(x, y, rel_x, rel_y, cell_size):
        column = (x - rel_x) // cell_size
        row = (y - rel_y) // cell_size
        # Flip row coordinate. 0, 0 should be top left
        row = abs(row - 2)
        return column, row

    def start_game(self):
        self.game_state = GameState.Running


def main():
    """ Main method """
    game = GameUI(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
