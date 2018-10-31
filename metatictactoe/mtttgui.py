from queue import Queue

import arcade
import time
from mttt import MetaTicTacToe, WrongBoardError, FieldTakenError

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MIN_WIDTH = 800
MIN_HEIGHT = 600

MARGIN = 30

COLOR_VALID = 242, 250, 234
COLOR_INVALID = 250, 234, 234


class GameUI(arcade.Window):
    mttt_board = None
    players = None
    active_player = None

    game_start = None
    game_end = None

    nxt_legal = None

    meta_x = 0
    meta_y = 0
    meta_size = 0

    info_x = 0
    info_y = 0

    def __init__(self, width, height):
        super().__init__(width, height, 'Meta Tic Tac Toe v0.2', resizable=True)
        self.set_min_size(MIN_WIDTH, MIN_HEIGHT)
        arcade.set_background_color(arcade.color.WHITE)
        self.background = None

    def setup(self):
        # Create your sprites and sprite lists here
        self.background = arcade.load_texture("resources/background.jpg")

        self.mttt_board = MetaTicTacToe()
        self.players = Queue(2)
        self.players.put('X')
        self.players.put('O')

        self.active_player = self.players.get()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.meta_size = round(min(width, height) * 0.80)
        self.meta_x = self.width - self.meta_size - MARGIN
        self.meta_y = self.height - self.meta_size - MARGIN

        self.info_x = MARGIN
        self.info_y = self.height - MARGIN - 17

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        arcade.draw_texture_rectangle(center_x=self.width // 2,
                                      center_y=self.height // 2,
                                      width=self.width,
                                      height=self.height,
                                      texture=self.background,
                                      repeat_count_x=1,
                                      repeat_count_y=1)
        self.draw_game_area()
        self.draw_clock()
        self.draw_active_player_display()

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
                winner = self.mttt_board.assert_board_winner(bd, br)
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

    def draw_clock(self):
        minutes, seconds = 0, 0
        if self.game_start:
            diff = int(time.time() - self.game_start)
            minutes, seconds = diff // 60, diff % 60
        arcade.draw_text('Time: {:02}:{:02}'.format(minutes, seconds),
                         self.info_x, self.info_y,
                         arcade.color.BLACK)

    def draw_active_player_display(self):
        arcade.draw_text(f'Current Player: {self.active_player}',
                         self.info_x, self.info_y - 20,
                         arcade.color.BLACK)

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if not self.game_area_hit(x, y):
            return

        cords = self.get_grid_coordinates(x, y)

        try:
            nxt = self.mttt_board.mark(self.active_player, *cords)
        except WrongBoardError:
            print(f'Must play in board: {self.nxt_legal}')
            return
        except FieldTakenError:
            print(f'Field {self.nxt_legal} id already marked')
            return

        self.nxt_legal = nxt
        self.players.put(self.active_player)
        self.active_player = self.players.get()

        if not self.game_start:
            self.game_start = time.time()

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


def main():
    """ Main method """
    game = GameUI(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
