from unittest.mock import MagicMock
import pytest

from neovim_prompt.action import Action, DEFAULT_ACTION


@pytest.fixture
def action():
    return DEFAULT_ACTION


def test_Action():
    action = Action()


def test_action_register():
    callback = lambda prompt: None
    action = Action()
    action.register('prompt:test', callback)
    assert 'prompt:test' in action.registry
    assert action.registry['prompt:test'] == callback


def test_action_register_from_rules():
    callback = lambda prompt: None
    action = Action()
    action.register_from_rules([
        ('prompt:test1', callback),
        ('prompt:test2', callback),
    ])
    assert 'prompt:test1' in action.registry
    assert 'prompt:test2' in action.registry
    assert action.registry['prompt:test1'] == callback
    assert action.registry['prompt:test2'] == callback


def test_action_call(prompt):
    prompt.text = 'foo'
    callback = lambda prompt: prompt.text
    action = Action()
    action.register('prompt:test', callback)
    assert action.call(prompt, 'prompt:test') == 'foo'

    with pytest.raises(AttributeError):
        action.call(prompt, 'prompt:not_a_registered_action')


def test_Action_from_rules():
    callback = lambda prompt: None
    action = Action.from_rules([
        ('prompt:test1', callback),
        ('prompt:test2', callback),
    ])
    assert 'prompt:test1' in action.registry
    assert 'prompt:test2' in action.registry
    assert action.registry['prompt:test1'] == callback
    assert action.registry['prompt:test2'] == callback


def test_accept(prompt, action):
    from neovim_prompt.prompt import Status
    assert action.call(prompt, 'prompt:accept') == Status.accept


def test_cancel(prompt, action):
    from neovim_prompt.prompt import Status
    assert action.call(prompt, 'prompt:cancel') == Status.cancel


def test_toggle_insert_mode(prompt, action):
    from neovim_prompt.prompt import InsertMode
    prompt.insert_mode = InsertMode.insert
    assert action.call(prompt, 'prompt:toggle_insert_mode') is None
    assert prompt.insert_mode == InsertMode.replace
    assert action.call(prompt, 'prompt:toggle_insert_mode') is None
    assert prompt.insert_mode == InsertMode.insert


def test_delete_char_before_caret(prompt, action):
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:delete_char_before_caret') is None
    assert prompt.text == 'Hell Goodbye'
    assert prompt.caret.locus == 4

    assert action.call(prompt, 'prompt:delete_char_before_caret') is None
    assert action.call(prompt, 'prompt:delete_char_before_caret') is None
    assert action.call(prompt, 'prompt:delete_char_before_caret') is None
    assert action.call(prompt, 'prompt:delete_char_before_caret') is None
    assert prompt.text == ' Goodbye'
    assert prompt.caret.locus == 0

    assert action.call(prompt, 'prompt:delete_char_before_caret') is None
    assert prompt.text == ' Goodbye'
    assert prompt.caret.locus == 0


def test_delete_char_under_caret(prompt, action):
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:delete_char_under_caret') is None
    assert prompt.text == 'HelloGoodbye'
    assert prompt.caret.locus == 5


def test_delete_text_after_caret(prompt, action):
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:delete_text_after_caret') is None
    assert prompt.text == 'Hello'
    assert prompt.caret.locus == 5


def test_delete_entire_text(prompt, action):
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:delete_entire_text') is None
    assert prompt.text == ''
    assert prompt.caret.locus == 0


def test_move_caret_to_left(prompt, action):
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:move_caret_to_left') is None
    assert prompt.text == 'Hello Goodbye'
    assert prompt.caret.locus == 4

    assert action.call(prompt, 'prompt:move_caret_to_left') is None
    assert action.call(prompt, 'prompt:move_caret_to_left') is None
    assert action.call(prompt, 'prompt:move_caret_to_left') is None
    assert action.call(prompt, 'prompt:move_caret_to_left') is None
    assert prompt.caret.locus == 0
    assert action.call(prompt, 'prompt:move_caret_to_left') is None
    assert prompt.caret.locus == 0


def test_move_caret_to_right(prompt, action):
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:move_caret_to_right') is None
    assert prompt.text == 'Hello Goodbye'
    assert prompt.caret.locus == 6

    assert action.call(prompt, 'prompt:move_caret_to_right') is None
    assert action.call(prompt, 'prompt:move_caret_to_right') is None
    assert action.call(prompt, 'prompt:move_caret_to_right') is None
    assert action.call(prompt, 'prompt:move_caret_to_right') is None
    assert action.call(prompt, 'prompt:move_caret_to_right') is None
    assert action.call(prompt, 'prompt:move_caret_to_right') is None
    assert action.call(prompt, 'prompt:move_caret_to_right') is None
    assert prompt.caret.locus == 13
    assert action.call(prompt, 'prompt:move_caret_to_right') is None
    assert prompt.caret.locus == 13


def test_move_caret_to_head(prompt, action):
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:move_caret_to_head') is None
    assert prompt.text == 'Hello Goodbye'
    assert prompt.caret.locus == 0
    assert action.call(prompt, 'prompt:move_caret_to_head') is None
    assert prompt.caret.locus == 0


def test_move_caret_to_lead(prompt, action):
    prompt.text = '    Hello Goodbye'
    prompt.caret.locus = 9
    assert action.call(prompt, 'prompt:move_caret_to_lead') is None
    assert prompt.text == '    Hello Goodbye'
    assert prompt.caret.locus == 4
    assert action.call(prompt, 'prompt:move_caret_to_lead') is None
    assert prompt.caret.locus == 4


def test_move_caret_to_tail(prompt, action):
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:move_caret_to_tail') is None
    assert prompt.text == 'Hello Goodbye'
    assert prompt.caret.locus == 13
    assert action.call(prompt, 'prompt:move_caret_to_tail') is None
    assert prompt.caret.locus == 13


def test_assign_previous_text(prompt, action):
    prompt.history = MagicMock()
    prompt.history.previous.side_effect = [
        'foo', 'bar', 'hoge',
    ]
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:assign_previous_text') is None
    assert prompt.text == 'foo'
    assert prompt.caret.locus == len(prompt.text)

    assert action.call(prompt, 'prompt:assign_previous_text') is None
    assert prompt.text == 'bar'
    assert prompt.caret.locus == len(prompt.text)

    assert action.call(prompt, 'prompt:assign_previous_text') is None
    assert prompt.text == 'hoge'
    assert prompt.caret.locus == len(prompt.text)


def test_assign_next_text(prompt, action):
    prompt.history = MagicMock()
    prompt.history.next.side_effect = [
        'foo', 'bar', 'hoge',
    ]
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:assign_next_text') is None
    assert prompt.text == 'foo'
    assert prompt.caret.locus == len(prompt.text)

    assert action.call(prompt, 'prompt:assign_next_text') is None
    assert prompt.text == 'bar'
    assert prompt.caret.locus == len(prompt.text)

    assert action.call(prompt, 'prompt:assign_next_text') is None
    assert prompt.text == 'hoge'
    assert prompt.caret.locus == len(prompt.text)


def test_assign_previous_matched_text(prompt, action):
    prompt.history = MagicMock()
    prompt.history.previous_match.side_effect = [
        'foo', 'bar', 'hoge',
    ]
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:assign_previous_matched_text') is None
    assert prompt.text == 'foo'
    assert prompt.caret.locus == len(prompt.text)

    assert action.call(prompt, 'prompt:assign_previous_matched_text') is None
    assert prompt.text == 'bar'
    assert prompt.caret.locus == len(prompt.text)

    assert action.call(prompt, 'prompt:assign_previous_matched_text') is None
    assert prompt.text == 'hoge'
    assert prompt.caret.locus == len(prompt.text)


def test_assign_next_matched_text(prompt, action):
    prompt.history = MagicMock()
    prompt.history.next_match.side_effect = [
        'foo', 'bar', 'hoge',
    ]
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:assign_next_matched_text') is None
    assert prompt.text == 'foo'
    assert prompt.caret.locus == len(prompt.text)

    assert action.call(prompt, 'prompt:assign_next_matched_text') is None
    assert prompt.text == 'bar'
    assert prompt.caret.locus == len(prompt.text)

    assert action.call(prompt, 'prompt:assign_next_matched_text') is None
    assert prompt.text == 'hoge'
    assert prompt.caret.locus == len(prompt.text)


def test_paste_from_register(prompt, action):
    prompt.nvim.eval = MagicMock()
    prompt.nvim.call = MagicMock()
    prompt.nvim.command = MagicMock()
    prompt.nvim.eval.return_value = 'a'
    prompt.nvim.call.side_effect = lambda fname, reg: '<%s>' % reg
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:paste_from_register') is None
    assert prompt.text == 'Hello<a> Goodbye'
    assert prompt.caret.locus == 8


def test_paste_from_default_register(prompt, action):
    prompt.nvim.vvars = {
        'register': '*',
    }
    prompt.nvim.call = MagicMock()
    prompt.nvim.command = MagicMock()
    prompt.nvim.call.side_effect = lambda fname, reg: '<%s>' % reg
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:paste_from_default_register') is None
    assert prompt.text == 'Hello<*> Goodbye'
    assert prompt.caret.locus == 8


def test_yank_to_register(prompt, action):
    prompt.nvim.eval = MagicMock()
    prompt.nvim.call = MagicMock()
    prompt.nvim.command = MagicMock()
    prompt.nvim.eval.return_value = 'a'
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:yank_to_register') is None
    assert prompt.text == 'Hello Goodbye'
    assert prompt.caret.locus == 5
    prompt.nvim.call.assert_called_with('setreg', 'a', 'Hello Goodbye')


def test_yank_to_default_register(prompt, action):
    prompt.nvim.vvars = {
        'register': '*',
    }
    prompt.nvim.call = MagicMock()
    prompt.nvim.command = MagicMock()
    prompt.text = 'Hello Goodbye'
    prompt.caret.locus = 5
    assert action.call(prompt, 'prompt:yank_to_default_register') is None
    assert prompt.text == 'Hello Goodbye'
    assert prompt.caret.locus == 5
    prompt.nvim.call.assert_called_with('setreg', '*', 'Hello Goodbye')
