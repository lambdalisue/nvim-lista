" Public ---------------------------------------------------------------------
function! lista#matcher#get(name, ...) abort
  try
    let matcher = call(
          \ printf('lista#matcher#%s#define', a:name),
          \ a:000,
          \)
  catch /^Vim\%((\a\+)\)\=:E117/
    let matcher = lista#matcher#or#define()
  endtry
  return extend(matcher, s:matcher)
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
