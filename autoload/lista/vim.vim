let s:sep = (!has('win32') && !has('win64')) || &shellslash ? '/' : '\\'
let s:rep = expand('<sfile>:p:h:h:h')
let s:lib = join([s:rep, 'rplugin', 'python3'], s:sep)
let s:status = 'pending'

function! s:init() abort
  if !has('patch-7.4.2367') || !has('python3')
    echohl WarningMsg
    echo 'vim-lista does not work with this version.'
    echo 'It requires Vim 7.4.2367 with Python3 support (+python3).'
    echohl None
    return 'disabled'
  endif
  try
    python3 << EOF
import vim
import sys
sys.path.insert(0, vim.eval('s:lib'))
EOF
    return 'ready'
  catch
    return 'disabled'
  endtry
endfunction

function! lista#vim#start() abort
  if s:status == 'disabled'
    echohl WarningMsg
    echo 'vim-lista does not work with this version.'
    echo 'It requires Vim 7.4.2367 with Python3 support (+python3).'
    echohl None
    return
  elseif s:status == 'pending'
    let s:status = s:init()
    return lista#vim#start()
  endif
  python3 << EOF
def _temporary_scope():
    from lista.lista import Lista
    from lista.compat import Nvim
    Lista(Nvim(vim)).start()
_temporary_scope()
del _temporary_scope
EOF
endfunction
