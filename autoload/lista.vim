if has('nvim')
  function! lista#start(default) abort
    return _lista_start(a:default)
  endfunction
else
  function! lista#start(default) abort
    return lista#python#start(a:default)
  endfunction
endif


if !exists('g:lista#custom_mapping')
  " Define Emacs-like prompt mapping
  let g:lista#custom_mapping = [
        \ ["\<C-D>", "\<Del>"],
        \ ["\<C-A>", "\<Home>"],
        \ ["\<C-E>", "\<End>"],
        \ ["\<C-F>", "\<Left>"],
        \ ["\<C-B>", "\<Right>"],
        \]
endif
