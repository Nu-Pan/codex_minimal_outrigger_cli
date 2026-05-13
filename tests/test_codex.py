"""Codex CLI 呼び出しラッパーのテスト。"""

import os
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from commons.codex import run_codex_exec
from commons.errors import CmocError


def test_run_codex_exec_retries_json_and_writes_full_log(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Structured Output の parse 失敗は 3 回までリトライし、試行ログを残す。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    state = tmp_path / "attempts.txt"
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                f"STATE={state}",
                "COUNT=0",
                "if [ -f \"$STATE\" ]; then COUNT=$(cat \"$STATE\"); fi",
                "COUNT=$((COUNT + 1))",
                "echo \"$COUNT\" > \"$STATE\"",
                "if [ \"$COUNT\" -lt 3 ]; then echo 'not-json'; else echo '{\"ok\": true}'; fi",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    output = run_codex_exec(repo, "prompt", read_only=True, expect_json=True)

    log_files = list((repo / ".cmoc" / "logs" / "codex_exec").glob("*.log"))
    log_content = log_files[0].read_text(encoding="utf-8")
    assert output.strip() == '{"ok": true}'
    assert state.read_text(encoding="utf-8").strip() == "3"
    assert "attempt: 1" in log_content
    assert "attempt: 2" in log_content
    assert "attempt: 3" in log_content


def test_run_codex_exec_retries_json_semantic_validation_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Structured Output の意味的失敗も 3 回までリトライする。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    state = tmp_path / "attempts.txt"
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                f"STATE={state}",
                "COUNT=0",
                "if [ -f \"$STATE\" ]; then COUNT=$(cat \"$STATE\"); fi",
                "COUNT=$((COUNT + 1))",
                "echo \"$COUNT\" > \"$STATE\"",
                "if [ \"$COUNT\" -lt 3 ]; then echo '{\"ok\": false}'; else echo '{\"ok\": true}'; fi",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    def validate(value: object) -> None:
        if not isinstance(value, dict) or value.get("ok") is not True:
            raise ValueError("ok must be true.")

    output = run_codex_exec(repo, "prompt", read_only=True, expect_json=True, json_validator=validate)

    log_files = list((repo / ".cmoc" / "logs" / "codex_exec").glob("*.log"))
    log_content = log_files[0].read_text(encoding="utf-8")
    assert output.strip() == '{"ok": true}'
    assert state.read_text(encoding="utf-8").strip() == "3"
    assert "attempt: 1" in log_content
    assert "attempt: 2" in log_content
    assert "attempt: 3" in log_content


def test_run_codex_exec_reports_json_semantic_validation_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Structured Output の意味的失敗が続いたら CmocError で詳細を出す。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "echo '{\"ok\": false}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    def validate(value: object) -> None:
        raise ValueError("ok must be true.")

    with pytest.raises(CmocError) as error:
        run_codex_exec(repo, "prompt", read_only=True, expect_json=True, json_validator=validate)

    assert "Last JSON error: ok must be true." in error.value.detail
    assert "Log:" in error.value.detail
    assert "Last stdout:" in error.value.detail
