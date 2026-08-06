from __future__ import annotations

import random

import flet as ft

from game import Game, Question, SpaceType

QUESTIONS = [
    Question(
        "オブジェクトストレージとして使う AWS サービスは？",
        ("Amazon S3", "Amazon EC2", "Amazon RDS", "Amazon Route 53"),
        0,
        "Amazon S3 はオブジェクトストレージサービスです。",
    ),
    Question(
        "Web アプリへの不正な HTTP(S) リクエストをルールで防ぐサービスは？",
        ("AWS WAF", "AWS KMS", "Amazon EFS", "Amazon SNS"),
        0,
        "AWS WAF は Web リクエストをルールでフィルタリングします。",
    ),
    Question(
        "高可用性を高める RDS の構成は？",
        ("Multi-AZ", "単一 AZ", "手動バックアップのみ", "最大サイズへ変更"),
        0,
        "Multi-AZ は障害時の自動フェイルオーバーを提供します。",
    ),
    Question(
        "S3 のログを低コストなストレージクラスへ自動移行する機能は？",
        ("S3 Lifecycle", "S3 ACL", "CloudTrail", "Route 53"),
        0,
        "S3 Lifecycle ルールでストレージクラスを移行できます。",
        is_exam=True,
    ),
    Question(
        "CloudFront 配信で過剰なリクエストを送る送信元を制限する設定は？",
        ("AWS WAF のレートベースルール", "EBS 暗号化", "IAM ユーザー", "S3 バケットポリシー"),
        0,
        "WAF のレートベースルールはリクエスト数に応じて送信元を制限します。",
        is_exam=True,
    ),
]

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


def main(page: ft.Page) -> None:
    page.title = "AWS すごろく"
    page.padding = 16
    page.bgcolor = "#E0F2FE"

    game = Game(QUESTIONS)
    status = ft.Text("青プレイヤーのターンです。サイコロを振ろう！", size=18, weight=ft.FontWeight.BOLD)
    board = ft.GridView(runs_count=10, max_extent=72, spacing=5, run_spacing=5, expand=True)
    player_cards = ft.Column(spacing=8)
    question_area = ft.Column(spacing=10)
    roll_button = ft.ElevatedButton("🎲 サイコロを振る", width=220)

    def token_for(position: int) -> str:
        tokens: list[str] = []
        for index, player in enumerate(game.players):
            if player.position == position:
                tokens.append("🔵" if index == 0 else "🩷")
        return "".join(tokens)

    def redraw_board() -> None:
        board.controls.clear()
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
                            ft.Text(token_for(position), size=14),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    bgcolor=color,
                    border_radius=10,
                    padding=4,
                    alignment=ft.alignment.center,
                )
            )

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
                ft.OutlinedButton(choice, on_click=lambda event, answer=index: answer_question(answer), width=320)
            )
        roll_button.disabled = True

    def answer_question(answer: int) -> None:
        question = game.pending_question
        correct = game.answer_question(answer)
        outcome = "正解！" if correct else "不正解。"
        status.value = f"{outcome} {question.explanation if question else ''}"
        clear_question()
        redraw_board()
        redraw_players()
        page.update()

    def roll_dice(event: ft.ControlEvent) -> None:
        roll = random.randint(1, 6)
        result = game.take_turn(roll)
        status.value = f"{game.players[result.player_index].name}: {result.roll} を出した。{result.message}"
        redraw_board()
        redraw_players()
        if result.question:
            show_question(result.question)
        else:
            clear_question()
        page.update()

    roll_button.on_click = roll_dice
    redraw_board()
    redraw_players()

    left_panel = ft.Container(content=player_cards, width=260, padding=12, bgcolor="#DBEAFE", border_radius=16)
    board_panel = ft.Container(
        content=board,
        expand=True,
        padding=12,
        border_radius=16,
        image=ft.DecorationImage(src="images/board-background.png", fit=ft.ImageFit.COVER, opacity=0.35),
    )
    right_panel = ft.Container(
        content=ft.Column([roll_button, ft.Divider(), status, ft.Divider(), question_area], scroll=ft.ScrollMode.AUTO),
        width=350,
        padding=12,
        bgcolor="#F8FAFC",
        border_radius=16,
    )
    page.add(ft.Text("☁️ AWS すごろく", size=28, weight=ft.FontWeight.BOLD), ft.Row([left_panel, board_panel, right_panel], expand=True))


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
