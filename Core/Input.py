import pygame
from Core.Joysticks import Joysticks
from Core.Debug import Debug


class Input(object):
    __instance = None
    __inited = False

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not isinstance(Input.__instance, Input):
            Input.__instance = super(Input, cls).__new__(cls, *args, **kwargs)
        return Input.__instance

    def __init__(self):
        if not Input.__inited:
            Input.__inited = True
            self.key_down_dict = {}
            self.key_updated = []

            self.mouse_down_dict = {}
            self.mouse_updated = []

            self.joystick_manager = Joysticks()

            self.joystick_dict = {}
            self.joystick_updated = {}
            for joystick in self.joystick_manager.joy_order:
                self.joystick_dict[joystick] = {}
                self.joystick_updated[joystick] = []

    def update_events(self, events):
        self.key_updated = []
        self.mouse_updated = []
        for joy_number in self.joystick_updated.keys():
            self.joystick_updated[joy_number] = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = event.key
                self.key_down_dict[key] = True
                self.key_updated.append(key)
            elif event.type == pygame.KEYUP:
                key = event.key
                self.key_down_dict[key] = False
                self.key_updated.append(key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button = event.button
                self.mouse_down_dict[button] = True
                self.mouse_updated.append(button)
            elif event.type == pygame.MOUSEBUTTONUP:
                button = event.button
                self.mouse_down_dict[button] = False
                self.mouse_updated.append(button)
            elif event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                joy_id = event.joy
                if joy_id not in self.joystick_manager.joy_order:
                    Debug.log_warning("Joy {} event, but not in joy_order", "Input Manager")
                    continue
                joy_number = self.joystick_manager.joy_order.index(joy_id)
                self.joystick_dict[joy_number][button] = True
                self.joystick_updated[joy_number].append(button)

    def get_key_down(self, key):
        if key not in self.key_updated or key not in self.key_down_dict.keys():
            return False
        is_key_down = self.key_down_dict.get(key, False)
        return is_key_down

    def get_key_up(self, key):
        if key not in self.key_updated or key not in self.key_down_dict.keys():
            return False
        is_key_down = self.key_down_dict.get(key, False)
        return not is_key_down

    def get_key(self, key):
        return self.key_down_dict.get(key, False)

    def get_mouse_down(self, button):
        if button not in self.mouse_updated or button not in self.mouse_down_dict.keys():
            return False
        is_button_down = self.mouse_down_dict.get(button, False)
        return is_button_down

    def get_mouse_up(self, button):
        if button not in self.mouse_updated or button not in self.mouse_down_dict.keys():
            return False
        is_button_down = self.mouse_down_dict.get(button, False)
        return not is_button_down

    def get_mouse(self, button):
        return self.mouse_down_dict.get(button, False)

    def get_screen_mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos
