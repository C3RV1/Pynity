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
