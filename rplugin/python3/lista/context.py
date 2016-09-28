class Context:
    __slots__ = [
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
    ]

    def __init__(self, nvim):
        self.text = ''
        self.caret_locus = 0
        buffer = nvim.current.buffer
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
        window = nvim.current.window
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
        self.viewinfo = nvim.call('winsaveview')
        self.undofile = nvim.call('tempname')
        nvim.command('silent wundo! %s' % self.undofile)

    def restore(self, nvim):
        if self.buffer_number != nvim.current.buffer.number:
            raise Exception('Buffer number mismatched')
        buffer = nvim.current.buffer
        buffer.options['readonly'] = False
        buffer.options['modifiable'] = True
        buffer[:] = self.buffer_content
        for k, v in self.buffer_options.items():
            buffer.options[k] = v
        window = nvim.current.window
        for k, v in self.window_options.items():
            window.options[k] = v
        nvim.call('winrestview', self.viewinfo)
        nvim.command('silent! rundo %s' % self.undofile)

    def to_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}

    @classmethod
    def from_dict(cls, d):
        context = cls.__new__()
        for k, v in d.items():
            if k in cls.__slots__:
                setattr(context, k, v)
        return context
