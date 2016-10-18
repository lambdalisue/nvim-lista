if has('nvim')
  function! lista#start(default) abort
    return _lista_start(a:default)
  endfunction
else
  function! lista#start(default) abort
    return lista#rplugin#start(a:default)
  endfunction
endif

if !exists('g:lista#custom_mappings')
  let g:lista#custom_mappings = [
        \ ['<C-T>', '<PageUp>'],
        \ ['<C-G>', '<PageDown>'],
        \ ['<C-6>', '<C-^>'],
        \]
endif
