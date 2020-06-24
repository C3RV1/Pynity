from Core.Component import Component
from Core.components.Transform import Transform
from Core.math.Vector2D import Vector2D
from Core.components.Camera import Camera
from Core.Screen import Screen
from Core.objects.Sprite import Sprite
from Core.Debug import Debug
import pygame


class SpriteRenderer(Component):
    def __init__(self, game_object, sprite, update_on_draw=True):
        Component.__init__(self, game_object)

        if not isinstance(sprite, Sprite):
            Debug.log_error("sprite parameter not Sprite object, disabling", self)
            self.enabled = False

        self.__sprite = sprite  # type: Sprite
        self.transform = None  # type: Transform
        self.__sprite_transformed = None
        self.sprite_size = Vector2D(0, 0)
        self.__current_world_scale = 1
        self.__current_world_rotation = 0
        self.update_on_draw = update_on_draw

    def start(self):
        self.transform = self.game_object.get_component(Transform)
        if not self.transform:
            Debug.log_error("Transform not found, disabling", self)
            self.enabled = False
        self.update_sprite()

    @property
    def sprite(self):
        return self.__sprite

    def update(self):
        if self.__current_world_scale != self.transform.world_scale:
            self.update_sprite()
        elif self.__current_world_rotation != int(self.transform.world_rotation):
            self.update_sprite()

    @sprite.setter
    def sprite(self, value):
        if not isinstance(value, Sprite):
            return
        self.__sprite = value
        self.update_sprite()

    def update_sprite(self):  # type: () -> None
        # def update_sprite(self, camera):  # type: (Camera) -> None
        # self.__current_world_scale = self.transform.world_scale * camera.transform.world_scale
        # self.__current_world_rotation = (int(self.transform.world_rotation) - camera.transform.world_rotation) % 360
        self.__current_world_scale = self.transform.world_scale
        self.__current_world_rotation = int(self.transform.world_rotation)

        new_size_x = int(self.__sprite.sprite_size.x * self.__current_world_scale.x)
        new_size_y = int(self.__sprite.sprite_size.y * self.__current_world_scale.y)

        self.__sprite_transformed = pygame.transform.scale(self.__sprite.sprite_surface, (new_size_x, new_size_y))

        if new_size_x != 0 and new_size_y != 0:
            self.__sprite_transformed = pygame.transform.rotate(self.__sprite_transformed,
                                                                -self.__current_world_rotation)  # type: pygame.Surface

        self.sprite_size.x = self.__sprite_transformed.get_width()
        self.sprite_size.y = self.__sprite_transformed.get_height()

    def sprite_world_position(self, camera):
        world_position = self.transform.world_position
        # world_position *= camera.transform.world_scale
        # world_position.relative_to(camera.transform.world_position)
        # world_position.rotate(-camera.transform.world_rotation)
        # world_position.make_global(camera.transform.world_position)
        world_position.x -= self.sprite_size.x / 2
        world_position.y -= self.sprite_size.y / 2
        return world_position

    def on_draw(self, camera):  # type: (Camera) -> None

        # self.update_sprite(camera)
        if self.update_on_draw:
            self.update_sprite()

        # Position in the world
        sprite_world_position = self.sprite_world_position(camera)  # type: Vector2D

        # Position of the screen in the world
        screen_in_world_position = camera.screen_in_world_position  # type: Vector2D

        # Position of the sprite relative to the screen
        sprite_in_screen_position = sprite_world_position
        sprite_in_screen_position.relative_to(screen_in_world_position)

        render_area = [0, 0, self.sprite_size.x, self.sprite_size.y]

        # We do not render what isn't visible
        if sprite_in_screen_position.x < 0:
            render_area[0] = min(-sprite_in_screen_position.x, self.sprite_size.x)
            sprite_in_screen_position.x += render_area[0]

        if sprite_in_screen_position.y < 0:
            render_area[1] = min(-sprite_in_screen_position.y, self.sprite_size.y)
            sprite_in_screen_position.y += render_area[1]

        if sprite_in_screen_position.x + (self.sprite_size.x - render_area[0]) > camera.render_size[0]:
            render_area[2] = max(camera.render_size[0] - sprite_in_screen_position.x, 0)

        if sprite_in_screen_position.y + (self.sprite_size.y - render_area[1]) > camera.render_size[1]:
            render_area[3] = max(camera.render_size[1] - sprite_in_screen_position.y, 0)

        sprite_in_screen_position += Vector2D(0, 0, lst=camera.render_pos)

        if render_area[0] == render_area[2] or render_area[1] == render_area[3]:
            return

        Screen.screen().blit(self.__sprite_transformed, sprite_in_screen_position.list(), render_area)