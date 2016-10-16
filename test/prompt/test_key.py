from curses import ascii
from collections import abc

from datetime import datetime, timedelta

import pytest

from neovim_prompt.key import Key


def test_Key_property():
    key = Key(0x00)
    assert isinstance(key, abc.Hashable)
    assert isinstance(key, abc.Container)
    assert isinstance(key, abc.Sized)


def test_Key_with_int():
    code = 0x00
    assert Key(code).code == code
    assert Key(code).char == '\x00'


def test_Key_with_bytes():
    code = b'\x80kb'
    assert Key(code).code == code
    assert Key(code).char == ''

    code = b'a'
    assert Key(code).code == ord(code)
    assert Key(code).char == 'a'

    code = b'INS'
    assert Key(code).code == b'INS'
    assert Key(code).char == 'INS'

    code = b'<prompt:accept>'
    assert Key(code).code == b'<prompt:accept>'
    assert Key(code).char == '<prompt:accept>'


def test_Key_with_bytes_special_key_constant_int():
    code = b'<CR>'
    assert Key(code).code == ascii.CR
    assert Key(code).char == '\r'

    code = b'<BSLASH>'
    assert Key(code).code == ord('\\')
    assert Key(code).char == '\\'

    code = b'<LT>'
    assert Key(code).code == ord('<')
    assert Key(code).char == '<'


def test_Key_with_bytes_special_key_constant_bytes():
    code = b'<BACKSPACE>'
    assert Key(code).code == b'\x80kb'
    assert Key(code).char == ''

    code = b'<DELETE>'
    assert Key(code).code == b'\x80kD'
    assert Key(code).char == ''

    code = b'<INSERT>'
    assert Key(code).code == b'\x80kI'
    assert Key(code).char == ''


def test_Key_with_bytes_special_key_ctrl():
    code = b'<C-A>'
    assert Key(code).code == ord('\x01')
    assert Key(code).char == '\x01'

    code = b'<C-H>'
    assert Key(code).code == ord('\x08')
    assert Key(code).char == '\x08'

    # NOTE:
    # https://github.com/vim/vim/blob/d58b0f982ad758c59abe47627216a15497e9c3c1/src/gui_w32.c#L1956-L1989
    # When user type '2', '6', or '-' with 'Ctrl' key, Vim assume they type
    # '^@', '^^', or '^_' instead. However, Vim reports "\x90\xfc\x046" for
    # :echo "\<C-6>" so <C-6> should not become <C-^> in key mapping level.
    code = b'<C-2>'
    assert Key(code).code == b'\x80\xfc\x042'
    assert Key(code).char == ''

    code = b'<C-6>'
    assert Key(code).code == b'\x80\xfc\x046'
    assert Key(code).char == ''

    code = b'<C-->'
    assert Key(code).code == b'\x80\xfc\x04-'
    assert Key(code).char == ''

    code = b'<C-BS>'
    assert Key(code).code == b'\x80\xfc\x04\x80kb'
    assert Key(code).char == ''

    code = b'<C-INS>'
    assert Key(code).code == b'\x80\xfc\x04\x80kI'
    assert Key(code).char == ''


def test_Key_with_bytes_special_key_meta():
    code = b'<M-A>'
    assert Key(code).code == b'\x80\xfc\x08A'
    assert Key(code).char == ''

    code = b'<M-z>'
    assert Key(code).code == b'\x80\xfc\x08z'
    assert Key(code).char == ''

    code = b'<M-BS>'
    assert Key(code).code == b'\x80\xfc\x08\x80kb'
    assert Key(code).char == ''

    code = b'<M-INS>'
    assert Key(code).code == b'\x80\xfc\x08\x80kI'
    assert Key(code).char == ''

    code = b'<A-A>'
    assert Key(code).code == b'\x80\xfc\x08A'
    assert Key(code).char == ''

    code = b'<A-z>'
    assert Key(code).code == b'\x80\xfc\x08z'
    assert Key(code).char == ''

    code = b'<A-BS>'
    assert Key(code).code == b'\x80\xfc\x08\x80kb'
    assert Key(code).char == ''

    code = b'<A-INS>'
    assert Key(code).code == b'\x80\xfc\x08\x80kI'
    assert Key(code).char == ''


def test_Key_with_bytes_special_key_leader():
    # NOTE: mapleader/maplocalleader are defined in conftest.py
    code = b'<Leader>'
    assert Key(code).code == ord(b'\\')
    assert Key(code).char == '\\'

    code = b'<LocalLeader>'
    assert Key(code).code == ord(b',')
    assert Key(code).char == ','


def test_Key_with_bytes_str():
    code = '<Backspace>'
    assert Key(code).code == b'\x80kb'
    assert Key(code).char == ''


def test_Key_reify():
    assert Key(0) == Key(0)
    assert Key(0) != Key(1)
    assert Key(0) is Key(0)

    assert Key(b'\x80kb') == Key(b'\x80kb')
    assert Key(b'\x80kb') != Key(b'\x80ku')
    assert Key(b'\x80kb') is Key(b'\x80kb')


def test_Key_immutability():
    key = Key(0)
    # Changing attributes is not permitted
    with pytest.raises(AttributeError):
        key.code = 1
    with pytest.raises(AttributeError):
        key.char = 1
    # Adding a new attribute is not permitted
    with pytest.raises(AttributeError):
        key.new_attribute = 1
