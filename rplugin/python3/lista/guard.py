import os
from . import operator


class Guard:
    def __init__(self, nvim):
        self.nvim = nvim

    def store(self):
        self.buffer = self.nvim.current.buffer
        self.buffer_options = {
            k: self.buffer.options[k] for k in [
                'buftype',
                'modified',
                'modifiable',
                'readonly',
            ]
        }
        self.window = self.nvim.current.window
        self.window_options = {
            k: self.window.options[k] for k in [
                'number',
                'relativenumber',
                'cursorline',
                'colorcolumn',
                'statusline',
            ]
        }

        self.view = operator.call(self.nvim, 'winsaveview')
        self.undofile = operator.call(self.nvim, 'tempname')
        self.nvim.command('silent wundo! %s' % self.undofile)
        self.content = self.buffer[:]

    def restore(self):
        assign_content(self.nvim, self.buffer, self.content)
        if os.path.isfile(self.undofile):
            self.nvim.command('silent rundo %s' % self.undofile)
        operator.call(self.nvim, 'winrestview', self.view)
        for key, value in self.window_options.items():
            self.window.options[key] = value
        for key, value in self.buffer_options.items():
            self.buffer.options[key] = value

    def __enter__(self):
        self.store()
        return self

    def __exit__(self, type, value, traceback):
        self.restore()


def assign_content(nvim, buf, content):
    eventignore = nvim.options['eventignore']
    modifiable = buf.options['modifiable']
    if isinstance(nvim.options['eventignore'], bytes):
        nvim.options['eventignore'] += b'TextChanged'
    else:
        nvim.options['eventignore'] += 'TextChanged'
    buf.options['modifiable'] = True
    buf[:] = content
    buf.options['modifiable'] = modifiable
    nvim.options['eventignore'] = eventignore
