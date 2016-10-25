import pytest

from neovim_prompt.caret import Caret
from neovim_prompt.context import Context


def test_locus(context):
    context.text = '  Hello world!'
    context.caret_locus = 0
    caret = Caret(context)
    assert caret.locus == context.caret_locus

    caret.locus -= 1
    assert caret.locus == context.caret_locus

    # lower limit
    caret.locus = -1
    assert caret.locus == 0

    # upper limit
    caret.locus = 100
    assert caret.locus == len(context.text)


def test_head(context):
    context.text = '  Hello world!'
    context.caret_locus = 0
    caret = Caret(context)
    assert caret.head == 0


def test_lead(context):
    context.text = '  Hello world!'
    context.caret_locus = 0
    caret = Caret(context)
    # The number of leading spaces
    assert caret.lead == 2


def test_tail(context):
    context.text = '  Hello world!'
    context.caret_locus = 0
    caret = Caret(context)
    assert caret.tail == len(context.text)


def test_get_backward_text(context):
    context.text = '  Hello world!'
    context.caret_locus = 0
    caret = Caret(context)
    caret.locus = caret.tail
    assert caret.get_backward_text() == '  Hello world!'

    caret.locus = caret.lead
    assert caret.get_backward_text() == '  '

    caret.locus = caret.head
    assert caret.get_backward_text() == ''

    caret.locus = 7
    assert caret.get_backward_text() == '  Hello'


def test_get_selected_text(context):
    context.text = '  Hello world!'
    context.caret_locus = 0
    caret = Caret(context)
    caret.locus = caret.tail
    assert caret.get_selected_text() == ''

    caret.locus = caret.lead
    assert caret.get_selected_text() == 'H'

    caret.locus = caret.head
    assert caret.get_selected_text() == ' '

    caret.locus = 8
    assert caret.get_selected_text() == 'w'


def test_get_forward_text(context):
    context.text = '  Hello world!'
    context.caret_locus = 0
    caret = Caret(context)
    caret.locus = caret.tail
    assert caret.get_forward_text() == ''

    caret.locus = caret.lead
    assert caret.get_forward_text() == 'ello world!'

    caret.locus = caret.head
    assert caret.get_forward_text() == ' Hello world!'

    caret.locus = 7
    assert caret.get_forward_text() == 'world!'
