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
    from .lista import Lista, Condition
    if '_lista_context' in nvim.current.buffer.vars:
        condition = Condition(
            **nvim.current.buffer.vars['_lista_context']
        )
    else:
        condition = Condition(
            text=args[0],
            caret_locus=0,
            selected_index=nvim.current.window.cursor[0] - 1,
            matcher_index=0,
            case_index=0,
        )
    lista = Lista(nvim, condition)
    status = lista.start()
    if status == STATUS_ACCEPT:
        nvim.call('cursor', [lista.selected_line, 0])
        nvim.command('normal! zvzz')
    nvim.current.buffer.vars['_lista_context'] = lista.store()._asdict()
