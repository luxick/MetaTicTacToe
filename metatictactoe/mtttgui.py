from queue import Queue

import arcade
import time
from mttt import MetaTicTacToe

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

MARGIN = 5


class GameUI(arcade.Window):
    mttt_board = None
    players = None
    active_player = None

    game_start = None
    game_end = None

    nxt_valid = None

    def __init__(self, width, height):
        super().__init__(width, height, 'Meta Tic Tac Toe')

        arcade.set_background_color(arcade.color.WHITE)

        self.game_area_size = 600
        self.game_area_x = self.width - self.game_area_size - MARGIN
        self.game_area_y = self.height - self.game_area_size - MARGIN

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
        board_x_center = self.game_area_x + self.game_area_size / 2
        board_y_center = self.game_area_y + self.game_area_size / 2
        arcade.draw_rectangle_outline(board_x_center, board_y_center,
                                      self.game_area_size, self.game_area_size,
                                      arcade.color.GRAY_BLUE)

        # Draw the meta board
        self.draw_board(self.game_area_x, self.game_area_y, self.game_area_size, arcade.color.BLACK)

        # Draw the boards
        board_size = self.game_area_size // 3
        for x in range(self.game_area_x,
                       self.game_area_x + self.game_area_size,
                       self.game_area_size // 3):
            for y in range(self.game_area_y,
                           self.game_area_y + self.game_area_size,
                           self.game_area_size // 3):
                self.draw_board(x, y, board_size, arcade.color.GRAY_BLUE)

    @staticmethod
    def draw_board(pos_x, pos_y, size, color):
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
        nxt = self.mttt_board.mark(self.active_player, *cords)

        if nxt == "Invalid Move":
            print(f'Must play in board: {self.nxt_valid}')
            return

        self.nxt_valid = nxt
        self.players.put(self.active_player)
        self.active_player = self.players.get()

        if not self.game_start:
            self.game_start = time.time()

    def game_area_hit(self, x, y):
        if x < self.game_area_x or x > self.game_area_x + self.game_area_size:
            return False
        if y < self.game_area_y or y > self.game_area_y + self.game_area_size:
            return False
        return True

    def get_grid_coordinates(self, x, y):
        # Get board
        board_size = self.game_area_size // 3
        column, row = self.get_cell_from_coordinates(x, y,
                                                     self.game_area_x, self.game_area_y,
                                                     board_size)
        # Get Field
        board_x = self.game_area_x + column * board_size
        board_y = self.game_area_y + (self.game_area_size - board_size) - row * board_size
        field_column, field_row = self.get_cell_from_coordinates(x, y,
                                                                 board_x, board_y,
                                                                 board_size // 3)

        print(f'Hit Board/Field: ({row}, {column}) ({field_row}, {field_column})\n')

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
