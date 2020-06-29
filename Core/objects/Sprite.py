import pygame
from Core.math.Vector2D import Vector2D
from Core.Debug import Debug
import os


class Sprite(object):
    def __init__(self, size=None, flags=pygame.HWSURFACE | pygame.SRCALPHA, surface=None):
        # type: (Vector2D, int, pygame.Surface) -> None

        if size is None and surface is None:
            Debug.log_error("No size and no surface", "Sprite Object")
            return

        if size is not None:
            self.sprite_surface = pygame.Surface(size.list(), flags=flags)
            self.sprite_size = size.copy()
        else:
            self.sprite_surface = surface
            self.sprite_size = Vector2D(surface.get_width(), surface.get_height())

    @staticmethod
    def from_path(path, convert_alpha=True):
        # type: (str, bool) -> Sprite

        if not os.path.isfile(path):
            Debug.log_error("Sprite {} not found".format(path), "Sprite Object")
            return None

        if convert_alpha:
            surface = pygame.image.load(path).convert_alpha()
        else:
            surface = pygame.image.load(path).convert()

        return Sprite(surface=surface)
