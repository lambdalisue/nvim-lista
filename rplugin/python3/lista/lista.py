from lista.prompt.prompt import (  # type: ignore
    Prompt, INSERT_MODE_INSERT,
)
from .matcher.all import Matcher as AllMatcher
from .matcher.fuzzy import Matcher as FuzzyMatcher
from .action import DEFAULT_ACTION_RULES, DEFAULT_ACTION_KEYMAP
from .indexer import Indexer
from .util import assign_content


CASE_SMART = 1
CASE_IGNORE = 2
CASE_NORMAL = 3

CASES = (
    CASE_SMART,
    CASE_IGNORE,
    CASE_NORMAL,
)


class Lista(Prompt):
    """Lista class."""

    prefix = '# '
    statusline = ''.join([
        '%%#ListaStatuslineMode%s# %s ',
        '%%#ListaStatuslineFile# %%f ',
        '%%#ListaStatuslineMiddle#%%=',
        '%%#ListaStatuslineMatcher# Matcher: %s (C-^ to switch) ',
        '%%#ListaStatuslineMatcher# Case: %s (C-I to switch) ',
        '%%#ListaStatuslineIndicator# %d/%d ',
    ])

    @property
    def selected_line(self):
        if len(self._indices) and self.context.selected_index >= 0:
            return self._indices[self.context.selected_index] + 1
        return 0

    def __init__(self, nvim, context):
        super().__init__(nvim, context)
        self._buffer = None
        self._indices = None
        self._previous = ''
        self.matcher = Indexer(
            [FuzzyMatcher(nvim), AllMatcher(nvim)],
            index=context.matcher_index,
        )
        self.case = Indexer(CASES, index=context.case_index)
        self.action.register_from_rules(DEFAULT_ACTION_RULES)
        self.keymap.register_from_rules(nvim, DEFAULT_ACTION_KEYMAP)
        self.apply_custom_mappings_from_vim_variable('lista#custom_mappings')

    def start(self, default):
        bufhidden = self.nvim.current.buffer.options['bufhidden']
        self.nvim.current.buffer.options['bufhidden'] = 'hide'
        try:
            return super().start(default)
        finally:
            self.nvim.current.buffer.options['bufhidden'] = bufhidden

    def switch_matcher(self):
        self.matcher.current.remove_highlight()
        self.matcher.next()
        self._previous = ''

    def switch_case(self):
        self.case.next()
        self._previous = ''

    def get_ignorecase(self):
        if self.case.current is CASE_IGNORE:
            return True
        elif self.case.current is CASE_NORMAL:
            return False
        elif self.case.current is CASE_SMART:
            return not any(c.isupper() for c in self.text)

    def on_init(self, default):
        self._buffer = self.nvim.current.buffer
        self._content = self._buffer[:]
        self._line_count = len(self._content)
        self._indices = list(range(self._line_count))
        self._bufhidden = self._buffer.options['bufhidden']
        self._buffer.options['bufhidden'] = 'hide'
        self.nvim.command('noautocmd keepjumps enew')
        self.nvim.current.buffer[:] = self._buffer[:]
        self.nvim.current.buffer.options['buftype'] = 'nofile'
        self.nvim.current.buffer.options['bufhidden'] = 'wipe'
        self.nvim.current.buffer.options['buflisted'] = False
        self.nvim.current.window.options['spell'] = False
        self.nvim.current.window.options['foldenable'] = False
        self.nvim.current.window.options['colorcolumn'] = ''
        self.nvim.current.window.options['cursorline'] = True
        self.nvim.current.window.options['cursorcolumn'] = False
        self.nvim.command('set syntax=lista')
        self.nvim.call('cursor', [self.context.selected_index + 1, 0])
        self.nvim.command('normal! zvzz')
        return super().on_init(default)

    def on_redraw(self):
        if self.insert_mode == INSERT_MODE_INSERT:
            insert_mode_name = 'insert'
        else:
            insert_mode_name = 'replace'

        if self.case.current == CASE_IGNORE:
            case_name = 'ignore'
        elif self.case.current == CASE_NORMAL:
            case_name = 'normal'
        elif self.case.current == CASE_SMART:
            case_name = 'smart'

        self.nvim.current.window.options['statusline'] = self.statusline % (
            insert_mode_name.capitalize(),
            insert_mode_name.upper(),
            self.matcher.current.name,
            case_name,
            len(self._indices),
            self._line_count,
        )
        self.nvim.command('redrawstatus')
        return super().on_redraw()

    def on_update(self, status):
        previous = self._previous
        self._previous = self.text

        if not previous or not self.text.startswith(previous):
            self._indices = list(range(self._line_count))
            if previous and self.text:
                self.nvim.call(
                    'cursor',
                    [1, self.nvim.current.window.cursor[1]]
                )
        elif previous and previous != self.text:
            self.nvim.call('cursor', [1, self.nvim.current.window.cursor[1]])

        ignorecase = self.get_ignorecase()
        self.matcher.current.filter(
            self.text,
            self._indices,
            self._content[:],
            ignorecase,
        )
        if len(self._indices) < 100:
            self.matcher.current.highlight(self.text, ignorecase)
        else:
            self.matcher.current.remove_highlight()
        assign_content(self.nvim, [self._content[i] for i in self._indices])
        return super().on_update(status)

    def on_term(self, status):
        self.matcher.current.remove_highlight()
        self.nvim.command('echo "%s" | redraw' % (
            "\n" * self.nvim.options['cmdheight']
        ))
        self.context.selected_index = self.nvim.current.window.cursor[0] - 1
        self.context.matcher_index = self.matcher.index
        self.context.case_index = self.case.index
        self.nvim.current.buffer.options['modified'] = False
        self.nvim.command('noautocmd keepjumps %dbuffer' % self._buffer.number)
        if self.text:
            ignorecase = self.get_ignorecase()
            caseprefix = '\c' if ignorecase else '\C'
            pattern = self.matcher.current.get_highlight_pattern(self.text)
            self.nvim.call('setreg', '/', caseprefix + pattern)
        return status
