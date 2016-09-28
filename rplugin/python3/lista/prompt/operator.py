import weakref


class Operator:
    def __init__(self, prompt):
        self.prompt = weakref.proxy(prompt)
        self.mode = 'insert'

    def _insert_text(self, text):
        self.prompt.context.text = ''.join([
            self.prompt.caret.get_backward_text(),
            text,
            self.prompt.caret.get_selected_text(),
            self.prompt.caret.get_forward_text(),
        ])
        self.prompt.caret.locus += len(text)

    def _replace_text(self, text):
        self.prompt.context.text = ''.join([
            self.prompt.caret.get_backward_text(),
            text,
            self.prompt.caret.get_forward_text(),
        ])
        self.prompt.caret.locus += len(text)

    def _update_text(self, text):
        if self.mode == 'insert':
            self._insert_text(text)
        else:
            self._replace_text(text)

    def accept(self, key):
        return 1

    def cancel(self, key):
        return -1

    def toggle_insert_mode(self, key):
        if self.mode == 'insert':
            self.mode = 'replace'
        else:
            self.mode = 'insert'

    def delete_char_before_caret(self, key):
        if self.prompt.caret.locus == 0:
            return
        self.prompt.context.text = ''.join([
            self.prompt.caret.get_backward_text()[:-1],
            self.prompt.caret.get_selected_text(),
            self.prompt.caret.get_forward_text(),
        ])
        self.prompt.caret.locus -= 1

    def delete_char_under_caret(self, key):
        self.prompt.context.text = ''.join([
            self.prompt.caret.get_backward_text(),
            self.prompt.caret.get_forward_text(),
        ])

    def delete_text_after_caret(self, key):
        self.prompt.context.text = self.prompt.caret.get_backward_text()
        self.prompt.caret.locus = self.prompt.caret.tail

    def move_caret_to_left(self, key):
        self.prompt.caret.locus -= 1

    def move_caret_to_right(self, key):
        self.prompt.caret.locus += 1

    def move_caret_to_head(self, key):
        self.prompt.caret.locus = self.prompt.caret.head

    def move_caret_to_lead(self, key):
        self.prompt.caret.locus = self.prompt.caret.lead

    def move_caret_to_tail(self, key):
        self.prompt.caret.locus = self.prompt.caret.tail

    def assign_previous_text(self, key):
        self.prompt.text = self.prompt.history.previous()

    def assign_next_text(self, key):
        self.prompt.text = self.prompt.history.next()

    def assign_previous_matched_text(self, key):
        self.prompt.text = self.prompt.history.previous_match()

    def assign_next_matched_text(self, key):
        self.prompt.text = self.prompt.history.next_match()

    def paste_from_register(self, key):
        self.prompt.nvim.command(r'echon "\""')
        reg = self.prompt.nvim.eval('nr2char(getchar())')
        val = self.prompt.nvim.call('getreg', reg)
        self._update_text(val)

    def update_text(self, key):
        self._update_text(key.char)

