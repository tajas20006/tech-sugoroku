from __future__ import annotations

import random
from collections.abc import Mapping, Sequence

from .board import Board
from .messages import DEFAULT_MESSAGE_POOLS
from .model import Item, Player, Question, SpaceType, TurnResult


class Game:
    """Aggregate root for one two-player game session."""

    def __init__(
        self,
        questions: Sequence[Question],
        rng_seed: int | None = None,
        *,
        rng: random.Random | None = None,
        board: Board | None = None,
        message_pools: Mapping[str, Sequence[str]] | None = None,
    ) -> None:
        if not questions:
            raise ValueError("At least one question is required.")
        if rng is not None and rng_seed is not None:
            raise ValueError("Pass either rng or rng_seed, not both.")
        self.questions = list(questions)
        self.rng = rng if rng is not None else random.Random(rng_seed)
        source_pools = message_pools or DEFAULT_MESSAGE_POOLS
        self.message_pools = {name: list(messages) for name, messages in source_pools.items()}
        self.board = board or Board.default()
        self.players = [Player("Player 1", "blue"), Player("Player 2", "pink")]
        self.current_player_index = 0
        self.pending_question: Question | None = None
        self.pending_player_index: int | None = None
        self.winner_index: int | None = None
        self.question_decks: dict[bool, list[Question]] = {False: [], True: []}

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def space_at(self, position: int) -> SpaceType:
        return self.board.space_at(position)

    def take_turn(self, roll: int) -> TurnResult:
        if self.winner_index is not None:
            raise ValueError("The game has already finished.")
        if self.pending_question is not None:
            raise ValueError("Answer the current question first.")
        if not 1 <= roll <= 6:
            raise ValueError("Roll must be between 1 and 6.")

        player_index = self.current_player_index
        player = self.current_player
        actual_roll = min(6, roll + player.roll_bonus)
        player.roll_bonus = 0
        start = player.position
        player.position = self.board.destination(start, actual_roll)
        payment_failure, payment_message = self._process_payments(player, start)
        if payment_failure:
            self._end_turn()
            return TurnResult(
                player_index,
                actual_roll,
                SpaceType.PAYMENT,
                payment_failure,
                payment_message=payment_failure,
            )

        space_type = self.space_at(player.position)
        if space_type in (SpaceType.QUIZ, SpaceType.EXAM):
            question = self._next_question(is_exam=space_type is SpaceType.EXAM)
            self.pending_question = question
            self.pending_player_index = player_index
            return TurnResult(
                player_index,
                actual_roll,
                space_type,
                "クイズに挑戦！",
                question,
                payment_message,
            )

        message = (
            payment_message
            if space_type is SpaceType.PAYMENT and payment_message
            else self._resolve_space(player, space_type)
        )
        if player.position == self.board.final_position and player.final_payment_paid:
            self.winner_index = player_index
            message = f"{player.name} がゴール！ 勝利です！"
        self._end_turn()
        return TurnResult(
            player_index,
            actual_roll,
            space_type,
            message,
            payment_message=payment_message,
        )

    def answer_question(self, answer_index: int) -> bool:
        if self.pending_question is None or self.pending_player_index is None:
            raise ValueError("There is no question to answer.")
        if not 0 <= answer_index < 4:
            raise ValueError("Answer index must be between 0 and 3.")
        player = self.players[self.pending_player_index]
        question = self.pending_question
        correct = answer_index == question.answer_index
        if correct:
            player.gain_credits(300 if question.is_exam else 100)
            if question.is_exam:
                player.badges += 1
        elif player.quiz_penalty_protected:
            player.quiz_penalty_protected = False
        else:
            player.lose_credits(80 if question.is_exam else 20)
        self.pending_question = None
        self.pending_player_index = None
        self._end_turn()
        return correct

    def apply_ddos(self, player_index: int) -> bool:
        player = self.players[player_index]
        if player.consume_item(Item.WAF):
            return True
        player.lose_credits(100)
        return False

    def consume_quiz_hint(self, player_index: int) -> int | None:
        player = self.players[player_index]
        question = self.pending_question
        if not player.quiz_hint_ready or question is None:
            return None
        player.quiz_hint_ready = False
        return next(index for index in range(4) if index != question.answer_index)

    def use_item(self, player_index: int, item: Item) -> str:
        if player_index != self.current_player_index:
            raise ValueError("Only the current player can use an item.")
        if self.pending_question is not None:
            raise ValueError("Answer the current question first.")
        player = self.players[player_index]
        if player.used_item_this_turn:
            raise ValueError("Only one active item can be used per turn.")
        if item not in player.items:
            raise ValueError("The player does not own this item.")
        player.used_item_this_turn = True
        if item is Item.AUTO_SCALING:
            player.consume_item(item)
            player.roll_bonus += 2
            return "Auto Scaling を使用！ 次のサイコロに +2。"
        if item is Item.CLOUDFRONT:
            player.consume_item(item)
            player.roll_bonus += 2
            return "CloudFront を使用！ 次のサイコロに +2。"
        if item is Item.COST_EXPLORER:
            player.consume_item(item)
            player.payment_discount += 50
            return "Cost Explorer を使用！ 次の支払日を 50 Credits 軽減。"
        if item is Item.RESERVED_INSTANCE:
            player.consume_item(item)
            player.loss_halved = True
            return "リザーブドインスタンスを適用！ 次のコスト発生を半減。"
        if item is Item.WELL_ARCHITECTED:
            player.consume_item(item)
            player.quiz_hint_ready = True
            return "Well-Architected Review を実施！ 次のクイズで選択肢を1つ除外。"
        if item is Item.SUPPORT_PLAN:
            player.consume_item(item)
            player.quiz_penalty_protected = True
            return "AWS サポートプランを利用！ 次のクイズ失敗ペナルティを無効化。"
        if item is Item.TRANSIT_GATEWAY:
            player.consume_item(item)
            player.roll_bonus += 3
            return "Transit Gateway を使用！ ショートカットで次のサイコロに +3。"
        if item is Item.LAMBDA:
            player.consume_item(item)
            player.extra_turns += 1
            return "Lambda を使用！ 次のターンをもう1回行える。"

        target_index = self._other_player_index(player_index)
        target = self.players[target_index]
        if item is Item.DDOS_ATTACK:
            player.consume_item(item)
            blocked = self.apply_ddos(target_index)
            return "相手の WAF に防がれた！" if blocked else "相手へ DDoS 攻撃！ -100 Credits"
        if item is Item.NAT_GATEWAY:
            player.consume_item(item)
            target.lose_credits(60)
            return "相手に不要な NAT Gateway が増えた！ -60 Credits"
        if item is Item.CLOUDWATCH_LOGS:
            player.consume_item(item)
            target.gain_halved = True
            return "相手の CloudWatch Logs が増殖！ 次の獲得クレジットを半減。"
        if item is Item.REGION_RUMOR:
            player.consume_item(item)
            if target.consume_item(Item.MULTI_AZ):
                return "相手の Multi-AZ が障害を回避！"
            target.skip_turns += 1
            return "リージョン障害のうわさが広がった！ 相手は1ターン休み。"
        player.used_item_this_turn = False
        return f"{item.value} は自動防御アイテムです。"

    def _process_payments(self, player: Player, start: int) -> tuple[str | None, str | None]:
        payment_message: str | None = None
        for position, cost in self.board.crossed_payments(start, player.position):
            discount = player.badges * 50 + player.payment_discount
            amount = max(0, cost - discount)
            if not player.pay(amount):
                player.position = self.board.previous_checkpoint(position)
                message = f"クレジット不足！ 前の支払日へ戻る。必要額: {amount}"
                return message, message
            player.payment_discount = 0
            payment_message = self._random_message("payment").format(amount=amount)
            if position == max(self.board.payments):
                player.final_payment_paid = True
        return None, payment_message

    def _resolve_space(self, player: Player, space_type: SpaceType) -> str:
        if space_type is SpaceType.GAIN:
            amount = 50 if player.gain_halved else 100
            player.gain_halved = False
            player.gain_credits(amount)
            return self._random_message("gain").format(amount=amount)
        if space_type is SpaceType.LOSS:
            if player.consume_item(Item.AWS_BACKUP):
                return "AWS Backup が損失を防いだ！"
            amount = 20 if player.loss_halved else 40
            player.loss_halved = False
            player.lose_credits(amount)
            return self._random_message("loss").format(amount=amount)
        if space_type is SpaceType.ITEM:
            item = self.rng.choice(list(Item))
            if player.acquire_item(item):
                return self._random_message("item").format(item=item.value)
            return "アイテム枠がいっぱいだ。"
        if space_type is SpaceType.SUMMIT:
            event = self.rng.choice(("credits", "item", "ddos"))
            if event == "credits":
                player.gain_credits(100)
                return self._random_message("summit_gain").format(amount=100)
            if event == "item":
                item = self.rng.choice(list(Item))
                if player.acquire_item(item):
                    return self._random_message("summit_item").format(item=item.value)
            protected = self.apply_ddos(self.current_player_index)
            return (
                self._random_message("ddos_defense")
                if protected
                else self._random_message("ddos").format(amount=100)
            )
        return "安全なマス。"

    def _next_question(self, is_exam: bool) -> Question:
        candidates = [question for question in self.questions if question.is_exam == is_exam]
        source = candidates or self.questions
        if not self.question_decks[is_exam]:
            self.question_decks[is_exam] = source.copy()
            self.rng.shuffle(self.question_decks[is_exam])
        question = self.question_decks[is_exam].pop()
        return Question(
            prompt=question.prompt,
            choices=question.choices,
            answer_index=question.answer_index,
            explanation=question.explanation,
            is_exam=is_exam,
        )

    def _random_message(self, category: str) -> str:
        return self.rng.choice(self.message_pools[category])

    def _other_player_index(self, player_index: int) -> int:
        return (player_index + 1) % len(self.players)

    def _end_turn(self) -> None:
        if self.winner_index is not None:
            return
        current = self.current_player
        if current.extra_turns:
            current.extra_turns -= 1
            current.used_item_this_turn = False
            return
        next_index = self._other_player_index(self.current_player_index)
        while self.players[next_index].skip_turns:
            self.players[next_index].skip_turns -= 1
            next_index = self._other_player_index(next_index)
        self.current_player_index = next_index
        self.current_player.used_item_this_turn = False
