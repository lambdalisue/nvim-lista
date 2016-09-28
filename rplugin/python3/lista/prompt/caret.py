class Caret:
    __slots__ = ['context']

    def __init__(self, context):
        self.context = context

    @property
    def locus(self):
        return self.context.caret_locus

    @locus.setter
    def locus(self, value):
        if value < self.head:
            self.context.caret_locus = self.head
        elif value > self.tail:
            self.context.caret_locus = self.tail
        else:
            self.context.caret_locus = value

    @property
    def head(self):
        return 0

    @property
    def lead(self):
        return len(self.context.text) - len(self.context.text.lstrip())

    @property
    def tail(self):
        return len(self.context.text)

    def get_backward_text(self):
        if self.locus == self.head:
            return ''
        return self.context.text[:self.locus]

    def get_selected_text(self):
        if self.locus == self.tail:
            return ''
        return self.context.text[self.locus]

    def get_forward_text(self):
        if self.locus >= self.tail - 1:
            return ''
        return self.context.text[self.locus+1:]

