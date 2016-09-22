let s:Guard = vital#lista#import('Vim.Guard')
let s:Config = vital#lista#import('App.Config')
let s:Prompt = vital#lista#import('Vim.Prompt')

" Prompt ---------------------------------------------------------------------
let s:parent = s:Prompt.new()
let s:prompt = {}

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
  if empty(previous) || self.input !~# '^' . lista#util#escape_pattern_vim(previous)
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
  call lista#util#assign_content(content)
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


" Public ---------------------------------------------------------------------
" options:
"   prefix:     String
"   matcher:    String
"   highlight:  0/1
function! lista#prompt#get(options) abort
  if exists('b:lista_prompt')
    let prompt = b:lista_prompt
  else
    let prompt = s:Prompt.new({
          \ 'prefix': a:options.prefix,
          \})
    let prompt.previous = ''
    let prompt.content = []
    let b:lista_prompt = extend(prompt, s:prompt)
  endif
  let prompt.matcher = lista#matcher#get(a:options.matcher)
  let prompt.highlight = a:options.highlight
  " Update content if necessary
  let content = getline(1, '$')
  if prompt.content != content
    let prompt.content = content
    let prompt.previous = ''
  endif
  return prompt
endfunction


call s:Config.define('lista#prompt', {
      \ 'prefix': '# ',
      \ 'matcher': 'or',
      \ 'disable_highlight': 0,
      \})
