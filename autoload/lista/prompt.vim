let s:String = vital#lista#import('Data.String')
let s:Guard = vital#lista#import('Vim.Guard')
let s:Prompt = vital#lista#import('Vim.Prompt')
let s:Validator = vital#lista#import('Data.Validator')

" Public ---------------------------------------------------------------------
let s:rule = s:Validator.new({
      \ 'prefix': { 'type': type('') },
      \ 'matcher': { 'type': type('') },
      \ 'highlight': { 'type': type(0) },
      \})
function! lista#prompt#get(...) abort
  let options = s:rule.validate(get(a:000, 0, {}))
  if exists('b:lista_prompt')
    let prompt = b:lista_prompt
  else
    let prompt = s:Prompt.new({
          \ 'prefix': options.prefix,
          \})
    let prompt.previous = ''
    let prompt.content = []
    let b:lista_prompt = extend(prompt, s:prompt)
  endif
  let prompt.matcher = lista#matcher#get(options.matcher)
  let prompt.highlight = options.highlight
  " Update content if necessary
  let content = getline(1, '$')
  if prompt.content != content
    let prompt.content = content
    let prompt.previous = ''
  endif
  return prompt
endfunction


" Prompt ---------------------------------------------------------------------
let s:parent = s:Prompt.new()
let s:prompt = {}

function! s:prompt.restore() abort
  call s:assign_content(self.content)
endfunction

function! s:prompt.start(...) abort
  let guard = s:Guard.store(['&l:statusline'])
  try
    let result = call(s:parent.start, a:000, self)
    call self.matcher.highlight('')
    call self.matcher.regsearch(self.input)
    return result
  finally
    call guard.restore()
  endtry
endfunction

function! s:prompt.keydown(key, char) abort
  if a:char ==# "\<C-N>"
    call setpos('.', [0, line('.')+1, col('.'), 0])
    return 1
  elseif a:char ==# "\<C-P>"
    call setpos('.', [0, line('.')-1, col('.'), 0])
    return 1
  endif
endfunction

function! s:prompt.callback() abort
  let previous = self.previous
  let self.previous = self.input
  if empty(previous) || self.input !~# '^' . s:String.escape_pattern(previous)
    let self.indices = self.matcher.filter(
          \ self.input,
          \ range(len(self.content)),
          \ self.content,
          \)
  else
    let self.indices = self.matcher.filter(
          \ self.input,
          \ self.indices,
          \ self.content,
          \)
  endif
  let content = map(
        \ copy(self.indices),
        \ 'self.content[v:val]'
        \)
  call s:assign_content(content)
  call self.redraw_statusline()
  if self.highlight
    call self.matcher.highlight(self.input)
  endif
endfunction

function! s:prompt.redraw_statusline() abort
  redrawstatus
  let &l:statusline = printf(
        \ "%%f %%= %s: %s/%s (%s)",
        \ get(self.matcher, 'name', 'unknown'),
        \ len(self.indices),
        \ len(self.content),
        \ get(self.matcher, 'implementation', '?'),
        \)
endfunction


" Private --------------------------------------------------------------------
function! s:assign_content(content) abort
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
