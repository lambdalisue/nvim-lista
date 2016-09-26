try:
    import neovim

    @neovim.plugin
    class ListaEntryPoint:
        def __init__(self, nvim):
            self.nvim = nvim

        @neovim.function('_lista_start', sync=True)
        def start(self, args):
            from .lista import Lista
            lista = Lista(self.nvim)
            lista.start()
            return

except ImportError:
    import vim

    def vim_call(name, *args, **kwargs):
        result = vim.Function(name)(*args, **kwargs)
        if isinstance(result, bytes):
            encoding = vim.eval('&encoding') or 'utf-8'
            if result.startswith(b"\x80"):
                result = "\udc80" + result[1:].decode(encoding)
            else:
                result = result.decode(encoding)
        return result

    vim.call = vim_call
