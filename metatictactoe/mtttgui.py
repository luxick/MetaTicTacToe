import sys
import os

import arcade

import const
from game_screen import GameScreen
from start_screen import StartScreen
from end_screen import EndScreen
from util import AppScreen
from mttt import Game, Player


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class GameUi(arcade.Window):
    screens = dict
    active_screen: AppScreen

    player1: Player
    player2: Player
    game: Game

    def __init__(self, width, height):
        title = f'Meta Tic Tac Toe v{const.VERSION}'
        super().__init__(width, height, title, resizable=True)
        self.set_min_size(const.MIN_WIDTH, const.MIN_HEIGHT)
        self.background = None

        # Create application screens
        self.screens = {AppScreen.Start: StartScreen(self),
                        AppScreen.Game: GameScreen(self),
                        AppScreen.End: EndScreen(self)}

    def setup(self):
        # Create your sprites and sprite lists here
        bg_path = resource_path('resources/background.jpg')
        self.background = arcade.load_texture(bg_path)

        self.player1 = Player('PLAYER 1')
        self.player2 = Player('PLAYER 2')
        self.game = Game(self.player1, self.player2)

        self.active_screen = AppScreen.Start

        for screen in self.screens.values():
            screen.setup()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        for screen in self.screens.values():
            screen.on_resize(width, height)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame
        arcade.start_render()

        # Draw the background
        arcade.draw_texture_rectangle(center_x=self.width // 2,
                                      center_y=self.height // 2,
                                      width=self.width,
                                      height=self.height,
                                      texture=self.background,
                                      repeat_count_x=1,
                                      repeat_count_y=1)

        self.screens[self.active_screen].on_draw()

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.screens[self.active_screen].update(delta_time)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        self.screens[self.active_screen].on_mouse_press(x, y, button, key_modifiers)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        self.screens[self.active_screen].on_mouse_release(x, y, button, key_modifiers)

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        self.screens[self.active_screen].on_key_press(key, modifiers)


def main():
    """ Main method """
    game = GameUi(const.INITIAL_WIDTH, const.INITIAL_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
