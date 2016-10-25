from neovim_prompt.context import Context
import pytest


def test_constructor():
    context = Context()
    assert isinstance(context, Context)
    assert context.text == ''
    assert context.caret_locus == 0


def test_to_dict():
    context = Context()
    assert context.to_dict() == {
            'text': '',
            'caret_locus': 0,
        }

    context.text = 'foo'
    context.caret_locus = 3
    assert context.to_dict() == {
            'text': 'foo',
            'caret_locus': 3,
        }


def test_from_dict():
    context = Context.from_dict({
            'text': '',
            'caret_locus': 0,
        })
    assert isinstance(context, Context)
    assert context.text == ''
    assert context.caret_locus == 0

    context = Context.from_dict({
            'text': 'foo',
            'caret_locus': 3,
        })
    assert isinstance(context, Context)
    assert context.text == 'foo'
    assert context.caret_locus == 3
