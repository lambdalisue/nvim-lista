from prompt.context import Context as BaseContext


class Context(BaseContext):
    __slots__ = (
        'text',
        'caret_locus',
        'selected_index',
        'matcher_index',
        'case_index',
    )

    def __init__(self):
        super().__init__()
        self.selected_index = 0
        self.matcher_index = 0
        self.case_index = 0
