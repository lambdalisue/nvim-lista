"""Keymap."""
import time
from operator import itemgetter
from datetime import datetime, timedelta
from typing import cast, Iterator, Optional, Sequence, Tuple, Union
from neovim import Nvim
from .key import Key, KeyCode
from .keystroke import Keystroke, KeystrokeExpr
from .util import getchar

Rule = Union[
    Tuple[KeystrokeExpr, KeystrokeExpr],
    Tuple[KeystrokeExpr, KeystrokeExpr, bool],
    Tuple[KeystrokeExpr, KeystrokeExpr, bool, bool],
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
                 noremap: bool=False,
                 nowait: bool=False) -> None:
        """Register."""
        self.registry[lhs] = (lhs, rhs, noremap, nowait)

    def register_from_rule(self, nvim: Nvim, rule: Rule) -> None:
        """Register."""
        if len(rule) == 2:
            lhs, rhs = cast('Tuple[KeystrokeExpr, KeystrokeExpr]', rule)
            noremap = False
            nowait = False
        elif len(rule) == 3:
            lhs, rhs, noremap = cast(
                'Tuple[KeystrokeExpr, KeystrokeExpr, bool]',
                rule
            )
            nowait = False
        else:
            lhs, rhs, noremap, nowait = cast(
                'Tuple[KeystrokeExpr, KeystrokeExpr, bool, bool]',
                rule
            )
        lhs = Keystroke.parse(nvim, lhs)
        rhs = Keystroke.parse(nvim, rhs)
        self.register(lhs, rhs, noremap, nowait)

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
        return cast(
            'Iterator[Keystroke]',
            sorted(candidates, key=itemgetter(0)),
        )

    def resolve(self,
                lhs: Keystroke,
                nowait: bool=False) -> Optional[Keystroke]:
        """Resolve."""
        candidates = list(self.filter(lhs))
        n = len(candidates)
        if n == 0:
            return lhs
        elif n == 1:
            _lhs, rhs, noremap, _nowait = candidates[0]
            if lhs == _lhs:
                return rhs if noremap else self.resolve(rhs, nowait=True)
        elif nowait:
            # Use the first matched candidate if lhs is equal
            _lhs, rhs, noremap, _nowait = candidates[0]
            if lhs == _lhs:
                return rhs if noremap else self.resolve(rhs, nowait=True)
        else:
            # Check if the current first candidate is defined as nowait
            _lhs, rhs, noremap, nowait = candidates[0]
            if nowait and lhs == _lhs:
                return rhs if noremap else self.resolve(rhs, nowait=True)
        return None

    def harvest(self, nvim: Nvim) -> Keystroke:
        if nvim.options['timeout']:
            timeoutlen = timedelta(
                milliseconds=int(nvim.options['timeoutlen'])
            )
        else:
            timeoutlen = None

        previous = None
        while True:
            code = _getcode(nvim, datetime.now() + timeoutlen)
            if code is None and previous is None:
                # timeout without input
                continue
            elif code is None:
                # timeout
                return self.resolve(previous, nowait=True) or previous
            previous = Keystroke((previous or ()) + (Key.parse(nvim, code),))
            keystroke = self.resolve(previous, nowait=False)
            if keystroke:
                # resolved
                return keystroke

    @classmethod
    def from_rules(cls, nvim: Nvim, rules: Sequence[Rule]) -> 'Keymap':
        """Create keymap from rule."""
        keymap = cls()
        keymap.register_from_rules(nvim, rules)
        return keymap


def _getcode(nvim: 'Nvim', timeout: Optional[datetime]) -> Optional[KeyCode]:
    while not timeout or timeout > datetime.now():
        code = getchar(nvim, False)
        if code != 0:
            return code
        time.sleep(0.01)
    return None


DEFAULT_KEYMAP_RULES = (
    ('<CR>', '<prompt:accept>', True),
    ('<ESC>', '<prompt:cancel>', True),
    ('<INSERT>', '<prompt:toggle_insert_mode>', True),
    ('<BS>', '<prompt:delete_char_before_caret>', True),
    ('<DEL>', '<prompt:delete_char_under_caret>', True),
    ('<C-U>', '<prompt:delete_entire_text>', True),
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
