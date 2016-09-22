if exists('g:loaded_lista')
  finish
endif
let g:loaded_lista = 1

command! Lista :call lista#start()
