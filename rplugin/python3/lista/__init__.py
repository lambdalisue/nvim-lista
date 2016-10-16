try:
    import neovim

    @neovim.plugin
    class ListaEntryPoint:
        def __init__(self, nvim):
            self.nvim = nvim

        @neovim.function('_lista_start', sync=True)
        def start(self, args):
            from .lista import Lista
            from .context import Context
            context = Context(self.nvim)
            lista = Lista(self.nvim, context)
            lista.start(args[0])
            return
except ImportError:
    pass
