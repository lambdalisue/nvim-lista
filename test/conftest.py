import os
import sys
import pytest
from unittest.mock import MagicMock

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'rplugin/python3'))


@pytest.fixture
def nvim():
    nvim = MagicMock(spec='neovim.Nvim')
    nvim.vars = {}
    nvim.options = {
        'encoding': 'utf-8',
    }
    return nvim


@pytest.fixture
def context():
    from lista.context import Context
    return Context()


@pytest.fixture
def lista(nvim, context):
    from lista.lista import Lista
    return Lista(nvim, context)
