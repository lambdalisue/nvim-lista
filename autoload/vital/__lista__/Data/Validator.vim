function! s:_vital_loaded(V) abort
  let s:List = a:V.import('Data.List')
  let s:t_number = type(0)
  let s:typenames = {
        \ '0': 'Number',
        \ '1': 'String',
        \ '2': 'Funcref',
        \ '3': 'List',
        \ '4': 'Dictionary',
        \ '5': 'Float',
        \ '6': 'Boolean',
        \ '7': 'None',
        \ '8': 'Job',
        \ '9': 'Channel',
        \}
endfunction

function! s:_vital_depends() abort
  return ['Data.List']
endfunction


function! s:new(schemes) abort
  let rule = {}
  let rule.schemes = {}
  let rule.defaults = {}
  for [name, scheme] in items(a:schemes)
    if type(scheme) == s:t_number
      let rule.schemes[name] = { 'type': scheme, 'xor': [], 'optional': 0 }
    else
      let rule.schemes[name] = extend({
            \ 'xor': [],
            \ 'optional': has_key(scheme, 'default'),
            \}, scheme)
      if has_key(scheme, 'default')
        let rule.defaults[name] = scheme.default
      endif
    endif
  endfor
  return extend(rule, s:rule)
endfunction


" Rule -----------------------------------------------------------------------
let s:rule = {}

function! s:rule.validate(options) abort
  let fieldnames = keys(a:options)
  for [name, scheme] in items(self.schemes)
    if s:List.has_common_items(fieldnames, scheme.xor)
      throw printf(
            \ 'vital: Data.Validator: %s conflicts with %s',
            \ a:name,
            \ string(s:List.intersect(fieldnames, scheme.xor))
            \)
    endif
    call self.validate_scheme(a:options, name, scheme)
  endfor
  return extend(a:options, self.defaults, 'keep')
endfunction

function! s:rule.validate_scheme(options, name, scheme) abort
  if !has_key(a:options, a:name)
    if !a:scheme.optional
      throw printf(
            \ 'vital: Data.Validator: A required field "%s" is missing',
            \ a:name,
            \)
    endif
    " Skip
    return
  endif
  if has_key(a:scheme, 'type') && type(a:options[a:name]) != a:scheme.type
    throw printf(
          \ 'vital: Data.Validator: %s requires to be %s but %s has specified',
          \ a:name,
          \ get(s:typenames, a:scheme.type, 'Unknwon'),
          \ get(s:typenames, type(a:options[a:name]), 'Unknown'),
          \)
  endif
endfunction
