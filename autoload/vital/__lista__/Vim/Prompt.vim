function! s:new(...) abort
  let prompt = extend(deepcopy(s:prompt), get(a:000, 0, {}))
  let prompt.cursor = s:_bind(s:cursor, prompt)
  let prompt.history = s:_bind(s:history, prompt)
  return prompt
endfunction

function! s:_bind(prototype, prompt) abort
  return extend(deepcopy(a:prototype), {
        \ 'prompt': a:prompt,
        \})
endfunction

" Cursor ---------------------------------------------------------------------
let s:cursor = { 'index': 0 }

function! s:cursor.lshift(...) abort
  let amount = get(a:000, 0, 1)
  let self.index -= amount
  let self.index = self.index <= 0 ? 0 : self.index
endfunction

function! s:cursor.rshift(...) abort
  let amount = get(a:000, 0, 1)
  let threshold = len(self.prompt.input)
  let self.index += amount
  let self.index = self.index >= threshold ? threshold : self.index
endfunction

function! s:cursor.home() abort
  let self.index = 0
endfunction

function! s:cursor.end() abort
  let self.index = len(self.prompt.input)
endfunction

function! s:cursor.ltext() abort
  return self.index == 0
        \ ? ''
        \ : self.prompt.input[:self.index-1]
endfunction

function! s:cursor.ctext() abort
  return self.prompt.input[self.index]
endfunction

function! s:cursor.rtext() abort
  return self.prompt.input[self.index+1:]
endfunction


" History --------------------------------------------------------------------
let s:history = { 'index': 0, 'cached': '' }

function! s:history.previous() abort
  if self.index == 0
    let self.cached = self.prompt.input
  endif
  let threshold = histnr('input') * -1
  let self.index = self.index <= threshold ? threshold : self.index - 1
  let self.prompt.input = histget('input', self.index)
  let self.prompt.cursor.index = len(self.prompt.input)
endfunction

function! s:history.next() abort
  let self.index = self.index >= 0 ? 0 : self.index + 1
  if self.index == 0
    let self.prompt.input = self.cached
  else
    let self.prompt.input = histget('input', self.index)
  endif
  let self.prompt.cursor.index = len(self.prompt.input)
endfunction


" Console ---------------------------------------------------------------------
let s:prompt = {
      \ 'prefix': '',
      \ 'input': '',
      \}

function! s:prompt.start(...) abort
  call inputsave()
  let self.input = get(a:000, 0, self.input)
  while !self.callback()
    redraw
    echohl Question | echon self.prefix
    echohl None     | echon self.cursor.ltext()
    echohl Cursor   | echon self.cursor.ctext()
    echohl None     | echon self.cursor.rtext()
    let key = getchar()
    let char = nr2char(key)
    if char ==# "\<CR>" || char ==# "\<Esc>"
      break
    elseif char ==# "\<C-H>" || key ==# "\<BS>"
      call self.remove()
    elseif char ==# "\<C-D>" || key ==# "\<DEL>"
      call self.delete()
    elseif char ==# "\<C-R>"
      echon '"'
      let reg = getreg(nr2char(getchar()))
      call self.insert(substitute(reg, '\n', '', 'g'))
    elseif key ==# "\<Left>" || char ==# "\<C-F>"
      call self.cursor.lshift()
    elseif key ==# "\<Right>" || char ==# "\<C-B>"
      call self.cursor.rshift()
    elseif key ==# "\<Home>" || char ==# "\<C-A>"
      call self.cursor.home()
    elseif key ==# "\<End>" || char ==# "\<C-E>"
      call self.cursor.end()
    elseif key ==# "\<Up>"
      call self.history.previous()
    elseif key ==# "\<Down>"
      call self.history.next()
    elseif !self.keydown(key, char)
      call self.insert(char)
    endif
  endwhile
  redraw | echo
  if !empty(self.input)
    call histadd('input', self.input)
  endif
  call inputrestore()
  return char ==# "\<Esc>" ? 0 : self.input
endfunction

function! s:prompt.replace(text) abort
  let self.input = a:text
  let self.cursor.index = strlen(a:text)
endfunction

function! s:prompt.insert(text) abort
  let lhs = self.cursor.ltext()
  let rhs = self.cursor.ctext() . self.cursor.rtext()
  let self.input = lhs . a:text . rhs
  call self.cursor.rshift(len(a:text))
endfunction

function! s:prompt.remove() abort
  let lhs = self.cursor.ltext()
  if empty(lhs)
    return
  endif
  let lhs = lhs[:-2]
  let rhs = self.cursor.ctext() . self.cursor.rtext()
  let self.input = lhs . rhs
  call self.cursor.lshift()
endfunction

function! s:prompt.delete() abort
  let lhs = self.cursor.ltext()
  let rhs = self.cursor.rtext()
  let self.input = lhs . rhs
endfunction

function! s:prompt.keydown(key, char) abort
  return 0
endfunction

function! s:prompt.callback() abort
  return 0
endfunction
