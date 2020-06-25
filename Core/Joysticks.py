import pygame


class Joysticks(object):
    __instance = None
    __inited = False

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not isinstance(Joysticks.__instance, Joysticks):
            Joysticks.__instance = super(Joysticks, cls).__new__(cls, *args, **kwargs)
        return Joysticks.__instance

    def __init__(self):
        if not Joysticks.__inited:
            pygame.joystick.init()
            self.__joystick = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            self.joystick_count = pygame.joystick.get_count()
            for joystick in self.__joystick:
                joystick.init()

            self.joy_order = [i for i in range(pygame.joystick.get_count())]

    def set_joy_id_order(self, joy_id_order):
        if len(joy_id_order) != len(self.joy_order):
            return
        if not all(joy_id in joy_id_order for joy_id in self.joy_order):
            return
        self.joy_order = list(joy_id_order)

    def joystick(self, number):
        return self.__joystick[self.joy_order[number]]
