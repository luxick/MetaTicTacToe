import arcade
from mttt import GameResult
from util import AppScreen


class EndScreen:
    def __init__(self, app: 'mtttgui.GameUI'):
        self.app = app

    def setup(self):
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        if self.app.game_result == GameResult.Won:
            # TODO Player objects should be in library and GameResult should return those as winners
            winner = self.app.screens[AppScreen.Game].active_player.name
            arcade.draw_text(text=f'Player "{winner}" won the game!',
                             start_x=self.app.width // 2,
                             start_y=self.app.height // 2,
                             color=arcade.color.BLACK,
                             font_size=30,
                             align="center",
                             anchor_x="center",
                             anchor_y="center")

        elif self.app.game_result == GameResult.Draw:
            arcade.draw_text(text=f'The game is a draw!',
                             start_x=self.app.width // 2,
                             start_y=self.app.height // 2,
                             color=arcade.color.BLACK,
                             font_size=30,
                             align="center",
                             anchor_x="center",
                             anchor_y="center")

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_resize(self, width, height):
        pass

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
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass
