from unittest.mock import MagicMock, patch
from neovim_prompt.history import History
import pytest


def setup():
    from neovim_prompt import nvim
    history_candidates = (
        'foo',
        'bar',
        'foobar',
        'hoge',
        'barhoge',
        'foobarhoge',
    )

    def histnr(histname):
        return len(history_candidates)

    def histget(histname, index):
        if index == 0:
            return ''
        return history_candidates[-(index+1)]

    def call(fname, *args):
        if fname == 'histnr':
            return histnr(*args)
        elif fname == 'histget':
            return histget(*args)

    nvim.call.side_effect = call


def test_current(prompt):
    prompt.text = 'fool'
    prompt.caret.get_backward_text.return_value = 'fo'
    history = History(prompt)
    assert history.current() == 'fool'


def test_previous(prompt):
    prompt.text = 'fool'
    prompt.caret.get_backward_text.return_value = 'fo'
    history = History(prompt)
    assert history.current() == 'fool'

    assert history.previous(prompt) == 'foo'
    assert history.current() == 'foo'

    assert history.previous(prompt) == 'bar'
    assert history.current() == 'bar'

    assert history.previous(prompt) == 'foobar'
    assert history.current() == 'foobar'

    assert history.previous(prompt) == 'hoge'
    assert history.current() == 'hoge'

    assert history.previous(prompt) == 'barhoge'
    assert history.current() == 'barhoge'

    assert history.previous(prompt) == 'foobarhoge'
    assert history.current() == 'foobarhoge'

    assert history.previous(prompt) == 'foobarhoge'
    assert history.current() == 'foobarhoge'


def test_next(prompt):
    prompt.text = 'fool'
    prompt.caret.get_backward_text.return_value = 'fo'
    history = History(prompt)
    [history.previous(prompt) for i in range(6)]
    assert history.current() == 'foobarhoge'

    assert history.next() == 'barhoge'
    assert history.current() == 'barhoge'

    assert history.next() == 'hoge'
    assert history.current() == 'hoge'

    assert history.next() == 'foobar'
    assert history.current() == 'foobar'

    assert history.next() == 'bar'
    assert history.current() == 'bar'

    assert history.next() == 'foo'
    assert history.current() == 'foo'

    assert history.next() == 'fool'
    assert history.current() == 'fool'

    assert history.next() == 'fool'
    assert history.current() == 'fool'


def test_previous_match(prompt):
    prompt.text = 'fool'
    prompt.caret.get_backward_text.return_value = 'fo'
    history = History(prompt)
    assert history.current() == 'fool'

    assert history.previous_match(prompt) == 'foo'
    assert history.current() == 'foo'

    assert history.previous_match(prompt) == 'foobar'
    assert history.current() == 'foobar'

    assert history.previous_match(prompt) == 'foobarhoge'
    assert history.current() == 'foobarhoge'

    assert history.previous_match(prompt) == 'foobarhoge'
    assert history.current() == 'foobarhoge'


def test_next_match(prompt):
    prompt.text = 'fool'
    prompt.caret.get_backward_text.return_value = 'fo'
    history = History(prompt)
    [history.previous(prompt) for i in range(6)]
    assert history.current() == 'foobarhoge'

    assert history.next_match() == 'foobar'
    assert history.current() == 'foobar'

    assert history.next_match() == 'foo'
    assert history.current() == 'foo'

    assert history.next_match() == 'fool'
    assert history.current() == 'fool'

    assert history.next_match() == 'fool'
    assert history.current() == 'fool'
