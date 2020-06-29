from Core.scene.Scene import Scene
import Core.Component


class GameObject(object):
    def __init__(self, scene, parent=None, name=""):
        self.components = []
        self.parent = parent  # type: GameObject
        self.__active = True
        self.scene = scene  # type: Scene

        self.name = name  # type: str

    @property
    def active(self):
        if self.parent is None:
            return self.__active
        return self.parent.active and self.__active

    @active.setter
    def active(self, value):
        self.__active = value
        self.do_start()

    def get_components(self, component_type):
        component_list = []
        for component in self.components:  # type: Core.Component.Component
            if isinstance(component, component_type):
                component_list.append(component)
        return component_list

    def get_component(self, component_type):
        for component in self.components:  # type: Core.Component.Component
            if isinstance(component, component_type):
                return component
        return None

    def do_start(self):
        if self.active:
            for component in self.components:  # type: Core.Component.Component
                component.do_start()

    def do_update(self):
        if self.active:
            for component in self.components:  # type: Core.Component.Component
                component.do_update()
