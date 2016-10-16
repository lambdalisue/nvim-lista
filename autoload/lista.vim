if has('nvim')
  function! lista#start(default) abort
    return _lista_start(a:default)
  endfunction
else
  function! lista#start(default) abort
    return lista#rplugin#start(a:default)
  endfunction
endif
