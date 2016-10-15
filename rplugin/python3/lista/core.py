from prompt.prompt import Prompt
from prompt.util import preparation_required
from .context import Context
from .matcher.all import Matcher as AllMatcher
from .matcher.fuzzy import Matcher as FuzzyMatcher


class Lista(Prompt):
    statusline = ''.join([
        '%%#ListaStatuslineMode%s# %s ',
        '%%#ListaStatuslineFile# %%f ',
        '%%#ListaStatuslineMiddle#%%=',
        '%%#ListaStatuslineMatcher# Matcher: %s (C-^ to switch) ',
        '%%#ListaStatuslineIndicator# %d/%d ',
    ])

    @classmethod
    def prepare(cls, nvim):
        super().prepare(nvim)
        Context.prepare(nvim)
        AllMatcher.prepare(nvim)
        FuzzyMatcher.prepare(nvim)

    @preparation_required
    def __new__(cls, context):
        return super().__new__(cls, context)

    def __init__(self, context):
        super().__init__(context)
        self.matcher = AllMatcher()
        self._previous = ''
        self.action.register(
            'lista:select_next_candidate',
            _select_next_candidate,
        )
        self.action.register(
            'lista:select_previous_candidate',
            _select_previous_candidate,
        )
        self.action.register(
            'lista:switch_matcher',
            _switch_matcher,
        )
        self.keymap.register_from_rules([
            ('<PageUp>', '<lista:select_previous_candidate>', 1),
            ('<PageDown>', '<lista:select_next_candidate>', 1),
            ('<C-^>', '<lista:switch_matcher>', 1),
            ('<C-T>', '<PageUp>'),
            ('<C-G>', '<PageDown>'),
            ('<C-6>', '<C-^>'),
        ])

    def assign_content(self, content):
        viewinfo = self.nvim.call('winsaveview')
        buffer_options = {
            k: self.buffer.options[k] for k in [
                'readonly',
                'modified',
                'modifiable',
            ]
        }
        self.buffer.options['readonly'] = False
        self.buffer.options['modifiable'] = True
        self.buffer[:] = content
        for k, v in buffer_options.items():
            self.buffer.options[k] = v
        self.nvim.call('winrestview', viewinfo)

    def switch_matcher(self):
        if isinstance(self.matcher, AllMatcher):
            self.matcher = FuzzyMatcher()
        else:
            self.matcher = AllMatcher()
        self._previous = ''

    def on_init(self, default):
        self.buffer = self.nvim.current.buffer
        self.window = self.nvim.current.window
        if self.context.buffer_number != self.buffer.number:
            self.nvim.command('echoerr "lista.nvim: Buffer number mismatch"')
            return True
        self.buffer.options['readonly'] = False
        self.buffer.options['modified'] = False
        self.buffer.options['modifiable'] = False
        self.window.options['spell'] = False
        self.window.options['foldenable'] = False
        self.window.options['colorcolumn'] = ''
        self.window.options['cursorline'] = True
        self.window.options['cursorcolumn'] = False
        self.nvim.command('set syntax=lista')
        return super().on_init(default)

    def on_redraw(self):
        self.window.options['statusline'] = self.statusline % (
            self.mode.capitalize(),
            self.mode.upper(),
            self.matcher.name,
            len(self.context.selected_indices),
            len(self.context.buffer_content),
        )
        self.nvim.command('redrawstatus')
        return super().on_redraw()

    def on_update(self, status):
        previous = self._previous
        self._previous = self.text

        if not previous or not self.text.startswith(previous):
            self.context.selected_indices = list(
                range(len(self.context.buffer_content))
            )
            if self.text:
                self.nvim.call('cursor', [1, self.window.cursor[1]])
        elif previous != self.text:
            self.nvim.call('cursor', [1, self.window.cursor[1]])

        self.matcher.highlight(self.text)
        self.matcher.filter(
            self.text,
            self.context.selected_indices,
            self.context.buffer_content,
        )
        self.assign_content([
            self.context.buffer_content[i]
            for i in self.context.selected_indices
        ])
        return super().on_update(status)

    def on_term(self, status, result):
        self.matcher.highlight('')
        self.nvim.command('echo "%s" | redraw' % (
            "\n" * self.nvim.options['cmdheight']
        ))
        self.context.selected_line = self.window.cursor[0]
        self.context.restore()
        if result:
            self.nvim.call(
                'setreg', '/', self.matcher.highlight_pattern(result)
            )
            if (self.context.selected_line and
                    len(self.context.selected_indices) > 0):
                line = self.context.selected_line
                index = self.context.selected_indices[line-1]
                self.nvim.call('cursor', [index + 1, 0])
        self.nvim.command('silent doautocmd Syntax')
        self.nvim.command('silent! normal! zvzz')
        return super().on_term(status, result)


def _select_next_candidate(prompt):
    line, col = prompt.window.cursor
    prompt.nvim.call('cursor', [line + 1, col])


def _select_previous_candidate(prompt):
    line, col = prompt.window.cursor
    prompt.nvim.call('cursor', [line - 1, col])


def _switch_matcher(prompt):
    prompt.switch_matcher()
