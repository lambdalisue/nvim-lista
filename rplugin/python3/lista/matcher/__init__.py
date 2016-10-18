"""Matcher module."""
from abc import ABCMeta, abstractmethod
from typing import Sequence
from neovim import Nvim

ESCAPE_VIM_PATTERN_TABLE = str.maketrans({
    '^': '\\^',
    '$': '\\$',
    '~': '\\~',
    '.': '\\.',
    '*': '\\*',
    '[': '\\[',
    ']': '\\]',
    '\\': '\\\\',
})


class AbstractMatcher(metaclass=ABCMeta):
    """An abstract macher class.

    Attributes:
        nvim (neovim.Nvim): A ``neovim.Nvim`` instance.
    """

    def __init__(self, nvim: Nvim) -> None:
        """Constructor.

        Args:
            nvim (neovim.Nvim): A ``neovim.Nvim`` instance.
        """
        self.nvim = nvim
        self._match_id = None    # type: int

    def remove_highlight(self) -> None:
        """Remove current highlight."""
        if self._match_id:
            self.nvim.call('matchdelete', self._match_id)
            self._match_id = None

    def highlight(self, query: str, ignorecase: bool) -> None:
        """Highlight ``query``.

        Args:
            query (str): A query string.
            ignorecase (bool): Boolean to indicate ignorecase.
        """
        self.remove_highlight()
        if not query:
            return
        pattern = self.get_highlight_pattern(query)
        self._match_id = self.nvim.call(
            'matchadd',
            'Title',
            ('\c' if ignorecase else '\C') + pattern,
            0,
        )

    @abstractmethod
    def get_highlight_pattern(self, query: str) -> str:
        """Get highlight pattern for ``query``.

        Args:
            query (str): A query string.
            ignorecase (bool): Boolean to indicate ignorecase.

        Returns:
            str: A pattern to highlight.
        """
        raise NotImplementedError

    @abstractmethod
    def filter(self,
               query: str,
               indices: Sequence[int],
               candidates: Sequence[str],
               ignorecase: bool) -> Sequence[int]:
        """Filter candidates with query and return indices.

        Args:
            query (str): A query string.
            indices (Sequence[int]): An index list available.
            candidates (Sequence[str]): A candidate list.
            ignorecase (bool): Boolean to indicate ignorecase.

        Returns:
            Sequence[int]: A filtered candidate indices.
        """
        raise NotImplementedError


def escape_vim_patterns(text: str) -> str:
    """Escape patterh character used in Vim regex.

    Args:
        text (str): A text being escape.

    Returns:
        str: A escaped text.
    """
    return text.translate(ESCAPE_VIM_PATTERN_TABLE)
