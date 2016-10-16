from curses import ascii
from collections import abc

from datetime import datetime, timedelta

import pytest

from neovim_prompt.key import Key


def test_Key_property():
    key = Key(0x01, '\x01')
    assert isinstance(key, abc.Hashable)
    assert isinstance(key, abc.Container)
    assert isinstance(key, abc.Sized)


def test_Key_parse_with_int(nvim):
    expr = 0x00
    assert Key.parse(nvim, expr).code == expr
    assert Key.parse(nvim, expr).char == '\x00'


def test_Key_parse_with_bytes(nvim):
    expr = b'\x80kb'
    assert Key.parse(nvim, expr).code == expr
    assert Key.parse(nvim, expr).char == ''

    expr = b'a'
    assert Key.parse(nvim, expr).code == ord(expr)
    assert Key.parse(nvim, expr).char == 'a'

    expr = b'INS'
    assert Key.parse(nvim, expr).code == b'INS'
    assert Key.parse(nvim, expr).char == 'INS'

    expr = b'<prompt:accept>'
    assert Key.parse(nvim, expr).code == b'<prompt:accept>'
    assert Key.parse(nvim, expr).char == '<prompt:accept>'


def test_Key_parse_with_bytes_special_key_constant_int(nvim):
    expr = b'<CR>'
    assert Key.parse(nvim, expr).code == ascii.CR
    assert Key.parse(nvim, expr).char == '\r'

    expr = b'<BSLASH>'
    assert Key.parse(nvim, expr).code == ord('\\')
    assert Key.parse(nvim, expr).char == '\\'

    expr = b'<LT>'
    assert Key.parse(nvim, expr).code == ord('<')
    assert Key.parse(nvim, expr).char == '<'


def test_Key_parse_with_bytes_special_key_constant_bytes(nvim):
    expr = b'<BACKSPACE>'
    assert Key.parse(nvim, expr).code == b'\x80kb'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<DELETE>'
    assert Key.parse(nvim, expr).code == b'\x80kD'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<INSERT>'
    assert Key.parse(nvim, expr).code == b'\x80kI'
    assert Key.parse(nvim, expr).char == ''


def test_Key_parse_with_bytes_special_key_ctrl(nvim):
    expr = b'<C-A>'
    assert Key.parse(nvim, expr).code == ord('\x01')
    assert Key.parse(nvim, expr).char == '\x01'

    expr = b'<C-H>'
    assert Key.parse(nvim, expr).code == ord('\x08')
    assert Key.parse(nvim, expr).char == '\x08'

    # NOTE:
    # https://github.com/vim/vim/blob/d58b0f982ad758c59abe47627216a15497e9c3c1/src/gui_w32.c#L1956-L1989
    # When user type '2', '6', or '-' with 'Ctrl' key, Vim assume they type
    # '^@', '^^', or '^_' instead. However, Vim reports "\x90\xfc\x046" for
    # :echo "\<C-6>" so <C-6> should not become <C-^> in key mapping level.
    expr = b'<C-2>'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x042'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<C-6>'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x046'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<C-->'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x04-'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<C-BS>'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x04\x80kb'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<C-INS>'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x04\x80kI'
    assert Key.parse(nvim, expr).char == ''


def test_Key_parse_with_bytes_special_key_meta(nvim):
    expr = b'<M-A>'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x08A'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<M-z>'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x08z'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<M-BS>'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x08\x80kb'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<M-INS>'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x08\x80kI'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<A-A>'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x08A'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<A-z>'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x08z'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<A-BS>'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x08\x80kb'
    assert Key.parse(nvim, expr).char == ''

    expr = b'<A-INS>'
    assert Key.parse(nvim, expr).code == b'\x80\xfc\x08\x80kI'
    assert Key.parse(nvim, expr).char == ''


def test_Key_parse_with_bytes_special_key_leader(nvim):
    nvim.vars = {
        'mapleader': '\\',
        'maplocalleader': ',',
    }
    expr = b'<Leader>'
    assert Key.parse(nvim, expr).code == ord(b'\\')
    assert Key.parse(nvim, expr).char == '\\'

    expr = b'<LocalLeader>'
    assert Key.parse(nvim, expr).code == ord(b',')
    assert Key.parse(nvim, expr).char == ','


def test_Key_parse_with_bytes_str(nvim):
    expr = '<Backspace>'
    assert Key.parse(nvim, expr).code == b'\x80kb'
    assert Key.parse(nvim, expr).char == ''


def test_Key_parse_reify(nvim):
    assert Key.parse(nvim, 0) == Key.parse(nvim, 0)
    assert Key.parse(nvim, 0) != Key.parse(nvim, 1)
    assert Key.parse(nvim, 0) is Key.parse(nvim, 0)

    assert Key.parse(nvim, b'\x80kb') == Key.parse(nvim, b'\x80kb')
    assert Key.parse(nvim, b'\x80kb') != Key.parse(nvim, b'\x80ku')
    assert Key.parse(nvim, b'\x80kb') is Key.parse(nvim, b'\x80kb')


def test_Key_immutability(nvim):
    key = Key.parse(nvim, 0)
    # Changing attributes is not permitted
    with pytest.raises(AttributeError):
        key.code = 1
    with pytest.raises(AttributeError):
        key.char = 1
    # Adding a new attribute is not permitted
    with pytest.raises(AttributeError):
        key.new_attribute = 1
