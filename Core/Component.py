from Core.GameObject import GameObject


class Component(object):
    def __init__(self, game_object):
        self.__enabled = True
        self.game_object = game_object  # type: GameObject
        self.game_object.components.append(self)
        self.__started = False

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        self.__enabled = value
        self.do_start()

    def do_start(self):
        if not self.__started and self.enabled:
            self.__started = True
            self.start()

    def start(self):
        pass

    def do_update(self):
        if not self.enabled:
            return
        if not self.__started:
            self.do_start()
        self.update()

    def update(self):
        pass

    def on_draw(self, camera):
        pass

    def on_render(self):
        pass
