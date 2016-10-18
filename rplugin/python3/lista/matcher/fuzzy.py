import re
from typing import Sequence, cast, Iterator, Pattern
from . import AbstractMatcher, escape_vim_patterns


class Matcher(AbstractMatcher):
    """A fuzzy matcher class for filter candidates."""
    name = 'fuzzy'

    def get_highlight_pattern(self, query: str) -> str:
        chars = map(escape_vim_patterns, list(query))
        chars = map(lambda x: '%s[^%s]\\{-}' % (x, x), chars)
        return ''.join(chars)

    def filter(self,
               query: str,
               indices: Sequence[int],
               candidates: Sequence[str],
               ignorecase: bool) -> Sequence[int]:
        chars = map(re.escape, list(query))  # type: ignore
        chars = map(lambda x: '%s[^%s]*?' % (x, x), chars)  # type: ignore
        pattern = ''.join(cast(Iterator[str], chars))

        if ignorecase:
            _pattern = re.compile(pattern.lower())
            indices[:] = [  # type: ignore
                i for i in indices
                if _pattern.search(candidates[i].lower())
            ]
        else:
            _pattern = re.compile(pattern)
            indices[:] = [  # type: ignore
                i for i in indices
                if _pattern.search(candidates[i])
            ]
