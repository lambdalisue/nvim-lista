"""Utility module."""
# NOTE:
# The 'encoding' option is usually not modified during Vim's live session (the
# behaviour for modifying 'encoding' option during Vim's live session is not
# defined, see :help encoding).
# Thus retrieve the value here to reduce Python --> Vim access.
# Additionally, vim.options['encoding'] returns "bytes" in Vim and "str" in
# Neovim so ensure the value to be a "str" instance.
from . import nvim
_ = nvim.options['encoding']
ENCODING = _ if isinstance(_, str) else _.decode('latin')


# Type annotation
try:
    from typing import Callable, Any, AnyStr  # noqa: F401
    from neovim import Nvim  # noqa: F401
except ImportError:
    pass


def ensure_bytes(seed: 'AnyStr') -> bytes:
    """Encode `str` to `bytes` if necessary and return."""
    if isinstance(seed, str):
        return seed.encode(ENCODING, 'surrogateescape')
    return seed


def ensure_str(seed: 'AnyStr') -> str:
    """Decode `bytes` to `str` if necessary and return."""
    if isinstance(seed, bytes):
        return seed.decode(ENCODING, 'surrogateescape')
    return seed


def int2chr(code: int) -> str:
    """Return a corresponding char of `code`.

    It uses "nr2char()" in Vim script when 'encoding' option is not utf-8.
    Otherwise it uses "chr()" in Python to improve the performance.
    """
    if ENCODING in ('utf-8', 'utf8'):
        return chr(code)
    return nvim.call('nr2char', code)
