lista
==============================================================================
[![Travis CI](https://img.shields.io/travis/lambdalisue/vim-lista/master.svg?style=flat-square&label=Travis%20CI)](https://travis-ci.org/lambdalisue/vim-lista)
[![AppVeyor](https://img.shields.io/appveyor/ci/lambdalisue/vim-lista/master.svg?style=flat-square&label=AppVeyor)](https://ci.appveyor.com/project/lambdalisue/vim-lista/branch/master)
![Version 1.0.0](https://img.shields.io/badge/version-1.0.0-yellow.svg?style=flat-square)
![Support Vim 7.4.2137 or above](https://img.shields.io/badge/support-Vim%207.4.2137%20or%20above-yellowgreen.svg?style=flat-square)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE.md)
[![Doc](https://img.shields.io/badge/doc-%3Ah%20lista-orange.svg?style=flat-square)](doc/lista.txt)


Introductions
-------------------------------------------------------------------------------
[![asciicast](https://asciinema.org/a/86747.png)](https://asciinema.org/a/86747)

**Note: This plugin is experimental**.

Install
-------------------------------------------------------------------------------

```vim
Plug 'lambdalisue/vim-lista'
```

Usage
-------------------------------------------------------------------------------
Execute `:Lista` and use `<C-n>/<C-p>` to select a candidate and hit `<CR>` to jump.

Key		| Description
--------------- | ---------------------------------------------------------------
`<CR>`		| Accept the input and return the value
`<C-M>`		| Accept the input and return the value
`<Esc>`		| Cancel the input and return 0
`<C-[>`		| Cancel the input and return 0
`<BS>`		| Remove a character before the cursor
`<C-H>`		| Remove a character before the cursor
`<Del>`		| Delete a character on the cursor
`<C-D>`		| Delete a character on the cursor
`<Left>`	| Shift a cursor left
`<C-F>`		| Shift a cursor left
`<Right>`	| Shift a cursor right
`<C-B>`		| Shift a cursor right
`<Home>`	| Shift a cursor to the beginning
`<C-A>`		| Shift a cursor to the beginning
`<End>`		| Shift a cursor to the end
`<C-E>`		| Shift a cursor to the end
`<Up>`		| Use previous input history
`<Down>`	| Use next input history
`<C-R>`		| Start a paste mode as like `i_CTRL-R`
`<C-n>`		| Select a next line
`<C-p>`		| Select a previous line
`<C-^>`		| Switch a matcher


See also
-------------------------------------------------------------------------------
This plugin has partially forked from or inspired by the following plugins.

- [Shougo/unite.vim](https://github.com/Shougo/unite.vim)
- [osyo-manga/vim-hopping](https://github.com/osyo-manga/vim-hopping)
- [Shougo/denite.nvim](https://github.com/Shougo/denite.nvim)
