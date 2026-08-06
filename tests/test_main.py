from pathlib import Path


def test_main_uses_current_flet_apis() -> None:
    source = Path("main.py").read_text(encoding="utf-8")

    assert "ft.app(" not in source
    assert "ft.ElevatedButton(" not in source
    assert "ft.OutlinedButton(" not in source
    assert "ft.ImageFit" not in source
    assert "ft.alignment.center" not in source
    assert "ft.run(" in source
    assert "ft.Button(" in source
    assert "ft.Alignment.CENTER" in source
    assert "ft.BoxFit.COVER" in source
    assert "ft.Stack(" in source
    assert "animate_position" in source
    assert "asyncio.sleep" in source
    assert "show_cutin" in source
    assert "cutin_overlay" in source
    assert "result.payment_message" in source
    assert "math.sin" in source
    assert "math.cos" in source
    assert "update_camera" in source
    assert "CAMERA_ZOOM" in source
    assert "CAMERA_OVERVIEW_ZOOM" in source
    assert "intro_overlay" in source
    assert "start_button" in source
    assert "focus_current_player" in source
    assert "await focus_current_player()" in source
    assert "use_item" in source
    assert "アイテムを使う" in source
    assert "ITEM_DESCRIPTIONS" in source
    assert "tooltip=ITEM_DESCRIPTIONS" in source
    assert "await focus_current_player()" in source
    assert "position % 10" not in source
