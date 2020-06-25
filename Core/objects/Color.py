

class RGBA:
    def __init__(self, r, g, b, a=255):
        self.__r = r
        self.__g = g
        self.__b = b
        self.__a = a

    @property
    def r(self):
        return self.__r

    @r.setter
    def r(self, value):
        if not isinstance(value, int):
            return
        self.__r = max(value, 0)
        self.__r %= 255

    @property
    def g(self):
        return self.__g

    @g.setter
    def g(self, value):
        if not isinstance(value, int):
            return
        self.__g = max(value, 0)
        self.__g %= 255

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, value):
        if not isinstance(value, int):
            return
        self.__b = max(value, 0)
        self.__b %= 255

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, value):
        if not isinstance(value, int):
            return
        self.__a = max(value, 0)
        self.__a %= 255

    def copy(self):
        return RGBA(self.__r, self.__g, self.__b, self.__a)

    def list_rgba(self):
        return self.__r, self.__g, self.__b, self.__a

    def list(self):
        return self.__r, self.__g, self.__b

    def __str__(self):
        return "RGBA({}, {}, {}, {})".format(self.__r, self.__g, self.__b, self.__a)
