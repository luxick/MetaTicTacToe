import arcade
import time
from mttt import MetaTicTacToe

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700


class GameUI(arcade.Window):
    mttt_board = None
    player_one = "X"
    player_two = "O"

    game_start = None
    game_end = None

    def __init__(self, width, height):
        super().__init__(width, height, 'Meta Tic Tac Toe')

        arcade.set_background_color(arcade.color.WHITE)

        self.clock_x = 3
        self.clock_y = self.height - 20

    def setup(self):
        # Create your sprites and sprite lists here
        self.mttt_board = MetaTicTacToe()

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        minutes, seconds = 0, 0
        if self.game_start:
            diff = int(time.time() - self.game_start)
            minutes, seconds = diff // 60, diff % 60
        arcade.draw_text('Time: {:02}:{:02}'.format(minutes, seconds),
                         self.clock_x,
                         self.clock_y,
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
        print(x, y, button, key_modifiers)
        if not self.game_start:
            self.game_start = time.time()

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
