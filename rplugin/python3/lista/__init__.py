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
    pass
