try:
    import vim as nvim
except ImportError:
    # For unittest
    from unittest.mock import MagicMock
    nvim = MagicMock()
    nvim.options = {
        'encoding': 'utf-8',
    }
    nvim.vars = {
        'mapleader': '\\',
        'maplocalleader': ',',
    }
