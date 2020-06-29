from Core.Component import Component
from Core.Debug import Debug
from Core.components.SpriteRenderer import SpriteRenderer
from Core.objects.Sprite import Sprite
from Core.objects import Color
from Core.math.Vector2D import Vector2D
from Core.GameObject import GameObject
from Core.from_internet import TextBetterRender
import pygame
import os


class Text(Component):
    def __init__(self, game_object, font=None, font_size=11, text=None, anti_alias=False, color=None,
                 outline_color=None, outline_width=2):
        # type: (GameObject, str, int, str, bool, Color.RGBA, Color.RGBA, int) -> None
        Component.__init__(self, game_object)

        self.sprite_renderer = None  # type: SpriteRenderer

        self.__font = font

        self.__font_object = None  # type: pygame.font.Font

        self.__font_size = font_size
        self.__text = text
        self.anti_alias = anti_alias

        self.__color = color  # type: Color.RGBA
        self.outline_color = outline_color  # type: Color.RGBA
        self.outline_width = outline_width

    def start(self):
        self.sprite_renderer = self.game_object.get_component(SpriteRenderer)  # type: SpriteRenderer
        if not self.sprite_renderer:
            Debug.log_error("SpriteRenderer not found, disabling", self)
            self.enabled = False

        self.__update_font()

    @property
    def font(self):
        # type: () -> str
        return self.__font

    @font.setter
    def font(self, value):
        # type: (str) -> None
        if not isinstance(value, str):
            return
        self.__font = value
        self.__update_font()

    @property
    def font_size(self):
        # type: () -> int
        return self.__font_size

    @font_size.setter
    def font_size(self, value):
        # type: (int) -> None
        if not isinstance(value, int):
            return
        self.__font_size = value
        self.__update_font()

    @property
    def text(self):
        # type: () -> str
        return str(self.__text)

    @text.setter
    def text(self, value):
        # type: (str) -> None
        if not isinstance(value, str):
            return
        self.__text = value
        self.__update_sprite()

    @property
    def color(self):
        # type: () -> Color.RGBA
        return self.__color.copy()

    @color.setter
    def color(self, value):
        # type: (Color.RGBA) -> None
        if not isinstance(value, Color.RGBA):
            return
        self.__color = value
        self.__update_sprite()

    def __update_font(self):
        if not isinstance(self.__font, str) or not isinstance(self.__font_size, int):
            return
        if not os.path.isfile(self.__font):
            Debug.log_error("Font {} not found".format(self.__font), self)
            return
        self.__font_object = pygame.font.Font(self.__font, self.__font_size)
        self.__update_sprite()

    def __update_sprite(self):
        if not self.sprite_renderer or not isinstance(self.__color, Color.RGBA):
            return
        # Render the text
        if isinstance(self.outline_color, Color.RGBA):
            new_sprite_surface = TextBetterRender.render(self.__text, self.__font_object,
                                                         color=self.__color.list(),
                                                         outline_color=self.outline_color.list(),
                                                         opx=self.outline_width,
                                                         anti_alias=self.anti_alias)
        else:
            new_sprite_surface = self.__font_object.render(self.__text, self.anti_alias, self.__color.list())
        alpha_surface = Sprite(size=Vector2D(0, 0, new_sprite_surface.get_size()))
        alpha_surface.sprite_surface.fill((255, 255, 255, self.__color.a))
        alpha_surface.sprite_surface.blit(new_sprite_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.sprite_renderer.sprite = alpha_surface
