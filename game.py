"""Backward-compatible public facade for the domain package.

New code should import domain types from :mod:`techsugoroku.domain` and use the
application factory.  This module remains so existing integrations keep working.
"""

from pathlib import Path

from techsugoroku.domain import (
    Board,
    Game,
    Item,
    Player,
    Question,
    SpaceType,
    TurnResult,
)
from techsugoroku.domain.board import DEFAULT_PAYMENTS, DEFAULT_SPACE_MAP
from techsugoroku.domain.messages import DEFAULT_MESSAGE_POOLS
from techsugoroku.infrastructure import MarkdownQuestionRepository

SPACE_MAP = DEFAULT_SPACE_MAP
PAYMENTS = DEFAULT_PAYMENTS


def load_questions(paths: list[str | Path]) -> list[Question]:
    return MarkdownQuestionRepository(paths).list()


__all__ = [
    "DEFAULT_MESSAGE_POOLS",
    "PAYMENTS",
    "SPACE_MAP",
    "Board",
    "Game",
    "Item",
    "Player",
    "Question",
    "SpaceType",
    "TurnResult",
    "load_questions",
]
