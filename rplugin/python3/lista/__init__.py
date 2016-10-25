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
    from .prompt.prompt import STATUS_ACCEPT
    from .lista import Lista
    from .context import Context
    if '_lista_context' in nvim.current.buffer.vars:
        context = Context.from_dict(
            nvim.current.buffer.vars['_lista_context']
        )
    else:
        context = Context()
        context.selected_index = nvim.current.window.cursor[0] - 1
    lista = Lista(nvim, context)
    status = lista.start(args[0])
    if status == STATUS_ACCEPT:
        nvim.call('cursor', [lista.selected_line, 0])
        nvim.command('normal! zvzz')
    nvim.current.buffer.vars['_lista_context'] = lista.context.to_dict()
