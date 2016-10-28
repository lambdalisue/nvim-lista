from abc import ABCMeta
from unittest.mock import MagicMock
import pytest
from lista.matcher.base import AbstractMatcher, escape_vim_patterns


@pytest.fixture
def matcher(nvim):
    class DummyMatcher(AbstractMatcher):
        def get_highlight_pattern(self, query):
            return query

        def filter(self, query, indices, candidates, ignorecase):
            return indices
    matcher = DummyMatcher(nvim)
    return matcher


def test_AbstractMatcher_constructor():
    assert isinstance(AbstractMatcher, ABCMeta)


def test_matcher_remove_highlight(matcher):
    nvim = matcher.nvim
    nvim.call = MagicMock()
    matcher.remove_highlight()
    assert not nvim.call.called

    matcher._match_id = 1
    matcher.remove_highlight()
    nvim.call.assert_called_with('matchdelete', 1)
    assert matcher._match_id is None


def test_matcher_highlight(matcher):
    nvim = matcher.nvim
    nvim.call = MagicMock()
    matcher._match_id = None
    matcher.highlight('foo', True)
    nvim.call.assert_called_with('matchadd', 'Title', '\cfoo', 0)

    matcher.highlight('foo', False)
    nvim.call.assert_called_with('matchadd', 'Title', '\Cfoo', 0)

def test_escape_vim_patterns():
    assert escape_vim_patterns('^') == '\\^'
    assert escape_vim_patterns('$') == '\\$'
    assert escape_vim_patterns('~') == '\\~'
    assert escape_vim_patterns('.') == '\\.'
    assert escape_vim_patterns('*') == '\\*'
    assert escape_vim_patterns('[') == '\\['
    assert escape_vim_patterns(']') == '\\]'
    assert escape_vim_patterns('\\') == '\\\\'
