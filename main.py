from __future__ import annotations

import asyncio
import math
import random

import flet as ft

from game import Game, Item, Question, SpaceType, load_questions

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
ITEM_DESCRIPTIONS = {
    Item.AUTO_SCALING: "サイコロ前に使用。次の出目を +2 します。",
    Item.CLOUDFRONT: "サイコロ前に使用。次の出目を +1 します。",
    Item.COST_EXPLORER: "いつでも使用可能。無駄なコストを見つけて +60 Credits。",
    Item.WAF: "自動防御。DDoS 攻撃を1回無効化します。",
    Item.AWS_BACKUP: "自動防御。次のコスト発生を1回無効化します。",
}
BOARD_WIDTH = 800
BOARD_HEIGHT = 480
CELL_SIZE = 44
CAMERA_ZOOM = 1.28
CAMERA_OVERVIEW_ZOOM = 0.42
TRACK_CENTER_X = 600
TRACK_CENTER_Y = 450


def main(page: ft.Page) -> None:
    page.title = "AWS すごろく"
    page.padding = 16
    page.bgcolor = "#E0F2FE"

    game = Game(QUESTIONS)
    has_started = False
    status = ft.Text("STARTを押して、クラウドの旅を始めよう！", size=18, weight=ft.FontWeight.BOLD)
    board = ft.Stack(width=BOARD_WIDTH, height=BOARD_HEIGHT)
    player_cards = ft.Column(spacing=8)
    question_area = ft.Column(spacing=10)
    roll_button = ft.Button("🎲 サイコロを振る", width=220, disabled=True)
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
    cutin_icon = ft.Text("", size=68, text_align=ft.TextAlign.CENTER)
    cutin_title = ft.Text("", size=28, weight=ft.FontWeight.BOLD, color="#FFFFFF", text_align=ft.TextAlign.CENTER)
    cutin_message = ft.Text("", size=15, color="#FFFFFF", text_align=ft.TextAlign.CENTER)
    cutin_overlay = ft.Container(
        content=ft.Column(
            [cutin_icon, cutin_title, cutin_message],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        left=0,
        top=0,
        width=BOARD_WIDTH,
        height=BOARD_HEIGHT,
        alignment=ft.Alignment.CENTER,
        bgcolor="#4C1D95E8",
        border_radius=16,
        opacity=0,
        scale=ft.Scale(0.88),
        animate_opacity=ft.Animation(160, ft.AnimationCurve.EASE_OUT),
        animate_scale=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
        ignore_interactions=True,
    )
    start_button = ft.Button("▶ START", width=220)
    how_to_button = ft.Button("❔ 遊び方", width=220)
    intro_overlay = ft.Container(
        content=ft.Column(
            [
                ft.Text("☁️", size=64, text_align=ft.TextAlign.CENTER),
                ft.Text("AWS すごろく", size=32, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                ft.Text("コースを見渡して、クラウドの旅を始めよう！", color="#FFFFFF"),
                start_button,
                how_to_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        ),
        left=0,
        top=0,
        width=BOARD_WIDTH,
        height=BOARD_HEIGHT,
        alignment=ft.Alignment.CENTER,
        bgcolor="#0F172ACC",
        border_radius=16,
        opacity=1,
        animate_opacity=ft.Animation(350, ft.AnimationCurve.EASE_OUT),
        ignore_interactions=False,
    )
    close_how_to_button = ft.Button("閉じる", width=180)
    how_to_overlay = ft.Container(
        content=ft.Column(
            [
                ft.Text("遊び方", size=30, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                ft.Text("知識とクレジットを集め、支払日を乗り越えてGOALを目指そう！", color="#FFFFFF"),
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [ft.Text("🎲", size=42), ft.Text("1. サイコロ", weight=ft.FontWeight.BOLD), ft.Text("出目の数だけ進む", size=12)],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            width=170,
                            padding=12,
                            alignment=ft.Alignment.CENTER,
                            bgcolor="#1D4ED8",
                            border_radius=12,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [ft.Image(src="images/tokens/player-blue.png", width=50, height=50), ft.Text("2. マス効果", weight=ft.FontWeight.BOLD), ft.Text("クイズで学んで稼ぐ", size=12)],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            width=170,
                            padding=12,
                            alignment=ft.Alignment.CENTER,
                            bgcolor="#7C3AED",
                            border_radius=12,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [ft.Text("🧾", size=42), ft.Text("3. 支払日", weight=ft.FontWeight.BOLD), ft.Text("クレジット不足に注意", size=12)],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            width=170,
                            padding=12,
                            alignment=ft.Alignment.CENTER,
                            bgcolor="#C2410C",
                            border_radius=12,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [ft.Image(src="images/items/auto-scaling.png", width=50, height=50), ft.Text("4. アイテム", weight=ft.FontWeight.BOLD), ft.Text("有利なタイミングで使う", size=12)],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            width=170,
                            padding=12,
                            alignment=ft.Alignment.CENTER,
                            bgcolor="#047857",
                            border_radius=12,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                close_how_to_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
        ),
        left=0,
        top=0,
        width=BOARD_WIDTH,
        height=BOARD_HEIGHT,
        alignment=ft.Alignment.CENTER,
        bgcolor="#172554F5",
        border_radius=16,
        opacity=0,
        animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        ignore_interactions=True,
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
    space_controls: list[ft.Container] = []
    visual_positions = [player.position for player in game.players]

    def world_coordinates(position: int) -> tuple[float, float]:
        angle = math.tau * position / 60 - math.pi / 2
        radius = 470 + 10 * math.sin(angle * 3) + 8 * math.cos(angle * 5)
        return (
            TRACK_CENTER_X + radius * math.cos(angle),
            TRACK_CENTER_Y + radius * 0.80 * math.sin(angle),
        )

    def screen_coordinates(position: int, focus_position: int | None, zoom: float) -> tuple[float, float]:
        world_x, world_y = world_coordinates(position)
        focus_x, focus_y = world_coordinates(focus_position) if focus_position is not None else (TRACK_CENTER_X, TRACK_CENTER_Y)
        return (
            BOARD_WIDTH / 2 + (world_x - focus_x) * zoom,
            BOARD_HEIGHT / 2 + (world_y - focus_y) * zoom,
        )

    def update_camera(focus_position: int | None, zoom: float = CAMERA_ZOOM) -> None:
        element_scale = zoom / CAMERA_ZOOM
        for position, space in enumerate(space_controls):
            x, y = screen_coordinates(position, focus_position, zoom)
            space.left, space.top = x - CELL_SIZE / 2, y - CELL_SIZE / 2
            space.scale = ft.Scale(element_scale)
        for index, token in enumerate(token_controls):
            x, y = screen_coordinates(visual_positions[index], focus_position, zoom)
            token.left, token.top = x - 22 + index * 10, y - 18
            token.scale = ft.Scale(element_scale)

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
            space = ft.Container(
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
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    animate_position=ft.Animation(360, ft.AnimationCurve.EASE_OUT),
                    animate_scale=ft.Animation(360, ft.AnimationCurve.EASE_OUT),
                )
            space_controls.append(space)
            board.controls.append(space)
        board.controls.extend(token_controls)
        board.controls.append(event_banner)
        board.controls.append(cutin_overlay)
        board.controls.append(intro_overlay)
        board.controls.append(how_to_overlay)

    def sync_tokens(focus_position: int) -> None:
        for index, player in enumerate(game.players):
            visual_positions[index] = player.position
        update_camera(focus_position)

    async def animate_token(player_index: int, start: int, destination: int) -> None:
        for position in range(start + 1, destination + 1):
            token = token_controls[player_index]
            visual_positions[player_index] = position
            update_camera(position)
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

    async def show_cutin(message: str, space_type: SpaceType) -> None:
        cutin_styles = {
            SpaceType.PAYMENT: ("🧾", "支払日", "#9A3412E8"),
            SpaceType.EXAM: ("🏆", "資格試験", "#854D0EE8"),
            SpaceType.SUMMIT: ("☁️", "AWS Summit", "#0E7490E8"),
            SpaceType.ITEM: ("🎁", "アイテム獲得", "#1D4ED8E8"),
            SpaceType.QUIZ: ("❓", "AWS クイズ", "#6D28D9E8"),
            SpaceType.LOSS: ("⚠️", "コスト発生", "#B91C1CE8"),
        }
        style = cutin_styles.get(space_type)
        if style is None:
            return
        cutin_icon.value, cutin_title.value, cutin_overlay.bgcolor = style
        cutin_message.value = message
        cutin_overlay.opacity = 0.96
        cutin_overlay.scale = ft.Scale(1.0)
        page.update()
        await asyncio.sleep(0.85)
        cutin_overlay.opacity = 0
        cutin_overlay.scale = ft.Scale(1.08)
        page.update()

    def redraw_players() -> None:
        player_cards.controls.clear()
        for index, player in enumerate(game.players):
            active = " ← TURN" if index == game.current_player_index and game.winner_index is None else ""
            card_contents: list[ft.Control] = [
                ft.Text(f"{'🔵' if index == 0 else '🩷'} {player.name}{active}", weight=ft.FontWeight.BOLD),
                ft.Text(f"位置: {player.position} / Credits: {player.credits}"),
                ft.Text("アイテム:", size=12),
            ]
            if player.items:
                card_contents.extend(
                    ft.Container(
                        content=ft.Text(item.value, size=12),
                        tooltip=ITEM_DESCRIPTIONS[item],
                        padding=5,
                        border_radius=8,
                        bgcolor="#E0E7FF",
                    )
                    for item in player.items
                )
            else:
                card_contents.append(ft.Text("なし", size=12))
            if player.roll_bonus:
                card_contents.append(ft.Text(f"次のサイコロ: +{player.roll_bonus}", color="#15803D", size=12))
            if has_started and index == game.current_player_index:
                usable_items = [item for item in player.items if item in (Item.AUTO_SCALING, Item.CLOUDFRONT, Item.COST_EXPLORER)]
                if usable_items:
                    card_contents.append(ft.Text("アイテムを使う", weight=ft.FontWeight.BOLD, size=12))
                    card_contents.extend(
                        ft.Button(
                            f"使う: {item.value}",
                            on_click=lambda event, selected=item: handle_use_item(selected),
                            width=210,
                        )
                        for item in usable_items
                    )
            player_cards.controls.append(
                ft.Container(
                    content=ft.Column(card_contents, spacing=2),
                    padding=10,
                    border_radius=10,
                    bgcolor="#FFFFFFCC",
                )
            )

    def clear_question() -> None:
        question_area.controls.clear()
        roll_button.disabled = not has_started or game.pending_question is not None or game.winner_index is not None

    def handle_use_item(item: Item) -> None:
        message = game.use_item(game.current_player_index, item)
        status.value = message
        redraw_players()
        page.update()

    def start_game(event: ft.ControlEvent) -> None:
        nonlocal has_started
        has_started = True
        intro_overlay.opacity = 0
        intro_overlay.ignore_interactions = True
        update_camera(game.current_player.position)
        roll_button.disabled = False
        status.value = "青プレイヤーのターンです。サイコロを振ろう！"
        page.update()

    def show_how_to(event: ft.ControlEvent) -> None:
        how_to_overlay.opacity = 1
        how_to_overlay.ignore_interactions = False
        page.update()

    def close_how_to(event: ft.ControlEvent) -> None:
        how_to_overlay.opacity = 0
        how_to_overlay.ignore_interactions = True
        page.update()

    async def focus_current_player() -> None:
        update_camera(game.current_player.position)
        page.update()
        await asyncio.sleep(0.38)

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
        sync_tokens(game.players[game.current_player_index].position)
        redraw_players()
        page.update()

    async def roll_dice(event: ft.ControlEvent) -> None:
        if not has_started:
            return
        await focus_current_player()
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
        sync_tokens(game.players[result.player_index].position)
        status.value = f"{game.players[result.player_index].name}: {result.roll} を出した。{result.message}"
        redraw_players()
        if result.payment_message and result.space_type is not SpaceType.PAYMENT:
            await show_cutin(result.payment_message, SpaceType.PAYMENT)
        await show_cutin(result.message, result.space_type)
        await show_event(result.message, result.space_type)
        if result.question:
            show_question(result.question)
        else:
            clear_question()
            await focus_current_player()
        page.update()

    roll_button.on_click = roll_dice
    start_button.on_click = start_game
    how_to_button.on_click = show_how_to
    close_how_to_button.on_click = close_how_to
    create_board()
    update_camera(None, CAMERA_OVERVIEW_ZOOM)
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
