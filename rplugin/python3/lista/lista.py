from enum import Enum
from typing import Optional, Sequence, Any  # noqa: F401
from neovim import Nvim
from neovim.api.buffer import Buffer  # noqa: F401
from neovim_prompt.prompt import Prompt, Status
from .matcher import AbstractMatcher  # noqa: F401
from .matcher.all import Matcher as AllMatcher
from .matcher.fuzzy import Matcher as FuzzyMatcher
from .action import DEFAULT_ACTION_RULES, DEFAULT_ACTION_KEYMAP
from .context import Context
from .indexer import Indexer
from .util import assign_content


class Case(Enum):
    """Case enum class."""

    smart = 1
    ignore = 2
    normal = 3


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

    def __init__(self, nvim: Nvim, context: Context) -> None:
        super().__init__(nvim, context)
        self._buffer = None  # type: Buffer
        self._indices = None  # type: Sequence[int]
        self._previous = ''
        self.matcher = Indexer([
            AllMatcher(nvim),
            FuzzyMatcher(nvim),
        ])
        self.case = Indexer(list(Case))  # type: ignore
        self.action.register_from_rules(DEFAULT_ACTION_RULES)
        self.keymap.register_from_rules(nvim, DEFAULT_ACTION_KEYMAP)
        self.apply_custom_mappings_from_vim_variable('lista#custom_mappings')

    def start(self, default: str) -> int:
        bufhidden = self.nvim.current.buffer.options['bufhidden']
        self.nvim.current.buffer.options['bufhidden'] = 'hide'
        try:
            return super().start(default) or 0
        finally:
            self.nvim.current.buffer.options['bufhidden'] = bufhidden

    def switch_matcher(self) -> None:
        self.matcher.current.remove_highlight()
        self.matcher.next()
        self._previous = ''

    def switch_case(self) -> None:
        self.case.next()
        self._previous = ''

    def get_ignorecase(self) -> bool:
        if self.case.current is Case.ignore:
            return True
        elif self.case.current is Case.normal:
            return False
        elif self.case.current is Case.smart:
            return not any(c.isupper() for c in self.text)

    def on_init(self, default: str) -> Optional[Status]:
        self._buffer = self.nvim.current.buffer
        self._line_count = len(self._buffer[:])
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
        self.nvim.call('cursor', [self.context.selected_line, 0])
        self.nvim.command('normal! zvzz')
        return super().on_init(default)

    def on_redraw(self) -> None:
        self.nvim.current.window.options['statusline'] = self.statusline % (
            self.insert_mode.name.capitalize(),
            self.insert_mode.name.upper(),
            self.matcher.current.name,
            self.case.current.name,
            len(self._indices),
            self._line_count,
        )
        self.nvim.command('redrawstatus')
        return super().on_redraw()

    def on_update(self, status: Status) -> Optional[Status]:
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
        self.matcher.current.highlight(self.text, ignorecase)
        self.matcher.current.filter(
            self.text,
            self._indices,
            self._buffer[:],
            ignorecase,
        )
        assign_content(self.nvim, [self._buffer[i] for i in self._indices])
        return super().on_update(status)

    def on_term(self, status: Status, result: str) -> int:
        self.matcher.current.remove_highlight()
        self.nvim.command('echo "%s" | redraw' % (
            "\n" * self.nvim.options['cmdheight']
        ))
        self.context.selected_line = self.nvim.current.window.cursor[0]
        self.nvim.current.buffer.options['modified'] = False
        self.nvim.command('noautocmd keepjumps %dbuffer' % self._buffer.number)
        if result:
            ignorecase = self.get_ignorecase()
            caseprefix = '\c' if ignorecase else '\C'
            pattern = self.matcher.current.get_highlight_pattern(result)
            self.nvim.call('setreg', '/', caseprefix + pattern)
            if self.context.selected_line and len(self._indices) > 0:
                line = self.context.selected_line
                return self._indices[line - 1] + 1
        return 0
