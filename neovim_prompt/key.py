"""Key module."""
from curses import ascii  # type: ignore
from collections import namedtuple
from . import nvim
from .util import ensure_bytes, ensure_str, int2chr

# Type annotation
try:
    from typing import cast
    from typing import Union, Tuple, Dict, Optional  # noqa: F401
    from neovim import Nvim  # noqa: F401
    KeyCode = Union[int, bytes]  # noqa: F401
    KeyExpr = Union[KeyCode, str]  # noqa: F401
except ImportError:
    cast = lambda t, x: x   # noqa: E731


ESCAPE_QUOTE = str.maketrans({
    '"': '\\"',
})

CTRL_KEY = b'\x80\xfc\x04'
META_KEY = b'\x80\xfc\x08'

# https://github.com/vim/vim/blob/d58b0f982ad758c59abe47627216a15497e9c3c1/src/gui_w32.c#L389-L456
SPECIAL_KEYS = {k: getattr(ascii, k) for k in ascii.controlnames}
SPECIAL_KEYS.update(dict(
    BSLASH=ord('\\'),
    LT=ord('<'),
    UP=b'\x80ku',
    DOWN=b'\x80kd',
    LEFT=b'\x80kl',
    RIGHT=b'\x80kr',
    F1=b'\x80k1',
    F2=b'\x80k2',
    F3=b'\x80k3',
    F4=b'\x80k4',
    F5=b'\x80k5',
    F6=b'\x80k6',
    F7=b'\x80k7',
    F8=b'\x80k8',
    F9=b'\x80k9',
    F10=b'\x80k;',
    F11=b'\x80F1',
    F12=b'\x80F2',
    F13=b'\x80F3',
    F14=b'\x80F4',
    F15=b'\x80F5',
    F16=b'\x80F6',
    F17=b'\x80F7',
    F18=b'\x80F8',
    F19=b'\x80F9',
    F20=b'\x80FA',
    F21=b'\x80FB',
    F22=b'\x80FC',
    F23=b'\x80FD',
    F24=b'\x80FE',
    HELP=b'\x80%1',
    BACKSPACE=b'\x80kb',
    INSERT=b'\x80kI',
    DELETE=b'\x80kD',
    HOME=b'\x80kh',
    END=b'\x80@7',
    PAGEUP=b'\x80kP',
    PAGEDOWN=b'\x80kN',
))
SPECIAL_KEYS_SWAP = {v: k for k, v in SPECIAL_KEYS.items()}
# Add aliases used in Vim. This requires to be AFTER making swap dictionary
SPECIAL_KEYS.update(dict(
    NOP=SPECIAL_KEYS['NUL'],
    RETURN=SPECIAL_KEYS['CR'],
    ENTER=SPECIAL_KEYS['CR'],
    SPACE=SPECIAL_KEYS['SP'],
    BS=SPECIAL_KEYS['BACKSPACE'],
    INS=SPECIAL_KEYS['INSERT'],
    DEL=SPECIAL_KEYS['DELETE'],
))


KeyBase = namedtuple('KeyBase', ['code', 'char'])


class Key(KeyBase):
    """Key class which indicate a single key.

    Note:
        This class defines ``__slots__`` attribute so sub-class must override
        the attribute to extend available attributes.

    Attributes:
        code (int or bytes): A code of the key. A bytes is used when the key is
            a special key in Vim (a key which starts from 0x80 in getchar()).
        char (str): A printable represantation of the key. It might be an empty
            string when the key is not printable.
    """

    __slots__ = ()  # type: Tuple[str, ...]
    __cached = {}   # type: Dict[KeyExpr, Key]

    def __new__(cls, expr: 'KeyExpr') -> 'Key':
        """Constructor.

        Args:
            expr (int, bytes, or str): A key expression.

        Returns:
            Key: A Key instance.
        """
        if expr in cls.__cached:
            return cls.__cached[expr]
        code = _resolve(expr)
        if isinstance(code, int):
            char = int2chr(code)
        elif not code.startswith(b'\x80'):
            char = ensure_str(code)
        else:
            char = ''
        self = super(Key, cls).__new__(cls, code, char)  # type: ignore
        cls.__cached[expr] = self
        return self


def _resolve(expr: 'KeyExpr') -> 'KeyCode':
    if isinstance(expr, int):
        return expr
    elif isinstance(expr, str):
        return _resolve(ensure_bytes(expr))
    elif isinstance(expr, bytes):
        if len(expr) == 1:
            return ord(expr)
        elif expr.startswith(b'\x80'):
            return expr
    else:
        raise AttributeError((
            '`expr` (%s) requires to be an instance of int|bytes|str but '
            '"%s" has specified.'
        ) % (expr, type(expr)))
    # Special key
    if expr.startswith(b'<') or expr.endswith(b'>'):
        inner = expr[1:-1]
        code = _resolve_from_special_keys(inner)
        if code != inner:
            return code
    return expr


def _resolve_from_special_keys(inner: bytes) -> 'KeyCode':
    inner_upper = inner.upper()
    inner_upper_str = ensure_str(inner_upper)
    if inner_upper_str in SPECIAL_KEYS:
        return SPECIAL_KEYS[inner_upper_str]
    elif inner_upper.startswith(b'C-'):
        if len(inner) == 3:
            if inner_upper[-1] in b'@ABCDEFGHIKLMNOPQRSTUVWXYZ[\\]^_?':
                return ascii.ctrl(inner[-1])
        return b''.join([
            CTRL_KEY,
            cast(bytes, _resolve_from_special_keys(inner[2:])),
        ])
    elif inner_upper.startswith(b'M-') or inner_upper.startswith(b'A-'):
        return b''.join([
            META_KEY,
            cast(bytes, _resolve_from_special_keys(inner[2:])),
        ])
    elif inner_upper == b'LEADER':
        leader = nvim.vars['mapleader']
        leader = ensure_bytes(leader)
        return _resolve(leader)
    elif inner_upper == b'LOCALLEADER':
        leader = nvim.vars['maplocalleader']
        leader = ensure_bytes(leader)
        return _resolve(leader)
    return inner
