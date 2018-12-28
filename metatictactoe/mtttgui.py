import sys
import os

import arcade
import pyglet

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
        super().__init__(width, height, title,
                         resizable=True,
                         fullscreen=True)
        self.set_min_size(const.MIN_WIDTH, const.MIN_HEIGHT)
        self.background = None
        self.unfocused = True

        # Create application screens
        self.screens = {AppScreen.Start: StartScreen(self),
                        AppScreen.Game: GameScreen(self),
                        AppScreen.End: EndScreen(self)}

    def setup(self):
        # Create your sprites and sprite lists here
        bg_path = resource_path(f'resources/{const.BG_FILE}')
        self.background = arcade.load_texture(bg_path)

        self.player1 = Player('PLAYER 1')
        self.player2 = Player('PLAYER 2')

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
        tile_size = self.background.width
        for x in range(0, self.width + tile_size, tile_size):
            for y in range(0, self.height + tile_size, tile_size):
                arcade.draw_texture_rectangle(center_x=x - (tile_size // 2),
                                              center_y=y - (tile_size // 2),
                                              width=tile_size,
                                              height=tile_size,
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
        self.screens[self.active_screen]\
            .on_mouse_press(x, y, button, key_modifiers)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        self.screens[self.active_screen]\
            .on_mouse_release(x, y, button, key_modifiers)

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if self.unfocused:
            if key == arcade.key.ESCAPE:
                self.set_fullscreen(False)
            if key == arcade.key.F:
                self.set_fullscreen(not self.fullscreen)

        self.screens[self.active_screen].on_key_press(key, modifiers)


def main():
    """ Main method """
    pyglet.font.add_file(resource_path('resources/font.ttf'))
    game = GameUi(const.INITIAL_WIDTH, const.INITIAL_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
