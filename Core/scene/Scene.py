from Core.Screen import Screen


class Scene:
    def __init__(self):
        self.game_objects = []
        self.background_colour = (255, 255, 255)
        self.fill_screen = False

    def start(self):
        for game_object in self.game_objects:
            if not game_object.active:
                continue
            for component in game_object.components:
                if not component.enabled:
                    continue
                component.start()

    def update(self):
        if self.fill_screen:
            Screen.screen().fill(self.background_colour)
        for game_object in self.game_objects:
            if not game_object.active:
                continue
            for component in game_object.components:
                if not component.enabled:
                    continue
                component.update()

        for game_object in self.game_objects:
            if not game_object.active:
                continue
            for component in game_object.components:
                if not component.enabled:
                    continue
                component.on_render()
