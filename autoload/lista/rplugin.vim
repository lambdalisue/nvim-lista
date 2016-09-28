let s:rep = expand('<sfile>:p:h:h:h')


function! s:init() abort
  if exists('s:result')
    return s:result
  endif
  let s:result = rplugin#init(s:rep, {
        \ 'python': 0,
        \ 'python3': has('python3'),
        \})
  return s:result
endfunction

function! lista#rplugin#start(default) abort
  if !s:init().python3
    echoerr 'vim-lista requires a Vim with Python3 support (+python3)'
    return
  endif
  python3 << EOC
def _temporary_scope():
    import vim
    import rplugin
    from lista.core import Lista
    from lista.context import Context
    nvim = rplugin.Neovim(vim)
    context = Context(nvim)
    lista = Lista(nvim, context)
    lista.start(nvim.eval('a:default'))
_temporary_scope()
del _temporary_scope
EOC
endfunction
