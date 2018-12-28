import arcade

import const
from mttt import Result, Player
from util import AppScreen, RestartButton
from util import mouse_press_buttons, mouse_release_buttons


class EndScreen:
    buttons: dict

    def __init__(self, app: 'mtttgui.GameUI'):
        self.app = app
        self.base_y = 0

    def setup(self):
        self.buttons = {'restart_button': RestartButton(self._restart_game)}

    def on_draw(self):
        """
        Render the screen.
        """
        game = self.app.game  # type: mttt.Game

        # Draw the background panel
        arcade.draw_rectangle_filled(center_x=self.app.width // 2,
                                     center_y=self.app.height // 2,
                                     width=self.app.width * 0.85,
                                     height=self.app.height * 0.85,
                                     color=const.COLOR_PANEL_BG)
        arcade.draw_rectangle_outline(center_x=self.app.width // 2,
                                      center_y=self.app.height // 2,
                                      width=self.app.width * 0.85,
                                      height=self.app.height * 0.85,
                                      color=arcade.color.BLACK)

        result = game.check_meta_board()

        if result == Result.PlayerOne or result == Result.PlayerTwo:
            name = self.app.game.current_player().name
            message = f'Winner: {name}'
            self.draw_header(message)

        elif result == Result.Draw:
            message = f'The Game Is A Draw'
            self.draw_header(message)

        center_y = self.base_y + 140
        self.draw_player_stats(center_y, self.app.player2)

        center_y += 55
        self.draw_player_stats(center_y, self.app.player1)

        self.buttons['restart_button'].draw()

    def draw_header(self, message: str):
        text_center_x = self.app.width // 2
        text_center_y = self.app.height * 0.75
        arcade.draw_text(text=message,
                         start_x=text_center_x,
                         start_y=text_center_y,
                         color=const.COLOR_TEXT,
                         font_size=35,
                         align="center",
                         anchor_x="center",
                         anchor_y="center",
                         font_name=const.FONT)

    def draw_player_stats(self, center_y: int, player: Player):
        center_x = self.app.width // 2
        width = self.app.width * 0.85
        height = 50
        arcade.draw_rectangle_filled(center_x=center_x,
                                     center_y=center_y,
                                     width=width,
                                     height=height,
                                     color=const.COLOR_PANEL_FG)

        arcade.draw_rectangle_outline(center_x=center_x,
                                      center_y=center_y,
                                      width=width,
                                      height=height,
                                      color=arcade.color.BLACK)

        arcade.draw_text(text=player.name,
                         start_x=center_x,
                         start_y=center_y,
                         width=width * 0.8,
                         font_size=20,
                         align='left',
                         anchor_x='center',
                         anchor_y='center',
                         color=const.COLOR_TEXT,
                         font_name=const.FONT)

        time = player.time
        minutes = int(time) // 60
        seconds = int(time) % 60
        time_string = f'Playtime {minutes:02}:{seconds:02}'
        arcade.draw_text(text=time_string,
                         start_x=center_x,
                         start_y=center_y,
                         width=width * 0.8,
                         font_size=20,
                         align='right',
                         anchor_x='center',
                         anchor_y='center',
                         color=const.COLOR_TEXT,
                         font_name=const.FONT)

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_resize(self, width, height):
        self.base_y = height - height * 0.85
        self.buttons['restart_button']\
            .update_position(center_x=width // 2,
                             center_y=self.base_y + 30,
                             width=200,
                             height=40)

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
        mouse_press_buttons(x, y, self.buttons.values())

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        mouse_release_buttons(x, y, self.buttons.values())

    def _restart_game(self):
        self.app.active_screen = AppScreen.Start
