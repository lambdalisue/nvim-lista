from unittest.mock import MagicMock
from neovim_prompt.digraph import Digraph
import pytest


def test_constructor():
    digraph1 = Digraph()
    digraph2 = Digraph()
    assert digraph1 is digraph2


def test_digraph_find(nvim):
    nvim.call = MagicMock()
    nvim.call.return_value = 'aa A 00  bb B 01\ncc C 02  ad D 03'
    digraph = Digraph()

    # It returns a corresponding character
    assert digraph.find(nvim, 'a', 'a') == 'A'
    assert digraph.find(nvim, 'b', 'b') == 'B'
    assert digraph.find(nvim, 'c', 'c') == 'C'

    # It automatically find from reversed one
    assert digraph.find(nvim, 'a', 'd') == 'D'
    assert digraph.find(nvim, 'd', 'a') == 'D'

    # It always return the char2 if missing
    assert digraph.find(nvim, 'a', 'c') == 'c'
    assert digraph.find(nvim, 'c', 'a') == 'a'


def test_digraph_retrieve(nvim):
    nvim.error = MagicMock()
    nvim.call = MagicMock()
    nvim.call.return_value = 'aa A 00  bb B 01\ncc C 02  ad D 03'
    digraph = Digraph()
    digraph.find(nvim, 'a', 'a')    # Make cache

    # It get chars and return a corresponding char
    nvim.call.side_effect = [ord('a'), ord('a')]
    assert digraph.retrieve(nvim) == 'A'
    nvim.call.side_effect = [ord('b'), ord('b')]
    assert digraph.retrieve(nvim) == 'B'
    nvim.call.side_effect = [ord('c'), ord('c')]
    assert digraph.retrieve(nvim) == 'C'

    # It immediately return a representation of a special key
    nvim.call.side_effect = [b'\x80kb', ord('a')]
    assert digraph.retrieve(nvim) == '<Backspace>'
    assert nvim.call() == ord('a')

    nvim.call.side_effect = [ord('a'), b'\x80kb']
    assert digraph.retrieve(nvim) == '<Backspace>'
