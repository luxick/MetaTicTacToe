from enum import Enum
import arcade
from const import KEY_CODES, COLOR_TRANSPARENT


class AppScreen(Enum):
    """
    All available screens of the application
    """
    Start = 0,
    Game = 1,
    End = 2


def mouse_press_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def mouse_release_buttons(x, y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()


def input_focused(x: int, y: int, input_list):
    """ Given an x, y, see if we need to register any input field clicks. """
    for text_input in input_list:
        if x > text_input.center_x + text_input.width / 2:
            continue
        if x < text_input.center_x - text_input.width / 2:
            continue
        if y > text_input.center_y + text_input.height / 2:
            continue
        if y < text_input.center_y - text_input.height / 2:
            continue
        text_input.on_focus()
        return text_input
    return None


class TextButton:
    """ Text-based button """
    def __init__(self,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = 0
        self.center_y = 0
        self.width = 0
        self.height = 0
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def update_position(self, center_x, center_y, width, height):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


class StartGameButton(TextButton):
    def __init__(self, action_function):
        super().__init__("Start Game", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class RestartButton(TextButton):
    def __init__(self, action_function):
        super().__init__("Restart", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class TextInput:
    def __init__(self,
                 text,
                 font_size=18,
                 font_face="Arial",
                 max_chars=12,
                 focused_bg=arcade.color.LIGHT_BLUE,
                 unfocused_bg=COLOR_TRANSPARENT,
                 box_weight=2):
        self.center_x = 0
        self.center_y = 0
        self.width = 0
        self.height = 0
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.max_chars = max_chars
        self.focused = False
        self.focused_bg = focused_bg
        self.unfocused_bg = unfocused_bg
        self.box_weight = box_weight

    def draw(self):
        """ Draw the text box """
        if not self.focused:
            color = self.unfocused_bg
            text = self.text
        else:
            color = self.focused_bg
            text = self.text + '_'

        lining_color = arcade.color.BLACK

        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, color)

        if self.focused:
            # Bottom horizontal
            arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                             self.center_x + self.width / 2, self.center_y - self.height / 2,
                             lining_color, self.box_weight)

            # Right vertical
            arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                             self.center_x + self.width / 2, self.center_y + self.height / 2,
                             lining_color, self.box_weight)

            # Top horizontal
            arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                             self.center_x + self.width / 2, self.center_y + self.height / 2,
                             lining_color, self.box_weight)

            # Left vertical
            arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                             self.center_x - self.width / 2, self.center_y + self.height / 2,
                             lining_color, self.box_weight)

        arcade.draw_text(text, self.center_x, self.center_y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_focus(self):
        self.focused = True

    def on_focus_lost(self):
        self.focused = False

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.BACKSPACE:
            self.text = self.text[:-1]
        if key in KEY_CODES and len(self.text) <= self.max_chars:
            self.text += KEY_CODES[key]

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def update_position(self, center_x, center_y, width, height):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height


class PlayerNameInput(TextInput):
    def __init__(self, player):
        super().__init__(player.name, 18, "Arial")
        self.player = player
        self.default_text = player.name

    def on_focus(self):
        super().on_focus()
        if self.text == self.default_text:
            self.text = ''

    def on_focus_lost(self):
        super().on_focus_lost()
        if self.text == '':
            self.text = self.default_text
        else:
            self.player.name = self.text
