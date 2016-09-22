" Note:
" Using stridx() is faster than using =~# but using stridx() + tolower() * 2
" is slower than using =~?
function! s:or_vim(indices, candidates, patterns, ignorecase) abort
  if a:ignorecase
    let patterns = map(copy(a:patterns), 'escape(v:val, ''^$~.*[]\"'')')
    for pattern in patterns
      call filter(a:indices, 'a:candidates[v:val] =~? ''\m'' . pattern')
    endfor
  else
    for pattern in a:patterns
      call filter(a:indices, 'stridx(a:candidates[v:val], pattern) != -1')
    endfor
  endif
  return a:indices
endfunction

if has('lua')
  function! s:or_lua(indices, candidates, patterns, ignorecase) abort
    lua << EOF
do
  local patterns = vim.eval('a:patterns')
  local candidates = vim.eval('a:candidates')
  local indices = vim.eval('a:indices')
  if (vim.eval('a:ignorecase') == 1) then
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

if !has('nvim') && has('python')
  function! s:or_python(indices, candidates, patterns, ignorecase) abort
    python << EOF
import vim
def _temporary_scope():
  patterns = vim.bindeval('a:patterns')
  candidates = vim.bindeval('a:candidates')
  indices = vim.bindeval('a:indices')
  if int(vim.eval('a:ignorecase')) == 1:
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

if !has('nvim') && has('python3')
  function! s:or_python3(indices, candidates, patterns, ignorecase) abort
    python3 << EOF
import vim
def _temporary_scope():
  patterns = vim.bindeval('a:patterns')
  candidates = vim.bindeval('a:candidates')
  indices = vim.bindeval('a:indices')
  if int(vim.eval('a:ignorecase')) == 1:
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

" NOTE:
" In vim:  lua < python < python3 < vim
" In nvim: vim << python < python3
" https://gist.github.com/7bd3235de531c5dfac05a2f2fe7ddbf0#file-test2-vim
if has('lua')
  function! lista#filter#or(...) abort
    return call('s:or_lua', a:000)
  endfunction
elseif !has('nvim') && has('python')
  function! lista#filter#or(...) abort
    return call('s:or_python', a:000)
  endfunction
elseif !has('nvim') && has('python3')
  function! lista#filter#or(...) abort
    return call('s:or_python3', a:000)
  endfunction
else
  function! lista#filter#or(...) abort
    return call('s:or_vim', a:000)
  endfunction
endif

