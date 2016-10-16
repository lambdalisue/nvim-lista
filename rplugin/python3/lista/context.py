from neovim_prompt.context import Context as BaseContext


class Context(BaseContext):
    __slots__ = (
        'nvim',
        'text',
        'caret_locus',
        'buffer_number',
        'buffer_content',
        'buffer_options',
        'window_options',
        'selected_line',
        'selected_indices',
        'viewinfo',
        'undofile',
    )

    def __init__(self, nvim: 'Nvim') -> None:
        super().__init__()
        self.nvim = nvim

    def __enter__(self) -> 'Context':
        buffer = self.nvim.current.buffer
        self.buffer_number = buffer.number
        self.buffer_content = buffer[:]
        self.buffer_options = {
            k: buffer.options[k] for k in [
                'syntax',
                'readonly',
                'modified',
                'modifiable',
            ]
        }
        window = self.nvim.current.window
        self.window_options = {
            k: window.options[k] for k in [
                'spell',
                'foldenable',
                'statusline',
                'colorcolumn',
                'cursorline',
                'cursorcolumn',
            ]
        }
        self.selected_line = 0
        self.selected_indices = range(len(self.buffer_content))
        self.viewinfo = self.nvim.call('winsaveview')
        self.undofile = self.nvim.call('tempname')
        self.nvim.command('silent wundo! %s' % self.undofile)

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.buffer_number != self.nvim.current.buffer.number:
            raise Exception('Buffer number mismatched')
        buffer = self.nvim.current.buffer
        buffer.options['readonly'] = False
        buffer.options['modifiable'] = True
        buffer[:] = self.buffer_content
        for k, v in self.buffer_options.items():
            buffer.options[k] = v
        window = self.nvim.current.window
        for k, v in self.window_options.items():
            window.options[k] = v
        self.nvim.call('winrestview', self.viewinfo)
        self.nvim.command('silent! rundo %s' % self.undofile)
