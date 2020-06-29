# Taken from https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame

import pygame

_circle_cache = {}


def _circle_points(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render(text, font, color=pygame.Color('dodgerblue'), outline_color=(255, 255, 255), opx=2,
           anti_alias=True):
    text_surface = font.render(text, anti_alias, color).convert_alpha()
    w = text_surface.get_width() + 2 * opx
    h = font.get_height()

    outline_surface = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    outline_surface.fill((0, 0, 0, 0))

    surf = outline_surface.copy()

    outline_surface.blit(font.render(text, anti_alias, outline_color).convert_alpha(), (0, 0))

    for dx, dy in _circle_points(opx):
        surf.blit(outline_surface, (dx + opx, dy + opx))

    surf.blit(text_surface, (opx, opx))
    return surf
