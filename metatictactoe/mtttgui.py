import arcade
import sys
import os
import const

from game_screen import GameScreen
from start_screen import StartScreen
from util import Player, AppScreen
from mttt import GameResult


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class GameUI(arcade.Window):
    screens = dict
    active_screen: AppScreen
    player_1: Player
    player_2: Player
    game_result: GameResult

    def __init__(self, width, height):
        super().__init__(width, height, f'Meta Tic Tac Toe v{const.VERSION}', resizable=True)
        self.set_min_size(const.MIN_WIDTH, const.MIN_HEIGHT)
        self.background = None

        # Create application screens
        self.screens = {AppScreen.Start: StartScreen(self),
                        AppScreen.Game: GameScreen(self)}

    def setup(self):
        # Create your sprites and sprite lists here
        bg_path = resource_path('resources/background.jpg')
        self.background = arcade.load_texture(bg_path)

        # TODO Create player objects from user input
        self.player_1 = Player('Player 1', 'X')
        self.player_2 = Player('Player 2', 'O')

        self.game_result = None
        self.active_screen = AppScreen.Start
        self.screens[AppScreen.Game].setup()
        self.screens[self.active_screen].setup()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        for screen in self.screens.values():
            screen.on_resize(width, height)

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

        self.screens[self.active_screen].on_draw()

        # TODO move to separate end screen
        # # Draw the game result, if finished
        # if self.active_screen == GameState.Finished:
        #     if self.game_result == GameResult.Won:
        #         arcade.draw_text(text=f'Player "{self.active_player.name}" won the game!',
        #                          start_x=self.width // 2,
        #                          start_y=self.height // 2,
        #                          color=arcade.color.BLACK,
        #                          font_size=30,
        #                          align="center",
        #                          anchor_x="center",
        #                          anchor_y="center")
        #     elif self.game_result == GameResult.Draw:
        #         arcade.draw_text(text=f'The game is a draw!',
        #                          start_x=self.width // 2,
        #                          start_y=self.height // 2,
        #                          color=arcade.color.BLACK,
        #                          font_size=30,
        #                          align="center",
        #                          anchor_x="center",
        #                          anchor_y="center")
        #     return

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


def main():
    """ Main method """
    game = GameUI(const.INITIAL_WIDTH, const.INITIAL_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
