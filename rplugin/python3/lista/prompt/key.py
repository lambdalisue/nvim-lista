import curses.ascii


class Key:
    __slots__ = ['code', 'char']
    __instances = {}

    SPECIALS = {
        'Up': '\udc80ku',
        'Down': '\udc80kd',
        'Left': '\udc80kl',
        'Right': '\udc80kr',
        'Home': '\udc80kh',
        'End': '\udc80@7',
        'PageUp': '\udc80kP',
        'PageDown': '\udc80kN',
        'Delete': '\udc80kD',
        'Backspace': '\udc80kb',
        'Insert': '\udc80kI',
    }

    def __new__(cls, code):
        if code not in cls.__instances:
            cls.__instances[code] = super().__new__(cls)
        return cls.__instances[code]

    def __init__(self, code):
        if hasattr(self, 'code'):
            return
        self.code = self.__class__.resolve(code)
        self.char = '' if isinstance(self.code, str) else chr(self.code)

    def __eq__(self, other):
        return self.code == other.code

    def __hash__(self):
        return hash(self.code)

    @classmethod
    def resolve(cls, code):
        if isinstance(code, int):
            return code
        elif isinstance(code, str) and code.startswith("\udc80"):
            return code[1:]
        elif code.startswith('^'):
            return cls.resolve(curses.ascii.ctrl(code[1:]))
        elif code in cls.SPECIALS:
            return cls.resolve(cls.SPECIALS[code])
        elif isinstance(getattr(curses.ascii, code, None), int):
            return getattr(curses.ascii, code)
        else:
            return ord(code)
