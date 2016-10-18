from unittest.mock import MagicMock
import pytest
from neovim_prompt.keystroke import Keystroke
from neovim_prompt.prompt import Prompt, Status, InsertMode


def test_Prompt_constructor(nvim, context):
    prompt = Prompt(nvim, context)


def test_prompt_text(prompt):
    assert prompt.text == ''
    assert prompt.caret.locus == 0
    prompt.text = 'foo'
    assert prompt.text == 'foo'
    assert prompt.caret.locus == 3


def test_prompt_apply_custom_mappings_from_vim_variable(prompt):
    nvim = prompt.nvim
    nvim.vars = {
        'prompt#custom_mappings': [
            ('<C-H>', '<BS>'),
            ('<C-D>', '<DEL>'),
        ]
    }

    # Fail silently
    prompt.apply_custom_mappings_from_vim_variable('does_not_exist')
    assert Keystroke.parse(nvim, '<C-H>') not in prompt.keymap.registry
    assert Keystroke.parse(nvim, '<C-D>') not in prompt.keymap.registry

    prompt.apply_custom_mappings_from_vim_variable('prompt#custom_mappings')
    assert Keystroke.parse(nvim, '<C-H>') in prompt.keymap.registry
    assert Keystroke.parse(nvim, '<C-D>') in prompt.keymap.registry


def test_insert_text(prompt):
    # docstring
    pass


def test_replace_text(prompt):
    # docstring
    pass


def test_update_text(prompt):
    # docstring
    pass


def test_start(prompt):
    nvim = prompt.nvim
    nvim.error = Exception
    nvim.call = MagicMock()
    nvim.eval = MagicMock()
    nvim.command = MagicMock()
    prompt.keymap = MagicMock()
    prompt.keymap.harvest.side_effect = [
        Keystroke.parse(nvim, 'a'),
        Keystroke.parse(nvim, 'b'),
        Keystroke.parse(nvim, 'c'),
        Keystroke.parse(nvim, '<prompt:accept>'),
    ]
    assert prompt.start() == 'abc'

    prompt.keymap.harvest.side_effect = [
        Keystroke.parse(nvim, 'a'),
        Keystroke.parse(nvim, 'b'),
        Keystroke.parse(nvim, 'c'),
        Keystroke.parse(nvim, '<prompt:accept>'),
    ]
    assert prompt.start('default') == 'defaultabc'

    prompt.keymap.harvest.side_effect = [
        Keystroke.parse(nvim, 'a'),
        Keystroke.parse(nvim, 'b'),
        Keystroke.parse(nvim, 'c'),
        Keystroke.parse(nvim, '<prompt:cancel>'),
    ]
    assert prompt.start() is None


def test_start_exception(prompt):
    nvim = prompt.nvim
    nvim.error = Exception
    nvim.call = MagicMock()
    nvim.eval = MagicMock()
    nvim.command = MagicMock()
    prompt.keymap = MagicMock()
    prompt.keymap.harvest.side_effect = KeyboardInterrupt
    assert prompt.start() is None

    prompt.keymap.harvest.side_effect = Exception
    assert prompt.start() is None


def test_on_init(prompt):
    prompt.nvim.call = MagicMock()
    prompt.text = 'Hello Goodbye'
    assert prompt.on_init(None) == None
    prompt.nvim.call.assert_called_with('inputsave')
    assert prompt.text == 'Hello Goodbye'

    assert prompt.on_init('default') == None
    prompt.nvim.call.assert_called_with('inputsave')
    assert prompt.text == 'default'


def test_on_update(prompt):
    assert prompt.on_update(Status.accept) == Status.accept
    assert prompt.on_update(Status.cancel) == Status.cancel


def test_on_redraw(prompt):
    prompt.nvim.command = MagicMock()
    prompt.prefix = '# '
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert prompt.on_redraw() == None
    prompt.nvim.command.assert_called_with('|'.join([
        'redraw',
        'echohl Question',
        'echon "# "',
        'echohl None',
        'echon "Hello"',
        'echohl Cursor',
        'echon " "',
        'echohl None',
        'echon "Goodbye"',
    ]))


def on_keypress(prompt):
    nvim = prompt.nvim
    prompt.action = MagicMock()
    prompt.action.call.return_value = Status.accept
    prompt.update_text = MagicMock()

    assert prompt.on_keypress(Keystroke.parse(nvim, '<prompt:accept>')) \
        == Status.accept
    prompt.action.call.assert_called_with(prompt, 'prompt:accept')

    assert prompt.on_keypress(Keystroke.parse(nvim, 'a')) == None
    prompt.update_text.assert_called_with('a')


def test_on_term(prompt):
    prompt.nvim.call = MagicMock()
    assert prompt.on_term(Status.accept, 'Hello Goodbye') == None
    prompt.nvim.call.assert_called_with('inputrestore')
