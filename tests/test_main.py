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
