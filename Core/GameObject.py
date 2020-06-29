import Core.scene.Scene


class GameObject(object):
    def __init__(self, scene, parent=None, name=""):
        self.components = []
        self.parent = parent  # type: GameObject
        self.__active = True
        self.scene = scene  # type: Core.scene.Scene

        self.name = name  # type: str

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        self.__active = value
        self.do_start()

    def get_components(self, component_type):
        component_list = []
        for component in self.components:
            if isinstance(component, component_type):
                component_list.append(component)
        return component_list

    def get_component(self, component_type):
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None

    def do_start(self):
        if self.__active:
            for component in self.components:
                component.do_start()

    def do_update(self):
        if self.__active:
            for component in self.components:
                component.do_update()
