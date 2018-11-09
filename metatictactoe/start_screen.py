import arcade
from util import AppScreen, check_mouse_press_for_buttons, check_mouse_release_for_buttons, StartGameButton


class StartScreen:
    def __init__(self, app: 'mtttgui.GameUI'):
        self.gui = app
        self.start_button = None
        self.start_button_x = 0
        self.start_button_y = 0

        self.start_button = None
        self.button_list = []
        self.buttons = {}

    def setup(self):
        start_button = StartGameButton(width=200,
                                       height=40,
                                       action_function=self._switch_to_game_screen)
        self.buttons['start_button'] = start_button

    def update(self, delta_time):
        pass

    def on_resize(self, width, height):
        self.start_button_x = width // 2
        self.start_button_y = height // 4

    def on_draw(self):
        self._draw_title()
        self._draw_player_list()
        self.buttons['start_button'].draw(self.start_button_x, self.start_button_y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        check_mouse_press_for_buttons(x, y, self.buttons.values())

    def on_mouse_release(self, x, y, button, key_modifiers):
        check_mouse_release_for_buttons(x, y, self.buttons.values())

    def _switch_to_game_screen(self):
        self.gui.active_screen = AppScreen.Game

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
