let s:Guard = vital#lista#import('Vim.Guard')

function! lista#start() abort
  let guard = s:Guard.store([
        \ '&cursorline',
        \ '&filetype',
        \ 'undolist',
        \ 'winview',
        \])
  let cursor = getpos('.')
  let prompt = lista#prompt#get()
  try
    let &filetype .= '.lista'
    setlocal cursorline
    if !empty(prompt.start())
      let cursor[1] = prompt._indices[line('.')-1] + 1
    endif
    call prompt.content(prompt._candidates)
  finally
    call guard.restore()
    call setpos('.', cursor)
  endtry
endfunction
