from .guard import Guard, assign_content
from .prompt import Prompt, Keys
from .matcher.all import Matcher as AllMatcher
from .matcher.fuzzy import Matcher as FuzzyMatcher


class Lista(Prompt):
    def __init__(self, nvim):
        self.guard = Guard(nvim)
        self.matcher = AllMatcher(nvim)
        self._previous = ''
        super().__init__(nvim)

    def __del__(self):
        del self.matcher

    def start(self, default=None):
        with self.guard:
            self.nvim.command('silent! normal! zO')
            self.buffer = self.nvim.current.buffer
            self.window = self.nvim.current.window
            self.content = self.buffer[:]
            self._previous = ''
            if super().start(default) is None:
                return
            cursor = self.window.cursor
        # Jump to the cursor
        if cursor[0] - 1 < len(self.indices):
            self.nvim.call('cursor', [
                self.indices[cursor[0] - 1] + 1,
                cursor[1]
            ])
            self.nvim.command('silent! normal! zv')

    def switch_matcher(self):
        if isinstance(self.matcher, AllMatcher):
            self.matcher = FuzzyMatcher(self.nvim)
        else:
            self.matcher = AllMatcher(self.nvim)

    def redraw_statusline(self):
        statusline = '%%f %%= Matcher: %s (C-^ to switch) | %d/%d'
        self.window.options['statusline'] = statusline % (
            self.matcher.name,
            len(self.indices),
            len(self.content),
        )
        self.nvim.command('redrawstatus')

    def on_init(self, default):
        self.buffer.options['modified'] = False
        self.buffer.options['modifiable'] = False
        self.buffer.options['readonly'] = False
        self.window.options['cursorline'] = True
        self.nvim.command('syntax clear')
        self.nvim.command('syntax match Comment /.*/ contains=Title')

    def on_term(self, result):
        self.matcher.highlight('')
        self.buffer.options['modified'] = False
        if result:
            self.nvim.call(
                'setreg',
                '/',
                self.matcher.highlight_pattern(result)
            )
        self.nvim.command('syntax clear | silent doautocmd <nomodeline> Syntax')

    def on_progress(self, key):
        if super().on_progress(key):
            return True

        previous = self._previous
        self._previous = self.input

        if not previous or not self.input.startswith(previous):
            self.indices = list(range(len(self.content)))

        self.matcher.highlight(self.input)
        self.matcher.filter(
            self.input,
            self.indices,
            self.content,
        )

        assign_content(self.nvim, self.buffer, list(map(
            lambda x: self.content[x],
            self.indices
        )))

    def on_keypress(self, key):
        if super().on_keypress(key):
            return True

        if key in (Keys.C_N, Keys.PageDown):
            line, col = self.window.cursor
            self.nvim.call('cursor', [line + 1, col])
        elif key in (Keys.C_P, Keys.PageUp):
            line, col = self.window.cursor
            self.nvim.call('cursor', [line - 1, col])
        elif key in (Keys.C_CARET,):
            self.switch_matcher()
        else:
            return False
        return True
