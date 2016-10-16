"""Prompt module."""
import re
import copy
from .key import Key
from .keystroke import Keystroke


# Type annotation
try:
    from typing import cast
    from typing import Optional, Union, Tuple  # noqa: F401
    from neovim import Nvim  # noqa: F401
    from .key import KeyCode  # noqa: F401
    from .context import Context  # noqa: F401
    from .action import Action  # noqa: F401
    KeystrokeType = Tuple[Key, ...]     # noqa: F401
    KeystrokeExpr = Union[KeystrokeType, bytes, str]    # noqa: F401
except ImportError:
    cast = lambda t, x: x   # noqa: E731


ACTION_KEYSTROKE_PATTERN = re.compile(r'<(\w+:\w+)>')

ESCAPE_ECHO = str.maketrans({
    '"': '\\"',
    '\\': '\\\\',
})

STATUS_ACCEPT = 1
STATUS_CANCEL = 0
STATUS_ERROR = -1

MODE_INSERT = 'insert'
MODE_REPLACE = 'replace'


class Prompt:
    """Prompt class."""
    prefix = '# '

    def __init__(self, nvim: 'Nvim', context: 'Context') -> None:
        from .caret import Caret
        from .history import History
        from .keymap import DEFAULT_KEYMAP_RULES, Keymap
        from .action import DEFAULT_ACTION
        self.nvim = nvim
        self.mode = MODE_INSERT
        self.context = context
        self.caret = Caret(context)
        self.history = History(self)
        self.action = copy.copy(DEFAULT_ACTION)    # type: ignore
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

    def insert_text(self, text):
        locus = self.caret.locus
        self.text = ''.join([
            self.caret.get_backward_text(),
            text,
            self.caret.get_selected_text(),
            self.caret.get_forward_text(),
        ])
        self.caret.locus = locus + len(text)

    def replace_text(self, text):
        locus = self.caret.locus
        self.text = ''.join([
            self.caret.get_backward_text(),
            text,
            self.caret.get_forward_text(),
        ])
        self.caret.locus = locus + len(text)

    def update_text(self, text):
        if self.mode == MODE_INSERT:
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

    def start(self, default: str=None) -> 'Optional[str]':
        if self.on_init(default):
            return None
        status = None   # Optional[int]
        try:
            while self.on_update(status) is None:
                self.on_redraw()
                rhs = self.resolve()
                status = self.on_keypress(rhs)
        except KeyboardInterrupt:
            status = STATUS_CANCEL
        except self.nvim.error:
            status = STATUS_ERROR
        self.nvim.command('redraw!')
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

    def on_keypress(self, keys):
        m = ACTION_KEYSTROKE_PATTERN.match(str(keys))
        if m:
            return self.action.call(self, m.group(1))
        else:
            return self.update_text(str(keys))

    def on_term(self, status, result):
        self.nvim.call('inputrestore')
