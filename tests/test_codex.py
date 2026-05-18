"""Codex CLI 呼び出しラッパーのテスト。"""

import json
import os
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from commons.codex import run_codex_exec
from commons.errors import CmocError

_BOOLEAN_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["ok"],
    "properties": {"ok": {"type": "boolean"}},
}


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
                "if [ \"$COUNT\" -lt 3 ]; then",
                "  echo 'not-json'",
                "else",
                "  echo '{\"ok\": true}'",
                "fi",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    output = run_codex_exec(
        repo,
        "prompt",
        read_only=True,
        expect_json=True,
        output_schema=_BOOLEAN_SCHEMA,
    )

    log_files = list((repo / ".cmoc" / "logs" / "codex_exec").glob("*.log"))
    log_content = log_files[0].read_text(encoding="utf-8")
    assert output.strip() == '{"ok": true}'
    assert state.read_text(encoding="utf-8").strip() == "3"
    assert "attempt: 1" in log_content
    assert "attempt: 2" in log_content
    assert "attempt: 3" in log_content


def test_run_codex_exec_passes_output_schema_file(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Structured Output schema はファイル化して codex exec に渡す。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    args_file = tmp_path / "args.txt"
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                f"printf '%s\\n' \"$@\" > {args_file}",
                "echo '{\"ok\": true}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")
    output = run_codex_exec(
        repo,
        "prompt",
        read_only=True,
        expect_json=True,
        output_schema=_BOOLEAN_SCHEMA,
    )

    args = args_file.read_text(encoding="utf-8").splitlines()
    schema_path = Path(args[args.index("--output-schema") + 1])
    log_content = next(
        (repo / ".cmoc" / "logs" / "codex_exec").glob("*.log")
    ).read_text(encoding="utf-8")
    assert output.strip() == '{"ok": true}'
    assert "--output-schema" in args
    assert (
        json.loads(schema_path.read_text(encoding="utf-8"))
        == _BOOLEAN_SCHEMA
    )
    assert f"output_schema: {schema_path}" in log_content


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
                "if [ \"$COUNT\" -lt 3 ]; then",
                "  echo '{\"ok\": false}'",
                "else",
                "  echo '{\"ok\": true}'",
                "fi",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    def validate(value: object) -> None:
        """`ok` が true になった試行だけを成功にする。"""
        if not isinstance(value, dict) or value.get("ok") is not True:
            raise ValueError("ok must be true.")

    output = run_codex_exec(
        repo,
        "prompt",
        read_only=True,
        expect_json=True,
        output_schema=_BOOLEAN_SCHEMA,
        json_validator=validate,
    )

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
        """常に semantic validation failure を発生させる。"""
        raise ValueError("ok must be true.")

    with pytest.raises(CmocError) as error:
        run_codex_exec(
            repo,
            "prompt",
            read_only=True,
            expect_json=True,
            output_schema=_BOOLEAN_SCHEMA,
            json_validator=validate,
        )

    assert "Last JSON error: ok must be true." in error.value.detail
    assert "Log:" in error.value.detail
    assert "Last stdout:" in error.value.detail


def test_run_codex_exec_requires_schema_for_structured_output(
    tmp_path: Path,
) -> None:
    """Structured Output 扱いの呼び出しは output_schema 未指定を拒否する。"""
    repo = tmp_path / "repo"
    repo.mkdir()

    with pytest.raises(ValueError):
        run_codex_exec(repo, "prompt", read_only=True, expect_json=True)


def test_run_codex_exec_retries_schema_validation_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """output_schema 不一致は cmoc 側検証で 3 回までリトライする。"""
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
                "echo '{\"ok\":\"not boolean\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    with pytest.raises(CmocError) as error:
        run_codex_exec(
            repo,
            "prompt",
            read_only=True,
            expect_json=True,
            output_schema=_BOOLEAN_SCHEMA,
        )

    assert state.read_text(encoding="utf-8").strip() == "3"
    assert "type does not match schema" in error.value.detail
