if has('nvim')
  function! lista#start(default) abort
    return _lista_start(a:default)
  endfunction
  function! lista#resume(default) abort
    return _lista_resume(a:default)
  endfunction
else
  function! lista#start(default) abort
    return lista#rplugin#start(a:default)
  endfunction
  function! lista#resume(default) abort
    return lista#rplugin#resume(a:default)
  endfunction
endif

if !exists('g:lista#custom_mappings')
  let g:lista#custom_mappings = []
endif
