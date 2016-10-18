from unittest.mock import MagicMock
import pytest
from neovim_prompt.action import Action
from lista.action import DEFAULT_ACTION_RULES, DEFAULT_ACTION_KEYMAP


@pytest.fixture
def action():
    action = Action.from_rules(DEFAULT_ACTION_RULES)
    return action


def test_select_next_candidate(lista, action):
    lista.nvim = MagicMock()
    lista.nvim.current.window.cursor = [1, 1]
    action.call(lista, 'lista:select_next_candidate')
    lista.nvim.call.assert_called_with('cursor', [2, 1])


def test_select_previous_candidate(lista, action):
    lista.nvim = MagicMock()
    lista.nvim.current.window.cursor = [2, 1]
    action.call(lista, 'lista:select_previous_candidate')
    lista.nvim.call.assert_called_with('cursor', [1, 1])


def test_switch_matcher(lista, action):
    lista.switch_matcher = MagicMock()
    action.call(lista, 'lista:switch_matcher')
    lista.switch_matcher.assert_called_with()


def test_switch_case(lista, action):
    lista.switch_case = MagicMock()
    action.call(lista, 'lista:switch_case')
    lista.switch_case.assert_called_with()
