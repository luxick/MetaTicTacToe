import arcade

import const
import util


class StartScreen:
    buttons: dict
    text_inputs: dict
    focused_input: util.PlayerNameInput

    player_1_y: int
    player_2_y: int

    def __init__(self, app: 'mtttgui.GameUI'):
        self.app = app

        self.p1_row_y = 0
        self.p2_row_y = 0

    def setup(self):
        self.buttons = {
            'start_button': util.StartGameButton(self._start_new_game)
        }
        self.text_inputs = {
            'player_1_name': util.PlayerNameInput(self.app.player1),
            'player_2_name': util.PlayerNameInput(self.app.player2)}
        self.focused_input = None

    def update(self, delta_time):
        pass

    def on_resize(self, width, height):
        base_y = height - height * 0.85
        self.buttons['start_button'].update_position(
            center_x=width // 2,
            center_y=base_y + 30,
            width=400,
            height=40)

        self.player_1_y = base_y + 210
        self.player_2_y = base_y + 150

        self.text_inputs['player_1_name'].update_position(
            center_x=width // 2,
            center_y=self.player_1_y,
            width=300,
            height=40)
        self.text_inputs['player_2_name'].update_position(
            center_x=width // 2,
            center_y=self.player_2_y,
            width=300,
            height=40)

    def on_draw(self):
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
        self._draw_title()

        arcade.draw_text(text='(click to change name)',
                         start_x=self.app.width // 2,
                         start_y=self.player_2_y - 60,
                         color=arcade.color.GRAY, width=self.app.width,
                         font_size=14, align="center",
                         anchor_x="center", anchor_y="center")

        self.buttons['start_button'].draw()
        for text_input in self.text_inputs.values():
            text_input.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        util.mouse_press_buttons(x, y, self.buttons.values())
        text_input = util.input_focused(x, y, self.text_inputs.values())
        if self.focused_input and self.focused_input != text_input:
            self.focused_input.on_focus_lost()
        self.focused_input = text_input

    def on_mouse_release(self, x, y, button, key_modifiers):
        util.mouse_release_buttons(x, y, self.buttons.values())

    def on_key_press(self, key, modifiers):
        if self.focused_input:
            if key == arcade.key.ENTER or key == arcade.key.ESCAPE:
                self.focused_input.on_focus_lost()
                self.focused_input = None
            else:
                self.focused_input.on_key_press(key, modifiers)

    def _start_new_game(self):
        self.app.screens[util.AppScreen.Game].setup()
        self.app.active_screen = util.AppScreen.Game

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
