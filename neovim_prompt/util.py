"""Utility module."""
from typing import AnyStr, Union
from neovim import Nvim

_cached_encoding = None     # type: str


def get_encoding(nvim: Nvim) -> str:
    """Return a Vim's internal encoding.

    The retrieve encoding is cached to the function instance while encoding
    options should not be changed in Vim's live session (see :h encoding) to
    enhance performance.

    Args:
        nvim (neovim.Nvim): A ``neovim.Nvim`` instance.

    Returns:
        str: A Vim's internal encoding.
    """
    global _cached_encoding
    if _cached_encoding is None:
        _cached_encoding = nvim.options['encoding']
    return _cached_encoding


def ensure_bytes(nvim: Nvim, seed: AnyStr) -> bytes:
    """Encode `str` to `bytes` if necessary and return."""
    if isinstance(seed, str):
        encoding = get_encoding(nvim)
        return seed.encode(encoding, 'surrogateescape')
    return seed


def ensure_str(nvim: Nvim, seed: AnyStr) -> str:
    """Decode `bytes` to `str` if necessary and return."""
    if isinstance(seed, bytes):
        encoding = get_encoding(nvim)
        return seed.decode(encoding, 'surrogateescape')
    return seed


def int2chr(nvim: Nvim, code: int) -> str:
    """Return a corresponding char of `code`.

    It uses "nr2char()" in Vim script when 'encoding' option is not utf-8.
    Otherwise it uses "chr()" in Python to improve the performance.
    """
    encoding = get_encoding(nvim)
    if encoding in ('utf-8', 'utf8'):
        return chr(code)
    return nvim.call('nr2char', code)


def getchar(nvim: Nvim, *args) -> Union[int, bytes]:
    """Call getchar and return int or bytes instance."""
    ret = nvim.call('getchar', *args)
    if isinstance(ret, int):
        return ret
    return ensure_bytes(nvim, ret)
