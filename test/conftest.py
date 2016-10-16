import os
import sys
import pytest
from unittest.mock import MagicMock

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)


@pytest.fixture
def context():
    Context = MagicMock(spec='neovim_prompt.context.Context')
    return Context()


@pytest.fixture
def prompt(context):
    Prompt = MagicMock(spec='neovim_prompt.prompt.Prompt')
    return Prompt(context)



