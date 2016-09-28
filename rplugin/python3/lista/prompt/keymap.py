from .key import Key


class Keymap:
    __slots__ = ['registry']

    def __init__(self, candidates=[]):
        self.registry = {}
        for candidate in candidates:
            self.register(*candidate)

    def resolve(self, lhs):
        if not isinstance(lhs, Key):
            lhs = Key(lhs)
        if lhs in self.registry:
            rhs, noremap = self.registry[lhs]
            return rhs if noremap else self.resolve(rhs)
        return lhs

    def register(self, lhs, rhs, noremap=False):
        if not isinstance(lhs, Key):
            lhs = Key(lhs)
        if not isinstance(rhs, Key):
            rhs = Key(rhs)
        self.registry[lhs] = (rhs, noremap)
