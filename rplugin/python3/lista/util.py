def assign_content(nvim, content):
    """Assign content to the current buffer.

    Args:
        nvim (neovim.Nvim): A ``neovim.Nvim`` instance.
        content (str): A str content.
    """
    viewinfo = nvim.call('winsaveview')
    nvim.current.buffer.options['modifiable'] = True
    nvim.current.buffer[:] = content
    nvim.current.buffer.options['modifiable'] = False
    nvim.call('winrestview', viewinfo)
