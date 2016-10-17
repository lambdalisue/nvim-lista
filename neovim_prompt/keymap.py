"""Keymap."""
from .keystroke import Keystroke, KeystrokeExpr
from typing import cast, Iterator, Optional, Sequence, Tuple, Union
from neovim import Nvim

Rule = Union[
    Tuple[KeystrokeExpr, KeystrokeExpr],
    Tuple[KeystrokeExpr, KeystrokeExpr, bool],
]


class Keymap:
    """Keymap."""

    __slots__ = ('registry',)

    def __init__(self) -> None:
        """Constructor."""
        self.registry = {}  # type: Dict[Keystroke, tuple]

    def register(self,
                 lhs: Keystroke,
                 rhs: Keystroke,
                 noremap: bool=False) -> None:
        """Register."""
        self.registry[lhs] = (lhs, rhs, noremap)

    def register_from_rule(self, nvim: Nvim, rule: Rule) -> None:
        """Register."""
        if len(rule) == 2:
            lhs, rhs = cast('Tuple[KeystrokeExpr, KeystrokeExpr]', rule)
            noremap = False
        else:
            lhs, rhs, noremap = cast(
                'Tuple[KeystrokeExpr, KeystrokeExpr, bool]',
                rule
            )
        lhs = Keystroke.parse(nvim, lhs)
        rhs = Keystroke.parse(nvim, rhs)
        self.register(lhs, rhs, noremap)

    def register_from_rules(self,
                            nvim: Nvim,
                            rules: Sequence[Rule]) -> None:
        """Register keymaps from rule tuple."""
        for rule in rules:
            self.register_from_rule(nvim, rule)

    def filter(self, lhs: Keystroke) -> Iterator[Keystroke]:
        """Filter."""
        candidates = (
            self.registry[k]
            for k in self.registry.keys() if k.startswith(lhs)
        )
        return cast('Iterator[Keystroke]', sorted(candidates))

    def resolve(self, lhs: Keystroke) -> Optional[Keystroke]:
        """Resolve."""
        candidates = list(self.filter(lhs))
        n = len(candidates)
        if n == 0:
            return lhs
        elif n == 1:
            _lhs, rhs, noremap = candidates[0]
            if lhs == _lhs:
                return rhs if noremap else self.resolve(rhs)
        return None

    @classmethod
    def from_rules(cls, nvim: Nvim, rules: Sequence[Rule]) -> 'Keymap':
        """Create keymap from rule."""
        keymap = cls()
        keymap.register_from_rules(nvim, rules)
        return keymap


DEFAULT_KEYMAP_RULES = (
    ('<CR>', '<prompt:accept>', True),
    ('<ESC>', '<prompt:cancel>', True),
    ('<INSERT>', '<prompt:toggle_insert_mode>', True),
    ('<BS>', '<prompt:delete_char_before_caret>', True),
    ('<DEL>', '<prompt:delete_char_under_caret>', True),
    ('<Left>', '<prompt:move_caret_to_left>', True),
    ('<Right>', '<prompt:move_caret_to_right>', True),
    ('<Home>', '<prompt:move_caret_to_head>', True),
    ('<End>', '<prompt:move_caret_to_tail>', True),
    ('<C-P>', '<prompt:assign_previous_text>', True),
    ('<C-N>', '<prompt:assign_next_text>', True),
    ('<Up>', '<prompt:assign_previous_matched_text>', True),
    ('<Down>', '<prompt:assign_next_matched_text>', True),
    ('<C-R>', '<prompt:paste_from_register>', True),
)
