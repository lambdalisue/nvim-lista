ESCAPE_VIM_PATTERN_TABLE = str.maketrans({
    '^': '\\^',
    '$': '\\$',
    '~': '\\~',
    '.': '\\.',
    '*': '\\*',
    '[': '\\[',
    ']': '\\]',
    '\\': '\\\\',
})


class AbstractMatcher:
    def __init__(self, nvim: 'Nvim') -> None:
        self.nvim = nvim
        self.match_id = None    # type: int

    @property
    def ignorecase(self):
        return self.nvim.options['ignorecase']

    def highlight_pattern(self, query: str) -> str:
        raise NotImplementedError

    def highlight(self, query: str) -> None:
        if self.match_id:
            self.nvim.call('matchdelete', self.match_id)
            self.match_id = None
        if not query:
            return
        pattern = self.highlight_pattern(query)
        self.match_id = self.nvim.call(
            'matchadd',
            'Title',
            ('\c' if self.ignorecase else '\C') + pattern,
            0,
        )

    def filter(self,
               query: str,
               indices: 'Sequence[int]',
               candidates: 'Sequence[str]') -> 'Sequence[int]':
        raise NotImplementedError


def escape_vim_patterns(text: str) -> str:
    """Escape patterh character used in Vim regex"""
    return text.translate(ESCAPE_VIM_PATTERN_TABLE)
