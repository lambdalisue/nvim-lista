let s:rep = expand('<sfile>:p:h:h:h')


function! lista#rplugin#start(default) abort
  if !lista#rplugin#init()
    return
  endif
  python3 << EOC
def _temporary_scope():
    import vim
    import rplugin
    from lista import start
    nvim = rplugin.Neovim(vim)
    start(nvim, [nvim.eval('a:default')], False)
_temporary_scope()
del _temporary_scope
EOC
endfunction

function! lista#rplugin#resume(default) abort
  if !lista#rplugin#init()
    return
  endif
  python3 << EOC
def _temporary_scope():
    import vim
    import rplugin
    from lista import start
    nvim = rplugin.Neovim(vim)
    start(nvim, [nvim.eval('a:default')], True)
_temporary_scope()
del _temporary_scope
EOC
endfunction

function! lista#rplugin#init() abort
  if exists('s:supported')
    return s:supported
  endif
  try
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
