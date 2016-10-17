from curses import ascii
from collections import abc
from contextlib import ExitStack

from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from neovim_prompt.key import Key
from neovim_prompt.keystroke import Keystroke


def test_Keystroke_property(nvim):
    keys = Keystroke.parse(nvim, 'abc')
    assert isinstance(keys, abc.Hashable)
    assert isinstance(keys, abc.Container)
    assert isinstance(keys, abc.Sized)


def test_Keystroke_parse_with_sequence(nvim):
    expr = [
        Key.parse(nvim, 'a'),
        Key.parse(nvim, 'b'),
        Key.parse(nvim, 'c'),
    ]
    keys = Keystroke.parse(nvim, expr)
    assert keys == tuple(expr)

    keys = Keystroke.parse(nvim, tuple(expr))
    assert keys == tuple(expr)


def test_Keystroke_parse_with_bytes(nvim):
    expr = [
        Key.parse(nvim, 'a'),
        Key.parse(nvim, 'b'),
        Key.parse(nvim, 'c'),
    ]
    keys = Keystroke.parse(nvim, b'abc')
    assert keys == tuple(expr)

    expr = [
        Key.parse(nvim, '<C-T>'),
        Key.parse(nvim, 'b'),
        Key.parse(nvim, '<Home>'),
    ]
    keys = Keystroke.parse(nvim, b'<C-T>b<Home>')
    assert keys == tuple(expr)


def test_Keystroke_parse_with_str(nvim):
    expr = [
        Key.parse(nvim, 'a'),
        Key.parse(nvim, 'b'),
        Key.parse(nvim, 'c'),
    ]
    keys = Keystroke.parse(nvim, 'abc')
    assert keys == tuple(expr)

    expr = [
        Key.parse(nvim, '<C-T>'),
        Key.parse(nvim, 'b'),
        Key.parse(nvim, '<Home>'),
    ]
    keys = Keystroke.parse(nvim, '<C-T>b<Home>')
    assert keys == tuple(expr)


def test_Keystroke_harvest(nvim):
    now = datetime.now()
    with patch('neovim_prompt.keystroke.datetime') as m1:
        def side_effect(*args):
            yield ord('a')
            yield ord('\x08')   # ^H
            yield '\udc80kI'    # Insert
            m1.now.return_value += timedelta(milliseconds=1000)
            yield ord('b')
            m1.now.return_value += timedelta(milliseconds=1001)
            yield ord('c')
        m1.now.return_value = now
        nvim.call = MagicMock()
        nvim.call.side_effect = side_effect()
        nvim.options = {
            'timeout': True,
            'timeoutlen': 1000,
        }

        keys = None
        timeout = None
        keys, timeout = Keystroke.harvest(nvim, keys, timeout)
        assert keys == Keystroke.parse(nvim, b'a')

        keys, timeout = Keystroke.harvest(nvim, keys, timeout)
        assert keys == Keystroke.parse(nvim, b'a<C-H>')

        keys, timeout = Keystroke.harvest(nvim, keys, timeout)
        assert keys == Keystroke.parse(nvim, b'a<C-H><INS>')

        keys, timeout = Keystroke.harvest(nvim, keys, timeout)
        assert keys == Keystroke.parse(nvim, b'a<C-H><INS>b')

        # timeout
        keys, timeout = Keystroke.harvest(nvim, keys, timeout)
        assert keys == Keystroke.parse(nvim, b'c')


        nvim.call.side_effect = side_effect()
        nvim.options = {
            'timeout': False,
            'timeoutlen': 1000,
        }

        keys = None
        timeout = None
        keys, timeout = Keystroke.harvest(nvim, keys, timeout)
        assert keys == Keystroke.parse(nvim, b'a')

        keys, timeout = Keystroke.harvest(nvim, keys, timeout)
        assert keys == Keystroke.parse(nvim, b'a<C-H>')

        keys, timeout = Keystroke.harvest(nvim, keys, timeout)
        assert keys == Keystroke.parse(nvim, b'a<C-H><INS>')

        keys, timeout = Keystroke.harvest(nvim, keys, timeout)
        assert keys == Keystroke.parse(nvim, b'a<C-H><INS>b')

        keys, timeout = Keystroke.harvest(nvim, keys, timeout)
        assert keys == Keystroke.parse(nvim, b'a<C-H><INS>bc')


def test_keystroke_startswith(nvim):
    rhs1 = Keystroke.parse(nvim, '<C-A>')
    rhs2 = Keystroke.parse(nvim, '<C-A><C-B>')
    rhs3 = Keystroke.parse(nvim, '<C-A><C-C>')

    assert rhs1.startswith(Keystroke.parse(nvim, ''))
    assert rhs2.startswith(Keystroke.parse(nvim, ''))
    assert rhs3.startswith(Keystroke.parse(nvim, ''))

    assert rhs1.startswith(Keystroke.parse(nvim, '<C-A>'))
    assert rhs2.startswith(Keystroke.parse(nvim, '<C-A>'))
    assert rhs3.startswith(Keystroke.parse(nvim, '<C-A>'))

    assert not rhs1.startswith(Keystroke.parse(nvim, '<C-A><C-B>'))
    assert rhs2.startswith(Keystroke.parse(nvim, '<C-A><C-B>'))
    assert not rhs3.startswith(Keystroke.parse(nvim, '<C-A><C-B>'))

    assert not rhs1.startswith(Keystroke.parse(nvim, '<C-A><C-B><C-C>'))
    assert not rhs2.startswith(Keystroke.parse(nvim, '<C-A><C-B><C-C>'))
    assert not rhs3.startswith(Keystroke.parse(nvim, '<C-A><C-B><C-C>'))


def test_keystroke_str(nvim):
    assert str(Keystroke.parse(nvim, 'abc')) == 'abc'
    assert str(Keystroke.parse(nvim, '<C-H><C-H>')) == '\x08\x08'
    assert str(Keystroke.parse(nvim, '<Backspace><Delete>')) == ''
    assert str(Keystroke.parse(nvim, '<prompt:accept>')) == '<prompt:accept>'
