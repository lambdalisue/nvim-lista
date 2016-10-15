import re
from . import AbstractMatcher, escape_vim_patterns


class Matcher(AbstractMatcher):
    name = 'fuzzy'

    def highlight_pattern(self, query):
        chars = map(escape_vim_patterns, list(query))
        chars = map(lambda x: '%s[^%s]\\{-}' % (x, x), chars)
        return ''.join(chars)

    def filter(self, query, indices, candidates):
        chars = map(re.escape, list(query))
        chars = map(lambda x: '%s[^%s]*?' % (x, x), chars)
        pattern = ''.join(chars)

        if type(self).nvim.eval('&ignorecase'):
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
