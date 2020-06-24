from Core.GameObject import GameObject


class Component(object):
    def __init__(self, game_object):
        self.enabled = True
        self.game_object = game_object  # type: GameObject
        self.game_object.components.append(self)

    def start(self):
        pass

    def update(self):
        pass

    def on_draw(self, camera):
        pass

    def on_render(self):
        pass
