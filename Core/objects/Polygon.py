from Core.math import Vector2D


class Polygon:
    def __init__(self, position, points):
        self.position = position
        self.points = points

    def get_points(self):
        points = list(self.points)
        for point in range(0, len(points)):
            points[point] = points[point].copy()
            points[point] += self.position
        return points

    def copy(self):
        return Polygon(self.position, list(self.points))

    def list(self):
        new_list = []
        for i in range(0, len(self.points)):
            p = self.points[i].copy()  # type: Vector2D.Vector2D
            p += self.position
            new_list.append(p.list())
        return new_list

    def relative_to(self, relative_origin):
        for point in range(0, len(self.points)):
            self.points[point] -= relative_origin
