lista
==============================================================================
[![Travis CI](https://img.shields.io/travis/lambdalisue/vim-lista/master.svg?style=flat-square&label=Travis%20CI)](https://travis-ci.org/lambdalisue/vim-lista)
[![AppVeyor](https://img.shields.io/appveyor/ci/lambdalisue/vim-lista/master.svg?style=flat-square&label=AppVeyor)](https://ci.appveyor.com/project/lambdalisue/vim-lista/branch/master)
![Version 1.0.0](https://img.shields.io/badge/version-1.0.0-yellow.svg?style=flat-square)
![Support Vim 8.0 or above](https://img.shields.io/badge/support-Vim%207.4.2137%20or%20above-yellowgreen.svg?style=flat-square)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE.md)
[![Doc](https://img.shields.io/badge/doc-%3Ah%20lista-orange.svg?style=flat-square)](doc/lista.txt)


Introductions
-------------------------------------------------------------------------------
[![asciicast](https://asciinema.org/a/87432.png)](https://asciinema.org/a/87432)

**Note: This plugin is experimental**.

Install
-------------------------------------------------------------------------------

```vim
Plug 'lambdalisue/vim-lista'
```

Usage
-------------------------------------------------------------------------------
Execute `:Lista` or `:ListaCursorWord` and use the following builtin mappings

Key		| Description
--------------- | ---------------------------------------------------------------
`<CR>`		| Accept the input and return the value
`<C-M>`		| Accept the input and return the value
`<Esc>`		| Cancel the input and return 0
`<C-[>`		| Cancel the input and return 0
`<BS>`		| Delete a character before the cursor
`<C-H>`		| Delete a character before the cursor
`<Del>`		| Delete a character under the cursor
`<C-D>`		| Delete a character under the cursor
`<Left>`	| Move a cursor left
`<Right>`	| Move a cursor right
`<Home>`	| Move a cursor to the head
`<End>`		| Move a cursor to the tail
`<Up>`		| Recall previous command-line from history that matches pattern in front of the cursor
`<Down>`	| Recall next command-line from history that matches pattern in front of the cursor
`<C-P>`		| Recall previous command-line from history
`<C-N>`		| Recall next command-line from history
`<PageUp>`	| Select a previous line of the buffer
`<PageDown>`	| Select a next line of the buffer
`<C-T>`		| Select a previous line of the buffer
`<C-G>`		| Select a next line of the buffer
`<C-R>`		| Insert the contents of a register or object under the cursor as if typed
`<C-^>`		| Switch a current matcher
`<Insert>`	| Toggle insert/replace mode

And the following Emacs-like custom mappings which is defined by `g:lista#custom_mapping`

Key		| Description
--------------- | ---------------------------------------------------------------
`<C-D>`		| Delete character under the cursor
`<C-F>`		| Move a cursor left
`<C-B>`		| Move a cursor right
`<C-A>`		| Move a cursor to the head
`<C-E>`		| Shift a cursor to the end

I personally assign the command to `#` and `g#` like:

```vim
nnoremap # :<C-u>Lista<CR>
nnoremap g# :<C-u>ListaCursorWord<CR>
```

If you prefer to use `<C-n>/<C-p>` to select candidate like denite.nvim, use

```vim
let g:lista#custom_mapping = [
      \ ["\<C-D>", "\<Del>"],
      \ ["\<C-A>", "\<Home>"],
      \ ["\<C-E>", "\<End>"],
      \ ["\<C-F>", "\<Left>"],
      \ ["\<C-B>", "\<Right>"],
      \ ["\<C-P>", "\<C-T>", 1],  " 1 means 'noremap'
      \ ["\<C-N>", "\<C-G>", 1],
      \]
```

Note that multi-byte characters are not supported only in GVim.


ToDo
-------------------------------------------------------------------------------

- [ ] Multikeys mapping (e.g. `<C-k>ab`)
- [ ] Digraphs (`<C-k> <char1> <char2>`)
- [ ] Translate `cmap`

See also
-------------------------------------------------------------------------------
This plugin has partially forked from or inspired by the following plugins.

- [Shougo/unite.vim](https://github.com/Shougo/unite.vim)
- [osyo-manga/vim-hopping](https://github.com/osyo-manga/vim-hopping)
- [Shougo/denite.nvim](https://github.com/Shougo/denite.nvim)
