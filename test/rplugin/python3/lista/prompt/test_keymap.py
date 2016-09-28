from lista.prompt.key import Key
from lista.prompt.keymap import Keymap
import pytest


@pytest.fixture
def keymap():
    return Keymap()


def test_register(keymap):
    assert keymap.registry == {}

    keymap.register('a', 'b')
    assert keymap.registry == {
        Key('a'): (Key('b'), False),
    }

    keymap.register('CR', 'DEL', True)
    assert keymap.registry == {
        Key('a'): (Key('b'), False),
        Key('CR'): (Key('DEL'), True),
    }


def test_resolve(keymap):
    keymap.register('Backspace', 'BS', noremap=True)
    keymap.register('A', 'Backspace')
    keymap.register('B', 'Backspace', noremap=True)

    assert keymap.resolve('Backspace') == Key('BS')
    assert keymap.resolve('A') == Key('BS')
    assert keymap.resolve('B') == Key('Backspace')
