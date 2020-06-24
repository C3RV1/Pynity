import pygame
import GameManager


class Button:
    def __init__(self, game_manager, rect, button_text, text_color, button_color,
                 font="0.game_assets/fonts/press_start_2p.ttf",
                 font_size=24, action=None, width=None):
        self.game_manager = game_manager  # type: GameManager.GameManager

        self.font = pygame.font.Font(font, font_size)

        self.button_text = self.font.render(button_text, False, text_color)  # type: pygame.Surface

        self.rect = rect

        self.button_pos = [0, 0]
        self.button_pos[0] = (rect[2] - self.button_text.get_width()) / 2
        self.button_pos[0] += rect[0]
        self.button_pos[1] = (rect[3] - self.button_text.get_height()) / 2
        self.button_pos[1] += rect[1]

        self.button_color = button_color

        self.action = action

        self.button_outline_width = width

    def draw(self):
        if self.button_outline_width is not None:
            pygame.draw.rect(self.game_manager.screen,
                             self.button_color,
                             (self.rect[0] + 5,
                              self.rect[1] + 5,
                              self.rect[2] - 10,
                              self.rect[3] - 10),
                             self.button_outline_width)
        else:
            pygame.draw.rect(self.game_manager.screen,
                             self.button_color,
                             (self.rect[0] + 5,
                              self.rect[1] + 5,
                              self.rect[2] - 10,
                              self.rect[3] - 10))

        self.game_manager.screen.blit(self.button_text, self.button_pos)

    def check_box(self, point):
        if self.rect[0] < point[0] < self.rect[0] + self.rect[2] and self.rect[1] < point[1] < self.rect[1] + self.rect[3]:
            return True
        return False