from Core.math import Vector2D


class Ray:
    def __init__(self, position, direction):
        # type: (Vector2D.Vector2D, Vector2D.Vector2D) -> None
        self.position = position.copy()  # type: Vector2D.Vector2D
        self.direction = direction.copy()  # type: Vector2D.Vector2D

    def cast(self, wall):
        x1 = float(wall[0].x)
        x2 = float(wall[1].x)
        y1 = float(wall[0].y)
        y2 = float(wall[1].y)

        x3 = float(self.position.x)
        x4 = float(self.position.x + self.direction.x)
        y3 = float(self.position.y)
        y4 = float(self.position.y + self.direction.y)

        denominator = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))

        if denominator == 0:
            return None

        t = ((x1 - x3) * (y3 - y4)) - ((y1 - y3) * (x3 - x4))
        t /= denominator
        u = ((x1 - x2) * (y1 - y3)) - ((y1 - y2) * (x1 - x3))
        u /= denominator

        if 0 <= u and 0 <= t <= 1:
            return Vector2D.Vector2D(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        return None
