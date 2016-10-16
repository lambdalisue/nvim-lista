neovim-prompt
==========================
.. image:: https://img.shields.io/travis/lambdalisue/neovim-prompt/master.svg
    :target: http://travis-ci.org/lambdalisue/neovim-prompt
    :alt: Build status

.. image:: https://img.shields.io/scrutinizer/g/lambdalisue/neovim-prompt/master.svg
    :target: https://scrutinizer-ci.com/g/lambdalisue/neovim-prompt/inspections
    :alt: Code quality

.. image:: https://coveralls.io/repos/github/lambdalisue/neovim-prompt/badge.svg?branch=master
    :target: https://coveralls.io/github/lambdalisue/neovim-prompt?branch=master
    :alt: Coverage

.. image:: https://requires.io/github/lambdalisue/neovim-prompt/requirements.svg?branch=master
    :target: https://requires.io/github/lambdalisue/neovim-prompt/requirements
    :alt: Requirements

.. image:: https://img.shields.io/pypi/v/neovim-prompt.svg
    :target: https://pypi.python.org/pypi/neovim-prompt/
    :alt: Version

.. image:: https://img.shields.io/pypi/status/neovim-prompt.svg
    :target: https://pypi.python.org/pypi/neovim-prompt/
    :alt: Status

.. image:: https://img.shields.io/pypi/l/neovim-prompt.svg
    :target: https://pypi.python.org/pypi/neovim-prompt/
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/neovim-prompt.svg
    :target: https://pypi.python.org/pypi/neovim-prompt/
    :alt: Python versions

Introductions
-------------------------------------------------------------------------------

This is a library to produce a flexible custom command-line prompt for Neovim plugin which is written in Python 3.
The plugin will also support Vim 8 by using `lambdalisue/vim-rplugin <https://github.com/lambdalisue/vim-rplugin>`_.

**Note that this is under development and API might be changed in the future.**

The prompt provides the following features

- Returns an input text when accepted, otherwise returns ``None``
- Move cursor left and right
- Move cursor head, lead and tail (beginning, beginning of printable character, and end)
- Delete a character before the caret
- Delete a character under the caret
- Delete text after the caret
- Recall command-line history
- Recall command-line history matches a pattern
- Insert the content of a register
- Yank the text to a register
- Toggle insert/replace mode
- Custom key mappings
- Custom prefix string
- Custom events
    - ``on_init()`` - called before the loop
    - ``on_redraw()`` - called to redraw statusline/commandline etc.
    - ``on_update()`` - called to update contents
    - ``on_keypress()`` - called to handle keys
    - ``on_term()`` - called after the loop

Documentation
-------------
http://neovim-prompt.readthedocs.org/en/latest/

Installation
------------
Use pip_ like::

    $ pip install neovim-prompt

.. _pip:  https://pypi.python.org/pypi/pip
