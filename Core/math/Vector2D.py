import Core.math
from Core.math import math2d
import math


class Vector2D:
    def __init__(self, x, y, lst=None):
        if lst is None:
            self.x = x
            self.y = y
        else:
            self.x = lst[0]
            self.y = lst[1]
        self.__magnitude = 0
        self.calc_magnitude()

    def relative_to(self, othervector):
        self.x = self.x - othervector.x
        self.y = self.y - othervector.y

    def make_global(self, global_origin):
        self.x = self.x + global_origin.x
        self.y = self.y + global_origin.y

    def calc_magnitude(self):
        self.__magnitude = (self.x ** 2 + self.y ** 2) ** 0.5

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector2D(self.x * other, self.y * other)
        elif isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)

    def __imul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            self.x *= other
            self.y *= other
        elif isinstance(other, Vector2D):
            self.x *= other.x
            self.y *= other.y
        return self

    @property
    def magnitude(self):
        self.calc_magnitude()
        return self.__magnitude

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __div__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x / other.x, self.y / other.y)
        else:
            return Vector2D(self.x / other, self.y / other)

    def __idiv__(self, other):
        if isinstance(other, Vector2D):
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other
        return self

    def copy(self):
        return Vector2D(self.x, self.y)

    def normalize(self):
        self.calc_magnitude()
        if self.__magnitude == 0:
            return
        self.x /= self.__magnitude
        self.y /= self.__magnitude
        self.calc_magnitude()

    def normalized(self):
        v = Vector2D(self.x, self.y)
        v.normalize()
        return v

    def __mod__(self, other):
        return self.x * other.x + self.y * other.y

    def rotate(self, rotation):
        angle = math.atan2(self.y, self.x)
        angle += math2d.degree_to_radian(rotation)
        self.calc_magnitude()
        h = self.__magnitude
        cos = math.cos(angle)
        sin = math.sin(angle)
        self.x = cos * h
        self.y = sin * h

    def __repr__(self):
        return "Vector2D ({:.5}, {:.5})".format(float(self.x), float(self.y))

    def str(self):
        return "Vector2D ({:.5}, {:.5})".format(float(self.x), float(self.y))

    def list(self):
        return [int(self.x), int(self.y)]

    def look_at_angle(self, p2):
        x_change = self.x - p2.x
        y_change = self.y - p2.y
        angle = math.atan2(y_change, x_change)
        angle = Core.math.math2d.radian_to_degree(angle) + 90
        angle %= 360
        return angle

    def align_to_origin_angle(self):
        angle = self.look_at_angle(Vector2D(0, 0))
        if angle > 180:
            angle -= 180

    def distance_to(self, p2):
        x_change = self.x - p2.x
        y_change = self.y - p2.y
        return Vector2D(x_change, y_change).magnitude

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def set(self, x, y):
        self.x = x
        self.y = y
