import pytest

from neovim_prompt.action import Action, DEFAULT_ACTION


def test_Action():
    action = Action()


def test_Action_register():
    callback = lambda prompt: None
    action = Action()
    action.register('prompt:test', callback)
    assert 'prompt:test' in action.registry
    assert action.registry['prompt:test'] == callback


def test_Action_register_from_rules():
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


def test_Action_call(prompt):
    prompt.text = 'foo'
    callback = lambda prompt: prompt.text
    action = Action()
    action.register('prompt:test', callback)
    assert action.call(prompt, 'prompt:test') == 'foo'


def test_Action_cls_from_rules():
    callback = lambda prompt: None
    action = Action.from_rules([
        ('prompt:test1', callback),
        ('prompt:test2', callback),
    ])
    assert 'prompt:test1' in action.registry
    assert 'prompt:test2' in action.registry
    assert action.registry['prompt:test1'] == callback
    assert action.registry['prompt:test2'] == callback
