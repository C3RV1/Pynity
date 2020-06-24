import colorama
from Core.Component import Component


class Debug(object):
    def __init__(self):
        pass

    @staticmethod
    def log(log_message, origin):
        if isinstance(origin, Component):
            msg = "[{}, {}] {}".format(origin.game_object.name, type(origin).__name__, log_message)
        elif isinstance(origin, str):
            msg = "[{}] {}".format(origin, log_message)
        else:
            return
        print colorama.Fore.WHITE + msg

    @staticmethod
    def log_error(log_message, origin):
        log_message = str(log_message)
        if isinstance(origin, Component):
            msg = "[{}, {}] {}".format(origin.game_object.name, type(origin).__name__, log_message)
        elif isinstance(origin, str):
            msg = "[{}] {}".format(origin, log_message)
        else:
            return
        print colorama.Fore.RED + msg

    @staticmethod
    def log_warning(log_message, origin):
        if isinstance(origin, Component):
            msg = "[{}, {}] {}".format(origin.game_object.name, type(origin).__name__, log_message)
        elif isinstance(origin, str):
            msg = "[{}] {}".format(origin, log_message)
        else:
            return
        print colorama.Fore.YELLOW + msg
