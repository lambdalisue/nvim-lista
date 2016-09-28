import pytest
import collections
from lista.prompt.caret import Caret


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
def caret(context):
    return Caret(context)


def test_locus(context, caret):
    assert caret.locus == context.caret_locus

    caret.locus -= 1
    assert caret.locus == context.caret_locus

    # lower limit
    caret.locus = -1
    assert caret.locus == 0

    # upper limit
    caret.locus = 100
    assert caret.locus == len(context.text)


def test_head(caret):
    assert caret.head == 0


def test_lead(caret):
    # The number of leading spaces
    assert caret.lead == 2


def test_tail(context, caret):
    assert caret.tail == len(context.text)


def test_get_backward_text(caret):
    caret.locus = caret.tail
    assert caret.get_backward_text() == '  Hello world!'

    caret.locus = caret.lead
    assert caret.get_backward_text() == '  '

    caret.locus = caret.head
    assert caret.get_backward_text() == ''

    caret.locus = 7
    assert caret.get_backward_text() == '  Hello'


def test_get_selected_text(caret):
    caret.locus = caret.tail
    assert caret.get_selected_text() == ''

    caret.locus = caret.lead
    assert caret.get_selected_text() == 'H'

    caret.locus = caret.head
    assert caret.get_selected_text() == ' '

    caret.locus = 8
    assert caret.get_selected_text() == 'w'


def test_get_forward_text(caret):
    caret.locus = caret.tail
    assert caret.get_forward_text() == ''

    caret.locus = caret.lead
    assert caret.get_forward_text() == 'ello world!'

    caret.locus = caret.head
    assert caret.get_forward_text() == ' Hello world!'

    caret.locus = 7
    assert caret.get_forward_text() == 'world!'
