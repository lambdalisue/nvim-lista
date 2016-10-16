"""Keystroke module."""
import re
from datetime import datetime, timedelta
from .key import Key
from .util import ensure_bytes

# Type annotation
try:
    from typing import cast
    from typing import Optional, Union, Tuple, Iterable  # noqa: F401
    from neovim import Nvim  # noqa: F401
    from .key import KeyCode  # noqa: F401

    KeystrokeType = Tuple[Key, ...]
    KeystrokeExpr = Union[KeystrokeType, bytes, str]
except ImportError:
    cast = lambda t, x: x   # noqa: E731


KEYS_PATTERN = re.compile(b'(?:<[^>]+>|\S)')


class Keystroke(tuple):
    """Keystroke class which indicate multiple keys pressed within timeout."""

    __hash__ = tuple.__hash__
    __slots__ = ()  # type: Tuple[str, ...]

    @classmethod
    def parse(cls, nvim: 'Nvim', expr: 'KeystrokeExpr') -> 'Keystroke':
        """Parse a keystroke expression and return a Keystroke instance.

        Args:
            nvim (neovim.Nvim): A ``neovim.Nvim`` instance.
            expr (tuple, bytes, str): A keystroke expression.

        Returns:
            Keystroke: A Keystroke instance.
        """
        keys = _ensure_keys(nvim, expr)
        instance = cls(cast('Iterable', keys))
        return instance

    @classmethod
    def harvest(cls,
                nvim: 'Nvim',
                previous: 'Optional[Keystroke]'=None,
                timeout: 'Optional[datetime]'=None
                ) -> 'Tuple[Keystroke, datetime]':
        """Harvest keystroke."""
        if previous is None and timeout is None:
            if nvim.options['timeout']:
                timeout = datetime.now() + timedelta(
                    milliseconds=int(nvim.options['timeoutlen']),
                )
        key = Key.parse(nvim, _getchar(nvim))
        if previous is None or (timeout and timeout < datetime.now()):
            keystroke = Keystroke([key])
        else:
            keystroke = Keystroke(previous + (key,))
        return (keystroke, timeout)

    def startswith(self, other: 'Keystroke') -> bool:
        """Startswith."""
        if len(self) < len(other):
            return False
        return all(lhs == rhs for lhs, rhs in zip(self, other))

    def __str__(self) -> str:
        return ''.join(k.char for k in self)


def _ensure_keys(nvim: 'Nvim', expr: 'KeystrokeExpr') -> 'KeystrokeType':
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


def _getchar(nvim: 'Nvim') -> 'KeyCode':
    ret = nvim.call('prompt#getchar')
    if isinstance(ret, int):
        return ret
    else:
        return bytes(ret)
