if exists('g:loaded_lista')
  finish
endif
let g:loaded_lista = 1

function! s:start(qargs) abort
  return lista#start(a:qargs)
endfunction

function! s:resume(qargs) abort
  return lista#resume(a:qargs)
endfunction

command! -nargs=? Lista  call s:start(<q-args>)
command! ListaCursorWord call s:start(expand('<cword>'))

command! -nargs=? ListaResume  call s:resume(<q-args>)
command! ListaResumeCursorWord call s:resume(expand('<cword>'))
