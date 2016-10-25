from .base import AbstractMatcher, escape_vim_patterns


class Matcher(AbstractMatcher):
    """An all matcher class for filter candidates."""
    name = 'all'

    def get_highlight_pattern(self, query):
        patterns = map(str.strip, query.split())
        return '\%%(%s\)' % '\|'.join(
            map(escape_vim_patterns, patterns)
        )

    def filter(self, query, indices, candidates, ignorecase):
        patterns = map(str.strip, query.split())

        if ignorecase:
            _patterns = list(map(str.lower, patterns))
            indices[:] = [
                i for i in indices
                if all(p in candidates[i].lower() for p in _patterns)
            ]
        else:
            _patterns = list(patterns)
            indices[:] = [
                i for i in indices
                if all(p in candidates[i] for p in _patterns)
            ]
