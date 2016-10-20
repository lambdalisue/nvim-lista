"""Prompt module."""
import re
import copy
import enum
from datetime import timedelta
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
    """A prompt status enum class."""

    progress = 0
    accept = 1
    cancel = 2
    error = 3


class InsertMode(enum.Enum):
    """A insert mode enum class."""

    insert = 1
    replace = 2


class Prompt:
    """Prompt class."""

    prefix = ''

    def __init__(self, nvim: Nvim, context: Context) -> None:
        """Constructor.

        Args:
            nvim (neovim.Nvim): A ``neovim.Nvim`` instance.
            context (Context): A ``neovim_prompt.context.Context`` instance.
        """
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

    @property
    def text(self) -> str:
        """str: A current context text.

        It automatically adjust the current caret locus to the tail of the text
        if any text is assigned.

        It calls the following overridable methods in order of the appearance.

        - on_init - Only once
        - on_update
        - on_redraw
        - on_keypress
        - on_term - Only once

        Example:
            >>> from neovim_prompt.context import Context
            >>> from unittest.mock import MagicMock
            >>> nvim = MagicMock()
            >>> nvim.options = {'encoding': 'utf-8'}
            >>> context = Context()
            >>> context.text = "Hello"
            >>> context.caret_locus = 3
            >>> prompt = Prompt(nvim, context)
            >>> prompt.text
            'Hello'
            >>> prompt.caret.locus
            3
            >>> prompt.text = "FooFooFoo"
            >>> prompt.text
            'FooFooFoo'
            >>> prompt.caret.locus
            9
        """
        return self.context.text

    @text.setter
    def text(self, value: str) -> None:
        self.context.text = value.replace("\n", " ")
        self.caret.locus = len(value)

    def apply_custom_mappings_from_vim_variable(self, varname: str) -> None:
        """Apply custom key mappings from Vim variable.

        Args:
            varname (str): A global Vim's variable name
        """
        if varname in self.nvim.vars:
            custom_mappings = self.nvim.vars[varname]
            for rule in custom_mappings:
                self.keymap.register_from_rule(self.nvim, rule)

    def insert_text(self, text: str) -> None:
        """Insert text after the caret.

        Args:
            text (str): A text which will be inserted after the caret.

        Example:
            >>> from neovim_prompt.context import Context
            >>> from unittest.mock import MagicMock
            >>> nvim = MagicMock()
            >>> nvim.options = {'encoding': 'utf-8'}
            >>> context = Context()
            >>> context.text = "Hello Goodbye"
            >>> context.caret_locus = 3
            >>> prompt = Prompt(nvim, context)
            >>> prompt.insert_text('AA')
            >>> prompt.text
            'HelAAlo Goodbye'
        """
        locus = self.caret.locus
        self.text = ''.join([
            self.caret.get_backward_text(),
            text,
            self.caret.get_selected_text(),
            self.caret.get_forward_text(),
        ])
        self.caret.locus = locus + len(text)

    def replace_text(self, text: str) -> None:
        """Replace text after the caret.

        Args:
            text (str): A text which will be replaced after the caret.

        Example:
            >>> from neovim_prompt.context import Context
            >>> from unittest.mock import MagicMock
            >>> nvim = MagicMock()
            >>> nvim.options = {'encoding': 'utf-8'}
            >>> context = Context()
            >>> context.text = "Hello Goodbye"
            >>> context.caret_locus = 3
            >>> prompt = Prompt(nvim, context)
            >>> prompt.replace_text('AA')
            >>> prompt.text
            'HelAA Goodbye'
        """
        locus = self.caret.locus
        self.text = ''.join([
            self.caret.get_backward_text(),
            text,
            self.caret.get_forward_text()[len(text) - 1:],
        ])
        self.caret.locus = locus + len(text)

    def update_text(self, text: str) -> None:
        """Insert or replace text after the caret.

        Args:
            text (str): A text which will be replaced after the caret.

        Example:
            >>> from neovim_prompt.context import Context
            >>> from unittest.mock import MagicMock
            >>> nvim = MagicMock()
            >>> nvim.options = {'encoding': 'utf-8'}
            >>> context = Context()
            >>> context.text = "Hello Goodbye"
            >>> context.caret_locus = 3
            >>> prompt = Prompt(nvim, context)
            >>> prompt.insert_mode = InsertMode.insert
            >>> prompt.update_text('AA')
            >>> prompt.text
            'HelAAlo Goodbye'
            >>> prompt.insert_mode = InsertMode.replace
            >>> prompt.update_text('BB')
            >>> prompt.text
            'HelAABB Goodbye'
        """
        if self.insert_mode == InsertMode.insert:
            self.insert_text(text)
        else:
            self.replace_text(text)

    def start(self, default: str=None) -> Optional[str]:
        """Start prompt with ``default`` text and return value.

        It starts prompt loop and return a input value when accepted. Otherwise
        it returns None.

        Args:
            default (None or str): A default text of the prompt. If omitted, a
                text in the context specified in the constructor is used.

        Returns:
            None or str: None if the prompt status is not Status.accept.
                Otherwise a input value.
        """
        status = self.on_init(default) or Status.progress
        if self.nvim.options['timeout']:
            timeoutlen = timedelta(
                milliseconds=int(self.nvim.options['timeoutlen'])
            )
        else:
            timeoutlen = None
        try:
            status = self.on_update(status) or Status.progress
            while status is Status.progress:
                self.on_redraw()
                status = self.on_keypress(
                    self.keymap.harvest(self.nvim, timeoutlen)
                ) or Status.progress
                status = self.on_update(status) or Status.progress
        except KeyboardInterrupt:
            status = Status.cancel
        except self.nvim.error:
            status = Status.error
        self.nvim.command('redraw!')
        if self.text:
            self.nvim.call('histadd', 'input', self.text)
        result = self.text if status is Status.accept else None
        return self.on_term(status, result) or result

    def on_init(self, default: Optional[str]) -> Optional[Status]:
        """Initialize the prompt.

        It calls 'inputsave' function in Vim and assign ``default`` text to the
        ``self.text`` to initialize the prompt text in default.

        Args:
            default (None or str): A default text of the prompt. If omitted, a
                text in the context specified in the constructor is used.

        Returns:
            None or Status: The return value will be used as a status of the
                prompt mainloop, indicating that if return value is not
                Status.progress, the prompt mainloop immediately terminated.
                Returning None is equal to returning Status.progress.
        """
        self.nvim.call('inputsave')
        if default:
            self.text = default

    def on_update(self, status: Optional[Status]) -> Status:
        """Update the prompt status and return the status.

        It is used to update the prompt status. In default, it does nothing and
        return the specified ``status`` directly.

        Args:
            status (Status): A prompt status which is updated by previous
                on_keypress call.

        Returns:
            None or Status: The return value will be used as a status of the
                prompt mainloop, indicating that if return value is not
                Status.progress, the prompt mainloop immediately terminated.
                Returning None is equal to returning Status.progress.
        """
        return status

    def on_redraw(self) -> None:
        """Redraw the prompt.

        It is used to redraw the prompt. In default, it echos specified prefix
        the caret, and input text.
        """
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

    def on_keypress(self, keystroke: Keystroke) -> Optional[Status]:
        """Handle a pressed keystroke and return the status.

        It is used to handle a pressed keystroke. Note that subclass should NOT
        override this method to perform actions. Register a new custom action
        instead. In default, it call action and return the result if the
        keystroke is <xxx:xxx>or call Vim function XXX and return the result
        if the keystroke is <call:XXX>.

        Args:
            keystroke (Keystroke): A pressed keystroke instance. Note that this
                instance is a reslved keystroke instace by keymap.

        Returns:
            None or Status: The return value will be used as a status of the
                prompt mainloop, indicating that if return value is not
                Status.progress, the prompt mainloop immediately terminated.
                Returning None is equal to returning Status.progress.
        """
        m = ACTION_KEYSTROKE_PATTERN.match(str(keystroke))
        if m:
            return self.action.call(self, m.group(1))
        else:
            self.update_text(str(keystroke))

    def on_term(self, status: Status, result: str) -> Optional[str]:
        """Finalize the prompt.

        It calls 'inputrestore' function in Vim to finalize the prompt in
        default. The return value is used as a return value of the prompt if
        non None is returned.

        Args:
            status (Status): A prompt status.
            result (str): An input text.

        Returns:
            None or str: If a return value is not None, the value is used as a
                return value of the prompt.
        """
        self.nvim.call('inputrestore')
