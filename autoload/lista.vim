let s:Guard = vital#lista#import('Vim.Guard')

function! lista#start() abort
  let guard = s:Guard.store([
        \ '&bufhidden',
        \])
  let prompt = lista#prompt#get()
  let saved_view = winsaveview()
  let cursor = getpos('.')
  let filename = bufname('%')
  let filetype = &filetype
  try
    setlocal bufhidden=hide
    noautocmd execute 'keepjumps edit' 'lista://' . filename
    setlocal cursorline
    setlocal nobuflisted
    setlocal buftype=nofile
    setlocal bufhidden=wipe
    execute 'setlocal filetype=' . filetype . '.lista'
    if !empty(prompt.start())
      let cursor[1] = prompt._indices[line('.')-1] + 1
    endif
    noautocmd execute 'keepjumps' prompt._bufnum 'buffer'
  finally
    keepjump call winrestview(saved_view)
    call guard.restore()
    call setpos('.', cursor)
  endtry
endfunction
