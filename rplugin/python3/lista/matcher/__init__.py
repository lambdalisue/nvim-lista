from .. import operator

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
    def __init__(self, nvim):
        self.nvim = nvim
        self.match_id = None

    def __del__(self):
        self.highlight('')

    def highlight_pattern(self, query):
        raise NotImplementedError

    def highlight(self, query):
        if self.match_id:
            operator.call(self.nvim, 'matchdelete', self.match_id)
            self.match_id = None
        if not query:
            return
        pattern = self.highlight_pattern(query)
        self.match_id = operator.call(
            self.nvim,
            'matchadd',
            'Title',
            pattern, 0,
        )

    def filter(self, query, indices, candidates):
        raise NotImplementedError


def escape_vim_patterns(text):
    """Escape patterh character used in Vim regex"""
    return text.translate(ESCAPE_VIM_PATTERN_TABLE)
