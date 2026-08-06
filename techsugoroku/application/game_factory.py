import random

from techsugoroku.domain import Game

from .ports import QuestionRepository


def create_game(repository: QuestionRepository, *, rng: random.Random | None = None) -> Game:
    """Create a game session from a replaceable learning-content source."""
    return Game(repository.list(), rng=rng)

