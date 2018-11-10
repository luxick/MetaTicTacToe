import arcade
from util import AppScreen, StartGameButton, PlayerNameInput
from util import check_mouse_press_for_buttons, check_mouse_release_for_buttons


class StartScreen:
    buttons: dict
    text_inputs: dict
    focused_input: PlayerNameInput

    def __init__(self, app: 'mtttgui.GameUI'):
        self.app = app

    def setup(self):
        self.buttons = {'start_button': StartGameButton(action_function=self._start_new_game)}
        self.text_inputs = {
            'player_1_name': PlayerNameInput('PLAYER 1'),
            'player_2_name': PlayerNameInput('PLAYER 2')}
        self.focused_input = None

    def update(self, delta_time):
        pass

    def on_resize(self, width, height):
        self.buttons['start_button'].update_position(width // 2, height // 4, 200, 40)
        self.text_inputs['player_1_name'].update_position(width // 2, height // 2, 300, 40)
        self.text_inputs['player_2_name'].update_position(width // 2, height // 2 - 44, 300, 40)

    def on_draw(self):
        self._draw_title()
        self.buttons['start_button'].draw()
        for text_input in self.text_inputs.values():
            text_input.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        check_mouse_press_for_buttons(x, y, self.buttons.values())

    def on_mouse_release(self, x, y, button, key_modifiers):
        check_mouse_release_for_buttons(x, y, self.buttons.values())

    def on_key_press(self, key, modifiers):
        if self.focused_input:
            if key == arcade.key.ENTER:
                print(f'Input successful: {self.focused_input.text}')
                self.focused_input = None
            elif key == arcade.key.ESCAPE:
                print('Input aborted')
                self.focused_input = None
            else:
                self.focused_input.on_key_press(key, modifiers)

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
