from Core.Screen import Screen


class Scene:
    def __init__(self):
        self.game_objects = []
        self.background_colour = (255, 255, 255)
        self.fill_screen = False
        self.active_routines = []

    def start(self):
        for game_object in self.game_objects:
            game_object.do_start()

    def update(self):
        if self.fill_screen:
            Screen.screen().fill(self.background_colour)

        for active_routine in self.active_routines:
            try:
                next(active_routine)
            except:
                self.active_routines.remove(active_routine)

        for game_object in self.game_objects:
            game_object.do_update()

        for game_object in self.game_objects:
            if not game_object.active:
                continue
            for component in game_object.components:
                if not component.enabled:
                    continue
                component.on_render()

    def get_game_objects(self, name):
        return_objects = []
        for game_object in self.game_objects:
            if game_object.name == name:
                return_objects.append(game_object)
        return return_objects

    def instantiate(self, game_object, order=-1):
        if order < 0:
            order += 1
            order = len(self.game_objects) - order
            if order < 0:
                return
        if order > len(self.game_objects):
            return
        self.game_objects.insert(order, game_object)
        game_object.do_start()

    def get_game_object(self, name):
        for game_object in self.game_objects:
            if game_object.name == name:
                return game_object
        return None

    def new_routing(self, routine):
        self.active_routines.append(routine)
