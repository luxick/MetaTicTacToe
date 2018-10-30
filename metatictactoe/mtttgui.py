from queue import Queue

import arcade
import time
from mttt import MetaTicTacToe, WrongBoardError, FieldTakenError

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800
META_BOARD_SIZE = 500

MARGIN = 20

COLOR_VALID = 242, 250, 234
COLOR_INVALID = 250, 234, 234


class GameUI(arcade.Window):
    mttt_board = None
    players = None
    active_player = None

    game_start = None
    game_end = None

    nxt_legal = None

    def __init__(self, width, height):
        super().__init__(width, height, 'Meta Tic Tac Toe')

        arcade.set_background_color(arcade.color.WHITE)

        self.game_area_x = self.width - META_BOARD_SIZE - MARGIN - 30
        self.game_area_y = self.height - META_BOARD_SIZE - MARGIN - 30

        self.info_x = MARGIN
        self.info_y = self.height - 15 - MARGIN

    def setup(self):
        # Create your sprites and sprite lists here
        self.mttt_board = MetaTicTacToe()
        self.players = Queue(2)
        self.players.put('X')
        self.players.put('O')

        self.active_player = self.players.get()

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        self.draw_clock()
        self.draw_active_player_display()
        self.draw_game_area()

    def draw_game_area(self):
        # Draw an outline around the game area
        board_x_center = self.game_area_x + META_BOARD_SIZE / 2
        board_y_center = self.game_area_y + META_BOARD_SIZE / 2
        arcade.draw_rectangle_outline(board_x_center, board_y_center,
                                      META_BOARD_SIZE, META_BOARD_SIZE,
                                      arcade.color.GRAY_BLUE)

        # Draw the boards
        board_size = META_BOARD_SIZE // 3
        for x in range(self.game_area_x,
                       self.game_area_x + META_BOARD_SIZE - board_size,
                       board_size):
            for y in range(self.game_area_y,
                           self.game_area_y + META_BOARD_SIZE - board_size,
                           board_size):

                bd, br, fd, fr = self.get_grid_coordinates(x, y)
                color = self.board_color(bd, br)
                self.draw_board(x, y, board_size, arcade.color.GRAY_BLUE, color)

                # Check if the board was finished
                winner = self.mttt_board.assert_board_winner(bd, br)
                if winner:
                    arcade.draw_rectangle_filled(x + board_size // 2,
                                                 y + board_size // 2,
                                                 board_size, board_size,
                                                 arcade.color.WHITE)
                    self.draw_player_mark(winner, x, y, board_size)
                    continue

                field_size = board_size // 3
                # Draw field contents
                for fx in range(x, x + board_size - field_size, field_size):
                    for fy in range(y, y + board_size - field_size, field_size):
                        fx_center = fx + field_size // 2
                        fy_center = fy + field_size // 2
                        a, b, c, d = self.get_grid_coordinates(fx_center, fy_center)
                        content = self.mttt_board[a][b][c][d]
                        if content:
                            self.draw_player_mark(content, fx, fy, field_size)

        # Draw the meta board
        self.draw_board(self.game_area_x, self.game_area_y, META_BOARD_SIZE, arcade.color.BLACK)

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
                             border_width=2,
                             color=arcade.color.BLACK)

            arcade.draw_line(start_x=x_left,
                             end_x=x_right,
                             start_y=y_high,
                             end_y=y_low,
                             border_width=2,
                             color=arcade.color.BLACK)
        if mark == 'O':
            arcade.draw_circle_outline(center_x=x + size // 2,
                                       center_y=y + size // 2,
                                       radius=size * 0.4375,
                                       border_width=2,
                                       color=arcade.color.BLACK)

    @staticmethod
    def draw_board(pos_x, pos_y, size, color, bg_color=None):
        # Draw background
        if bg_color:
            arcade.draw_rectangle_filled(pos_x + size // 2,
                                         pos_y + size // 2,
                                         size, size, bg_color)
        # Draw vertical lines
        for x in range(pos_x,
                       pos_x + size,
                       size // 3):
            arcade.draw_line(x, pos_y,
                             x, pos_y + size,
                             color)
        # Draw horizontal lines
        for y in range(pos_y,
                       pos_y + size,
                       size // 3):
            arcade.draw_line(pos_x, y,
                             pos_x + size, y,
                             arcade.color.GRAY_BLUE)

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

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

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
        if x < self.game_area_x or x > self.game_area_x + META_BOARD_SIZE:
            return False
        if y < self.game_area_y or y > self.game_area_y + META_BOARD_SIZE:
            return False
        return True

    def get_grid_coordinates(self, x, y):
        # Get board
        board_size = META_BOARD_SIZE // 3
        column, row = self.get_cell_from_coordinates(x, y,
                                                     self.game_area_x, self.game_area_y,
                                                     board_size)
        # Get Field
        board_x = self.game_area_x + column * board_size
        board_y = self.game_area_y + (META_BOARD_SIZE - board_size) - row * board_size
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

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = GameUI(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
