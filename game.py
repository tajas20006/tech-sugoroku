from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum


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


@dataclass(frozen=True)
class Question:
    prompt: str
    choices: tuple[str, str, str, str]
    answer_index: int
    explanation: str
    is_exam: bool = False


@dataclass
class Player:
    name: str
    color: str
    position: int = 0
    credits: int = 200
    items: list[Item] = field(default_factory=list)
    badges: int = 0
    final_payment_paid: bool = False


@dataclass
class TurnResult:
    player_index: int
    roll: int
    space_type: SpaceType
    message: str
    question: Question | None = None


SPACE_MAP: dict[int, SpaceType] = {
    **{position: SpaceType.GAIN for position in (3, 12, 20, 28, 38, 48)},
    **{position: SpaceType.LOSS for position in (6, 18, 26, 42, 52)},
    **{position: SpaceType.QUIZ for position in (8, 22, 35, 50)},
    **{position: SpaceType.PAYMENT for position in (15, 30, 45, 55)},
    **{position: SpaceType.ITEM for position in (10, 32, 47)},
    25: SpaceType.SUMMIT,
    40: SpaceType.EXAM,
    54: SpaceType.EXAM,
    59: SpaceType.GOAL,
}
PAYMENTS = {15: 150, 30: 300, 45: 500, 55: 800}


class Game:
    def __init__(self, questions: list[Question], rng_seed: int | None = None) -> None:
        if not questions:
            raise ValueError("At least one question is required.")
        self.questions = questions
        self.rng = random.Random(rng_seed)
        self.players = [Player("Player 1", "blue"), Player("Player 2", "pink")]
        self.current_player_index = 0
        self.pending_question: Question | None = None
        self.pending_player_index: int | None = None
        self.winner_index: int | None = None

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def space_at(self, position: int) -> SpaceType:
        return SPACE_MAP.get(position, SpaceType.NORMAL)

    def take_turn(self, roll: int) -> TurnResult:
        if self.winner_index is not None:
            raise ValueError("The game has already finished.")
        if self.pending_question is not None:
            raise ValueError("Answer the current question first.")
        if not 1 <= roll <= 6:
            raise ValueError("Roll must be between 1 and 6.")

        player_index = self.current_player_index
        player = self.current_player
        actual_roll = min(6, roll + self._consume_item(player, Item.AUTO_SCALING, bonus=2))
        start = player.position
        player.position = min(59, player.position + actual_roll)
        payment_message = self._process_payments(player, start)
        if payment_message:
            self._end_turn()
            return TurnResult(player_index, actual_roll, SpaceType.PAYMENT, payment_message)

        space_type = self.space_at(player.position)
        if space_type in (SpaceType.QUIZ, SpaceType.EXAM):
            question = self._next_question(is_exam=space_type is SpaceType.EXAM)
            self.pending_question = question
            self.pending_player_index = player_index
            return TurnResult(player_index, actual_roll, space_type, "クイズに挑戦！", question)

        message = self._resolve_space(player, space_type)
        if player.position == 59 and player.final_payment_paid:
            self.winner_index = player_index
            message = f"{player.name} がゴール！ 勝利です！"
        self._end_turn()
        return TurnResult(player_index, actual_roll, space_type, message)

    def answer_question(self, answer_index: int) -> bool:
        if self.pending_question is None or self.pending_player_index is None:
            raise ValueError("There is no question to answer.")
        if not 0 <= answer_index < 4:
            raise ValueError("Answer index must be between 0 and 3.")
        player = self.players[self.pending_player_index]
        question = self.pending_question
        correct = answer_index == question.answer_index
        if correct:
            player.credits += 250 if question.is_exam else 80
            if question.is_exam:
                player.badges += 1
        else:
            self._lose_credits(player, 150 if question.is_exam else 40)
        self.pending_question = None
        self.pending_player_index = None
        self._end_turn()
        return correct

    def apply_ddos(self, player_index: int) -> bool:
        player = self.players[player_index]
        if Item.WAF in player.items:
            player.items.remove(Item.WAF)
            return True
        self._lose_credits(player, 100)
        return False

    def _process_payments(self, player: Player, start: int) -> str | None:
        for position, cost in PAYMENTS.items():
            if start < position <= player.position:
                discount = player.badges * 50
                amount = max(0, cost - discount)
                if player.credits < amount:
                    player.position = max((checkpoint for checkpoint in PAYMENTS if checkpoint < position), default=0)
                    return f"クレジット不足！ 前の支払日へ戻る。必要額: {amount}"
                player.credits -= amount
                if position == 55:
                    player.final_payment_paid = True
        return None

    def _resolve_space(self, player: Player, space_type: SpaceType) -> str:
        if space_type is SpaceType.GAIN:
            player.credits += 80
            return "コスト最適化に成功！ +80 Credits"
        if space_type is SpaceType.LOSS:
            if self._consume_item(player, Item.AWS_BACKUP):
                return "AWS Backup が損失を防いだ！"
            self._lose_credits(player, 60)
            return "OpenSearch にお金を溶かした。-60 Credits"
        if space_type is SpaceType.ITEM:
            if len(player.items) < 3:
                item = self.rng.choice(list(Item))
                player.items.append(item)
                return f"{item.value} を手に入れた！"
            return "アイテム枠がいっぱいだ。"
        if space_type is SpaceType.SUMMIT:
            event = self.rng.choice(("credits", "item", "ddos"))
            if event == "credits":
                player.credits += 100
                return "AWS Summit で学びを得た！ +100 Credits"
            if event == "item" and len(player.items) < 3:
                item = self.rng.choice(list(Item))
                player.items.append(item)
                return f"AWS Summit で {item.value} を獲得！"
            protected = self.apply_ddos(self.current_player_index)
            return "WAF が DDoS を防いだ！" if protected else "DDoS 攻撃が直撃！ -100 Credits"
        return "安全なマス。"

    def _next_question(self, is_exam: bool) -> Question:
        candidates = [question for question in self.questions if question.is_exam == is_exam]
        source = candidates or self.questions
        question = self.rng.choice(source)
        return Question(
            prompt=question.prompt,
            choices=question.choices,
            answer_index=question.answer_index,
            explanation=question.explanation,
            is_exam=is_exam,
        )

    def _consume_item(self, player: Player, item: Item, bonus: int = 0) -> int:
        if item not in player.items:
            return 0
        player.items.remove(item)
        return bonus

    def _lose_credits(self, player: Player, amount: int) -> None:
        player.credits = max(0, player.credits - amount)

    def _end_turn(self) -> None:
        if self.winner_index is None:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
