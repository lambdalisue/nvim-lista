import weakref


class History:
    __slots__ = ['prompt', '_index', '_cached', '_backward', '_threshold']

    def __init__(self, prompt):
        self.prompt = weakref.proxy(prompt)
        self._index = 0
        self._cached = ''
        self._threshold = 0

    def current(self):
        return self.prompt.nvim.call('histget', 'input', self._index)

    def previous(self):
        if self._index == 0:
            self._cached = self.prompt.text
            self._threshold = self.prompt.nvim.call('histnr', 'input')
        if self._index < self._threshold:
            self._index += 1
        return self.current()

    def next(self):
        if self._index == 0:
            return self._cached
        self._index -= 1
        return self.current()

    def previous_match(self):
        if self._index == 0:
            self._backward = self.prompt.caret.get_backward_text()
        index = _index = self._index - 1
        while _index < self._index:
            _index = self._index
            candidate = self.previous()
            if candidate.startswith(self._backward):
                return candidate
        self._index = index
        return self.previous()

    def next_match(self):
        if self._index == 0:
            return self._cached
        index = _index = self._index + 1
        while _index > self._index:
            _index = self._index
            candidate = self.next()
            if candidate.startswith(self._backward):
                return candidate
        self._index = index
        return self.next()
