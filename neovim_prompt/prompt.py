"""Prompt module."""
import re
import copy
import enum
from typing import Optional, Union, Tuple
from neovim import Nvim
from .key import Key
from .keystroke import Keystroke
from .context import Context

KeystrokeType = Tuple[Key, ...]     # noqa: F401
KeystrokeExpr = Union[KeystrokeType, bytes, str]    # noqa: F401


ACTION_KEYSTROKE_PATTERN = re.compile(r'<(\w+:\w+)>')

ESCAPE_ECHO = str.maketrans({
    '"': '\\"',
    '\\': '\\\\',
})


class Status(enum.Enum):
    accept = 1
    cancel = 0
    error = -1


class InsertMode(enum.Enum):
    insert = 'insert'
    replace = 'replace'


class Prompt:
    """Prompt class."""

    prefix = '# '

    def __init__(self, nvim: Nvim, context: Context) -> None:
        """Constructor."""
        from .caret import Caret
        from .history import History
        from .keymap import DEFAULT_KEYMAP_RULES, Keymap
        from .action import DEFAULT_ACTION
        self.nvim = nvim
        self.insert_mode = InsertMode.insert
        self.context = context
        self.caret = Caret(context)
        self.history = History(self)
        self.action = copy.copy(DEFAULT_ACTION)     # type: ignore
        self.keymap = Keymap.from_rules(nvim, DEFAULT_KEYMAP_RULES)
        # Apply custom keymapping
        if 'prompt#custom_mappings' in nvim.vars:
            custom_mappings = nvim.vars['prompt#custom_mappings']
            for rule in custom_mappings:
                self.keymap.register_from_rule(nvim, rule)

    @property
    def text(self) -> str:
        return self.context.text

    @text.setter
    def text(self, value: str) -> None:
        self.context.text = value.replace("\n", " ")
        self.caret.locus = len(value)

    def insert_text(self, text: str) -> None:
        locus = self.caret.locus
        self.text = ''.join([
            self.caret.get_backward_text(),
            text,
            self.caret.get_selected_text(),
            self.caret.get_forward_text(),
        ])
        self.caret.locus = locus + len(text)

    def replace_text(self, text: str) -> None:
        locus = self.caret.locus
        self.text = ''.join([
            self.caret.get_backward_text(),
            text,
            self.caret.get_forward_text(),
        ])
        self.caret.locus = locus + len(text)

    def update_text(self, text: str) -> None:
        if self.insert_mode == InsertMode.replace:
            self.insert_text(text)
        else:
            self.replace_text(text)

    def resolve(self) -> Keystroke:
        timeout = None
        previous = None
        keystroke = None
        while keystroke is None:
            previous, timeout = Keystroke.harvest(
                self.nvim,
                previous,
                timeout,
            )
            keystroke = self.keymap.resolve(previous)
        return keystroke

    def start(self, default: str=None) -> Optional[str]:
        if self.on_init(default):
            return None
        status = None   # Optional[int]
        try:
            while self.on_update(status) is None:
                self.on_redraw()
                #rhs = self.resolve()
                rhs = self.keymap.harvest(self.nvim)
                status = self.on_keypress(rhs)
        except KeyboardInterrupt:
            status = Status.cancel
        except self.nvim.error:
            status = Status.error
        self.nvim.command('redraw!')
        if self.text:
            self.nvim.call('histadd', 'input', self.text)
        result = self.text if status == Status.accept else None
        return self.on_term(status, result) or result

    def on_init(self, default: str) -> Optional[int]:
        self.nvim.call('inputsave')
        if default:
            self.text = default

    def on_redraw(self) -> None:
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

    def on_update(self, status: Status) -> Optional[Status]:
        return status

    def on_keypress(self, keys: Keystroke) -> Optional[Status]:
        m = ACTION_KEYSTROKE_PATTERN.match(str(keys))
        if m:
            return self.action.call(self, m.group(1))
        else:
            self.update_text(str(keys))

    def on_term(self, status: Status, result: str) -> Optional[str]:
        self.nvim.call('inputrestore')
