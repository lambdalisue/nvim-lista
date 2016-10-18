"""Keystroke module."""
import re
from typing import cast, Union, Tuple, Iterable
from neovim import Nvim
from .key import Key
from .util import ensure_bytes


KeystrokeType = Tuple[Key, ...]
KeystrokeExpr = Union[KeystrokeType, bytes, str]


KEYS_PATTERN = re.compile(b'(?:<[^>]+>|\S)')


class Keystroke(tuple):
    """Keystroke class which indicate multiple keys."""

    __hash__ = tuple.__hash__
    __slots__ = ()  # type: Tuple[str, ...]

    def __str__(self) -> str:
        return ''.join(str(k) for k in self)

    def startswith(self, other: 'Keystroke') -> bool:
        """Check if the keystroke starts from ``other``.

        Args:
            other (Keystroke): A keystroke instance will be checked.

        Returns:
            bool: True if the keystroke starts from ``other``.
        """
        if len(self) < len(other):
            return False
        return all(lhs == rhs for lhs, rhs in zip(self, other))

    @classmethod
    def parse(cls, nvim: Nvim, expr: KeystrokeExpr) -> 'Keystroke':
        """Parse a keystroke expression and return a Keystroke instance.

        Args:
            nvim (neovim.Nvim): A ``neovim.Nvim`` instance.
            expr (tuple, bytes, str): A keystroke expression.

        Example:
            >>> from unittest.mock import MagicMock
            >>> nvim = MagicMock()
            >>> nvim.options = {'encoding': 'utf-8'}
            >>> Keystroke.parse(nvim, 'abc')
            (Key(code=97, ...), Key(code=98, ...), Key(code=99, ...))
            >>> Keystroke.parse(nvim, '<Insert>')
            (Key(code=b'\x80kI', char=''),)

        Returns:
            Keystroke: A Keystroke instance.
        """
        keys = _ensure_keys(nvim, expr)
        instance = cls(cast(Iterable, keys))
        return instance


def _ensure_keys(nvim: Nvim, expr: KeystrokeExpr) -> KeystrokeType:
    if isinstance(expr, (bytes, str)):
        expr_bytes = ensure_bytes(nvim, expr)   # type: ignore
        keys = tuple(
            Key.parse(nvim, k)
            for k in KEYS_PATTERN.findall(expr_bytes)
        )
    else:
        keys = tuple(expr)
    return keys
