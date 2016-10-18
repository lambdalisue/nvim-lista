from typing import Sequence
from . import AbstractMatcher, escape_vim_patterns


class Matcher(AbstractMatcher):
    """An all matcher class for filter candidates."""
    name = 'all'

    def get_highlight_pattern(self, query: str) -> str:
        patterns = map(str.strip, query.split())
        return '\%%(%s\)' % '\|'.join(
            map(escape_vim_patterns, patterns)
        )

    def filter(self,
               query: str,
               indices: Sequence[int],
               candidates: Sequence[str],
               ignorecase: bool) -> Sequence[int]:
        patterns = map(str.strip, query.split())

        if ignorecase:
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
