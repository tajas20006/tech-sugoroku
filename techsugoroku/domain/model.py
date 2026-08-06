from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Self


class SpaceType(str, Enum):
    NORMAL = "normal"
    GAIN = "gain"
    LOSS = "loss"
    QUIZ = "quiz"
    PAYMENT = "payment"
    ITEM = "item"
    SUMMIT = "summit"
    EXAM = "exam"
    GOAL = "goal"


class Item(str, Enum):
    WAF = "WAF"
    AUTO_SCALING = "Auto Scaling"
    AWS_BACKUP = "AWS Backup"
    COST_EXPLORER = "Cost Explorer"
    CLOUDFRONT = "CloudFront"
    RESERVED_INSTANCE = "リザーブドインスタンス"
    WELL_ARCHITECTED = "Well-Architected Review"
    SUPPORT_PLAN = "AWS サポートプラン"
    TRANSIT_GATEWAY = "Transit Gateway"
    LAMBDA = "Lambda"
    DDOS_ATTACK = "DDoS 攻撃"
    NAT_GATEWAY = "不要な NAT Gateway"
    CLOUDWATCH_LOGS = "無限 CloudWatch Logs"
    REGION_RUMOR = "リージョン障害のうわさ"
    MULTI_AZ = "Multi-AZ"


class Inventory(list[Item]):
    """List-compatible inventory that owns the three-item invariant."""

    MAX_ITEMS = 3

    def __init__(self, items: list[Item] | None = None) -> None:
        values = items or []
        self._ensure_capacity(len(values))
        super().__init__(values)

    def append(self, item: Item) -> None:
        self._ensure_capacity(len(self) + 1)
        super().append(item)

    def extend(self, items: list[Item]) -> None:
        self._ensure_capacity(len(self) + len(items))
        super().extend(items)

    def insert(self, index: int, item: Item) -> None:
        self._ensure_capacity(len(self) + 1)
        super().insert(index, item)

    def __iadd__(self, items: list[Item]) -> Self:
        self.extend(items)
        return self

    def __imul__(self, multiplier: int) -> Self:
        self._ensure_capacity(len(self) * max(0, multiplier))
        super().__imul__(multiplier)
        return self

    def __setitem__(self, key: int | slice, value: Item | list[Item]) -> None:
        if isinstance(key, slice):
            updated = list(self)
            updated[key] = value  # type: ignore[index,assignment]
            self._ensure_capacity(len(updated))
        super().__setitem__(key, value)  # type: ignore[index,assignment]

    @classmethod
    def _ensure_capacity(cls, size: int) -> None:
        if size > cls.MAX_ITEMS:
            raise ValueError("A player cannot hold more than three items.")


@dataclass(frozen=True)
class Question:
    prompt: str
    choices: tuple[str, str, str, str]
    answer_index: int
    explanation: str
    is_exam: bool = False

    def __post_init__(self) -> None:
        if len(self.choices) != 4:
            raise ValueError("A question must have exactly four choices.")
        if not 0 <= self.answer_index < len(self.choices):
            raise ValueError("Answer index must identify one of the choices.")


@dataclass
class Player:
    name: str
    color: str
    position: int = 0
    credits: int = 300
    items: Inventory = field(default_factory=Inventory)
    badges: int = 0
    final_payment_paid: bool = False
    roll_bonus: int = 0
    payment_discount: int = 0
    loss_halved: bool = False
    quiz_hint_ready: bool = False
    quiz_penalty_protected: bool = False
    extra_turns: int = 0
    skip_turns: int = 0
    gain_halved: bool = False
    used_item_this_turn: bool = False

    MAX_ITEMS = 3

    def __post_init__(self) -> None:
        if not isinstance(self.items, Inventory):
            self.items = Inventory(self.items)

    def __setattr__(self, name: str, value: object) -> None:
        if name == "credits" and isinstance(value, int) and value < 0:
            raise ValueError("Credits cannot be negative.")
        super().__setattr__(name, value)

    def gain_credits(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("Credit gain cannot be negative.")
        self.credits += amount
        return amount

    def lose_credits(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("Credit loss cannot be negative.")
        lost = min(self.credits, amount)
        self.credits -= lost
        return lost

    def pay(self, amount: int) -> bool:
        if amount < 0:
            raise ValueError("Payment cannot be negative.")
        if self.credits < amount:
            return False
        self.credits -= amount
        return True

    def acquire_item(self, item: Item) -> bool:
        if len(self.items) >= self.MAX_ITEMS:
            return False
        self.items.append(item)
        return True

    def consume_item(self, item: Item) -> bool:
        if item not in self.items:
            return False
        self.items.remove(item)
        return True


@dataclass(frozen=True)
class TurnResult:
    player_index: int
    roll: int
    space_type: SpaceType
    message: str
    question: Question | None = None
    payment_message: str | None = None
