# The GameManager singleton initiates all the other Core elements
from Core.GameManager import GameManager

# The SceneManager singleton manages the current scene
from Core.scene.SceneManager import SceneManager

# DemoScene is a scene we created to demonstrate what Pynity can do so far
from demo.DemoScene import DemoScene


def main():
    # We start the GameManager with a screen size of 1280x720
    game_manager = GameManager(screen_size=(1280, 720))

    # Using the SceneManager we load the DemoScene
    SceneManager().load_scene(DemoScene, ())

    # We start the main loop of the game
    game_manager.main_loop()


if __name__ == '__main__':
    main()
