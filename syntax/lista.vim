if exists('b:current_syntax')
  finish
endif
let b:current_syntax = 'lista'

highlight default link ListaStatuslineModeInsert  Define
highlight default link ListaStatuslineModeReplace Todo
highlight default link ListaStatuslineFile        Comment
highlight default link ListaStatuslineMiddle      None
highlight default link ListaStatuslineMatcher     Statement
highlight default link ListaStatuslineIndicator   Tag

syntax match Comment /.*/ contains=Title
