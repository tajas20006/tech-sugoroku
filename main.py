from __future__ import annotations

import asyncio
import random

import flet as ft

from game import Game, Question, SpaceType, load_questions

QUESTIONS = load_questions(["assets/quiz.md", "assets/quiz-architecture.md"])

SPACE_STYLES = {
    SpaceType.NORMAL: ("#F8FAFC", "·"),
    SpaceType.GAIN: ("#BBF7D0", "+"),
    SpaceType.LOSS: ("#FECACA", "−"),
    SpaceType.QUIZ: ("#DDD6FE", "?"),
    SpaceType.PAYMENT: ("#FED7AA", "¥"),
    SpaceType.ITEM: ("#BFDBFE", "□"),
    SpaceType.SUMMIT: ("#BAE6FD", "★"),
    SpaceType.EXAM: ("#FDE68A", "🏆"),
    SpaceType.GOAL: ("#FDE68A", "GOAL"),
}
BOARD_WIDTH = 800
BOARD_HEIGHT = 480
CELL_SIZE = 80


def main(page: ft.Page) -> None:
    page.title = "AWS すごろく"
    page.padding = 16
    page.bgcolor = "#E0F2FE"

    game = Game(QUESTIONS)
    status = ft.Text("青プレイヤーのターンです。サイコロを振ろう！", size=18, weight=ft.FontWeight.BOLD)
    board = ft.Stack(width=BOARD_WIDTH, height=BOARD_HEIGHT)
    player_cards = ft.Column(spacing=8)
    question_area = ft.Column(spacing=10)
    roll_button = ft.Button("🎲 サイコロを振る", width=220)
    die_display = ft.Text("🎲", size=44, text_align=ft.TextAlign.CENTER)
    die_box = ft.Container(
        content=die_display,
        alignment=ft.Alignment.CENTER,
        animate_scale=ft.Animation(90, ft.AnimationCurve.EASE_OUT),
        scale=ft.Scale(1.0),
    )
    event_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF")
    event_banner = ft.Container(
        content=event_text,
        left=180,
        top=12,
        width=440,
        padding=12,
        alignment=ft.Alignment.CENTER,
        bgcolor="#2563EB",
        border_radius=16,
        opacity=0,
        animate_opacity=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
    )
    token_controls = [
        ft.Container(
            content=ft.Image(src=f"images/tokens/player-{color}.png", width=42, height=42),
            width=42,
            height=42,
            animate_position=ft.Animation(120, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
            scale=ft.Scale(1.0),
        )
        for color in ("blue", "pink")
    ]

    def token_coordinates(player_index: int, position: int) -> tuple[int, int]:
        column = position % 10
        row = position // 10
        return column * CELL_SIZE + 16 + player_index * 22, row * CELL_SIZE + 31

    def create_board() -> None:
        board.controls.clear()
        board.controls.append(
            ft.Container(
                width=BOARD_WIDTH,
                height=BOARD_HEIGHT,
                border_radius=16,
                image=ft.DecorationImage(src="images/board-background.png", fit=ft.BoxFit.COVER, opacity=0.48),
            )
        )
        for position in range(60):
            space_type = game.space_at(position)
            color, marker = SPACE_STYLES[space_type]
            label = "START" if position == 0 else marker
            board.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(str(position), size=10, color="#334155"),
                            ft.Text(label, size=13, weight=ft.FontWeight.BOLD),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    bgcolor=color,
                    border_radius=10,
                    padding=4,
                    alignment=ft.Alignment.CENTER,
                    left=(position % 10) * CELL_SIZE + 3,
                    top=(position // 10) * CELL_SIZE + 3,
                    width=CELL_SIZE - 6,
                    height=CELL_SIZE - 6,
                )
            )
        board.controls.extend(token_controls)
        board.controls.append(event_banner)

    def sync_tokens() -> None:
        for index, player in enumerate(game.players):
            token_controls[index].left, token_controls[index].top = token_coordinates(index, player.position)

    async def animate_token(player_index: int, start: int, destination: int) -> None:
        for position in range(start + 1, destination + 1):
            token = token_controls[player_index]
            token.left, token.top = token_coordinates(player_index, position)
            token.scale = ft.Scale(1.18)
            page.update()
            await asyncio.sleep(0.11)
            token.scale = ft.Scale(1.0)
            page.update()
            await asyncio.sleep(0.04)

    async def show_event(message: str, space_type: SpaceType) -> None:
        event_text.value = message
        event_banner.bgcolor = {
            SpaceType.GAIN: "#16A34A",
            SpaceType.LOSS: "#DC2626",
            SpaceType.PAYMENT: "#EA580C",
            SpaceType.QUIZ: "#7C3AED",
            SpaceType.EXAM: "#A16207",
            SpaceType.ITEM: "#2563EB",
            SpaceType.SUMMIT: "#0891B2",
        }.get(space_type, "#475569")
        event_banner.opacity = 1
        page.update()
        await asyncio.sleep(0.8)
        event_banner.opacity = 0
        page.update()

    def redraw_players() -> None:
        player_cards.controls.clear()
        for index, player in enumerate(game.players):
            active = " ← TURN" if index == game.current_player_index and game.winner_index is None else ""
            items = "、".join(item.value for item in player.items) or "なし"
            player_cards.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"{'🔵' if index == 0 else '🩷'} {player.name}{active}", weight=ft.FontWeight.BOLD),
                            ft.Text(f"位置: {player.position} / Credits: {player.credits}"),
                            ft.Text(f"アイテム: {items}", size=12),
                        ],
                        spacing=2,
                    ),
                    padding=10,
                    border_radius=10,
                    bgcolor="#FFFFFFCC",
                )
            )

    def clear_question() -> None:
        question_area.controls.clear()
        roll_button.disabled = game.pending_question is not None or game.winner_index is not None

    def show_question(question: Question) -> None:
        question_area.controls.clear()
        title = "🏆 資格試験" if question.is_exam else "❓ AWS クイズ"
        question_area.controls.append(ft.Text(title, size=18, weight=ft.FontWeight.BOLD))
        question_area.controls.append(ft.Text(question.prompt, size=16))
        for index, choice in enumerate(question.choices):
            question_area.controls.append(
                ft.Button(choice, on_click=lambda event, answer=index: answer_question(answer), width=320)
            )
        roll_button.disabled = True

    def answer_question(answer: int) -> None:
        question = game.pending_question
        correct = game.answer_question(answer)
        outcome = "正解！" if correct else "不正解。"
        status.value = f"{outcome} {question.explanation if question else ''}"
        clear_question()
        sync_tokens()
        redraw_players()
        page.update()

    async def roll_dice(event: ft.ControlEvent) -> None:
        roll_button.disabled = True
        for _ in range(10):
            die_display.value = f"🎲 {random.randint(1, 6)}"
            die_box.scale = ft.Scale(1.12)
            status.value = "サイコロが回転中……"
            page.update()
            await asyncio.sleep(0.08)
            die_box.scale = ft.Scale(1.0)
        roll = random.randint(1, 6)
        die_display.value = f"🎲 {roll}"
        die_box.scale = ft.Scale(1.35)
        page.update()
        await asyncio.sleep(0.18)
        die_box.scale = ft.Scale(1.0)
        start_position = game.current_player.position
        result = game.take_turn(roll)
        landing_position = min(59, start_position + result.roll)
        await animate_token(result.player_index, start_position, landing_position)
        sync_tokens()
        status.value = f"{game.players[result.player_index].name}: {result.roll} を出した。{result.message}"
        redraw_players()
        await show_event(result.message, result.space_type)
        if result.question:
            show_question(result.question)
        else:
            clear_question()
        page.update()

    roll_button.on_click = roll_dice
    create_board()
    sync_tokens()
    redraw_players()

    left_panel = ft.Container(content=player_cards, width=260, padding=12, bgcolor="#DBEAFE", border_radius=16)
    board_panel = ft.Container(content=board, padding=12, border_radius=16, bgcolor="#FFFFFF99")
    right_panel = ft.Container(
        content=ft.Column([die_box, roll_button, ft.Divider(), status, ft.Divider(), question_area], scroll=ft.ScrollMode.AUTO),
        width=350,
        padding=12,
        bgcolor="#F8FAFC",
        border_radius=16,
    )
    page.add(ft.Text("☁️ AWS すごろく", size=28, weight=ft.FontWeight.BOLD), ft.Row([left_panel, board_panel, right_panel], expand=True))


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
