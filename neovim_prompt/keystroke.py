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
    """Keystroke class which indicate multiple keys pressed within timeout."""

    __hash__ = tuple.__hash__
    __slots__ = ()  # type: Tuple[str, ...]

    def __str__(self) -> str:
        return ''.join(str(k) for k in self)

    def startswith(self, other: 'Keystroke') -> bool:
        """Startswith."""
        if len(self) < len(other):
            return False
        return all(lhs == rhs for lhs, rhs in zip(self, other))

    @classmethod
    def parse(cls, nvim: Nvim, expr: KeystrokeExpr) -> 'Keystroke':
        """Parse a keystroke expression and return a Keystroke instance.

        Args:
            nvim (neovim.Nvim): A ``neovim.Nvim`` instance.
            expr (tuple, bytes, str): A keystroke expression.

        Returns:
            Keystroke: A Keystroke instance.
        """
        keys = _ensure_keys(nvim, expr)
        instance = cls(cast(Iterable, keys))
        return instance


def _ensure_keys(nvim: Nvim, expr: KeystrokeExpr) -> KeystrokeType:
    """Ensure keys."""
    if isinstance(expr, (bytes, str)):
        expr_bytes = ensure_bytes(nvim, expr)   # type: ignore
        keys = tuple(
            Key.parse(nvim, k)
            for k in KEYS_PATTERN.findall(expr_bytes)
        )
    else:
        keys = tuple(expr)
    return keys
