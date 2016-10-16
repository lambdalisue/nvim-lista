from neovim_prompt.context import Context as BaseContext


class Context(BaseContext):
    __slots__ = (
        'text',
        'caret_locus',
        'content',
        'selected_line',
        'selected_indices',
    )
