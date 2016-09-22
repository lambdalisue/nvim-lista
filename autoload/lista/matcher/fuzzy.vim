let s:Config = vital#lista#import('App.Config')


" Public ---------------------------------------------------------------------
function! lista#matcher#fuzzy#define(...) abort
  let matcher = copy(s:matcher)
  if g:lista#matcher#fuzzy#lua
    let matcher.filter = function('s:filter_lua')
    let matcher.implementation = 'lua'
  elseif g:lista#matcher#fuzzy#python
    let matcher.filter = function('s:filter_python')
    let matcher.implementation = 'python'
  elseif g:lista#matcher#fuzzy#python3
    let matcher.filter = function('s:filter_python3')
    let matcher.implementation = 'python3'
  else
    let matcher.filter = function('s:filter_vim')
    let matcher.implementation = 'vim'
  endif
  return matcher
endfunction


" Matcher --------------------------------------------------------------------
let s:matcher = { 'name': 'fuzzy' }

" REF:
" https://github.com/Shougo/unite.vim/blob/master/autoload/unite/filters/matcher_fuzzy.vim#L40
function! s:matcher.pattern(input) abort
  if empty(a:input)
    return ''
  endif
  let chars = map(split(a:input, '\zs'), 'lista#util#escape_pattern_vim(v:val)')
  let chars = map(chars, 'printf(''%s[^%s]\{-}'', v:val, v:val)')
  return join(chars, '')
endfunction


" Private --------------------------------------------------------------------
function! s:filter_vim(input, indices, candidates) abort dict
  let pattern = self.pattern(a:input)
  return filter(a:indices, 'a:candidates[v:val] =~ pattern')
endfunction

if has('lua')
  " FORKED FROM:
  " https://github.com/Shougo/unite.vim/blob/master/autoload/unite/filters.vim#L105
  function! s:filter_lua(input, indices, candidates) abort
    let pattern = lista#util#escape_pattern_lua(a:input)
    let pattern = substitute(pattern, '[[:alnum:]_/-]\ze.', '\0.-', 'g')
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
    let chars = map(split(a:input, '\zs'), 'lista#util#escape_pattern_python(v:val)')
    let chars = map(chars, 'printf(''%s[^%s]*?'', v:val, v:val)')
    let pattern = join(chars, '')
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
    let chars = map(split(a:input, '\zs'), 'lista#util#escape_pattern_python(v:val)')
    let chars = map(chars, 'printf(''%s[^%s]*?'', v:val, v:val)')
    let pattern = join(chars, '')
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


call s:Config.define('lista#matcher#fuzzy', {
      \ 'lua': has('lua'),
      \ 'python': !has('nvim') && has('python'),
      \ 'python3': !has('nvim') && has('python3'),
      \})
