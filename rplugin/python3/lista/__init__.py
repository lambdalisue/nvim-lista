try:
    import neovim

    @neovim.plugin
    class ListaEntryPoint:
        def __init__(self, nvim):
            self.nvim = nvim

        @neovim.function('_lista_start', sync=True)
        def start(self, args):
            return start(self.nvim, args)
except ImportError:
    pass


def start(nvim, args):
    from .lista import Lista
    from .context import Context
    if '_lista_context' in nvim.current.buffer.vars:
        context = Context.from_dict(
            nvim.current.buffer.vars['_lista_context']
        )
    else:
        context = Context()
        context.selected_line = nvim.current.window.cursor[0]
    lista = Lista(nvim, context)
    linenum = lista.start(args[0])
    if linenum > 0:
        nvim.call('cursor', [linenum, 0])
        nvim.command('normal! zvzz')
    nvim.current.buffer.vars['_lista_context'] = lista.context.to_dict()
