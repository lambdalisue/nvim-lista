if exists('g:loaded_lista')
  finish
endif
let g:loaded_lista = 1

command! -nargs=* -bang -range
      \ -complete=customlist,lista#complete
      \ Lista
      \ call lista#command(<q-bang>, [<line1>, <line2>], <q-args>)

command! -nargs=* -bang -range
      \ -complete=customlist,lista#complete
      \ ListaCursorWord
      \ call lista#command(<q-bang>, [<line1>, <line2>], <q-args>, 1)
