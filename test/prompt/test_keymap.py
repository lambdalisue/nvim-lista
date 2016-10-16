from curses import ascii
from collections import abc

from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from neovim_prompt.keystroke import Keystroke
from neovim_prompt.keymap import Keymap


def test_Keymap_property():
    keymap = Keymap()


def test_Keymap_register():
    lhs = Keystroke('<C-H>')
    rhs = Keystroke('<BS>')
    keymap = Keymap()
    keymap.register(lhs, rhs)
    assert keymap.registry[lhs] == (lhs, rhs, False)

    keymap.register(lhs, rhs, True)
    assert keymap.registry[lhs] == (lhs, rhs, True)


def test_Keymap_register_from_rule():
    lhs = Keystroke('<C-H>')
    rhs = Keystroke('<BS>')
    keymap = Keymap()
    keymap.register_from_rule(('<C-H>', '<BS>'))
    assert keymap.registry[lhs] == (lhs, rhs, False)

    keymap.register_from_rule(('<C-H>', '<BS>', True))
    assert keymap.registry[lhs] == (lhs, rhs, True)


def test_Keymap_filter():
    lhs1 = Keystroke('<C-X><C-F>')
    lhs2 = Keystroke('<C-X><C-B>')
    lhs3 = Keystroke('<C-A>')
    keymap = Keymap()
    keymap.register_from_rule(('<C-X><C-F>', '<A>'))
    keymap.register_from_rule(('<C-X><C-B>', '<B>'))
    keymap.register_from_rule(('<C-A>', '<C>'))

    assert keymap.filter(Keystroke('')) == sorted((
        (lhs3, Keystroke('<C>'), False),
        (lhs1, Keystroke('<A>'), False),
        (lhs2, Keystroke('<B>'), False),
    ))

    assert keymap.filter(Keystroke('<C-X>')) == sorted((
        (lhs1, Keystroke('<A>'), False),
        (lhs2, Keystroke('<B>'), False),
    ))

    assert keymap.filter(Keystroke('<C-X><C-F>')) == sorted((
        (lhs1, Keystroke('<A>'), False),
    ))


def test_Keymap_resolve():
    lhs1 = Keystroke('<C-X><C-F>')
    lhs2 = Keystroke('<C-X><C-B>')
    lhs3 = Keystroke('<C-A>')
    keymap = Keymap()
    keymap.register_from_rule(('<C-X><C-F>', '<A>'))
    keymap.register_from_rule(('<C-X><C-B>', '<B>'))
    keymap.register_from_rule(('<C-A>', '<C>'))

    assert keymap.resolve(Keystroke('')) is None
    assert keymap.resolve(Keystroke('<C-A>')) == Keystroke('<C>')
    assert keymap.resolve(Keystroke('<C-X>')) is None
    assert keymap.resolve(Keystroke('<C-X><C-F>')) == Keystroke('<A>')

    # remap
    keymap.register_from_rule(('<B>', '<D>'))
    assert keymap.resolve(Keystroke('<C-X><C-B>')) == Keystroke('<D>')
    # noremap
    keymap.register_from_rule(('<C-X><C-B>', '<B>', True))
    assert keymap.resolve(Keystroke('<C-X><C-B>')) == Keystroke('<B>')

    keymap.register_from_rule(('<C-Y><C-K>', '<E>'))
    assert keymap.resolve(Keystroke('<C-Y>')) is None
