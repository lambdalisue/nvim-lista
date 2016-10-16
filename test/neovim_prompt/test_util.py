import neovim_prompt.util as util
import pytest


def test_ensure_bytes(nvim):
    assert isinstance(util.ensure_bytes(nvim, 'foo'), bytes)
    assert isinstance(util.ensure_bytes(nvim, b'foo'), bytes)


def test_ensure_str(nvim):
    assert isinstance(util.ensure_str(nvim, 'foo'), str)
    assert isinstance(util.ensure_str(nvim, b'foo'), str)


def test_int2chr(nvim):
    # NOTE: utf-8
    assert util.int2chr(nvim, 97) == 'a'
    assert util.int2chr(nvim, 12354) == 'あ'
