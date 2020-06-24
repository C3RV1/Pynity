import Core.GameManager
from Core.scene.Scene import Scene


class SceneManager(object):
    __instance = None
    __inited = False

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not isinstance(SceneManager.__instance, SceneManager):
            SceneManager.__instance = super(SceneManager, cls).__new__(cls, *args, **kwargs)
        return SceneManager.__instance

    def __init__(self):
        if not SceneManager.__inited:
            SceneManager.__inited = True
            self.active_scene = None  # type: Scene
            self.game_manager = Core.GameManager.GameManager()

    def main_loop(self):
        if not self.active_scene:
            self.game_manager.exit()
        self.active_scene.update()

    def load_scene(self, scene, args):
        self.active_scene = scene(*args)
        self.active_scene.start()
