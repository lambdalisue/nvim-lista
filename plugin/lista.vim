if exists('g:loaded_lista')
  finish
endif
let g:loaded_lista = 1

function! s:command(qargs) abort
  return lista#start(a:qargs)
endfunction
command! -nargs=? Lista  call s:command(<q-args>)
command! ListaCursorWord call s:command(expand('<cword>'))
