from Core.Component import Component
from Core.Debug import Debug
from Core.components.SpriteRenderer import SpriteRenderer
from Core.objects.Sprite import Sprite
from Core.objects import Color
from Core.math.Vector2D import Vector2D
import pygame
import os


class Text(Component):
    def __init__(self, game_object, font=None, font_size=11, text=None, anti_alias=False, color=None,
                 background_color=None):
        Component.__init__(self, game_object)

        self.sprite_renderer = None  # type: SpriteRenderer

        self.__font = font

        self.__font_object = None  # type: pygame.font.Font

        self.__font_size = font_size
        self.__text = text
        self.anti_alias = anti_alias

        self.__color = color  # type: Color.RGBA
        self.background_color = background_color  # type: Color.RGBA

    def start(self):
        self.sprite_renderer = self.game_object.get_component(SpriteRenderer)  # type: SpriteRenderer
        if not self.sprite_renderer:
            Debug.log_error("SpriteRenderer not found, disabling", self)
            self.enabled = False

        self.__update_font()

    @property
    def font(self):
        return self.__font

    @font.setter
    def font(self, value):
        if not isinstance(value, str):
            return
        self.__font = value
        self.__update_font()

    @property
    def font_size(self):
        return self.__font_size

    @font_size.setter
    def font_size(self, value):
        if not isinstance(value, int):
            return
        self.__font_size = value
        self.__update_font()

    @property
    def text(self):
        return str(self.__text)

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            return
        self.__text = value
        self.__update_sprite()

    @property
    def color(self):
        return self.__color.copy()

    @color.setter
    def color(self, value):
        if not isinstance(value, Color.RGBA):
            return
        self.__color = value

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
        new_sprite_surface = self.__font_object.render(self.__text, self.anti_alias, self.__color.list())
        new_sprite = Sprite(surface=self.__font_object.render(self.__text, self.anti_alias, self.__color.list()))
        new_sprite.sprite_surface.set_alpha(self.__color.a)
        if isinstance(self.background_color, Color.RGBA):
            new_sprite_surface = self.__font_object.render(self.__text, self.anti_alias, self.__color.list())
            new_sprite_surface.set_alpha(self.__color.a)
            new_sprite = Sprite(size=Vector2D(0, 0, lst=new_sprite_surface.get_size()))
            new_sprite.sprite_surface.fill(self.background_color.list_rgba())
            new_sprite.sprite_surface.blit(new_sprite_surface, (0, 0))
        else:
            new_sprite = Sprite(surface=new_sprite_surface)
            new_sprite.sprite_surface.set_alpha(self.__color.a)
        self.sprite_renderer.sprite = new_sprite
