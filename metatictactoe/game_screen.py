import arcade

import const
import mttt
from util import AppScreen


class GameScreen:
    game: mttt.Game

    def __init__(self, app: 'mtttgui.GameUI'):
        self.app = app
        # Initialize position variables
        self.meta_x = 0
        self.meta_y = 0
        self.meta_size = 0

        self.panel_x = 0
        self.panel_y = 0
        self.panel_width = 0
        self.panel_height = 0

    def setup(self):
        """
        Set up a new game board and players
        """
        initial_state = mttt.State([], self.app.player1, self.app.player2)
        self.game = mttt.Game(initial_state)
        self.game.reset_board()
        self.app.game = self.game

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.game.state.play_time += delta_time
        self.game.current_player().time += delta_time

    def on_resize(self, width, height):
        """
        Gets called when the main window is being resized.
        Use to update widget positions and sizes.
        """
        self.meta_size = round(min(width, height)) - 2 * const.MARGIN

        margins = 2 * const.MARGIN
        overlap = width - self.meta_size - self.meta_size // 2 - margins
        if overlap < 0:
            self.meta_size = self.meta_size + overlap

        self.panel_width = self.meta_size // 2
        self.panel_height = self.meta_size

        # horizontally center game area
        abs_width = self.meta_size + self.panel_width + const.MARGIN
        free_space = width - abs_width
        self.panel_x = free_space // 2
        self.meta_x = self.panel_x + self.panel_width + const.MARGIN

        self.meta_y = height - self.meta_size - const.MARGIN
        self.panel_y = self.meta_y

    def on_draw(self):
        """
        Render the game screen
        """
        self.draw_game_area()
        self.draw_panel_bg()
        self.draw_panel_items()

    def on_mouse_release(self, x, y, *_):
        if not self.game_area_hit(x, y):
            return

        cords = self.pos_to_grid_cell(x, y)

        # Run the game logic
        try:
            self.game.mark(*cords)
        except mttt.WrongBoardError:
            return
        except mttt.FieldTakenError:
            return

        # Check if the game has ended
        result = self.game.check_meta_board()
        if result != mttt.Result.Ongoing:
            self.app.active_screen = AppScreen.End
            return

        # Prepare next turn
        self.game.next_player()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        pass

    def draw_panel_bg(self):
        center_x = self.panel_x + self.panel_width // 2
        center_y = self.panel_y + self.panel_height // 2
        arcade.draw_rectangle_filled(center_x=center_x,
                                     center_y=center_y,
                                     width=self.panel_width,
                                     height=self.panel_height,
                                     color=const.COLOR_PANEL_BG)
        arcade.draw_rectangle_outline(center_x=center_x,
                                      center_y=center_y,
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
        self.draw_time_item(center_x=item_x,
                            center_y=item_y,
                            width=item_width,
                            height=item_height,
                            text=text,
                            time=self.game.state.play_time)

        # Draw current player mark
        x = self.panel_x + 75
        y = self.panel_y + 5
        size = self.panel_width - 150

        arcade.draw_rectangle_filled(x + size // 2, y + size // 2, size, size,
                                     const.COLOR_PANEL_FG)
        arcade.draw_rectangle_outline(x + size // 2, y + size // 2, size, size,
                                      arcade.color.BLACK)
        self.draw_player_mark(self.game.current_player().mark, x, y, size)

        # Draw Player name above it
        item_y = y + size + 5 + item_height // 2
        self.draw_text_item(center_x=item_x,
                            center_y=item_y,
                            width=item_width,
                            height=item_height,
                            text=self.game.current_player().name)

        item_y = item_y + 5 + item_height
        self.draw_text_item(center_x=item_x,
                            center_y=item_y,
                            width=item_width,
                            height=item_height,
                            text='Now Playing')

    def draw_game_area(self):
        # Draw the board outlines
        board_size = self.meta_size // 3
        for num_x in range(0, 3):
            for num_y in range(0, 3):
                x = self.meta_x + num_x * board_size
                y = self.meta_y + num_y * board_size

                bd, br, fd, fr = self.pos_to_grid_cell(x, y)
                color = self.board_color(bd, br)

                # Check if the board was finished
                result = self.game.check_board_by_idx(bd, br)
                if result != mttt.Result.Ongoing:
                    arcade.draw_rectangle_filled(x + board_size // 2,
                                                 y + board_size // 2,
                                                 board_size, board_size,
                                                 const.COLOR_PANEL_BG)
                    self.draw_player_mark(result, x, y, board_size)
                    # Exit early if this board was already finished
                    continue

                # Draw field outlines
                self.draw_board(x, y, board_size,
                                arcade.color.GRAY_BLUE,
                                color, line_padding=0.03)

                field_size = board_size // 3
                # Draw field contents
                for num_fx in range(0, 3):
                    for num_fy in range(0, 3):
                        fx = x + num_fx * field_size
                        fy = y + num_fy * field_size
                        fx_center = fx + field_size // 2
                        fy_center = fy + field_size // 2
                        a, b, c, d = self.pos_to_grid_cell(fx_center, fy_center)
                        content = self.game.state.board[a][b][c][d]
                        if content:
                            self.draw_player_mark(content, fx, fy, field_size)

        # Draw the meta board
        self.draw_board(self.meta_x, self.meta_y, self.meta_size,
                        arcade.color.BLACK, border_width=2)

        # Draw an outline around the game area
        arcade.draw_rectangle_outline(center_x=self.meta_x + self.meta_size / 2,
                                      center_y=self.meta_y + self.meta_size / 2,
                                      width=self.meta_size,
                                      height=self.meta_size,
                                      color=arcade.color.BLACK,
                                      border_width=2)

    def board_color(self, bd, br):
        nxt = self.game.state.next_board
        if not nxt or nxt == (bd, br):
            return const.COLOR_VALID
        return const.COLOR_INVALID

    def pos_to_grid_cell(self, x, y):
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

    def game_area_hit(self, x, y):
        if x < self.meta_x or x > self.meta_x + self.meta_size:
            return False
        if y < self.meta_y or y > self.meta_y + self.meta_size:
            return False
        return True

    @staticmethod
    def draw_player_mark(result, x, y, size):
        if result == mttt.Result.PlayerOne:

            x_left = x + size * 0.125
            x_right = x_left + size * 0.75
            y_low = y + size * 0.125
            y_high = y_low + size * 0.75
            arcade.draw_line(start_x=x_left,
                             end_x=x_right,
                             start_y=y_low,
                             end_y=y_high,
                             border_width=8,
                             color=arcade.color.BLACK)
            arcade.draw_line(start_x=x_left,
                             end_x=x_right,
                             start_y=y_high,
                             end_y=y_low,
                             border_width=8,
                             color=arcade.color.BLACK)

        elif result == mttt.Result.PlayerTwo:
            arcade.draw_circle_outline(center_x=x + size // 2,
                                       center_y=y + size // 2,
                                       radius=size * 0.4,
                                       border_width=8,
                                       color=arcade.color.BLACK)

        elif result == mttt.Result.Draw:
            arcade.draw_rectangle_filled(center_x=x + size // 2,
                                         center_y=y + size // 2,
                                         width=size,
                                         height=size,
                                         color=arcade.color.LIGHT_GRAY)

    @staticmethod
    def draw_time_item(center_x, center_y, width, height, text, time,
                       text_color=const.COLOR_TEXT,
                       background_color=const.COLOR_PANEL_FG):
        arcade.draw_rectangle_filled(center_x, center_y, width, height,
                                     background_color)
        arcade.draw_rectangle_outline(center_x, center_y, width, height,
                                      arcade.color.BLACK)
        arcade.draw_text(text=f'{text}:',
                         start_x=center_x,
                         start_y=center_y,
                         width=width * 0.8,
                         align='left',
                         anchor_x='center',
                         anchor_y='center',
                         color=text_color,
                         font_size=14,
                         font_name=const.FONT)
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
                         color=text_color,
                         font_size=14,
                         font_name=const.FONT)

    @staticmethod
    def draw_text_item(center_x, center_y, width, height, text,
                       text_color=const.COLOR_TEXT,
                       background_color=const.COLOR_PANEL_FG):

        arcade.draw_rectangle_filled(center_x=center_x,
                                     center_y=center_y,
                                     width=width,
                                     height=height,
                                     color=background_color)

        arcade.draw_rectangle_outline(center_x=center_x,
                                      center_y=center_y,
                                      width=width,
                                      height=height,
                                      color=arcade.color.BLACK)

        arcade.draw_text(text=text,
                         start_x=center_x,
                         start_y=center_y,
                         width=width * 0.8,
                         align='center',
                         anchor_x='center',
                         anchor_y='center',
                         color=text_color,
                         font_size=14,
                         font_name=const.FONT)

    @staticmethod
    def draw_board(pos_x, pos_y, size, color, bg_color=None,
                   line_padding=0.0, border_width=1):
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

    @staticmethod
    def get_cell_from_coordinates(x, y, rel_x, rel_y, cell_size):
        column = (x - rel_x) // cell_size
        row = (y - rel_y) // cell_size
        # Flip row coordinate. 0, 0 should be top left
        row = abs(row - 2)
        return column, row
