# The Screen singleton controls the screen surface
from Core.Screen import Screen

# A scene is an environment made of game objects where they can interact
from Core.scene.Scene import Scene

# A game object is any object present in a scene
from Core.GameObject import GameObject

from Core.objects.Sprite import Sprite

# The Transform component handles position, scale and rotation
from Core.components.Transform import Transform

# The Camera component handles rendering all the components and game objects
from Core.components.Camera import Camera

# The SpriteRenderer component handles the rendering of Sprite objects from a Camera component
from Core.components.SpriteRenderer import SpriteRenderer

# DemoMovement is a custom component we made to control our player
from demo.DemoMovement import DemoMovement

# 2 dimensional vectors
from Core.math.Vector2D import Vector2D


class DemoScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        # The order in which objects and components are created determine the order of script execution
        # as well as the order of rendering and drawing

        demo_background = GameObject(self, name="Demo Background")

        Transform(demo_background, scale=Vector2D(2, 2))
        SpriteRenderer(demo_background, Sprite.from_path("./demo_assets/sprites/demo_background.jpg"),
                       update_on_draw=False)

        demo_player = GameObject(self, name="Demo Player")

        Transform(demo_player, scale=Vector2D(2, 2))
        SpriteRenderer(demo_player, Sprite.from_path("./demo_assets/sprites/demo_player.png"))
        DemoMovement(demo_player)

        main_camera = GameObject(self, name="Main Camera", parent=demo_player)

        Transform(main_camera)
        Camera(main_camera, [0, 0, Screen().screen_size()[0], Screen().screen_size()[1]])

