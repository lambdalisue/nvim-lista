from lista.prompt import Prompt
from unittest.mock import MagicMock
import pytest


class Context:
    __slots__ = ['text', 'caret_locus']

    def __init__(self):
        #            01234567890123
        self.text = '  Hello world!'
        self.caret_locus = len(self.text)


@pytest.fixture
def context():
    return Context()

@pytest.fixture
def nvim():
    nvim = MagicMock()
    nvim.call.return_value = ord('A')

@pytest.fixture
def prompt(nvim, context):
    return Prompt(nvim, context)


def test_text(context, prompt):
    assert prompt.text == context.text
    assert prompt.caret.locus == len(prompt.text)
    prompt.text = '00000'
    assert prompt.caret.locus == len(prompt.text)
