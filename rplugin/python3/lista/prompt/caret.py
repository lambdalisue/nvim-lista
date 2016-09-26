class Caret:
    def __init__(self, prompt):
        self.prompt = prompt
        self._index = 0

    @property
    def min(self):
        return 0

    @property
    def max(self):
        return len(self.prompt.input)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if value < self.min:
            self._index = self.min
        elif value > self.max:
            self._index = self.max
        else:
            self._index = value

    @property
    def lhs(self):
        if self.index == self.min:
            return ''
        return self.prompt.input[:self.index]

    @property
    def char(self):
        if self.index == self.max:
            return ''
        return self.prompt.input[self.index]

    @property
    def rhs(self):
        if self.index == self.max:
            return ''
        return self.prompt.input[self.index+1:]

    def replace(self, text):
        self.prompt.input = text
        self.index = self.max

    def insert(self, text):
        self.prompt.input = ''.join([
            self.lhs,
            text,
            self.char,
            self.rhs,
        ])
        self.index += len(text)

    def backspace(self):
        if not self.lhs:
            return
        self.prompt.input = ''.join([
            self.lhs[:-1],
            self.char,
            self.rhs,
        ])
        self.index -= 1

    def delete(self):
        self.prompt.input = ''.join([
            self.lhs,
            self.rhs,
        ])
