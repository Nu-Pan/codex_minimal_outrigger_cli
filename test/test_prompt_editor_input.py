"""prompt editor input の外部挙動を検証する。

正本仕様:
- {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
- {{work-root}}/oracle/src/oracle/prompt_builder/editor_input.py
"""

import os
from pathlib import Path
from types import SimpleNamespace

import pytest
from oracle.prompt_builder.editor_input import (
    build_prompt_editor_input_console_guidance,
)

import commons.prompt_editor_input as prompt_editor_input_module
from cmoc_runtime import CmocError

_SKELETON = "# skeleton\n\n{{original-prompt-here}}\n"


def test_editor_input_reuses_saved_path_and_preserves_existing_data(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """同じ本文 path を保存まで使い、timestamp 衝突と旧データの変更を避ける。"""
    timestamps = iter(
        [
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000002000",
        ]
    )
    old_recovery = tmp_path / ".cmoc/gu/editor_input/old_orig.md"
    old_log = tmp_path / ".cmoc/gu/log/editor_input/old_orig.md"
    for existing in (old_recovery, old_log):
        existing.parent.mkdir(parents=True, exist_ok=True)
        existing.write_bytes(b"old input\r\n")
    opened: list[Path] = []
    monkeypatch.setattr(
        prompt_editor_input_module, "timestamp", lambda: next(timestamps)
    )
    monkeypatch.setattr(
        prompt_editor_input_module, "_select_editor", lambda: ["fake-editor"]
    )

    def fake_run(argv: list[str]) -> SimpleNamespace:
        path = Path(argv[-1])
        opened.append(path)
        assert path.read_bytes() == b""
        path.write_text(
            f"<!-- editor note -->\ninput-{len(opened)}\n", encoding="utf-8"
        )
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(prompt_editor_input_module.subprocess, "run", fake_run)
    paths = []
    for number in (1, 2):
        input_path = prompt_editor_input_module.reserve_prompt_editor_input(tmp_path)
        paths.append(input_path)
        assert input_path.parent == old_log.parent
        prompt_editor_input_module.edit_prompt_editor_input(
            tmp_path, input_path, _SKELETON
        )
        original_prompt = prompt_editor_input_module.collect_prompt_editor_input(
            tmp_path, input_path
        )
        assert original_prompt == f"<!-- editor note -->\ninput-{number}"
        assert input_path.read_text(encoding="utf-8") == original_prompt + "\n"

    assert opened == paths
    assert [path.name for path in paths] == [
        "2026-06-27_10-00_00_000001000_orig.md",
        "2026-06-27_10-00_00_000002000_orig.md",
    ]
    assert paths[0].read_text(encoding="utf-8") == "<!-- editor note -->\ninput-1\n"
    assert set(old_log.parent.iterdir()) == {old_log, *paths}
    assert list(old_recovery.parent.iterdir()) == [old_recovery]
    assert old_log.read_bytes() == old_recovery.read_bytes() == b"old input\r\n"
    captured = capsys.readouterr()
    assert captured.out == ""
    guidance = build_prompt_editor_input_console_guidance()
    assert captured.err.count(guidance) == 2
    handoff_lines = captured.err.replace(guidance, "").splitlines()
    assert len(handoff_lines) == 2
    assert all(
        line.startswith("editor input handoff target ID: eit_")
        for line in handoff_lines
    )


def test_editor_input_freezes_one_final_read_for_storage_and_prompt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """最終読み取り後の再編集にかかわらず、保存と抽出に固定した原文を使う。"""
    input_path = prompt_editor_input_module.reserve_prompt_editor_input(tmp_path)
    raw_input = "  <!-- note -->\r\n確定した入力\r\n".encode("utf-8")
    input_path.write_bytes(raw_input)
    original_read_bytes = Path.read_bytes
    final_reads = 0

    def read_then_edit(path: Path) -> bytes:
        nonlocal final_reads
        content = original_read_bytes(path)
        if path == input_path:
            final_reads += 1
            path.write_text("later human edit", encoding="utf-8")
        return content

    monkeypatch.setattr(Path, "read_bytes", read_then_edit)
    original_prompt = prompt_editor_input_module.collect_prompt_editor_input(
        tmp_path, input_path
    )

    assert final_reads == 1
    assert original_read_bytes(input_path) == raw_input
    assert original_prompt == raw_input.decode("utf-8").strip()


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
    input_path = prompt_editor_input_module.reserve_prompt_editor_input(tmp_path)
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
        input_path,
        _SKELETON,
    )

    expected_argv = [f"/fake/{expected_editor}"]
    if wait_for_editor:
        expected_argv.append("--wait")
    assert calls == [[*expected_argv, str(input_path)]]


@pytest.mark.parametrize("replacement", ["symlink", "directory", "missing", "fifo"])
def test_editor_input_rejects_invalid_final_file_without_reading(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    replacement: str,
) -> None:
    """通常 file 以外の入力は読み取りも上書きも行わない。"""
    input_path = prompt_editor_input_module.reserve_prompt_editor_input(tmp_path)
    outside = tmp_path / "outside.md"
    outside.write_text("must remain", encoding="utf-8")
    input_path.unlink()
    if replacement == "symlink":
        input_path.symlink_to(outside)
    elif replacement == "directory":
        input_path.mkdir()
    elif replacement == "fifo":
        os.mkfifo(input_path)

    def unexpected_read(_path: Path) -> bytes:
        pytest.fail("invalid input must not be read")

    monkeypatch.setattr(Path, "read_bytes", unexpected_read)
    with pytest.raises(CmocError, match="editor input file"):
        prompt_editor_input_module.collect_prompt_editor_input(tmp_path, input_path)
    assert outside.read_text(encoding="utf-8") == "must remain"


@pytest.mark.parametrize(
    "relative_path", ["outside.md", ".cmoc/gu/editor_input/recovery.md"]
)
@pytest.mark.parametrize("operation", ["edit", "collect"])
def test_editor_input_rejects_path_outside_input_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    relative_path: str,
    operation: str,
) -> None:
    """旧復旧先を含む所定 directory 外の file を編集・確定しない。"""
    reserved = prompt_editor_input_module.reserve_prompt_editor_input(tmp_path)
    outside = tmp_path / relative_path
    outside.parent.mkdir(parents=True, exist_ok=True)
    outside.write_text("do not overwrite\n", encoding="utf-8")

    def unexpected_run(_argv: list[str]) -> SimpleNamespace:
        pytest.fail("invalid input must not reach the editor")

    monkeypatch.setattr(prompt_editor_input_module.subprocess, "run", unexpected_run)
    with pytest.raises(CmocError, match="editor input file"):
        if operation == "edit":
            prompt_editor_input_module.edit_prompt_editor_input(
                tmp_path, outside, _SKELETON
            )
        else:
            prompt_editor_input_module.collect_prompt_editor_input(tmp_path, outside)
    assert outside.read_text(encoding="utf-8") == "do not overwrite\n"
    assert reserved.exists()


@pytest.mark.parametrize("symlinked_directory", ["gu", "log"])
def test_editor_input_rejects_symlinked_storage_directory(
    tmp_path: Path,
    symlinked_directory: str,
) -> None:
    """保存先 directory の symlink をたどって外部へ作成しない。"""
    root = tmp_path / "repository"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    gu = root / ".cmoc" / "gu"
    gu.mkdir(parents=True)
    if symlinked_directory == "gu":
        gu.rmdir()
        gu.symlink_to(outside, target_is_directory=True)
    else:
        (gu / "log").symlink_to(outside, target_is_directory=True)

    with pytest.raises(CmocError, match="保存先"):
        prompt_editor_input_module.reserve_prompt_editor_input(root)

    assert not (outside / "editor_input").exists()
    assert not (outside / "log").exists()


def test_editor_input_closes_handoff_when_target_id_display_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """target ID の表示失敗でも一時 handoff target を残さない。"""
    input_path = prompt_editor_input_module.reserve_prompt_editor_input(tmp_path)
    closed = False

    class FakeTarget:
        """target close の呼び出しだけを記録する。"""

        target_id = "eit_test"

        def close(self) -> None:
            nonlocal closed
            closed = True

    monkeypatch.setattr(
        prompt_editor_input_module,
        "_select_editor",
        lambda: ["fake-editor"],
    )
    monkeypatch.setattr(
        prompt_editor_input_module,
        "start_editor_input_handoff",
        lambda _root, _path, _skeleton: FakeTarget(),
    )

    def fail_print(*_args: object, **_kwargs: object) -> None:
        """target ID 表示の失敗を再現する。"""
        raise BrokenPipeError

    monkeypatch.setattr(
        prompt_editor_input_module,
        "print",
        fail_print,
        raising=False,
    )

    with pytest.raises(BrokenPipeError):
        prompt_editor_input_module.edit_prompt_editor_input(
            tmp_path,
            input_path,
            _SKELETON,
        )

    assert closed
    assert input_path.exists()


def test_editor_input_keeps_input_when_editor_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """エディタ失敗時は入力を復旧用に残し、handoff guide は削除する。"""
    input_path = prompt_editor_input_module.reserve_prompt_editor_input(tmp_path)
    monkeypatch.setattr(
        prompt_editor_input_module, "_select_editor", lambda: ["fake-editor"]
    )

    def failed_editor(argv: list[str]) -> SimpleNamespace:
        Path(argv[-1]).write_text("recoverable input\n", encoding="utf-8")
        return SimpleNamespace(returncode=7)

    monkeypatch.setattr(prompt_editor_input_module.subprocess, "run", failed_editor)
    with pytest.raises(CmocError, match="正常終了"):
        prompt_editor_input_module.edit_prompt_editor_input(
            tmp_path, input_path, _SKELETON
        )
    assert input_path.read_text(encoding="utf-8") == "recoverable input\n"
    assert list(input_path.parent.iterdir()) == [input_path]


@pytest.mark.parametrize("failure_stage", ["write", "flush", "replace"])
def test_editor_input_preserves_input_when_final_save_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_stage: str,
) -> None:
    """保存途中の書き込み・flush・置換の失敗で、本文を失わない。"""
    input_path = prompt_editor_input_module.reserve_prompt_editor_input(tmp_path)
    raw_input = b"recoverable input\r\n"
    input_path.write_bytes(raw_input)
    real_temporary_file = prompt_editor_input_module.tempfile.NamedTemporaryFile

    def fail(*_args, **_kwargs):
        raise OSError("save failed")

    if failure_stage == "write":

        def partial_write_file(*args, **kwargs):
            temporary = real_temporary_file(*args, **kwargs)
            write = temporary.write

            def partial_write(content):
                write(content[:3])
                fail()

            monkeypatch.setattr(temporary, "write", partial_write)
            return temporary

        monkeypatch.setattr(
            prompt_editor_input_module.tempfile,
            "NamedTemporaryFile",
            partial_write_file,
        )
    elif failure_stage == "flush":
        monkeypatch.setattr(prompt_editor_input_module.os, "fsync", fail)
    else:
        monkeypatch.setattr(prompt_editor_input_module.os, "replace", fail)

    with pytest.raises(OSError, match="save failed"):
        prompt_editor_input_module.collect_prompt_editor_input(tmp_path, input_path)
    assert input_path.read_bytes() == raw_input
    assert list(input_path.parent.iterdir()) == [input_path]
