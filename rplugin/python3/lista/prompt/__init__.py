from .key import Keys
from .caret import Caret


class Prompt:
    prefix = '# '

    def __init__(self, nvim):
        self.nvim = nvim
        self.caret = Caret(self)
        self.input = ''

    def start(self, default=None):
        self.nvim.call('inputsave')
        if default:
            self.input = default
        self.caret.index = self.caret.max

        self.on_init(default)

        key = None
        while not self.on_progress(key):
            self.redraw_promptline()
            self.redraw_statusline()

            key = self.nvim.call('getchar')
            if isinstance(key, str) and key.startswith("\udc80"):
                key = key[1:]
                char = ''
            else:
                char = self.nvim.call('nr2char', key)

            if key == Keys.CR or key == Keys.ESC:
                break
            elif not self.on_keypress(key):
                self.caret.insert(char)

        self.nvim.command('redraw | echo')
        if self.input:
            self.nvim.call('histadd', 'input', self.input)
        self.nvim.call('inputrestore')
        result = None if key == Keys.ESC else self.input
        self.on_term(result)
        return result

    def redraw_promptline(self):
        self.nvim.command(' | '.join([
            'redraw',
            'echohl Question',
            'echon "%s"' % self.prefix,
            'echohl None',
            'echon "%s"' % self.caret.lhs,
            'echohl Cursor',
            'echon "%s"' % self.caret.char,
            'echohl None',
            'echon "%s"' % self.caret.rhs,
        ]))

    def redraw_statusline(self):
        pass

    def on_init(self, default):
        pass

    def on_term(self, result):
        pass

    def on_progress(self, key):
        if key == Keys.CR or key == Keys.ESC:
            return True
        return False

    def on_keypress(self, key):
        if key in (Keys.C_H, Keys.BS, Keys.Backspace):
            self.caret.backspace()
        elif key in (Keys.C_D, Keys.DEL):
            self.caret.delete()
        elif key in (Keys.C_F, Keys.Left):
            self.caret.index -= 1
        elif key in (Keys.C_B, Keys.Right):
            self.caret.index += 1
        elif key in (Keys.C_A, Keys.Home):
            self.caret.index = self.caret.min
        elif key in (Keys.C_E, Keys.End):
            self.caret.index = self.caret.max
        else:
            return False
        return True
