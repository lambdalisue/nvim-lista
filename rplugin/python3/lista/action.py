def _select_next_candidate(lista):
    line, col = lista.nvim.current.window.cursor
    lista.nvim.call('cursor', [line + 1, col])


def _select_previous_candidate(lista):
    line, col = lista.nvim.current.window.cursor
    lista.nvim.call('cursor', [line - 1, col])


def _switch_matcher(lista):
    lista.switch_matcher()


def _switch_case(lista):
    lista.switch_case()


DEFAULT_ACTION_RULES = [
    ('lista:select_next_candidate', _select_next_candidate),
    ('lista:select_previous_candidate', _select_previous_candidate),
    ('lista:switch_matcher', _switch_matcher),
    ('lista:switch_case', _switch_case),
]


DEFAULT_ACTION_KEYMAP = [
    ('<PageUp>', '<lista:select_previous_candidate>', True),
    ('<PageDown>', '<lista:select_next_candidate>', True),
    ('<C-^>', '<lista:switch_matcher>', True),
    ('<C-I>', '<lista:switch_case>', True),
]
