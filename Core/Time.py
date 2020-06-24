import GameManager


class Time(object):
    def __init__(self):
        pass

    @staticmethod
    def delta_time():
        game_manager_instance = GameManager.GameManager()
        return game_manager_instance.delta_time
