let s:Guard = vital#quern#import('Vim.Guard')
let s:Prompt = vital#quern#import('Vim.Prompt')

function! quern#start() abort
  let guard = s:Guard.store([
        \ '&cursorline',
        \ '&conceallevel',
        \ '&concealcursor'
        \])
  let cursor = getpos('.')
  let content = getline(1, '$')
  let mid = matchadd('Conceal', '^\d\+:', 10, -1, {'conceal': ''})
  try
    set cursorline
    set conceallevel=3
    set concealcursor=nvic
    let prompt = s:Prompt.new({ 'prefix': '# ' })
    let prompt = extend(prompt, s:prompt)
    let prompt.bufnr = bufnr('%')
    let prompt.candidates = map(copy(content), '(v:key + 1) . '':'' . v:val')
    let cursor[1] = 1
    call setpos('.', cursor)
    call s:assign_content(prompt.candidates)
    call prompt.start()
    let cursor[1] = str2nr(matchstr(getline('.'), '^\d\+\ze:'))
  finally
    call guard.restore()
    call s:assign_content(content)
    call setpos('.', cursor)
    call matchdelete(mid)
  endtry
endfunction

function! s:assign_content(content) abort
  let gurad = s:Guard.store(['&modifiable', '&modified'])
  let saved_view = winsaveview()
  try
    set modifiable
    silent keepjumps %delete _
    call setline(1, a:content)
  finally
    keepjump call winrestview(saved_view)
    call gurad.restore()
  endtry
endfunction

function! s:define_syntax() abort
  call matchadd('QuernLineNum', '^\d\+:', 10, -1, {'conceal': ''})
endfunction

let s:prompt = {}

function! s:prompt.callback() abort
  let candidates = filter(
        \ copy(self.candidates),
        \ 'v:val =~# self.input'
        \)
  call s:assign_content(candidates)
endfunction

function! s:prompt.keydown(key, char) abort
  if a:char ==# "\<C-N>"
    call setpos('.', [0, line(".")+1, col('.'), 0])
    return 1
  elseif a:char ==# "\<C-P>"
    call setpos('.', [0, line(".")-1, col('.'), 0])
    return 1
  endif
endfunction

