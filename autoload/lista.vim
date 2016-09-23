let s:Guard = vital#lista#import('Vim.Guard')
let s:Config = vital#lista#import('App.Config')
let s:Argument = vital#lista#import('Argument')
let s:Validator = vital#lista#import('Data.Validator')

call s:Config.define('lista', {
      \ 'prefix': '# ',
      \ 'matcher': 'and',
      \ 'highlight': 1,
      \})
let s:rule = s:Validator.new({
      \ 'prefix': { 'type': type(''), 'default': g:lista#prefix },
      \ 'matcher': { 'type': type(''), 'default': g:lista#matcher },
      \ 'highlight': { 'type': type(0), 'default': g:lista#highlight },
      \})
function! lista#start(default, ...) abort
  let options = s:rule.validate(get(a:000, 0, {}))
  let guard = s:Guard.store([
        \ '&cursorline',
        \ '&filetype',
        \ 'undolist',
        \ 'winview',
        \])
  let cursor = getpos('.')
  let prompt = lista#prompt#get(options)
  try
    let &filetype .= '.lista'
    setlocal cursorline
    if !empty(prompt.start(a:default))
      let cursor[1] = get(prompt.indices, line('.')-1, cursor[1]-1) + 1
    endif
  finally
    call prompt.restore()
    call guard.restore()
    call setpos('.', cursor)
  endtry
endfunction

function! lista#command(bang, range, qargs, ...) abort
  let cursorword = get(a:000, 0, 0)
  let args = s:Argument.new(a:qargs)
  let options = {}
  let options.prefix = args.get('--prefix', g:lista#prefix)
  let options.matcher = args.get('-m|--matcher', g:lista#matcher)
  let options.highlight = !args.get('-n|--no-highlight', !g:lista#highlight)
  let default = cursorword ? expand('<cword>') : args.get_p(0)
  return lista#start(default, options)
endfunction

function! lista#complete(arglead, cmdline, cursorpos) abort
  let candidates = []
  if a:arglead =~# '^\%(-m\|--matcher=\)'
    let prefix = matchstr(a:arglead, '^\%(-m\|--matcher=\)')
    let candidates = map(
          \ ['or', 'fuzzy'],
          \ 'prefix . v:val',
          \)
  else
    let candidates = [
          \ '--prefix=',
          \ '-m', '--matcher=',
          \ '-n', '--no-highlight',
          \]
  endif
  return filter(candidates, 'v:val =~# ''^'' . a:arglead')
endfunction
