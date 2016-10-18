import re
from typing import Sequence
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
        chars = map(re.escape, list(query))
        chars = map(lambda x: '%s[^%s]*?' % (x, x), chars)
        pattern = ''.join(chars)

        if ignorecase:
            pattern = re.compile(pattern.lower())
            indices[:] = [
                i for i in indices
                if pattern.search(candidates[i].lower())
            ]
        else:
            pattern = re.compile(pattern)
            indices[:] = [
                i for i in indices
                if pattern.search(candidates[i])
            ]
