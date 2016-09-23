function! s:_vital_loaded(V) abort
  let s:Base = a:V.import('Matcher.Base')
endfunction

function! s:_vital_depends() abort
  return ['Matcher.Base']
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

" REF:
" https://github.com/Shougo/unite.vim/blob/master/autoload/unite/filters/matcher_fuzzy.vim#L40
function! s:pattern(input) abort
  if empty(a:input)
    return ''
  endif
  let chars = map(split(a:input, '\zs'), 's:Base.escape_pattern_vim(v:val)')
  let chars = map(chars, 'printf(''%s[^%s]\{-}'', v:val, v:val)')
  return join(chars, '')
endfunction

if has('lua')
  " FORKED FROM:
  " https://github.com/Shougo/unite.vim/blob/master/autoload/unite/filters.vim#L105
  function! s:filter_lua(input, indices, candidates) abort
    let pattern = s:Base.escape_pattern_lua(a:input)
    let pattern = substitute(pattern, '[[:alnum:]_/-]\ze.', '\0.-', 'g')
    return s:Base.filter_lua(pattern, a:indices, a:candidates)
  endfunction
endif

if has('python')
  function! s:filter_python(input, indices, candidates) abort
    let chars = map(split(a:input, '\zs'), 's:Base.escape_pattern_python(v:val)')
    let chars = map(chars, 'printf(''%s[^%s]*?'', v:val, v:val)')
    let pattern = join(chars, '')
    return s:Base.filter_python(pattern, a:indices, a:candidates)
  endfunction
endif

if has('python3')
  function! s:filter_python3(input, indices, candidates) abort
    let chars = map(split(a:input, '\zs'), 's:Base.escape_pattern_python(v:val)')
    let chars = map(chars, 'printf(''%s[^%s]*?'', v:val, v:val)')
    let pattern = join(chars, '')
    return s:Base.filter_python3(pattern, a:indices, a:candidates)
  endfunction
endif

function! s:filter_vim(input, indices, candidates) abort
  let pattern = s:pattern(a:input)
  return s:Base.filter_vim(pattern, a:indices, a:candidates)
endfunction

