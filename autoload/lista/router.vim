function! lista#router#command(bang, range, args) abort
  return lista#start()
endfunction

function! lista#router#complete(arglead, cmdline, cursorpos) abort
  return []
endfunction
