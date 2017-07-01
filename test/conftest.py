import os
import sys
import pytest
from unittest.mock import MagicMock

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'rplugin/python3'))


@pytest.fixture
def nvim():
    nvim = MagicMock(autospec='neovim.Nvim')
    nvim.vars = {}
    nvim.options = {
        'encoding': 'utf-8',
    }
    return nvim


@pytest.fixture
def lista(nvim):
    from lista.lista import Lista, Condition
    return Lista(nvim, Condition(
        text='',
        caret_locus=0,
        selected_index=0,
        matcher_index=0,
        case_index=0,
    ))
