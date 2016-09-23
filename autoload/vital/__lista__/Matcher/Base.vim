function! s:_vital_loaded(V) abort
  let s:String = a:V.import('Data.String')
endfunction

function! s:_vital_depends() abort
  return ['Data.String']
endfunction

if has('lua')
  " FORKED FROM:
  " https://github.com/Shougo/unite.vim/blob/master/autoload/unite/filters.vim#L105
  function! s:filter_lua(input, indices, candidates) abort
    let pattern = a:input
    lua << EOF
do
  local indices = vim.eval('a:indices')
  local candidates = vim.eval('a:candidates')
  local pattern = vim.eval('pattern')
  if (vim.eval('&ignorecase') == 1) then
    pattern = string.lower(pattern)
    for j = #indices-1, 0, -1 do
      if string.find(string.lower(candidates[indices[j]]), pattern) == nil then
        indices[j] = nil
      end
    end
  else
    for j = #indices-1, 0, -1 do
      if string.find(candidates[indices[j]], pattern) == nil then
        indices[j] = nil
      end
    end
  end
end
EOF
    return a:indices
  endfunction
endif

if has('python')
  function! s:filter_python(input, indices, candidates) abort
    let pattern = a:input
    python << EOF
import vim
def _temporary_scope():
  import re
  indices = vim.bindeval('a:indices')
  candidates = vim.bindeval('a:candidates')
  pattern = vim.bindeval('pattern')
  if int(vim.eval('&ignorecase')) == 1:
    pattern = re.compile(pattern.lower())
    indices[:] = [
      i for i in indices
      if pattern.search(candidates[i].lower())
    ]
  else:
    pattern = re.compile(pattern)
    indices[:] = [
      i for i in indices
      if pattern.search(candidates[i])
    ]
_temporary_scope()
del _temporary_scope
EOF
    return a:indices
  endfunction
endif

if has('python3')
  function! s:filter_python3(input, indices, candidates) abort
    let pattern = a:input
    python3 << EOF
import vim
def _temporary_scope():
  import re
  indices = vim.bindeval('a:indices')
  candidates = vim.bindeval('a:candidates')
  pattern = vim.bindeval('pattern')
  if int(vim.eval('&ignorecase')) == 1:
    pattern = re.compile(pattern.lower())
    indices[:] = [
      i for i in indices
      if pattern.search(candidates[i].lower())
    ]
  else:
    pattern = re.compile(pattern)
    indices[:] = [
      i for i in indices
      if pattern.search(candidates[i])
    ]
_temporary_scope()
del _temporary_scope
EOF
    return a:indices
  endfunction
endif

function! s:filter_vim(input, indices, candidates) abort
  let pattern = a:input
  return filter(a:indices, 'a:candidates[v:val] =~ pattern')
endfunction

" COPIED FROM:
" https://github.com/Shougo/unite.vim/blob/master/autoload/unite/filters.vim#L149 
function! s:escape_pattern_lua(text) abort
  return substitute(substitute(substitute(substitute(a:text,
        \ '\\ ', ' ', 'g'),
        \ '[%\[\]().+?^$-]', '%\0', 'g'),
        \ '\*\@<!\*\*\@!', '.*', 'g'),
        \ '\*\*\+', '.*', 'g')
endfunction

function! s:escape_pattern_python(text) abort
  return escape(a:text, '.^$*+?{}\[]|()')
endfunction

function! s:escape_pattern_vim(text) abort
  return s:String.escape_pattern(a:text)
endfunction


