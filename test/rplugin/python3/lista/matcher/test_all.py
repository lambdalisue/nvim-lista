from unittest.mock import MagicMock
import pytest
from lista.matcher.all import Matcher


@pytest.fixture
def matcher(nvim):
    matcher = Matcher(nvim)
    return matcher


def test_Matcher_constructor(nvim):
    matcher = Matcher(nvim)
    assert matcher.name == 'all'


def test_matcher_get_highlight_pattern(matcher):
    assert matcher.get_highlight_pattern('a b c') \
        == '\%(a\|b\|c\)'


def test_matcher_filter_ignorecase(matcher):
    candidates = [
        'Planning',
        'Pre-Alpha',
        'Alpha',
        'Beta',
        'Production/Stable',
        'Mature',
        'Inactive',
    ]
    indices = list(range(len(candidates)))

    matcher.filter('', indices, candidates, True)
    assert indices == [
        0, 1, 2, 3, 4, 5, 6,
    ]

    matcher.filter('p a', indices, candidates, True)
    assert indices == [
        0, 1, 2, 4,
    ]

    matcher.filter('p an', indices, candidates, True)
    assert indices == [
        0,
    ]

    matcher.filter('', indices, candidates, True)
    assert indices == [
        0,
    ]


def test_matcher_filter_noignorecase(matcher):
    candidates = [
        'Planning',
        'Pre-Alpha',
        'Alpha',
        'Beta',
        'Production/Stable',
        'Mature',
        'Inactive',
    ]
    indices = list(range(len(candidates)))

    matcher.filter('', indices, candidates, False)
    assert indices == [
        0, 1, 2, 3, 4, 5, 6,
    ]

    matcher.filter('p a', indices, candidates, False)
    assert indices == [
        1, 2,
    ]

    matcher.filter('', indices, candidates, False)
    assert indices == [
        1, 2,
    ]
