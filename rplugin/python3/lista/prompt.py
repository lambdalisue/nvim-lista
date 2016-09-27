import curses.ascii
ESCAPE_ECHO = str.maketrans({
    '"': '\\"',
    '\\': '\\\\',
})


class Keys:
    CR = curses.ascii.CR
    ESC = curses.ascii.ESC
    DEL = curses.ascii.DEL
    BS = curses.ascii.BS

    C_A = ord(curses.ascii.ctrl('a'))
    C_B = ord(curses.ascii.ctrl('b'))
    C_D = ord(curses.ascii.ctrl('d'))
    C_E = ord(curses.ascii.ctrl('e'))
    C_F = ord(curses.ascii.ctrl('f'))
    C_H = ord(curses.ascii.ctrl('h'))
    C_N = ord(curses.ascii.ctrl('n'))
    C_P = ord(curses.ascii.ctrl('p'))
    C_R = ord(curses.ascii.ctrl('r'))
    C_CARET = ord(curses.ascii.ctrl('^'))

    Up = "ku"
    Down = "kd"
    Left = "kl"
    Right = "kr"

    Home = "kh"
    End = "@7"
    PageUp = "kP"
    PageDown = "kN"

    Delete = "kD"
    Backspace = "kb"


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
        if self.index >= self.max - 1:
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
            'echon "%s"' % self.prefix.translate(ESCAPE_ECHO),
            'echohl None',
            'echon "%s"' % self.caret.lhs.translate(ESCAPE_ECHO),
            'echohl Cursor',
            'echon "%s"' % self.caret.char.translate(ESCAPE_ECHO),
            'echohl None',
            'echon "%s"' % self.caret.rhs.translate(ESCAPE_ECHO),
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
        elif key in (Keys.C_D, Keys.DEL, Keys.Delete):
            self.caret.delete()
        elif key in (Keys.C_F, Keys.Left):
            self.caret.index -= 1
        elif key in (Keys.C_B, Keys.Right):
            self.caret.index += 1
        elif key in (Keys.C_A, Keys.Home):
            self.caret.index = self.caret.min
        elif key in (Keys.C_E, Keys.End):
            self.caret.index = self.caret.max
        elif key in (Keys.C_R,):
            self.nvim.command('echon \'"\'')
            reg = self.nvim.call('nr2char', self.nvim.call('getchar'))
            val = self.nvim.call('getreg', reg)
            self.caret.insert(val.replace("\n", ''))
        else:
            return False
        return True
