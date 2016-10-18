from neovim import Nvim


def assign_content(nvim: Nvim, content: str) -> None:
    viewinfo = nvim.call('winsaveview')
    nvim.current.buffer.options['modifiable'] = True
    nvim.current.buffer[:] = content
    nvim.current.buffer.options['modifiable'] = False
    nvim.call('winrestview', viewinfo)
