"""Keystroke module."""
import re
import time
from datetime import datetime, timedelta
from typing import cast, Optional, Union, Tuple, Iterable
from neovim import Nvim
from .key import Key
from .util import ensure_bytes, getchar


KeystrokeType = Tuple[Key, ...]
KeystrokeExpr = Union[KeystrokeType, bytes, str]


KEYS_PATTERN = re.compile(b'(?:<[^>]+>|\S)')


class Keystroke(tuple):
    """Keystroke class which indicate multiple keys pressed within timeout."""

    __hash__ = tuple.__hash__
    __slots__ = ()  # type: Tuple[str, ...]

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

    @classmethod
    def harvest(cls,
                nvim: Nvim,
                previous: Optional['Keystroke']=None,
                timeout: Optional[datetime]=None
                ) -> Tuple['Keystroke', datetime]:
        """Harvest keystroke."""
        if previous is None and timeout is None:
            if nvim.options['timeout']:
                timeout = datetime.now() + timedelta(
                    milliseconds=int(nvim.options['timeoutlen']),
                )
        key = Key.parse(nvim, getchar(nvim))
        if key is None:
            keystroke = previous
        elif previous is None or (timeout and timeout < datetime.now()):
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
        return ''.join(str(k) for k in self)


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


def _getchar(nvim: 'Nvim', timeout: Optional[datetime]) -> Optional[Key]:
    while not timeout or timeout > datetime.now():
        char = getchar(nvim, False)
        if char != 0:
            return char
        time.sleep(0.01)
    return None
