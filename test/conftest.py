import os
import sys
import pytest
from unittest.mock import MagicMock

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)


@pytest.fixture
def nvim():
    nvim = MagicMock(spec='neovim.Nvim')
    nvim.options = {
        'encoding': 'utf-8',
    }
    return nvim


@pytest.fixture
def context():
    from neovim_prompt.context import Context
    return Context()


@pytest.fixture
def prompt(nvim, context):
    from neovim_prompt.prompt import Prompt
    return Prompt(nvim, context)
