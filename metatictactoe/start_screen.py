import arcade
from util import AppScreen, StartGameButton
from util import check_mouse_press_for_buttons, check_mouse_release_for_buttons


class StartScreen:
    buttons: dict

    def __init__(self, app: 'mtttgui.GameUI'):
        self.app = app
        self.start_button = None
        self.start_button_x = 0
        self.start_button_y = 0

    def setup(self):
        self.buttons = {'start_button': StartGameButton(action_function=self._start_new_game)}

    def update(self, delta_time):
        pass

    def on_resize(self, width, height):
        self.buttons['start_button'].update_position(width // 2, height // 4, 200, 40)

    def on_draw(self):
        self._draw_title()
        self._draw_player_list()
        self.buttons['start_button'].draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        check_mouse_press_for_buttons(x, y, self.buttons.values())

    def on_mouse_release(self, x, y, button, key_modifiers):
        check_mouse_release_for_buttons(x, y, self.buttons.values())

    def _start_new_game(self):
        self.app.screens[AppScreen.Game].setup()
        self.app.active_screen = AppScreen.Game

    def _draw_title(self):
        title_x = self.app.width // 2
        title_y = self.app.height * 0.75
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
        x = self.app.width // 2
        y = self.app.height // 2

        arcade.draw_text(text=f'{self.app.player_1.name} ({self.app.player_1.mark})',
                         start_x=x,
                         start_y=y,
                         color=arcade.color.BLACK,
                         align='center',
                         anchor_x='center',
                         anchor_y='center',
                         font_size=20)
        arcade.draw_text(text=f'{self.app.player_2.name} ({self.app.player_2.mark})',
                         start_x=x,
                         start_y=y - 40,
                         color=arcade.color.BLACK,
                         align='center',
                         anchor_x='center',
                         anchor_y='center',
                         font_size=20)
