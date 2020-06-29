from Core.Component import Component
from Core.GameObject import GameObject
from Core.components.Transform import Transform
from Core.Debug import Debug


class Camera(Component):
    def __init__(self, game_object, render_rect):
        # type: (GameObject, list) -> None
        Component.__init__(self, game_object)
        self.render_pos = (render_rect[0], render_rect[1])
        self.render_size = (render_rect[2], render_rect[3])
        self.transform = None  # type: Transform

    def start(self):
        self.transform = self.game_object.get_component(Transform)
        if not self.transform:
            Debug.log_error("Transform not found, disabling", self)
            self.enabled = False

    def on_render(self):
        for game_object in self.game_object.scene.game_objects:  # type: GameObject
            if not game_object.active:
                continue
            for component in game_object.components:
                if not component.enabled:
                    continue
                component.on_draw(self)

    @property
    def screen_in_world_position(self):
        world_position = self.transform.world_position
        world_position.x -= self.render_size[0] / 2
        world_position.y -= self.render_size[1] / 2
        return world_position
