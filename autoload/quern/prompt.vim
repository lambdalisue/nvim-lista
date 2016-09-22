let s:Guard = vital#quern#import('Vim.Guard')
let s:String = vital#quern#import('Data.String')
let s:Prompt = vital#quern#import('Vim.Prompt')
let s:parent = s:Prompt.new()
let s:prompt = {}

function! s:prompt.start(...) abort
  let self.input = get(a:000, 0, self.input)
  return call(s:parent.start, [], self)
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
    let self._indices = quern#filter#or(
          \ range(len(self._candidates)),
          \ self._candidates,
          \ patterns,
          \ &ignorecase,
          \)
  else
    let self._indices = quern#filter#or(
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

function! quern#prompt#new() abort
  let prompt = s:Prompt.new({
        \ 'prefix': '# ',
        \ '_bufnum': bufnr('%'),
        \})
  let prompt._previous = ''
  let prompt._candidates = getline(1, '$')
  let b:quern_prompt = extend(prompt, s:prompt)
  return prompt
endfunction

function! quern#prompt#get() abort
  let prompt = exists('b:quern_prompt')
        \ ? b:quern_prompt
        \ : quern#prompt#new()
  let content = getline(1, '$')
  if prompt._candidates != content
    let prompt._previous = ''
    let prompt._candidates = content
  endif
  return prompt
endfunction
