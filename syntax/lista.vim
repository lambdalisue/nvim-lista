if exists('b:current_syntax')
  finish
endif
let b:current_syntax = 'lista'

" TODO
" Better to not use highlight definition of external plugin
highlight default link ListaStatuslineModeInsert  LightLineLeft_insert_0 
highlight default link ListaStatuslineModeReplace LightLineLeft_replace_0 
highlight default link ListaStatuslineFile        LightLineLeft_active_1 
highlight default link ListaStatuslineMiddle      LightLineMiddle_active
highlight default link ListaStatuslineMatcher     LightLineRight_active_1 
highlight default link ListaStatuslineIndicator   LightLineRight_active_0 

syntax match Comment /.*/ contains=Title
