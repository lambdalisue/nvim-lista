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
    @classmethod
    def prepare(cls, nvim):
        cls.nvim = nvim

    def __init__(self):
        self.match_id = None

    def __del__(self):
        self.highlight('')

    def highlight_pattern(self, query):
        raise NotImplementedError

    def highlight(self, query):
        if self.match_id:
            type(self).nvim.call('matchdelete', self.match_id)
            self.match_id = None
        if not query:
            return
        pattern = self.highlight_pattern(query)
        self.match_id = type(self).nvim.call(
            'matchadd',
            'Title',
            ('\c' if type(self).nvim.options['ignorecase'] else '\C') + pattern,
            0,
        )

    def filter(self, query, indices, candidates):
        raise NotImplementedError


def escape_vim_patterns(text):
    """Escape patterh character used in Vim regex"""
    return text.translate(ESCAPE_VIM_PATTERN_TABLE)
