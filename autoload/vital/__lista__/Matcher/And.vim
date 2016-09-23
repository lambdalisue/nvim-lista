function! s:_vital_loaded(V) abort
  let s:String = a:V.import('Data.String')
endfunction

function! s:_vital_depends() abort
  return ['Data.String']
endfunction

function! s:_vital_created(module) abort
  if exists('*s:filter_lua')
    let a:module.filter = function('s:filter_lua')
    let a:module.implementation = 'lua'
  elseif exists('*s:filter_python') && !has('nvim')
    let a:module.filter = function('s:filter_python')
    let a:module.implementation = 'python'
  elseif exists('*s:filter_python3') && !has('nvim')
    let a:module.filter = function('s:filter_python3')
    let a:module.implementation = 'python3'
  else
    let a:module.filter = function('s:filter_vim')
    let a:module.implementation = 'vim'
  endif
endfunction

function! s:pattern(input) abort
  if empty(a:input)
    return ''
  endif
  let terms = map(split(a:input), 's:String.escape_pattern(v:val)')
  return '\%(' . join(terms, '\|') . '\)'
endfunction

if has('lua')
  " FORKED FROM:
  " https://github.com/Shougo/unite.vim/blob/master/autoload/unite/filters.vim#L73
  function! s:filter_lua(input, indices, candidates) abort
    let patterns = filter(split(a:input), '!empty(v:val)')
    lua << EOF
do
  local indices = vim.eval('a:indices')
  local candidates = vim.eval('a:candidates')
  local patterns = vim.eval('patterns')
  if (vim.eval('&ignorecase') == 1) then
    for j = #indices-1, 0, -1 do
      for i = 0, #patterns-1 do
        if (string.find(string.lower(candidates[indices[j]]), string.lower(patterns[i]), 1, true) == nil) then
          indices[j] = nil
          break
        end
      end
    end
  else
    for j = #indices-1, 0, -1 do
      for i = 0, #patterns-1 do
        if (string.find(candidates[indices[j]], patterns[i], 1, true) == nil) then
          indices[j] = nil
          break
        end
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
    let patterns = filter(split(a:input), '!empty(v:val)')
    python << EOF
import vim
def _temporary_scope():
  indices = vim.bindeval('a:indices')
  candidates = vim.bindeval('a:candidates')
  patterns = vim.bindeval('patterns')
  if int(vim.eval('&ignorecase')) == 1:
    indices[:] = [
      i for i in indices
      if all(p.lower() in candidates[i].lower() for p in patterns)
    ]
  else:
    indices[:] = [
      i for i in indices
      if all(p in candidates[i] for p in patterns)
    ]
_temporary_scope()
del _temporary_scope
EOF
    return a:indices
  endfunction
endif

if has('python3')
  function! s:filter_python3(input, indices, candidates) abort
    let patterns = filter(split(a:input), '!empty(v:val)')
    python3 << EOF
import vim
def _temporary_scope():
  indices = vim.bindeval('a:indices')
  candidates = vim.bindeval('a:candidates')
  patterns = vim.bindeval('patterns')
  if int(vim.eval('&ignorecase')) == 1:
    indices[:] = [
      i for i in indices
      if all(p.lower() in candidates[i].lower() for p in patterns)
    ]
  else:
    indices[:] = [
      i for i in indices
      if all(p in candidates[i] for p in patterns)
    ]
_temporary_scope()
del _temporary_scope
EOF
    return a:indices
  endfunction
endif

function! s:filter_vim(input, indices, candidates) abort dict
  let patterns = split(a:input)
  if &ignorecase
    let patterns = map(patterns, 's:String.escape_pattern(v:val)')
    for pattern in patterns
      call filter(
            \ a:indices,
            \ 'a:candidates[v:val] =~? pattern'
            \)
    endfor
  else
    for pattern in patterns
      call filter(
            \ a:indices,
            \ 'stridx(a:candidates[v:val], pattern) != -1'
            \)
    endfor
  endif
  return a:indices
endfunction

