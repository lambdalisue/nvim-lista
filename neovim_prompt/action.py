"""Action module."""
from typing import Callable, Optional, Dict, Tuple, Sequence    # noqa: F401
from .prompt import Prompt

ActionCallback = Callable[[Prompt], Optional[int]]
ActionRules = Sequence[Tuple[str, ActionCallback]]


class Action:
    """Action class which holds action callbacks.

    Attributes:
        registry (dict): An action dictionary.
    """

    __slots__ = ('registry',)

    def __init__(self) -> None:
        """Constructor."""
        self.registry = {}  # type: Dict[str, ActionCallback]

    def register(self, name: str, callback: ActionCallback=None) -> None:
        """Register action callback to a specified name.

        Args:
            name (str): An action name which follow {namespace}:{action name}
            callback (Callable): An action callback which take a
                ``prompt.prompt.Prompt`` instance and return None or int.
        """
        self.registry[name] = callback

    def register_from_rules(self, rules: ActionRules) -> None:
        """Register action callbacks from rules.

        Args:
            rules (Iterable): An iterator which returns rules. A rule is a
                (name, callback) tuple.
        """
        for rule in rules:
            self.register(*rule)

    def call(self, prompt: Prompt, name: str) -> Optional[int]:
        """Call a callback of specified action.

        Args:
            prompt (Prompt): A ``prompt.prompt.Prompt`` instance.
            name (str): An action name.

        Returns:
            None or int: None or int which represent the prompt status.
        """
        if name not in self.registry:
            raise AttributeError(
                'No action "%s" has registered.' % name
            )
        fn = self.registry[name]
        return fn(prompt)

    @classmethod
    def from_rules(cls, rules: ActionRules) -> 'Action':
        """Create a new action instance from rules.

        Args:
            rules (Iterable): An iterator which returns rules. A rule is a
                (name, callback) tuple.

        Returns:
            Action: An action instance.
        """
        action = cls()
        action.register_from_rules(rules)
        return action


# Default actions -------------------------------------------------------------
def _accept(prompt):
    from .prompt import STATUS_ACCEPT
    return STATUS_ACCEPT


def _cancel(prompt):
    from .prompt import STATUS_CANCEL
    return STATUS_CANCEL


def _toggle_insert_mode(prompt):
    from .prompt import MODE_INSERT, MODE_REPLACE
    if prompt.mode == MODE_INSERT:
        prompt.mode = MODE_REPLACE
    else:
        prompt.mode = MODE_INSERT


def _delete_char_before_caret(prompt):
    if prompt.caret.locus == 0:
        return
    prompt.context.text = ''.join([
        prompt.caret.get_backward_text()[:-1],
        prompt.caret.get_selected_text(),
        prompt.caret.get_forward_text(),
    ])
    prompt.caret.locus -= 1


def _delete_char_under_caret(prompt):
    prompt.context.text = ''.join([
        prompt.caret.get_backward_text(),
        prompt.caret.get_forward_text(),
    ])


def _delete_text_after_caret(prompt):
    prompt.context.text = prompt.caret.get_backward_text()
    prompt.caret.locus = prompt.caret.tail


def _move_caret_to_left(prompt):
    prompt.caret.locus -= 1


def _move_caret_to_right(prompt):
    prompt.caret.locus += 1


def _move_caret_to_head(prompt):
    prompt.caret.locus = prompt.caret.head


def _move_caret_to_lead(prompt):
    prompt.caret.locus = prompt.caret.lead


def _move_caret_to_tail(prompt):
    prompt.caret.locus = prompt.caret.tail


def _assign_previous_text(prompt):
    prompt.text = prompt.history.previous()


def _assign_next_text(prompt):
    prompt.text = prompt.history.next()


def _assign_previous_matched_text(prompt):
    prompt.text = prompt.history.previous_match()


def _assign_next_matched_text(prompt):
    prompt.text = prompt.history.next_match()


def _paste_from_register(prompt):
    prompt.nvim.command(r'echon "\""')
    reg = prompt.nvim.eval('nr2char(getchar())')
    val = prompt.nvim.call('getreg', reg)
    prompt.update_text(val)


def _paste_from_default_register(prompt):
    val = prompt.nvim.call('getreg', prompt.nvim.vvars['register'])
    prompt.update_text(val)


def _yank_to_register(prompt):
    prompt.nvim.command(r'echon "\""')
    reg = prompt.nvim.eval('nr2char(getchar())')
    prompt.nvim.call('setreg', reg, prompt.text)


def _yank_to_default_register(prompt):
    prompt.nvim.call('setreg', prompt.nvim.vvars['register'], prompt.text)


DEFAULT_ACTION = Action.from_rules([
    ('prompt:accept', _accept),
    ('prompt:cancel', _cancel),
    ('prompt:toggle_insert_mode', _toggle_insert_mode),
    ('prompt:delete_char_before_caret', _delete_char_before_caret),
    ('prompt:delete_char_under_caret', _delete_char_under_caret),
    ('prompt:delete_text_after_caret', _delete_text_after_caret),
    ('prompt:move_caret_to_left', _move_caret_to_left),
    ('prompt:move_caret_to_right', _move_caret_to_right),
    ('prompt:move_caret_to_head', _move_caret_to_head),
    ('prompt:move_caret_to_lead', _move_caret_to_lead),
    ('prompt:move_caret_to_tail', _move_caret_to_tail),
    ('prompt:assign_previous_text', _assign_previous_text),
    ('prompt:assign_next_text', _assign_next_text),
    ('prompt:assign_previous_matched_text', _assign_previous_matched_text),
    ('prompt:assign_next_matched_text', _assign_next_matched_text),
    ('prompt:paste_from_register', _paste_from_register),
    ('prompt:paste_from_default_register', _paste_from_default_register),
    ('prompt:yank_to_register', _yank_to_register),
    ('prompt:yank_to_default_register', _yank_to_default_register),
])
