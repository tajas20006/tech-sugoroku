from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from .model import SpaceType

DEFAULT_SPACE_MAP: dict[int, SpaceType] = {
    **{position: SpaceType.GAIN for position in (3, 12, 20, 28, 38, 48)},
    **{position: SpaceType.LOSS for position in (6, 18, 26, 42, 52)},
    **{position: SpaceType.QUIZ for position in (5, 8, 13, 17, 22, 27, 35, 39, 44, 50, 53, 57)},
    **{position: SpaceType.PAYMENT for position in (15, 30, 45, 55)},
    **{position: SpaceType.ITEM for position in (2, 10, 16, 24, 32, 37, 47, 51, 56)},
    25: SpaceType.SUMMIT,
    40: SpaceType.EXAM,
    54: SpaceType.EXAM,
    59: SpaceType.GOAL,
}
DEFAULT_PAYMENTS = {15: 100, 30: 180, 45: 280, 55: 400}


@dataclass(frozen=True)
class Board:
    final_position: int
    spaces: Mapping[int, SpaceType]
    payments: Mapping[int, int]

    def __post_init__(self) -> None:
        if self.final_position < 1:
            raise ValueError("A board needs a positive final position.")
        if any(position < 0 or position > self.final_position for position in self.spaces):
            raise ValueError("Every space must be on the board.")
        if any(position < 0 or position > self.final_position for position in self.payments):
            raise ValueError("Every payment must be on the board.")
        object.__setattr__(self, "spaces", MappingProxyType(dict(self.spaces)))
        object.__setattr__(self, "payments", MappingProxyType(dict(self.payments)))

    @classmethod
    def default(cls) -> Board:
        return cls(59, DEFAULT_SPACE_MAP, DEFAULT_PAYMENTS)

    def space_at(self, position: int) -> SpaceType:
        if not 0 <= position <= self.final_position:
            raise ValueError("Position is outside the board.")
        return self.spaces.get(position, SpaceType.NORMAL)

    def destination(self, start: int, roll: int) -> int:
        return min(self.final_position, start + roll)

    def crossed_payments(self, start: int, destination: int) -> tuple[tuple[int, int], ...]:
        return tuple(
            (position, cost)
            for position, cost in self.payments.items()
            if start < position <= destination
        )

    def previous_checkpoint(self, payment_position: int) -> int:
        return max((position for position in self.payments if position < payment_position), default=0)
