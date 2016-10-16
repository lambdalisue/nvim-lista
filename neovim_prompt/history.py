"""Command-line history module."""
from . import nvim

# Type annotation
try:
    from typing import Optional  # noqa: F401
    from neovim import Nvim  # noqa: F401
    from .prompt import Prompt  # noqa: F401
except ImportError:
    pass


class History:
    """History class which manage a Vim's command-line history for input. """

    __slots__ = ('_index', '_cached', '_backward', '_threshold')

    def __init__(self, prompt: 'Prompt') -> None:
        """Constructor.

        Args:
            prompt (Prompt): The ``prompt.prompt.Prompt`` instance. The
                instance is used to initialize internal variables and never
                stored.

        """
        self._index = 0
        self._cached = prompt.text
        self._backward = prompt.caret.get_backward_text()
        self._threshold = 0

    def current(self) -> str:
        """Current command-line history value of input.

        Returns:
            str: A current command-line history value of input which an
                internal index points to. It returns a cached value when the
                internal index points to 0.
        """
        if self._index == 0:
            return self._cached
        return nvim.call('histget', 'input', -self._index)

    def previous(self, prompt: 'Prompt') -> str:
        """Get previous command-line history value of input.

        It increases an internal index and points to a previous command-line
        history value.

        Note that it cahces a ``prompt.text`` when the internal index was 0 (an
        initial value) and the cached value is used when the internal index
        points to 0.
        This behaviour is to mimic a Vim's builtin command-line history
        behaviour.

        Args:
            prompt (Prompt): An instance of ``prompt.prompt.Prompt``.

        Returns:
            str: A previous command-line history value of input.
        """
        if self._index == 0:
            self._cached = prompt.text
            self._threshold = nvim.call('histnr', 'input')
        if self._index < self._threshold:
            self._index += 1
        return self.current()

    def next(self) -> str:
        """Get next command-line history value of input.

        It decreases an internal index and points to a next command-line
        history value.

        Returns:
            str: A next command-line history value of input.
        """
        if self._index > 0:
            self._index -= 1
        return self.current()

    def previous_match(self, prompt: 'Prompt') -> str:
        """Get previous command-line history value which matches with an
        initial query text.

        The initial query text is a text before the cursor when an internal
        index was 0 (like a cached value but only before the cursor.)
        It increases an internal index until a previous command-line history
        value matches to an initial query text and points to the matched
        previous history value.
        This behaviour is to mimic a Vim's builtin command-line history
        behaviour.

        Args:
            prompt (Prompt): An instance of ``prompt.prompt.Prompt``.

        Returns:
            str: A matched previous command-line history value of input.
        """
        if self._index == 0:
            self._backward = prompt.caret.get_backward_text()
        index = _index = self._index - 1
        while _index < self._index:
            _index = self._index
            candidate = self.previous(prompt)
            if candidate.startswith(self._backward):
                return candidate
        self._index = index
        return self.previous(prompt)

    def next_match(self) -> str:
        """Get next command-line history value of input which matches with an
        initial query text.

        The initial query text is a text before the cursor when an internal
        index was 0 (like a cached value but only before the cursor.)
        It decreases an internal index until a next command-line history value
        matches to an initial query text and points to the matched next
        command-line history value.
        This behaviour is to mimic a Vim's builtin command-line history
        behaviour.

        Returns:
            str: A matched previous history value.
        """
        if self._index == 0:
            return self._cached
        index = _index = self._index + 1
        while _index > self._index:
            _index = self._index
            candidate = self.next()
            if candidate.startswith(self._backward):
                return candidate
        self._index = index
        return self.next()
