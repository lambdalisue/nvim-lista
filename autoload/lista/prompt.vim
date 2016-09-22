let s:Guard = vital#lista#import('Vim.Guard')
let s:Config = vital#lista#import('App.Config')
let s:String = vital#lista#import('Data.String')
let s:Prompt = vital#lista#import('Vim.Prompt')
let s:parent = s:Prompt.new()
let s:prompt = {}

function! s:prompt.start(...) abort
  let self.input = get(a:000, 0, self.input)
  let result = call(s:parent.start, [], self)
  let patterns = filter(split(self.input), '!empty(v:val)')
  call self.remove_highlights()
  call setreg('/', '\<\%(' . join(patterns, '\|') . '\)\>')
  return result
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
  let patterns = filter(split(self.input), '!empty(v:val)')
  let previous = self._previous
  let self._previous = self.input
  if empty(previous) || self.input !~# '^' . s:String.escape_pattern(previous)
    let self._indices = lista#filter#or(
          \ range(len(self._candidates)),
          \ self._candidates,
          \ patterns,
          \ &ignorecase,
          \)
  else
    let self._indices = lista#filter#or(
          \ self._indices,
          \ self._candidates,
          \ patterns,
          \ &ignorecase,
          \)
  endif
  let candidates = map(
        \ copy(self._indices),
        \ 'self._candidates[v:val]'
        \)
  call self.content(candidates)

  if g:lista#prompt#disable_highlight
    return
  endif
  " Highlight patterns used
  call self.remove_highlights()
  let self._matchids = map(
        \ copy(patterns),
        \ 'matchadd(''Search'', s:String.escape_pattern(v:val), 0)'
        \)
endfunction

function! s:prompt.content(content) abort
  let saved_view = winsaveview()
  let gurad = s:Guard.store(['&modifiable', '&modified'])
  try
    set modifiable
    silent keepjumps %delete _
    call setline(1, a:content)
  finally
    call gurad.restore()
    keepjump call winrestview(saved_view)
  endtry
endfunction

function! s:prompt.remove_highlights() abort
  call filter(self._matchids, 'matchdelete(v:val)')
endfunction

function! lista#prompt#new() abort
  let prompt = s:Prompt.new({
        \ 'prefix': '# ',
        \ '_bufnum': bufnr('%'),
        \})
  let prompt._matchids = []
  let prompt._previous = ''
  let prompt._candidates = getline(1, '$')
  let b:lista_prompt = extend(prompt, s:prompt)
  return prompt
endfunction

function! lista#prompt#get() abort
  let prompt = exists('b:lista_prompt')
        \ ? b:lista_prompt
        \ : lista#prompt#new()
  let content = getline(1, '$')
  if prompt._candidates != content
    let prompt._previous = ''
    let prompt._candidates = content
  endif
  return prompt
endfunction


call s:Config.define('lista#prompt', {
      \ 'disable_highlight': 0,
      \})
