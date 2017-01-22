try:
    import neovim

    @neovim.plugin
    class ListaEntryPoint:
        def __init__(self, nvim):
            self.nvim = nvim

        @neovim.function('_lista_start', sync=True)
        def start(self, args):
            return start(self.nvim, args, False)

        @neovim.function('_lista_resume', sync=True)
        def resume(self, args):
            return start(self.nvim, args, True)

except ImportError:
    pass


def start(nvim, args, resume):
    import traceback
    try:
        from .prompt.prompt import STATUS_ACCEPT
        from .lista import Lista, Condition
        if resume and '_lista_context' in nvim.current.buffer.vars:
            context = nvim.current.buffer.vars['_lista_context']
            context['text'] = context['text'] if not args[0] else args[0]
            condition = Condition(**context)
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
    except Exception as e:
        from .prompt.util import ESCAPE_ECHO
        nvim.command('redraw')
        nvim.command('echohl ErrorMsg')
        for line in traceback.format_exc().splitlines():
            nvim.command('echomsg "%s"' % line.translate(ESCAPE_ECHO))
