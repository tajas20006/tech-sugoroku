from typing import Protocol

from techsugoroku.domain import Question


class QuestionRepository(Protocol):
    """Port used by the application to obtain learning content."""

    def list(self) -> list[Question]: ...

