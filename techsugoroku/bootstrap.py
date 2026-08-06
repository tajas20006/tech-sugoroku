"""Composition root for the desktop application."""

from pathlib import Path

from techsugoroku.application import create_game
from techsugoroku.domain import Game
from techsugoroku.infrastructure import MarkdownQuestionRepository

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_QUESTION_PATHS = (
    PROJECT_ROOT / "assets" / "quiz.md",
    PROJECT_ROOT / "assets" / "quiz-architecture.md",
)


def create_default_game() -> Game:
    return create_game(MarkdownQuestionRepository(DEFAULT_QUESTION_PATHS))

