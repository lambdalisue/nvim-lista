from curses import ascii
from collections import abc

from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from neovim_prompt.keystroke import Keystroke
from neovim_prompt.keymap import Keymap


def test_Keymap_property():
    keymap = Keymap()


def test_Keymap_register(nvim):
    lhs = Keystroke.parse(nvim, '<C-H>')
    rhs = Keystroke.parse(nvim, '<BS>')
    keymap = Keymap()
    keymap.register(lhs, rhs)
    assert keymap.registry[lhs] == (lhs, rhs, False)

    keymap.register(lhs, rhs, True)
    assert keymap.registry[lhs] == (lhs, rhs, True)


def test_Keymap_register_from_rule(nvim):
    lhs = Keystroke.parse(nvim, '<C-H>')
    rhs = Keystroke.parse(nvim, '<BS>')
    keymap = Keymap()
    keymap.register_from_rule(nvim, ('<C-H>', '<BS>'))
    assert keymap.registry[lhs] == (lhs, rhs, False)

    keymap.register_from_rule(nvim, ('<C-H>', '<BS>', True))
    assert keymap.registry[lhs] == (lhs, rhs, True)


def test_Keymap_filter(nvim):
    lhs1 = Keystroke.parse(nvim, '<C-X><C-F>')
    lhs2 = Keystroke.parse(nvim, '<C-X><C-B>')
    lhs3 = Keystroke.parse(nvim, '<C-A>')
    keymap = Keymap()
    keymap.register_from_rule(nvim, ('<C-X><C-F>', '<A>'))
    keymap.register_from_rule(nvim, ('<C-X><C-B>', '<B>'))
    keymap.register_from_rule(nvim, ('<C-A>', '<C>'))

    assert keymap.filter(Keystroke.parse(nvim, '')) == sorted((
        (lhs3, Keystroke.parse(nvim, '<C>'), False),
        (lhs1, Keystroke.parse(nvim, '<A>'), False),
        (lhs2, Keystroke.parse(nvim, '<B>'), False),
    ))

    assert keymap.filter(Keystroke.parse(nvim, '<C-X>')) == sorted((
        (lhs1, Keystroke.parse(nvim, '<A>'), False),
        (lhs2, Keystroke.parse(nvim, '<B>'), False),
    ))

    assert keymap.filter(Keystroke.parse(nvim, '<C-X><C-F>')) == sorted((
        (lhs1, Keystroke.parse(nvim, '<A>'), False),
    ))


def test_Keymap_resolve(nvim):
    lhs1 = Keystroke.parse(nvim, '<C-X><C-F>')
    lhs2 = Keystroke.parse(nvim, '<C-X><C-B>')
    lhs3 = Keystroke.parse(nvim, '<C-A>')
    keymap = Keymap()
    keymap.register_from_rule(nvim, ('<C-X><C-F>', '<A>'))
    keymap.register_from_rule(nvim, ('<C-X><C-B>', '<B>'))
    keymap.register_from_rule(nvim, ('<C-A>', '<C>'))

    assert keymap.resolve(Keystroke.parse(nvim, '')) is None
    assert keymap.resolve(Keystroke.parse(nvim, '<C-A>')) == \
        Keystroke.parse(nvim, '<C>')
    assert keymap.resolve(Keystroke.parse(nvim, '<C-X>')) is None
    assert keymap.resolve(Keystroke.parse(nvim, '<C-X><C-F>')) == \
        Keystroke.parse(nvim, '<A>')

    # remap
    keymap.register_from_rule(nvim, ('<B>', '<D>'))
    assert keymap.resolve(Keystroke.parse(nvim, '<C-X><C-B>')) == \
        Keystroke.parse(nvim, '<D>')
    # noremap
    keymap.register_from_rule(nvim, ('<C-X><C-B>', '<B>', True))
    assert keymap.resolve(Keystroke.parse(nvim, '<C-X><C-B>')) == \
        Keystroke.parse(nvim, '<B>')

    keymap.register_from_rule(nvim, ('<C-Y><C-K>', '<E>'))
    assert keymap.resolve(Keystroke.parse(nvim, '<C-Y>')) is None
