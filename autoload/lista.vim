if has('nvim')
  function! lista#start() abort
    return _lista_start()
  endfunction
else
  function! lista#start() abort
    return lista#python#start()
  endfunction
endif
