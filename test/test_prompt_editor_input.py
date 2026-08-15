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

_SKELETON = "# skeleton\n\n{{original-prompt-here}}\n"


def test_editor_input_separates_work_and_saved_files_without_overwriting(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """可変な作業 file と保存記録を分離し、timestamp 衝突を回避する。"""
    timestamps = iter(
        [
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000002000",
        ]
    )
    opened: list[Path] = []
    initial_texts: list[str] = []
    skeletons = ["# first\n\n{{original-prompt-here}}\n", _SKELETON]

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
        """初期値を記録し、利用者の最終入力へ置き換える。"""
        path = Path(argv[-1])
        opened.append(path)
        initial_texts.append(path.read_text(encoding="utf-8"))
        path.write_text(
            f"<!-- editor note -->\ninput-{len(opened)}\n",
            encoding="utf-8",
        )
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(prompt_editor_input_module.subprocess, "run", fake_run)

    first_work, first_copy = prompt_editor_input_module.reserve_prompt_editor_input(
        tmp_path
    )
    prompt_editor_input_module.edit_prompt_editor_input(
        tmp_path,
        first_work,
        skeletons[0],
    )
    first_input = prompt_editor_input_module.collect_prompt_editor_input(
        tmp_path,
        first_work,
        first_copy,
    )
    prompt_editor_input_module.finalize_prompt_editor_input(first_work)
    second_work, second_copy = prompt_editor_input_module.reserve_prompt_editor_input(
        tmp_path
    )
    prompt_editor_input_module.edit_prompt_editor_input(
        tmp_path,
        second_work,
        skeletons[1],
    )
    second_input = prompt_editor_input_module.collect_prompt_editor_input(
        tmp_path,
        second_work,
        second_copy,
    )
    prompt_editor_input_module.finalize_prompt_editor_input(second_work)

    assert initial_texts == [
        build_prompt_editor_input_initial_text(skeleton) for skeleton in skeletons
    ]
    assert first_work.parent == tmp_path / ".cmoc" / "gu" / "aw" / "editor_input"
    assert first_copy.parent == (
        tmp_path / ".cmoc" / "gu" / "ar" / "log" / "editor_input"
    )
    assert first_work.name == first_copy.name == "2026-06-27_10-00_00_000001000_orig.md"
    assert (
        second_work.name
        == second_copy.name
        == ("2026-06-27_10-00_00_000002000_orig.md")
    )
    assert first_work != second_work
    assert not first_work.exists()
    assert not second_work.exists()
    assert first_copy.read_text(encoding="utf-8") == ("<!-- editor note -->\ninput-1\n")
    assert second_copy.read_text(encoding="utf-8") == (
        "<!-- editor note -->\ninput-2\n"
    )
    assert first_input == "input-1"
    assert second_input == "input-2"
    assert not list(first_copy.parent.glob("*_cmpl.md"))


def test_editor_input_uses_one_final_read_for_copy_and_prompt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """保存コピーと prompt 抽出を同じ一回の最終読み取り結果から行う。"""
    editor_work, input_copy = prompt_editor_input_module.reserve_prompt_editor_input(
        tmp_path
    )
    monkeypatch.setattr(
        prompt_editor_input_module,
        "_select_editor",
        lambda: ["fake-editor"],
    )

    def fake_run(argv: list[str]) -> SimpleNamespace:
        """最終読み取り対象へ raw 入力を書き込む。"""
        Path(argv[-1]).write_bytes(b"<!-- note -->\r\nfinal input\r\n")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(prompt_editor_input_module.subprocess, "run", fake_run)
    prompt_editor_input_module.edit_prompt_editor_input(
        tmp_path,
        editor_work,
        _SKELETON,
    )
    original_read_bytes = Path.read_bytes
    final_reads = 0

    def record_read_bytes(path: Path) -> bytes:
        """editor work file の読み取り回数を記録する。"""
        nonlocal final_reads
        if path == editor_work:
            final_reads += 1
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", record_read_bytes)

    original_prompt = prompt_editor_input_module.collect_prompt_editor_input(
        tmp_path,
        editor_work,
        input_copy,
    )

    assert final_reads == 1
    assert input_copy.read_bytes() == b"<!-- note -->\r\nfinal input\r\n"
    assert original_prompt == "final input"


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
    editor_work, input_copy = prompt_editor_input_module.reserve_prompt_editor_input(
        tmp_path
    )
    editor_started = False

    def fake_run(_argv: list[str]) -> SimpleNamespace:
        """不正 skeleton で呼ばれてはならない editor 起動を記録する。"""
        nonlocal editor_started
        editor_started = True
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(prompt_editor_input_module.subprocess, "run", fake_run)

    with pytest.raises(CmocError, match="skeleton"):
        prompt_editor_input_module.edit_prompt_editor_input(
            tmp_path,
            editor_work,
            complete_prompt_skeleton,
        )

    assert editor_started is False
    assert editor_work.exists()
    assert not input_copy.exists()


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
    editor_work, _input_copy = prompt_editor_input_module.reserve_prompt_editor_input(
        tmp_path
    )
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

    prompt_editor_input_module.edit_prompt_editor_input(
        tmp_path,
        editor_work,
        _SKELETON,
    )

    expected_argv = [f"/fake/{expected_editor}"]
    if wait_for_editor:
        expected_argv.append("--wait")
    assert calls == [[*expected_argv, str(editor_work)]]


@pytest.mark.parametrize("replacement", ["symlink", "directory", "missing"])
def test_editor_input_rejects_non_regular_final_work_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    replacement: str,
) -> None:
    """エディタ終了後の symlink、directory、欠落 file を拒否する。"""
    editor_work, input_copy = prompt_editor_input_module.reserve_prompt_editor_input(
        tmp_path
    )
    monkeypatch.setattr(
        prompt_editor_input_module,
        "_select_editor",
        lambda: ["fake-editor"],
    )

    def fake_run(_argv: list[str]) -> SimpleNamespace:
        """エディタが作業 file の種別を変更した状態を再現する。"""
        editor_work.unlink()
        if replacement == "symlink":
            target = editor_work.with_name("symlink-target.md")
            target.write_text("outside snapshot\n", encoding="utf-8")
            editor_work.symlink_to(target)
        elif replacement == "directory":
            editor_work.mkdir()
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(prompt_editor_input_module.subprocess, "run", fake_run)
    prompt_editor_input_module.edit_prompt_editor_input(
        tmp_path,
        editor_work,
        _SKELETON,
    )

    with pytest.raises(CmocError, match="editor work file"):
        prompt_editor_input_module.collect_prompt_editor_input(
            tmp_path,
            editor_work,
            input_copy,
        )

    assert not input_copy.exists()


def test_editor_input_rejects_path_outside_work_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """所定の editor work directory 外にある通常 file を拒否する。"""
    reserved_work, input_copy = prompt_editor_input_module.reserve_prompt_editor_input(
        tmp_path
    )
    outside = tmp_path / "outside.md"
    outside.write_text("do not overwrite\n", encoding="utf-8")
    editor_started = False

    def fake_run(_argv: list[str]) -> SimpleNamespace:
        """境界外 path で呼ばれてはならない editor 起動を記録する。"""
        nonlocal editor_started
        editor_started = True
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(prompt_editor_input_module.subprocess, "run", fake_run)

    with pytest.raises(CmocError, match="editor work file"):
        prompt_editor_input_module.edit_prompt_editor_input(
            tmp_path,
            outside,
            _SKELETON,
        )

    assert editor_started is False
    assert outside.read_text(encoding="utf-8") == "do not overwrite\n"
    assert reserved_work.exists()
    assert not input_copy.exists()


def test_editor_input_keeps_work_file_when_editor_or_cleanup_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """エディタ失敗と確定後の削除失敗では作業 file を残す。"""
    monkeypatch.setattr(
        prompt_editor_input_module,
        "_select_editor",
        lambda: ["fake-editor"],
    )
    failed_editor_work, failed_copy = (
        prompt_editor_input_module.reserve_prompt_editor_input(tmp_path)
    )
    monkeypatch.setattr(
        prompt_editor_input_module.subprocess,
        "run",
        lambda _argv: SimpleNamespace(returncode=7),
    )

    with pytest.raises(CmocError, match="正常終了"):
        prompt_editor_input_module.edit_prompt_editor_input(
            tmp_path,
            failed_editor_work,
            _SKELETON,
        )
    assert failed_editor_work.exists()
    assert not failed_copy.exists()

    failed_finalize_work, saved_copy = (
        prompt_editor_input_module.reserve_prompt_editor_input(tmp_path)
    )

    def successful_editor(argv: list[str]) -> SimpleNamespace:
        """確定後の削除失敗前まで入力処理を成功させる。"""
        Path(argv[-1]).write_text("recoverable input\n", encoding="utf-8")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(
        prompt_editor_input_module.subprocess,
        "run",
        successful_editor,
    )
    prompt_editor_input_module.edit_prompt_editor_input(
        tmp_path,
        failed_finalize_work,
        _SKELETON,
    )
    original_prompt = prompt_editor_input_module.collect_prompt_editor_input(
        tmp_path,
        failed_finalize_work,
        saved_copy,
    )
    assert original_prompt == "recoverable input"
    failed_finalize_work.unlink()
    failed_finalize_work.mkdir()

    with pytest.raises(IsADirectoryError):
        prompt_editor_input_module.finalize_prompt_editor_input(failed_finalize_work)

    assert failed_finalize_work.is_dir()
    assert saved_copy.read_text(encoding="utf-8") == "recoverable input\n"
