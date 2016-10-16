from curses import ascii
from collections import abc
from contextlib import ExitStack

from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from neovim_prompt.key import Key
from neovim_prompt.keystroke import Keystroke


def test_Keystroke_property():
    keys = Keystroke('abc')
    assert isinstance(keys, abc.Hashable)
    assert isinstance(keys, abc.Container)
    assert isinstance(keys, abc.Sized)


def test_Keystroke_with_sequence():
    expr = [
        Key('a'),
        Key('b'),
        Key('c'),
    ]
    keys = Keystroke(expr)
    assert keys == tuple(expr)

    keys = Keystroke(tuple(expr))
    assert keys == tuple(expr)


def test_Keystroke_with_bytes():
    expr = [
        Key('a'),
        Key('b'),
        Key('c'),
    ]
    keys = Keystroke(b'abc')
    assert keys == tuple(expr)

    expr = [
        Key('<C-T>'),
        Key('b'),
        Key('<Home>'),
    ]
    keys = Keystroke(b'<C-T>b<Home>')
    assert keys == tuple(expr)


def test_Keystroke_with_str():
    expr = [
        Key('a'),
        Key('b'),
        Key('c'),
    ]
    keys = Keystroke('abc')
    assert keys == tuple(expr)

    expr = [
        Key('<C-T>'),
        Key('b'),
        Key('<Home>'),
    ]
    keys = Keystroke('<C-T>b<Home>')
    assert keys == tuple(expr)


def test_Keystroke_startswith():
    rhs1 = Keystroke('<C-A>')
    rhs2 = Keystroke('<C-A><C-B>')
    rhs3 = Keystroke('<C-A><C-C>')

    assert rhs1.startswith(Keystroke(''))
    assert rhs2.startswith(Keystroke(''))
    assert rhs3.startswith(Keystroke(''))

    assert rhs1.startswith(Keystroke('<C-A>'))
    assert rhs2.startswith(Keystroke('<C-A>'))
    assert rhs3.startswith(Keystroke('<C-A>'))

    assert not rhs1.startswith(Keystroke('<C-A><C-B>'))
    assert rhs2.startswith(Keystroke('<C-A><C-B>'))
    assert not rhs3.startswith(Keystroke('<C-A><C-B>'))

    assert not rhs1.startswith(Keystroke('<C-A><C-B><C-C>'))
    assert not rhs2.startswith(Keystroke('<C-A><C-B><C-C>'))
    assert not rhs3.startswith(Keystroke('<C-A><C-B><C-C>'))


def test_Keystroke_str():
    assert str(Keystroke('abc')) == 'abc'
    assert str(Keystroke('<C-H><C-H>')) == '\x08\x08'
    assert str(Keystroke('<Backspace><Delete>')) == ''
    assert str(Keystroke('<prompt:accept>')) == '<prompt:accept>'


def test_Keystroke_cls_extend():
    keys1 = Keystroke('')
    keys2 = Keystroke.extend(keys1, '<C-A>')
    keys3 = Keystroke.extend(keys2, '<C-B>')

    assert keys1 == Keystroke('')
    assert keys2 == Keystroke('<C-A>')
    assert keys3 == Keystroke('<C-A><C-B>')


def test_Keystroke_cls_harvest():
    from neovim_prompt import nvim
    now = datetime.now()
    with patch('neovim_prompt.keystroke.datetime') as m1:
        def side_effect(*args):
            yield ord('a')
            yield ord('\x08')       # ^H
            yield list(b'\x80kI')   # Insert
            m1.now.return_value += timedelta(milliseconds=1000)
            yield ord('b')
            m1.now.return_value += timedelta(milliseconds=1001)
            yield ord('c')
        m1.now.return_value = now
        nvim.call.side_effect = side_effect()
        nvim.options = {
            'timeout': True,
            'timeoutlen': 1000,
        }

        keys = None
        timeout = None
        keys, timeout = Keystroke.harvest(keys, timeout)
        assert keys == Keystroke(b'a')

        keys, timeout = Keystroke.harvest(keys, timeout)
        assert keys == Keystroke(b'a<C-H>')

        keys, timeout = Keystroke.harvest(keys, timeout)
        assert keys == Keystroke(b'a<C-H><INS>')

        keys, timeout = Keystroke.harvest(keys, timeout)
        assert keys == Keystroke(b'a<C-H><INS>b')

        # timeout
        keys, timeout = Keystroke.harvest(keys, timeout)
        assert keys == Keystroke(b'c')


        nvim.call.side_effect = side_effect()
        nvim.options = {
            'timeout': False,
            'timeoutlen': 1000,
        }

        keys = None
        timeout = None
        keys, timeout = Keystroke.harvest(keys, timeout)
        assert keys == Keystroke(b'a')

        keys, timeout = Keystroke.harvest(keys, timeout)
        assert keys == Keystroke(b'a<C-H>')

        keys, timeout = Keystroke.harvest(keys, timeout)
        assert keys == Keystroke(b'a<C-H><INS>')

        keys, timeout = Keystroke.harvest(keys, timeout)
        assert keys == Keystroke(b'a<C-H><INS>b')

        keys, timeout = Keystroke.harvest(keys, timeout)
        assert keys == Keystroke(b'a<C-H><INS>bc')
