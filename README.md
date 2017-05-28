lista
==============================================================================

[![Join the chat at https://gitter.im/lista-nvim/Lobby](https://badges.gitter.im/lista-nvim/Lobby.svg)](https://gitter.im/lista-nvim/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Travis CI](https://img.shields.io/travis/lambdalisue/lista.nvim/master.svg?style=flat-square&label=Travis%20CI)](https://travis-ci.org/lambdalisue/lista.nvim)
[![Coverage Status](https://coveralls.io/repos/github/lambdalisue/lista.nvim/badge.svg?branch=master)](https://coveralls.io/github/lambdalisue/lista.nvim?branch=master)
[![Code Quality](https://img.shields.io/scrutinizer/g/lambdalisue/neovim-prompt/master.svg)](https://scrutinizer-ci.com/g/lambdalisue/lista.nvim/?branch=master)
![Version 1.0.0-dev](https://img.shields.io/badge/version-1.0.0--dev-yellow.svg?style=flat-square)
![Support Neovim 0.1.6 or above](https://img.shields.io/badge/support-Neovim%200.1.6%20or%20above-green.svg?style=flat-square)
![Support Vim 8.0 or above](https://img.shields.io/badge/support-Vim%208.0.0%20or%20above-yellowgreen.svg?style=flat-square)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE.md)
[![Doc](https://img.shields.io/badge/doc-%3Ah%20lista-orange.svg?style=flat-square)](doc/lista.txt)


Introductions
-------------------------------------------------------------------------------
[![asciicast](https://asciinema.org/a/87432.png)](https://asciinema.org/a/87432)

*lista* is a plugin to filter content lines and jump to where you want.

Install
-------------------------------------------------------------------------------

Install it with your favorite plugin manager.

```vim
Plug 'lambdalisue/lista.nvim'
```

Install [lambdalisue/vim-rplugin](https://github.com/lambdalisue/vim-rplugin) as well if you want to make it available on Vim 8.0.

Usage
-------------------------------------------------------------------------------
Execute `:Lista` or `:ListaCursorWord` and use the following builtin mappings

Key		| Description
--------------- | ---------------------------------------------------------------
`<CR>`		| Accept the input and jump to the selected line
`<C-J>`		| Accept the input and jump to the selected line
`<C-M>`		| Accept the input and jump to the selected line
`<Esc>`		| Cancel the input and return to the original line
`<C-[>`		| Cancel the input and return to the original line
`<BS>`		| Delete a character before the cursor
`<C-H>`		| Delete a character before the cursor
`<C-W>`		| Delete a word before the cursor
`<Del>`		| Delete a character under the cursor
`<Left>`	| Move a cursor left
`<S-Left>`	| Move a cursor one word left
`<C-Left>`	| Move a cursor one word left
`<Right>`	| Move a cursor right
`<S-Right>`	| Move a cursor one word left
`<C-Right>`	| Move a cursor one word left
`<Home>`	| Move a cursor to the head
`<End>`		| Move a cursor to the tail
`<Up>`		| Recall previous command-line from history that matches pattern in front of the cursor
`<Down>`	| Recall next command-line from history that matches pattern in front of the cursor
`<S-Up>`	| Recall previous command-line from history
`<S-Down>`	| Recall next command-line from history
`<C-P>`		| Recall previous command-line from history
`<C-N>`		| Recall next command-line from history
`<PageUp>`	| Select a previous line of the buffer
`<PageDown>`	| Select a next line of the buffer
`<S-Tab>`	| Select a previous line of the buffer
`<Tab>`		| Select a next line of the buffer
`<C-T>`		| Select a previous line of the buffer
`<C-G>`		| Select a next line of the buffer
`<C-R>`		| Insert the contents of a register or object under the cursor as if typed
`<C-V>`		| Start to input a control character
`<C-K>`		| Start to input a digraph
`<Insert>`	| Toggle insert/replace mode
`<C-^>`		| Switch a current matcher
`<C-6>`		| Switch a current matcher
`<C-_>`		| Switch ignorecase
`<C-->`		| Switch ignorecase

I personally assign the command to `#` and `g#` like:

```vim
nnoremap # :<C-u>Lista<CR>
nnoremap g# :<C-u>ListaCursorWord<CR>
```

If you prefer to use `<C-n>/<C-p>` to select candidate, use

```vim
let g:lista#custom_mappings = [
      \ ['<C-f>', '<Left>'],
      \ ['<C-b>', '<Right>'],
      \ ['<C-a>', '<Home>'],
      \ ['<C-e>', '<End>'],
      \ ['<C-d>', '<Del>'],
      \ ['<C-P>', '<lista:select_previous_candidate>', 'noremap'],
      \ ['<C-N>', '<lista:select_next_candidate>', 'noremap'],
      \ [';', 'pinkyless#stickyshift#enter(";")', 'expr noremap'],
      \]
```

- [lambdalisue/pinkyless.vim](https://github.com/lambdalisue/pinkyless.vim)


See also
-------------------------------------------------------------------------------
This plugin has partially forked from or inspired by the following plugins.

- [Shougo/unite.vim](https://github.com/Shougo/unite.vim)
- [osyo-manga/vim-hopping](https://github.com/osyo-manga/vim-hopping)
- [Shougo/denite.nvim](https://github.com/Shougo/denite.nvim)
- [lambdalisue/neovim-prompt](https://github.com/lambdalisue/neovim-prompt)
