if exists('g:loaded_lista')
  finish
endif
let g:loaded_lista = 1

command! -nargs=* -bang -range
      \ -complete=customlist,lista#router#complete
      \ Lista
      \ call lista#router#command(<q-bang>, [<line1>, <line2>], <q-args>)
