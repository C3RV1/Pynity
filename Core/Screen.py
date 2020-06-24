import pygame


class Screen:
    __screen = None  # type: pygame.Surface
    __screen_size = None  # type: tuple

    @staticmethod
    def new_screen(size, flags):
        if not Screen.__screen:
            Screen.__screen = pygame.display.set_mode(size, flags=flags)
            Screen.__screen_size = size

    @staticmethod
    def screen():  # type: () -> pygame.Surface
        if not Screen.__screen:
            raise Exception("Screen not created")
        return Screen.__screen

    @staticmethod
    def screen_size():
        if not Screen.__screen:
            raise Exception("Screen not created")
        return tuple(Screen.__screen_size)
