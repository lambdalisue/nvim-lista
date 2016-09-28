from .caret import Caret
from .key import Key
from .keymap import Keymap
from .history import History
from .operator import Operator


ESCAPE_ECHO = str.maketrans({
    '"': '\\"',
    '\\': '\\\\',
})


class Prompt:
    prefix = '# '

    def __init__(self, nvim, context):
        self.nvim = nvim
        self.context = context
        self.caret = Caret(context)
        self.keymap = Keymap(nvim.vars['lista#custom_mapping'])
        self.history = History(self)
        self.operator = Operator(self)

    @property
    def text(self):
        return self.context.text

    @text.setter
    def text(self, value):
        self.context.text = value
        self.caret.locus = len(value)

    def start(self, default=None):
        if self.on_init(default):
            return None
        status = None
        try:
            while not self.on_update(status):
                self.on_redraw()
                key = Key(self.nvim.call('getchar'))
                key = self.keymap.resolve(key)
                status = self.on_keypress(key)
        except self.nvim.error:
            status = -1
            pass
        if self.text:
            self.nvim.call('histadd', 'input', self.text)
        result = None if status == -1 else self.text
        return self.on_term(status, result) or result

    def on_init(self, default):
        self.nvim.call('inputsave')
        if default:
            self.text = default

    def on_redraw(self):
        backward_text = self.caret.get_backward_text()
        selected_text = self.caret.get_selected_text()
        forward_text = self.caret.get_forward_text()
        self.nvim.command('|'.join([
            'redraw',
            'echohl Question',
            'echon "%s"' % self.prefix.translate(ESCAPE_ECHO),
            'echohl None',
            'echon "%s"' % backward_text.translate(ESCAPE_ECHO),
            'echohl Cursor',
            'echon "%s"' % selected_text.translate(ESCAPE_ECHO),
            'echohl None',
            'echon "%s"' % forward_text.translate(ESCAPE_ECHO),
        ]))

    def on_update(self, status):
        return status

    def on_keypress(self, key):
        if key == Key('CR'):
            return self.operator.accept(key)
        elif key == Key('ESC'):
            return self.operator.cancel(key)
        elif key == Key('Insert'):
            return self.operator.toggle_insert_mode(key)
        elif key in (Key('BS'), Key('Backspace')):
            return self.operator.delete_char_before_caret(key)
        elif key in (Key('DEL'), Key('Delete')):
            return self.operator.delete_char_under_caret(key)
        elif key == Key('^K'):
            # TODO: <C-K> is used for digraph so should use different key
            return self.operator.delete_text_after_caret(key)
        elif key == Key('Left'):
            return self.operator.move_caret_to_left(key)
        elif key == Key('Right'):
            return self.operator.move_caret_to_right(key)
        elif key == Key('Home'):
            return self.operator.move_caret_to_head(key)
        elif key == Key('End'):
            return self.operator.move_caret_to_tail(key)
        elif key == Key('^P'):
            return self.operator.assign_previous_text(key)
        elif key == Key('^N'):
            return self.operator.assign_next_text(key)
        elif key == Key('Up'):
            return self.operator.assign_previous_matched_text(key)
        elif key == Key('Down'):
            return self.operator.assign_next_matched_text(key)
        elif key == Key('^R'):
            return self.operator.paste_from_register(key)
        else:
            return self.operator.update_text(key)

    def on_term(self, status, result):
        self.nvim.call('inputrestore')
