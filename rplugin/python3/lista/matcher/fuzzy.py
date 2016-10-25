import re
from .base import AbstractMatcher, escape_vim_patterns


class Matcher(AbstractMatcher):
    """A fuzzy matcher class for filter candidates."""
    name = 'fuzzy'

    def get_highlight_pattern(self, query):
        chars = map(escape_vim_patterns, list(query))
        chars = map(lambda x: '%s[^%s]\\{-}' % (x, x), chars)
        return ''.join(chars)

    def filter(self, query, indices, candidates, ignorecase):
        chars = map(re.escape, list(query))
        chars = map(lambda x: '%s[^%s]*?' % (x, x), chars)
        pattern = ''.join(chars)

        if ignorecase:
            _pattern = re.compile(pattern.lower())
            indices[:] = [
                i for i in indices
                if _pattern.search(candidates[i].lower())
            ]
        else:
            _pattern = re.compile(pattern)
            indices[:] = [
                i for i in indices
                if _pattern.search(candidates[i])
            ]
