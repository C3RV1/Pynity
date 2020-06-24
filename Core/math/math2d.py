import math
import pygame
#import numpy


# Make an position relative to another
def relative_to(global_position, relative_origin):
    return [global_position[0] - relative_origin[0], global_position[1] - relative_origin[1]]


# Make a position global knowing that is relative to relative_origin
def make_global(relative_position, relative_origin):
    return [relative_position[0] + relative_origin[0], relative_position[1] + relative_origin[1]]


def degree_to_radian(degree):
    return (degree * math.pi) / 180.0


def radian_to_degree(radian):
    return (radian * 180.0) / math.pi


# Rotates a vector around (0, 0)
def vector_rotate(vector, rotation):
    angle = math.atan2(vector[1], vector[0])
    angle += degree_to_radian(rotation)
    h = get_vector_length(vector)
    cos = math.cos(angle)
    sin = math.sin(angle)
    vector[0] = cos * h
    vector[1] = sin * h


# Transform any rotation into 0-360
def to360rotation(rotation):
    r = rotation
    while r < 0:
        r += 360
    r = r % 360
    return r


# Changes the length of a vector to the specified length
def set_vector_length(vector, length):
    angle = math.atan2(vector[1], vector[0])
    cos = math.cos(angle)
    sin = math.sin(angle)
    vector[0] = cos * length
    vector[1] = sin * length


# Returns the length of a vector
def get_vector_length(vector):
    return math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))


# Returns -1 if num < -min_val, 1 if num > min_val, 0 if -min_value <= num <= min_val
def get_sign(num, min_val=0.01):
    min_val = abs(min_val)
    if num > min_val:
        return 1
    elif num < -min_val:
        return -1
    return 0


# Gets the rotation to make p1 look at p2
def vector_look_at(p1, p2):
    x_change = p1[0] - p2[0]
    y_change = p1[1] - p2[1]
    return to360rotation(radian_to_degree(math.atan2(y_change, x_change)))


def invert_surface(surface):
    pixels = pygame.surfarray.pixels2d(surface)
    pixels ^= 2 ** 32 - 1
    del pixels
