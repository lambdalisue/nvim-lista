let s:String = vital#lista#import('Data.String')
let s:Guard = vital#lista#import('Vim.Guard')


function! lista#util#assign_content(content) abort
  let gurad = s:Guard.store([
        \ '&modifiable',
        \ '&modified',
        \ 'winview',
        \])
  try
    set modifiable
    silent keepjumps %delete _
    call setline(1, a:content)
  finally
    call gurad.restore()
  endtry
endfunction

function! lista#util#escape_pattern_vim(text) abort
  return s:String.escape_pattern(a:text)
endfunction

function! lista#util#escape_pattern_python(text) abort
  return escape(a:text, '.^$*+?{}\[]|()')
endfunction

" COPIED FROM:
" https://github.com/Shougo/unite.vim/blob/master/autoload/unite/filters.vim#L149 
function! lista#util#escape_pattern_lua(text) abort
  return substitute(substitute(substitute(substitute(a:text,
        \ '\\ ', ' ', 'g'),
        \ '[%\[\]().+?^$-]', '%\0', 'g'),
        \ '\*\@<!\*\*\@!', '.*', 'g'),
        \ '\*\*\+', '.*', 'g')
endfunction
