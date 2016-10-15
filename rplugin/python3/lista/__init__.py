try:
    import neovim

    @neovim.plugin
    class ListaEntryPoint:
        def __init__(self, nvim):
            from .core import Lista
            Lista.prepare(nvim)

        @neovim.function('_lista_start', sync=True)
        def start(self, args):
            from .core import Lista
            from .context import Context
            context = Context()
            lista = Lista(context)
            lista.start(args[0])
            return
except ImportError:
    pass
