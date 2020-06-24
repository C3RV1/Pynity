import pygame
from Core.objects.Ray import Ray
from Core.math.Vector2D import Vector2D
from Core.objects.Polygon import Polygon


def draw_mask(polygons, light_point, surface):
    # need to understand https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    # need to understand https://thecodingtrain.com/CodingChallenges/145-2d-ray-casting.html

    collision_points = []

    for polygon in range(0, len(polygons)):
        polygons[polygon] = polygons[polygon].get_points()

    for polygon in polygons:
        # points = polygon.points
        for point in range(0, len(polygon)):
            for i in range(0, 3):
                point_to_light = light_point.copy()
                point_to_light -= polygon[point]
                point_to_light.x += i - 1
                ray_light_to_point = Ray(light_point, point_to_light)

                closest_point = None
                closest_distance = (1280 + 1) ** 2 + (720 + 1) ** 2
                for polygon1 in polygons:
                    for point1 in range(0, len(polygon1)):
                        wall = [polygon1[point1], polygon1[(point1 + 1) % len(polygon1)]]
                        # wall = [polygon1[(point1 + 1) % len(polygon1)], polygon1[point1]]
                        coll = ray_light_to_point.cast(wall)

                        if coll is not None:
                            coll = coll.copy()
                            coll_to_light = coll.copy()  # type: Vector2D
                            coll_to_light -= light_point
                            distance = coll_to_light.magnitude ** 2
                            if distance < closest_distance:
                                closest_distance = distance
                                closest_point = coll

                if closest_point is not None:
                    collision_points.append(closest_point)

    polygon_points = sorted(collision_points, key=lambda x: light_point.look_at_angle(x))

    list_points = []
    for vector in polygon_points:
        list_points.append(vector.list())

    if len(list_points) > 2:
        pygame.draw.polygon(surface, (128, 128, 40), list_points)
    return


def optimized_shadows(polygons, light_point, surface, box_borders=(Vector2D(0, 0),
                                                                   Vector2D(1280, 0),
                                                                   Vector2D(1280, 720),
                                                                   Vector2D(0, 720)),
                      color=(0, 0, 0)):
    # need to understand https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    # need to understand https://thecodingtrain.com/CodingChallenges/145-2d-ray-casting.html

    # Convert polygon object to polygon array
    for polygon in range(0, len(polygons)):
        if isinstance(polygons[polygon], Polygon):
            polygons[polygon] = polygons[polygon].get_points()

    # List of screen_borders
    screen_borders = list(box_borders)

    # Loop over all polygons
    for polygon in polygons:
        casted_points = [None for point in polygon]
        touched_side = [0 for point in polygon]
        for point in range(0, len(polygon)):
            point_to_light = light_point.copy()
            point_to_light -= polygon[point]
            ray_light_to_point = Ray(polygon[point], point_to_light)

            closest_point = None
            closest_d = 10000
            side = 0

            for i in range(0, len(screen_borders)):
                p1 = screen_borders[i]
                p2 = screen_borders[(i + 1) % len(screen_borders)]
                hit = ray_light_to_point.cast([p1, p2])

                if hit:
                    d = hit.copy()
                    d -= polygon[point]
                    d = d.magnitude
                    if d < closest_d:
                        closest_point = hit.copy()
                        closest_d = d
                        side = i
                        break

            if closest_point:
                casted_points[point] = closest_point.copy()
                touched_side[point] = side

        for point in range(0, len(polygon)):
            if casted_points[point] is None or casted_points[(point + 1) % len(polygon)] is None:
                continue
            points = [point, (point + 1) % len(polygon)]
            if touched_side[points[0]] > touched_side[points[1]]:
                t = points[0]
                points[0] = points[1]
                points[1] = t

            extra_points = []

            if abs(touched_side[points[0]] - touched_side[points[1]]) == 2:  # Parallel touching
                if touched_side[points[0]] % 2 == 0:  # Horizontal
                    d = casted_points[points[0]].x
                    if d > light_point.x:
                        extra_points.append(screen_borders[1].list())
                        extra_points.append(screen_borders[2].list())
                    else:
                        extra_points.append(screen_borders[0].list())
                        extra_points.append(screen_borders[3].list())
                else:  # Vertical
                    d = casted_points[points[0]].y
                    if d > light_point.y:
                        extra_points.append(screen_borders[2].list())
                        extra_points.append(screen_borders[3].list())
                    else:
                        extra_points.append(screen_borders[0].list())
                        extra_points.append(screen_borders[1].list())
            elif abs(touched_side[points[0]] - touched_side[points[1]]) == 1:  # Contiguous sides
                extra_points.append(screen_borders[touched_side[points[1]]].list())
            elif abs(touched_side[points[0]] - touched_side[points[1]]) == 3:  # Contiguous sides
                extra_points.append(screen_borders[0].list())

            polygon_points = [polygon[points[0]].list(), casted_points[points[0]].list()]
            polygon_points.extend(extra_points)
            polygon_points.extend([casted_points[points[1]].list(),
                                   polygon[points[1]].list()])
            try:
                pygame.draw.polygon(surface, color, polygon_points)
            except Exception as e:
                print polygon_points
                raise e
    return
