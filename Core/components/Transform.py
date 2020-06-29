from Core.Component import Component
from Core.math.Vector2D import Vector2D
from Core.Debug import Debug


class Transform(Component):
    def __init__(self, game_object, position=None, scale=None, rotation=None):
        Component.__init__(self, game_object)
        if isinstance(position, Vector2D):
            self.position = position
        else:
            self.position = Vector2D(0, 0)

        if isinstance(scale, Vector2D):
            self.__scale = scale
        else:
            self.__scale = Vector2D(1, 1)

        if isinstance(rotation, int):
            self.__rotation = rotation
        else:
            self.__rotation = 0.0

    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, value):
        self.__rotation = value % 360

    @property
    def scale(self):
        return self.__scale.copy()

    @scale.setter
    def scale(self, value):
        if not isinstance(value, Vector2D):
            Debug.log_warning("Scale is not Vector2D, is of type {}".format(type(value).__name__), self)
            return
        self.__scale = value.copy()
        self.__scale.x = max(self.__scale.x, 0)
        self.__scale.y = max(self.__scale.y, 0)

    @property
    def world_position(self):
        if self.game_object.parent is None:
            return self.position.copy()
        else:
            position_copy = self.position.copy()
            parent_transform = self.game_object.parent.get_component(Transform)  # type: Transform
            if parent_transform is None:
                return position_copy
            position_copy *= parent_transform.world_scale
            position_copy.rotate(parent_transform.rotation)
            position_copy.make_global(parent_transform.world_position)
            return position_copy

    @world_position.setter
    def world_position(self, value):
        if not isinstance(value, Vector2D):
            return
        if self.game_object.parent is None:
            self.position = value.copy()
        else:
            parent_transform = self.game_object.parent.get_component(Transform)  # type: Transform
            if parent_transform is None:
                return
            self.position = value.copy()
            self.position.relative_to(parent_transform.world_position)
            self.position.rotate(-parent_transform.rotation)
            self.position /= parent_transform.world_scale

    @property
    def world_scale(self):
        if self.game_object.parent is None:
            return self.__scale.copy()
        else:
            scale_copy = self.__scale.copy()
            parent_transform = self.game_object.parent.get_component(Transform)  # type: Transform
            if parent_transform is None:
                return scale_copy
            scale_copy *= parent_transform.world_scale
            return scale_copy

    @property
    def world_rotation(self):
        if self.game_object.parent is None:
            return self.__rotation
        else:
            rotation_copy = self.__rotation
            parent_transform = self.game_object.parent.get_component(Transform)  # type: Transform
            if parent_transform is None:
                return rotation_copy
            rotation_copy += parent_transform.world_rotation
            rotation_copy %= 360.0
            return rotation_copy

    @world_rotation.setter
    def world_rotation(self, value):
        value %= 360
        parent_transform = self.game_object.parent.get_component(Transform)  # type: Transform
        if parent_transform is None:
            return
        self.__rotation = value
        self.__rotation -= parent_transform.world_rotation
        self.__rotation %= 360

    def world_to_local_position(self, world_position):
        if self.game_object.parent is None:
            return world_position
        else:
            parent_transform = self.game_object.parent.get_component(Transform)  # type: Transform
            local_position = world_position.copy()
            local_position.relative_to(parent_transform.world_position)
            local_position.rotate(-parent_transform.world_rotation)
            local_position /= parent_transform.world_scale
            return local_position

    def local_to_world_position(self, local_position):
        if self.game_object.parent is None:
            return local_position
        else:
            parent_transform = self.game_object.parent.get_component(Transform)  # type: Transform
            world_position = local_position.copy()  # type: Vector2D
            world_position *= parent_transform.world_scale
            world_position.rotate(parent_transform.world_rotation)
            world_position.make_global(parent_transform.world_position)
            return world_position

    def world_to_local_scale(self, world_scale):
        pass

    def local_to_world_scale(self, local_scale):
        pass

    def world_to_local_rotation(self, world_rotation):
        pass

    def local_to_world_rotation(self, local_rotation):
        pass
