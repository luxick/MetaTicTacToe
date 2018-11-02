import arcade
import widgets


class SetupScreen:
    def __init__(self, gui: arcade.Window):
        self.gui = gui
        self.start_button = None
        self.start_button_x = 0
        self.start_button_y = 0

        self.start_button = None
        self.button_list = []
        self.buttons = {}

    def setup(self):
        start_button = widgets.StartGameButton(width=200,
                                               height=40,
                                               action_function=self.gui.start_game)
        self.buttons['start_button'] = start_button

    def on_resize(self, width, height):
        self.start_button_x = width // 2
        self.start_button_y = height // 4

    def on_draw(self):
        self._draw_title()
        self._draw_player_list()
        self.buttons['start_button'].draw(self.start_button_x, self.start_button_y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        widgets.check_mouse_press_for_buttons(x, y, self.buttons.values())

    def on_mouse_release(self, x, y, button, key_modifiers):
        widgets.check_mouse_release_for_buttons(x, y, self.buttons.values())

    def _draw_title(self):
        title_x = self.gui.width // 2
        title_y = self.gui.height * 0.75
        title_text = 'Meta Tic Tac Toe'
        arcade.draw_text(text=title_text,
                         start_x=title_x,
                         start_y=title_y,
                         color=arcade.color.BLACK,
                         align='center',
                         anchor_x='center',
                         anchor_y='center',
                         font_size=40)

    def _draw_player_list(self):
        x = self.gui.width // 2
        y = self.gui.height // 2

        arcade.draw_text(text=f'{self.gui.player_1.name} ({self.gui.player_1.mark})',
                         start_x=x,
                         start_y=y,
                         color=arcade.color.BLACK,
                         align='center',
                         anchor_x='center',
                         anchor_y='center',
                         font_size=20)
        arcade.draw_text(text=f'{self.gui.player_2.name} ({self.gui.player_2.mark})',
                         start_x=x,
                         start_y=y - 40,
                         color=arcade.color.BLACK,
                         align='center',
                         anchor_x='center',
                         anchor_y='center',
                         font_size=20)
