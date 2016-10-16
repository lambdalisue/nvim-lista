import neovim_prompt.util as util
import pytest


def test_ensure_bytes():
    assert isinstance(util.ensure_bytes('foo'), bytes)
    assert isinstance(util.ensure_bytes(b'foo'), bytes)


def test_ensure_str():
    assert isinstance(util.ensure_str('foo'), str)
    assert isinstance(util.ensure_str(b'foo'), str)


def test_int2chr():
    # NOTE: utf-8
    assert util.int2chr(97) == 'a'
    assert util.int2chr(12354) == 'あ'
