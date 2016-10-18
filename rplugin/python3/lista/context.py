from neovim_prompt.context import Context as BaseContext


class Context(BaseContext):
    __slots__ = (
        'text',
        'caret_locus',
        'selected_line',
    )

    def __init__(self):
        super().__init__()
        self.selected_line = 1
