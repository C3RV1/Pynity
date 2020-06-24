

class GameObject:
    def __init__(self, scene, parent=None, name=""):
        self.components = []
        self.parent = parent  # type: GameObject
        self.active = True
        self.scene = scene
        self.scene.game_objects.append(self)

        self.name = name

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
