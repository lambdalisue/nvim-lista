let s:matchers = {}

" Public ---------------------------------------------------------------------
function! lista#matcher#get(name, ...) abort
  let name = has_key(s:matchers, a:name) ? a:name : 'and'
  let matcher = copy(s:matchers[name])
  let matcher.name = name
  let matcher = extend(matcher, s:matcher)
  return matcher
endfunction

function! lista#matcher#register(name, matcher) abort
  let s:matchers[a:name] = a:matcher
endfunction


" Matcher --------------------------------------------------------------------
let s:matcher = { 'match_id': 0 }

function! s:matcher.highlight(input) abort
  if self.match_id > 0
    call matchdelete(self.match_id)
    let self.match_id = 0
  endif
  if !empty(a:input)
    let self.match_id = matchadd('Search', self.pattern(a:input), 0)
  endif
endfunction

function! s:matcher.regsearch(input) abort
  if !empty(a:input)
    call setreg('/', self.pattern(a:input))
  endif
endfunction


" Registration ---------------------------------------------------------------
call lista#matcher#register('and', vital#lista#import('Matcher.And'))
call lista#matcher#register('fuzzy', vital#lista#import('Matcher.Fuzzy'))
