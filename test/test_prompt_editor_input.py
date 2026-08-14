"""prompt editor input の外部挙動を検証する。

正本仕様:
- {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
- {{work-root}}/oracle/src/oracle/prompt_builder/editor_input.py
"""

from pathlib import Path
from types import SimpleNamespace

import pytest
from oracle.prompt_builder.editor_input import build_prompt_editor_input_initial_text

import commons.prompt_editor_input as prompt_editor_input_module
from cmoc_runtime import CmocError


def test_editor_input_uses_canonical_text_and_keeps_timestamp_collisions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """正本の初期値を使い、同じ timestamp の入力を上書きせず保持する。"""
    timestamps = iter(
        [
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000002000",
        ]
    )
    opened: list[Path] = []
    initial_texts: list[str] = []
    skeletons = [
        "# first skeleton\n\n{{original-prompt-here}}\n",
        "# second skeleton\n\n{{original-prompt-here}}\n",
    ]

    monkeypatch.setattr(
        prompt_editor_input_module,
        "timestamp",
        lambda: next(timestamps),
    )
    monkeypatch.setattr(
        prompt_editor_input_module,
        "_select_editor",
        lambda: ["fake-editor"],
    )

    def fake_run(argv: list[str]) -> SimpleNamespace:
        """editor subprocess の代わりに入力 file を作成する。"""
        path = Path(argv[-1])
        opened.append(path)
        initial_texts.append(path.read_text(encoding="utf-8"))
        path.write_text(f"input-{len(opened)}\n", encoding="utf-8")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(prompt_editor_input_module.subprocess, "run", fake_run)

    first_stamp, first_path, first_complete_path = (
        prompt_editor_input_module.reserve_prompt_editor_input(tmp_path)
    )
    first_input = prompt_editor_input_module.collect_prompt_editor_input(
        first_path,
        skeletons[0],
    )
    second_stamp, second_path, second_complete_path = (
        prompt_editor_input_module.reserve_prompt_editor_input(tmp_path)
    )
    second_input = prompt_editor_input_module.collect_prompt_editor_input(
        second_path,
        skeletons[1],
    )

    assert initial_texts == [
        build_prompt_editor_input_initial_text(skeleton) for skeleton in skeletons
    ]
    assert first_stamp == "2026-06-27_10-00_00_000001000"
    assert second_stamp == "2026-06-27_10-00_00_000002000"
    assert first_path.name == "2026-06-27_10-00_00_000001000_orig.md"
    assert second_path.name == "2026-06-27_10-00_00_000002000_orig.md"
    assert first_complete_path.name == "2026-06-27_10-00_00_000001000_cmpl.md"
    assert second_complete_path.name == "2026-06-27_10-00_00_000002000_cmpl.md"
    assert first_path != second_path
    assert first_input == "input-1"
    assert second_input == "input-2"


@pytest.mark.parametrize(
    "complete_prompt_skeleton",
    [
        "# marker is missing\n",
        "{{original-prompt-here}}\n{{original-prompt-here}}\n",
    ],
)
def test_editor_input_rejects_skeleton_without_one_placeholder(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    complete_prompt_skeleton: str,
) -> None:
    """置換対象が一つでない skeleton ではエディタを起動しない。"""
    original_path = tmp_path / "input_orig.md"
    original_path.touch()
    editor_started = False

    def fake_run(_argv: list[str]) -> SimpleNamespace:
        """不正 skeleton で呼ばれてはならない editor 起動を記録する。"""
        nonlocal editor_started
        editor_started = True
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(prompt_editor_input_module.subprocess, "run", fake_run)

    with pytest.raises(CmocError, match="skeleton"):
        prompt_editor_input_module.collect_prompt_editor_input(
            original_path,
            complete_prompt_skeleton,
        )

    assert editor_started is False


@pytest.mark.parametrize(
    ("available_editors", "expected_editor", "wait_for_editor"),
    [
        (("code", "nano", "vim", "vi"), "code", True),
        (("nano", "vim", "vi"), "nano", False),
        (("vim", "vi"), "vim", False),
        (("vi",), "vi", False),
    ],
)
def test_editor_input_selects_editor_in_specified_priority(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    available_editors: tuple[str, ...],
    expected_editor: str,
    wait_for_editor: bool,
) -> None:
    """仕様の優先順と code 専用の --wait を editor 起動 argv で検証する。"""
    original_path = tmp_path / "input_orig.md"
    calls: list[list[str]] = []

    monkeypatch.setattr(
        prompt_editor_input_module.shutil,
        "which",
        lambda command: f"/fake/{command}" if command in available_editors else None,
    )

    def fake_run(argv: list[str]) -> SimpleNamespace:
        """選択された editor の argv を記録して正常終了する。"""
        calls.append(argv)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(prompt_editor_input_module.subprocess, "run", fake_run)

    prompt_editor_input_module.collect_prompt_editor_input(
        original_path,
        "# skeleton\n\n{{original-prompt-here}}\n",
    )

    expected_argv = [f"/fake/{expected_editor}"]
    if wait_for_editor:
        expected_argv.append("--wait")
    assert calls == [[*expected_argv, str(original_path)]]
