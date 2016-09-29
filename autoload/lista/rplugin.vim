let s:rep = expand('<sfile>:p:h:h:h')


function! lista#rplugin#start(default) abort
  if !lista#rplugin#init()
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


function! lista#rplugin#init() abort
  if exists('s:supported')
    return s:supported
  endif
  try
    call prompt#rplugin#init()
    let result = rplugin#init(s:rep, {
          \ 'python': 0,
          \ 'python3': has('python3'),
          \})
    let s:supported = result.python3
    if !s:supported
      echoerr 'It requires a Neovim or Vim with Python3 support (+python3)'
    endif
  catch /^Vim\%((\a\+)\)\=:E117/
    echoerr 'It requires a lambdalisue/vim-rplugin in Vim8.'
    echoerr 'https://github.com/lambdalisue/vim-rplugin'
    let s:supported = 0
  endtry
  return s:supported
endfunction
