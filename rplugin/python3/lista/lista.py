from neovim_prompt.prompt import Prompt, InsertMode
from .matcher.all import Matcher as AllMatcher
from .matcher.fuzzy import Matcher as FuzzyMatcher


class Lista(Prompt):
    statusline = ''.join([
        '%%#ListaStatuslineMode%s# %s ',
        '%%#ListaStatuslineFile# %%f ',
        '%%#ListaStatuslineMiddle#%%=',
        '%%#ListaStatuslineMatcher# Matcher: %s (C-^ to switch) ',
        '%%#ListaStatuslineMatcher# %s (C-I to switch) ',
        '%%#ListaStatuslineIndicator# %d/%d ',
    ])

    def __init__(self, nvim: 'Nvim', context: 'Context') -> None:
        super().__init__(nvim, context)
        self.matcher = AllMatcher(nvim)
        self._previous = ''
        self.action.register_from_rules([
            ('lista:select_next_candidate', _select_next_candidate),
            ('lista:select_previous_candidate', _select_previous_candidate),
            ('lista:switch_matcher', _switch_matcher),
            ('lista:switch_ignorecase', _switch_ignorecase),
        ])
        self.keymap.register_from_rules(nvim, [
            ('<PageUp>', '<lista:select_previous_candidate>', 1),
            ('<PageDown>', '<lista:select_next_candidate>', 1),
            ('<C-^>', '<lista:switch_matcher>', 1),
            ('<C-I>', '<lista:switch_ignorecase>', 1),
            ('<C-T>', '<PageUp>'),
            ('<C-G>', '<PageDown>'),
            ('<C-6>', '<C-^>'),
        ])

    @property
    def case_mode(self):
        if self.nvim.options['ignorecase']:
            return 'Case-insensitive'
        else:
            return 'Case-sensitive'

    @property
    def insert_mode_display(self):
        if self.insert_mode == InsertMode.insert:
            return 'insert'
        else:
            return 'replace'

    def assign_content(self, content):
        viewinfo = self.nvim.call('winsaveview')
        self.nvim.current.buffer.options['modifiable'] = True
        self.nvim.current.buffer[:] = content
        self.nvim.current.buffer.options['modifiable'] = False
        self.nvim.call('winrestview', viewinfo)

    def switch_matcher(self):
        self.matcher.highlight('')
        if isinstance(self.matcher, AllMatcher):
            self.matcher = FuzzyMatcher(self.nvim)
        else:
            self.matcher = AllMatcher(self.nvim)
        self._previous = ''

    def switch_ignorecase(self):
        if self.nvim.options['ignorecase']:
            self.nvim.options['ignorecase'] = False
        else:
            self.nvim.options['ignorecase'] = True
        self._previous = ''

    def on_init(self, default):
        viewinfo = self.nvim.call('winsaveview')
        self.context.content = self.nvim.current.buffer[:]
        self.context.selected_line = 0
        self.context.selected_indices = list(range(len(self.context.content)))
        self.buffer = self.nvim.current.buffer
        self.nvim.command('keepjumps enew')
        self.nvim.current.buffer[:] = self.context.content
        self.nvim.current.buffer.options['bufhidden'] = 'wipe'
        self.nvim.current.buffer.options['readonly'] = False
        self.nvim.current.buffer.options['readonly'] = False
        self.nvim.current.buffer.options['modified'] = False
        self.nvim.current.buffer.options['modifiable'] = False
        self.nvim.current.window.options['spell'] = False
        self.nvim.current.window.options['foldenable'] = False
        self.nvim.current.window.options['colorcolumn'] = ''
        self.nvim.current.window.options['cursorline'] = True
        self.nvim.current.window.options['cursorcolumn'] = False
        self.nvim.command('set syntax=lista')
        self.nvim.call('winrestview', viewinfo)
        return super().on_init(default)

    def on_redraw(self):
        self.nvim.current.window.options['statusline'] = self.statusline % (
            self.insert_mode_display.capitalize(),
            self.insert_mode_display.upper(),
            self.matcher.name,
            self.case_mode,
            len(self.context.selected_indices),
            len(self.context.content),
        )
        self.nvim.command('redrawstatus')
        return super().on_redraw()

    def on_update(self, status):
        previous = self._previous
        self._previous = self.text

        if not previous or not self.text.startswith(previous):
            self.context.selected_indices = list(
                range(len(self.context.content))
            )
            if self.text:
                self.nvim.call(
                    'cursor',
                    [1, self.nvim.current.window.cursor[1]]
                )
        elif previous != self.text:
            self.nvim.call('cursor', [1, self.nvim.current.window.cursor[1]])

        self.matcher.highlight(self.text)
        self.matcher.filter(
            self.text,
            self.context.selected_indices,
            self.context.content,
        )
        self.assign_content([
            self.context.content[i]
            for i in self.context.selected_indices
        ])
        return super().on_update(status)

    def on_term(self, status, result):
        self.matcher.highlight('')
        self.nvim.command('echo "%s" | redraw' % (
            "\n" * self.nvim.options['cmdheight']
        ))
        self.context.selected_line = self.nvim.current.window.cursor[0]
        self.nvim.current.buffer.options['modified'] = False
        self.nvim.command('keepjumps %dbuffer' % self.buffer.number)
        if result:
            self.nvim.call(
                'setreg', '/', self.matcher.highlight_pattern(result)
            )
            if (self.context.selected_line and
                    len(self.context.selected_indices) > 0):
                line = self.context.selected_line
                index = self.context.selected_indices[line-1]
                self.nvim.call('cursor', [index + 1, 0])
                self.nvim.command('normal! zvzz')
        return super().on_term(status, result)


def _select_next_candidate(prompt):
    line, col = prompt.nvim.current.window.cursor
    prompt.nvim.call('cursor', [line + 1, col])


def _select_previous_candidate(prompt):
    line, col = prompt.nvim.current.window.cursor
    prompt.nvim.call('cursor', [line - 1, col])


def _switch_matcher(prompt):
    prompt.switch_matcher()


def _switch_ignorecase(prompt):
    prompt.switch_ignorecase()
