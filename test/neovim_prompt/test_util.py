from unittest.mock import MagicMock, patch
import pytest
import neovim_prompt.util as util


def test_ensure_bytes(nvim):
    assert isinstance(util.ensure_bytes(nvim, 'foo'), bytes)
    assert isinstance(util.ensure_bytes(nvim, b'foo'), bytes)


def test_ensure_str(nvim):
    assert isinstance(util.ensure_str(nvim, 'foo'), str)
    assert isinstance(util.ensure_str(nvim, b'foo'), str)


def test_int2chr(nvim):
    assert util.int2chr(nvim, 97) == 'a'
    assert util.int2chr(nvim, 12354) == 'あ'

    with patch('neovim_prompt.util.get_encoding') as get_encoding:
        get_encoding.return_value = 'sjis'

        def nr2char(fname: str, code: int):
            b = code.to_bytes(2, byteorder='big')
            return b.decode('sjis')

        nvim.call = MagicMock()
        nvim.call.side_effect = nr2char
        code = int.from_bytes(b'\x82\x60', byteorder='big')
        assert util.int2chr(nvim, code) == 'Ａ'


def test_getchar(nvim):
    nvim.call = MagicMock()
    nvim.call.return_value = 97
    assert util.getchar(nvim) == 97

    nvim.call.return_value = b'a'
    assert util.getchar(nvim) == b'a'

    nvim.call.return_value = 'a'
    assert util.getchar(nvim) == b'a'
