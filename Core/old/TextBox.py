import GameManager
import pygame


class TextBoxTypes:
    STRING = 0
    INTEGER = 1


class TextBox:
    def __init__(self, game_manager, rect, text_color, text_box_type=TextBoxTypes.STRING,
                 default_text="", font="0.game_assets/fonts/press_start_2p.ttf", allowed_characters=None,
                 font_size=30, max_value=None):
        self.game_manager = game_manager  # type: GameManager.GameManager

        self.font = pygame.font.Font(font, font_size)

        self.text_color = text_color

        self.current_text = default_text

        self.rect = list(rect)
        self.rect.append(self.font.render("TestText", False, (0, 0, 0)).get_height() / 2 + 10)
        self.rect[1] -= self.rect[3] / 2

        self.current_text_rendered = None

        self.render_current_text()

        self.type = text_box_type

        self.max_value = max_value

        self.allowed_characters = allowed_characters

    def key_down(self, key, unicode_char_event):
        if key == pygame.K_BACKSPACE:
            if len(self.current_text) > 0:
                self.current_text = self.current_text[:-1]
                self.render_current_text()
            return

        elif key <= 127:
            char = chr(key)

            if self.allowed_characters is not None:
                if char not in self.allowed_characters:
                    return

            if self.type == TextBoxTypes.INTEGER:
                if char not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    return
            else:
                if self.max_value is not None:
                    if len(self.current_text) + 1 > self.max_value:
                        return

            self.current_text += unicode_char_event.unicode

            if self.type == TextBoxTypes.INTEGER:
                if self.max_value is not None:
                    try:
                        if int(self.current_text) > self.max_value:
                            self.current_text = str(self.max_value)
                    except:
                        self.current_text = ""
        self.render_current_text()

    def key_up(self, key, unicode_char_event):
        pass

    def render_current_text(self):
        self.current_text_rendered = self.font.render(self.current_text, False, self.text_color)

        while self.current_text_rendered.get_width() > self.rect[2] - 10:
            if len(self.current_text) == 0:
                break
            self.current_text = self.current_text[:-1]
            self.current_text_rendered = self.font.render(self.current_text, False, self.text_color)

    def draw(self):
        self.game_manager.screen.blit(self.current_text_rendered, (self.rect[0],
                                                                   self.rect[1]))

    def check_box(self, point):
        if self.rect[0] - 10 < point[0] < self.rect[0] + self.rect[2] + 10 and self.rect[1] - 10 < point[1] < self.rect[1] + self.rect[3] + 10:
            return True
        return False

    def get_text(self):
        return str(self.current_text)