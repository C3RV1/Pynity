import pygame
import random
import time
import Core.scene.SceneManager
from Core.Joysticks import Joysticks
from Core.Input import Input
from Core.Screen import Screen
from Core.Debug import Debug


class GameManager(object):
    __instance = None
    __inited = False

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not isinstance(GameManager.__instance, GameManager):
            GameManager.__instance = super(GameManager, cls).__new__(cls, *args, **kwargs)
        return GameManager.__instance

    def __del__(self):
        self.exit()

    def __init__(self, screen_size=None, full_screen=True, log_fps=False):
        if not GameManager.__inited:
            pygame.init()

            self.running = True

            if not screen_size:
                Debug.log_error("Screen size not specified", "GameManager")
                self.running = False
                return

            GameManager.__inited = True
            flags = pygame.HWSURFACE | pygame.DOUBLEBUF
            if full_screen:
                flags = flags | pygame.FULLSCREEN
            Screen.new_screen(screen_size, flags)

            self.delta_time = 1
            self.scene_manager = Core.scene.SceneManager.SceneManager()
            self.input_manager = Input()

            self.pygame_clock = pygame.time.Clock()  # type: pygame
            self.pygame_clock.tick()

            self.joystick_manager = Joysticks()

            self.log_fps = log_fps

            random.seed(time.time())

    def main_loop(self):
        while self.running:
            events = pygame.event.get()
            self.input_manager.update_events(events)
            for event in events:
                if event.type == pygame.QUIT:
                    self.exit()

            self.delta_time = float(self.pygame_clock.tick(90)) / (10 ** 3)

            if self.log_fps:
                Debug.log("FPS: {}".format(1/self.delta_time), "GameManager")

            self.scene_manager.main_loop()

            pygame.display.flip()

    def exit(self):
        if self.running:
            self.running = False
            pygame.quit()
