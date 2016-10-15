from . import AbstractMatcher, escape_vim_patterns


class Matcher(AbstractMatcher):
    name = 'all'

    def highlight_pattern(self, query):
        patterns = map(str.strip, query.split())
        return '\%%(%s\)' % '\|'.join(
            map(escape_vim_patterns, patterns)
        )

    def filter(self, query, indices, candidates):
        patterns = map(str.strip, query.split())
        if type(self).nvim.eval('&ignorecase'):
            patterns = list(map(str.lower, patterns))
            indices[:] = [
                i for i in indices
                if all(p in candidates[i].lower() for p in patterns)
            ]
        else:
            patterns = list(patterns)
            indices[:] = [
                i for i in indices
                if all(p in candidates[i] for p in patterns)
            ]



