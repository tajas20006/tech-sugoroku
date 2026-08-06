from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from techsugoroku.domain import Question


class MarkdownQuestionRepository:
    """Load de-duplicated four-choice questions from Markdown assets."""

    def __init__(self, paths: Sequence[str | Path]) -> None:
        self.paths = tuple(Path(path) for path in paths)

    def list(self) -> list[Question]:
        questions: list[Question] = []
        seen_prompts: set[str] = set()
        for path in self.paths:
            self._read_file(path, questions, seen_prompts)
        return questions

    @staticmethod
    def _read_file(path: Path, questions: list[Question], seen_prompts: set[str]) -> None:
        is_exam = False
        current: dict[str, str] = {}

        def add_current(question_data: dict[str, str], exam: bool) -> None:
            required = {"prompt", "choices", "answer", "explanation"}
            if not required <= question_data.keys():
                return
            choices = tuple(question_data["choices"].split(" / "))
            if len(choices) != 4 or question_data["answer"] not in choices:
                return
            prompt = question_data["prompt"]
            if prompt in seen_prompts:
                return
            seen_prompts.add(prompt)
            questions.append(
                Question(
                    prompt=prompt,
                    choices=(choices[0], choices[1], choices[2], choices[3]),
                    answer_index=choices.index(question_data["answer"]),
                    explanation=question_data["explanation"],
                    is_exam=exam,
                )
            )

        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                add_current(current, is_exam)
                current = {}
                is_exam = "資格試験" in line
            elif line.startswith("### "):
                add_current(current, is_exam)
                current = {}
            elif line.startswith("- 問題: "):
                current["prompt"] = line.removeprefix("- 問題: ")
            elif line.startswith("- 選択肢: "):
                current["choices"] = line.removeprefix("- 選択肢: ")
            elif line.startswith("- 正解: "):
                current["answer"] = line.removeprefix("- 正解: ")
            elif line.startswith("- 解説: "):
                current["explanation"] = line.removeprefix("- 解説: ")
        add_current(current, is_exam)

