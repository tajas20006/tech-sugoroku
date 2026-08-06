from __future__ import annotations

import ast
import random
from pathlib import Path

import pytest

from game import Game as LegacyGame
from game import load_questions
from techsugoroku.application import create_game
from techsugoroku.bootstrap import create_default_game
from techsugoroku.domain import Board, Game, Item, Player, Question, SpaceType
from techsugoroku.infrastructure import MarkdownQuestionRepository


def sample_question() -> Question:
    return Question(
        prompt="Which service stores objects?",
        choices=("Amazon S3", "Amazon EC2", "Amazon RDS", "Amazon VPC"),
        answer_index=0,
        explanation="Amazon S3 is object storage.",
    )


def test_board_owns_space_and_payment_rules() -> None:
    board = Board.default()

    assert board.space_at(3) is SpaceType.GAIN
    assert board.space_at(15) is SpaceType.PAYMENT
    assert board.space_at(1) is SpaceType.NORMAL
    assert board.crossed_payments(14, 16) == ((15, 100),)


def test_player_enforces_credit_floor_and_inventory_capacity() -> None:
    player = Player("Player", "blue", credits=20)

    lost = player.lose_credits(40)
    assert lost == 20
    assert player.credits == 0

    assert player.acquire_item(Item.WAF)
    assert player.acquire_item(Item.AWS_BACKUP)
    assert player.acquire_item(Item.MULTI_AZ)
    assert not player.acquire_item(Item.CLOUDFRONT)
    assert len(player.items) == 3


def test_player_rejects_direct_credit_or_inventory_invariant_violations() -> None:
    player = Player("Player", "blue")

    with pytest.raises(ValueError, match="Credits cannot be negative"):
        player.credits = -1

    player.items.extend([Item.WAF, Item.AWS_BACKUP, Item.MULTI_AZ])
    with pytest.raises(ValueError, match="more than three items"):
        player.items.append(Item.CLOUDFRONT)


def test_game_accepts_an_injected_random_generator() -> None:
    rng = random.Random(42)

    game = Game([sample_question()], rng=rng)

    assert game.rng is rng


def test_application_factory_uses_a_replaceable_question_repository() -> None:
    class InMemoryQuestionRepository:
        def list(self) -> list[Question]:
            return [sample_question()]

    rng = random.Random(11)
    game = create_game(InMemoryQuestionRepository(), rng=rng)

    assert game.questions == [sample_question()]
    assert game.rng is rng


def test_markdown_repository_and_legacy_loader_share_the_adapter() -> None:
    paths = ["assets/quiz.md", "assets/quiz-architecture.md"]

    repository_questions = MarkdownQuestionRepository(paths).list()

    assert repository_questions == load_questions(paths)
    assert len(repository_questions) >= 50


def test_composition_root_builds_a_game_from_project_assets() -> None:
    game = create_default_game()

    assert len(game.questions) >= 50


def test_legacy_game_import_is_the_domain_aggregate() -> None:
    assert LegacyGame is Game


def test_domain_layer_does_not_import_outer_layers_or_flet() -> None:
    forbidden_roots = {"flet", "pathlib", "techsugoroku.application", "techsugoroku.infrastructure"}

    for path in Path("techsugoroku/domain").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imports.update(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )
        assert not imports & forbidden_roots, f"{path} imports an outer layer: {imports & forbidden_roots}"
