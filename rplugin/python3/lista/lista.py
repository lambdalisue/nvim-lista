import re
from collections import namedtuple
from lista.prompt.prompt import (  # type: ignore
    INSERT_MODE_INSERT,
    Prompt,
)
from .action import DEFAULT_ACTION_KEYMAP, DEFAULT_ACTION_RULES
from .indexer import Indexer
from .matcher.all import Matcher as AllMatcher
from .matcher.fuzzy import Matcher as FuzzyMatcher
from .util import assign_content

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9a-zA-Z;]*m')

CASE_SMART = 1
CASE_IGNORE = 2
CASE_NORMAL = 3

CASES = (
    CASE_SMART,
    CASE_IGNORE,
    CASE_NORMAL,
)


Condition = namedtuple('Condition', [
    'text',
    'caret_locus',
    'selected_index',
    'matcher_index',
    'case_index',
])


class Lista(Prompt):
    """Lista class."""

    prefix = '# '

    statusline = ''.join([
        '%%#ListaStatuslineMode%s# %s ',
        '%%#ListaStatuslineFile# %s ',
        '%%#ListaStatuslineMiddle#%%=',
        '%%#ListaStatuslineMatcher# Matcher: %s (C-^ to switch) ',
        '%%#ListaStatuslineMatcher# Case: %s (C-_ to switch) ',
        '%%#ListaStatuslineIndicator# %d/%d ',
    ])

    selected_index = 0

    matcher_index = 0

    case_index = 0

    @property
    def selected_line(self):
        if len(self._indices) and self.selected_index >= 0:
            return self._indices[self.selected_index] + 1
        return 0

    def __init__(self, nvim, condition):
        super().__init__(nvim)
        self._buffer = None
        self._indices = None
        self._previous = ''
        self.action.register_from_rules(DEFAULT_ACTION_RULES)
        self.keymap.register_from_rules(nvim, DEFAULT_ACTION_KEYMAP)
        self.keymap.register_from_rules(
            nvim,
            nvim.vars.get('lista#custom_mappings', [])
        )
        self.restore(condition)

    def start(self):
        bufhidden = self.nvim.current.buffer.options['bufhidden']
        self.nvim.current.buffer.options['bufhidden'] = 'hide'
        try:
            return super().start()
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

    def on_init(self):
        self._buffer = self.nvim.current.buffer
        self._buffer_name = self.nvim.eval('simplify(expand("%:~:."))')
        self._content = list(map(
            lambda x: ANSI_ESCAPE.sub('', x),
            self._buffer[:]
        ))
        self._line_count = len(self._content)
        self._indices = list(range(self._line_count))
        self._bufhidden = self._buffer.options['bufhidden']
        self._buffer.options['bufhidden'] = 'hide'
        self.nvim.command('noautocmd keepjumps enew')
        self.nvim.current.buffer[:] = self._content
        self.nvim.current.buffer.options['buftype'] = 'nofile'
        self.nvim.current.buffer.options['bufhidden'] = 'wipe'
        self.nvim.current.buffer.options['buflisted'] = False
        self.nvim.current.window.options['spell'] = False
        self.nvim.current.window.options['foldenable'] = False
        self.nvim.current.window.options['colorcolumn'] = ''
        self.nvim.current.window.options['cursorline'] = True
        self.nvim.current.window.options['cursorcolumn'] = False
        self.nvim.command('set syntax=lista')
        self.nvim.call('cursor', [self.selected_index + 1, 0])
        self.nvim.command('normal! zvzz')
        return super().on_init()

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
            self._buffer_name,
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
        if len(self._indices) < 1000:
            self.matcher.current.highlight(self.text, ignorecase)
        else:
            self.matcher.current.remove_highlight()
        assign_content(self.nvim, [self._content[i] for i in self._indices])
        return super().on_update(status)

    def on_term(self, status):
        self.matcher.current.remove_highlight()
        self.nvim.command('echo "%s" | redraw' % (
            '\n' * self.nvim.options['cmdheight']
        ))
        self.selected_index = self.nvim.current.window.cursor[0] - 1
        self.matcher_index = self.matcher.index
        self.case_index = self.case.index
        self.nvim.current.buffer.options['modified'] = False
        self.nvim.command('noautocmd keepjumps %dbuffer' % self._buffer.number)
        if self.text:
            ignorecase = self.get_ignorecase()
            caseprefix = '\c' if ignorecase else '\C'
            pattern = self.matcher.current.get_highlight_pattern(self.text)
            self.nvim.call('setreg', '/', caseprefix + pattern)
        return status

    def store(self):
        """Save current prompt condition into a Condition instance."""
        return Condition(
            text=self.text,
            caret_locus=self.caret.locus,
            selected_index=self.selected_index,
            matcher_index=self.matcher_index,
            case_index=self.case_index,
        )

    def restore(self, condition):
        """Load current prompt condition from a Condition instance."""
        self.text = condition.text
        self.caret.locus = condition.caret_locus
        self.selected_index = condition.selected_index
        self.matcher_index = condition.matcher_index
        self.case_index = condition.case_index
        self.matcher = Indexer(
            [AllMatcher(self.nvim), FuzzyMatcher(self.nvim)],
            index=self.matcher_index,
        )
        self.case = Indexer(CASES, index=self.case_index)
