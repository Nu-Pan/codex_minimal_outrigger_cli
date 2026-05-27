"""Codex CLI 呼び出しラッパーのテスト。"""

import io
import json
import os
import subprocess
from hashlib import sha256
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from commons.codex import run_codex_exec
from commons.errors import CmocError
from commons.subcommand_log import _TeeTextIO
from commons.subcommand_log import subcommand_log

_BOOLEAN_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["ok"],
    "properties": {"ok": {"type": "boolean"}},
}
_ENUM_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["severity"],
    "properties": {
        "severity": {
            "type": "string",
            "enum": ["fatal", "warning", "inconclusive"],
            "description": "問題点の分類。",
        },
    },
}


def test_run_codex_exec_retries_json_and_writes_full_log(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Structured Output の parse 失敗は 3 回までリトライし、各呼び出しログを残す。"""
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
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                f"STATE={state}",
                "COUNT=0",
                "if [ -f \"$STATE\" ]; then COUNT=$(cat \"$STATE\"); fi",
                "COUNT=$((COUNT + 1))",
                "echo \"$COUNT\" > \"$STATE\"",
                "if [ \"$COUNT\" -lt 3 ]; then",
                "  echo 'not-json' > \"$LAST\"",
                "else",
                "  echo '{\"ok\": true}' > \"$LAST\"",
                "fi",
                "echo '{\"event\":\"done\"}'",
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

    log_files = sorted(
        (repo / ".cmoc" / "logs" / "codex_exec" / "call").glob("*.log")
    )
    log_contents = [path.read_text(encoding="utf-8") for path in log_files]
    assert output.strip() == '{"ok": true}'
    assert state.read_text(encoding="utf-8").strip() == "3"
    assert len(log_files) == 3
    assert all(content.startswith("---\n") for content in log_contents)
    attempt_flags = [
        f"attempt: {index}" in content
        for index, content in enumerate(log_contents, 1)
    ]
    assert attempt_flags == [True, True, True]
    assert all("returncode: 0" in content for content in log_contents)
    assert all(
        content.count("## Codex Exec Call") == 1
        for content in log_contents
    )
    assert not any("## Attempt 1" in content for content in log_contents)
    captured = capsys.readouterr().out
    assert "codex exec attempt (1/3) prompt:" in captured
    assert "codex exec attempt (3/3) output:" in captured


def test_run_codex_exec_notifies_console_and_subcommand_log(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Codex CLI 呼び出し通知は目的・相対ログ・時間・戻り値を tee する。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "echo 'ok' > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    with subcommand_log(repo):
        output = run_codex_exec(
            repo,
            "prompt",
            purpose="unit test codex call",
            read_only=True,
        )

    captured = capsys.readouterr().out
    subcommand_logs = list(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.log")
    )
    log_content = subcommand_logs[0].read_text(encoding="utf-8")
    notification_head = (
        "codex exec: unit test codex call "
        "log=.cmoc/logs/codex_exec/call/"
    )
    assert output == "ok\n"
    assert notification_head in captured
    assert " elapsed=" in captured
    assert " returncode=0" in captured
    assert notification_head in log_content
    assert " elapsed=" in log_content
    assert " returncode=0" in log_content


def test_run_codex_exec_rejects_uncommitted_oracle_change_after_workspace_write(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """workspace-write 後の未コミット oracle ファイル差分は共通処理で拒否する。"""
    repo = _init_git_repo(tmp_path)
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "mkdir -p oracles",
                "echo 'changed by codex' > oracles/spec.md",
                "echo 'ok' > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
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
            read_only=False,
            skip_index_maintenance=True,
        )

    assert "oracles ファイルを変更しました" in error.value.message
    assert "未コミット差分:" in error.value.detail
    assert "oracles/spec.md" in error.value.detail


def test_run_codex_exec_rejects_committed_oracle_change_after_workspace_write(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """workspace-write 実行中の commit range に含まれる oracle 変更を拒否する。"""
    repo = _init_git_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("initial spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")
    _git(repo, "commit", "-m", "add oracle")
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "echo 'committed by codex' > oracles/spec.md",
                "git add oracles/spec.md",
                "git commit -m 'codex oracle change' >/dev/null",
                "echo 'ok' > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
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
            read_only=False,
            skip_index_maintenance=True,
        )

    assert "Codex CLI 実行中の commit range 変更:" in error.value.detail
    assert "oracles/spec.md" in error.value.detail
    assert _git(repo, "status", "--porcelain", "--", "oracles").stdout == ""


def test_run_codex_exec_allows_oracles_index_and_ignored_paths(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """oracles 配下でも INDEX.md と root .gitignore 対象は oracle ファイル扱いしない。"""
    repo = _init_git_repo(tmp_path)
    (repo / ".gitignore").write_text("oracles/ignored.md\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "add gitignore")
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "mkdir -p oracles",
                "echo 'index' > oracles/INDEX.md",
                "echo 'ignored' > oracles/ignored.md",
                "echo 'ok' > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    output = run_codex_exec(
        repo,
        "prompt",
        read_only=False,
        skip_index_maintenance=True,
    )

    assert output == "ok\n"


def test_subcommand_log_avoids_existing_timestamp_file(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """サブコマンドログは timestamp 衝突時に既存ファイルへ追記しない。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    log_dir = repo / ".cmoc" / "logs" / "sub_commands"
    log_dir.mkdir(parents=True)
    existing_log = log_dir / "2026-05-04_03-02_01_001.log"
    existing_log.write_text("existing log\n", encoding="utf-8")
    timestamps = iter(
        [
            "2026-05-04_03-02_01_001",
            "2026-05-04_03-02_01_002",
        ]
    )
    monkeypatch.setattr(
        "commons.subcommand_log.make_timestamp",
        lambda: next(timestamps),
    )

    with subcommand_log(repo):
        print("new invocation")

    new_log = log_dir / "2026-05-04_03-02_01_002.log"
    assert existing_log.read_text(encoding="utf-8") == "existing log\n"
    assert new_log.exists()
    assert "new invocation" in new_log.read_text(encoding="utf-8")


def test_subcommand_log_excludes_logs_in_linked_worktree(
    tmp_path: Path,
) -> None:
    """`.git` が file の worktree でも実 gitdir の exclude にログ除外を入れる。"""
    repo = _init_git_repo(tmp_path)
    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "-b", "linked", str(linked))

    with subcommand_log(linked):
        print("linked worktree invocation")

    exclude_path = Path(
        _git(
            linked,
            "rev-parse",
            "--path-format=absolute",
            "--git-path",
            "info/exclude",
        ).stdout.strip()
    )
    assert (linked / ".git").is_file()
    assert "/.cmoc/logs/" in exclude_path.read_text(encoding="utf-8")
    assert _git(linked, "status", "--porcelain").stdout == ""


def test_tee_text_io_writes_log_when_console_write_fails() -> None:
    """console write 失敗時も log file sink への write は試行済みにする。"""
    log_file = io.StringIO()
    tee = _TeeTextIO(_FailingTextIO(fail_write=True), log_file)

    with pytest.raises(BrokenPipeError):
        tee.write("durable log\n")

    assert log_file.getvalue() == "durable log\n"


def test_tee_text_io_flushes_log_when_console_flush_fails() -> None:
    """console flush 失敗時も log file sink への flush は試行済みにする。"""
    log_file = _RecordingTextIO()
    tee = _TeeTextIO(_FailingTextIO(fail_flush=True), log_file)

    with pytest.raises(BrokenPipeError):
        tee.flush()

    assert log_file.flushed


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
    stdin_file = tmp_path / "stdin.txt"
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                f"printf '%s\\n' \"$@\" > {args_file}",
                f"cat > {stdin_file}",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "echo '{\"ok\": true}' > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
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
    schema_files = list(
        (repo / ".cmoc" / "logs" / "codex_exec" / "output_schema").glob("*.log")
    )
    second_output = run_codex_exec(
        repo,
        "prompt",
        read_only=True,
        expect_json=True,
        output_schema=_BOOLEAN_SCHEMA,
    )

    args = args_file.read_text(encoding="utf-8").splitlines()
    stdin_prompt = stdin_file.read_text(encoding="utf-8")
    schema_path = Path(args[args.index("--output-schema") + 1])
    last_message_path = Path(args[args.index("--output-last-message") + 1])
    log_contents = [
        path.read_text(encoding="utf-8")
        for path in (
            repo / ".cmoc" / "logs" / "codex_exec" / "call"
        ).glob("*.log")
    ]
    schema_body = json.dumps(
        _BOOLEAN_SCHEMA,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    schema_hash = sha256(schema_body.encode("utf-8")).hexdigest()
    assert output.strip() == '{"ok": true}'
    assert second_output.strip() == '{"ok": true}'
    assert "--json" in args
    assert "--output-last-message" in args
    assert last_message_path.parent == (
        repo / ".cmoc" / "logs" / "codex_exec" / "output_last_message"
    )
    assert last_message_path.suffix == ".log"
    assert "--model" in args
    assert "-c" in args
    assert args[-1] == "-"
    assert "prompt" not in args
    assert stdin_prompt == "prompt"
    assert 'model_reasoning_effort="medium"' in args
    assert "--output-schema" in args
    assert schema_path == (
        repo
        / ".cmoc"
        / "logs"
        / "codex_exec"
        / "output_schema"
        / f"{schema_hash}.log"
    )
    assert schema_path.read_text(encoding="utf-8") == schema_body
    assert schema_files == [schema_path]
    assert list(
        (repo / ".cmoc" / "logs" / "codex_exec" / "output_schema").glob("*.log")
    ) == [schema_path]
    assert any(
        f"output_schema: \"{schema_path}\"" in content
        for content in log_contents
    )
    assert any(
        f"output_last_message: \"{last_message_path}\"" in content
        for content in log_contents
    )


def test_run_codex_exec_prints_output_head80_before_escaping_newlines(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """回収出力の進捗は元文字列を 80 文字で切ってから改行を可視化する。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "printf '%079d\\nbbbbbbbbbb' 0 | tr '0' 'a' > \"$LAST\"",
                "printf '%079d\\nbbbbbbbbbb' 0 | tr '0' 'a'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")
    prompt = "p" * 79 + "\n" + "q" * 10

    run_codex_exec(repo, prompt, read_only=True)

    captured = capsys.readouterr().out
    assert f"prompt: {'p' * 79}\\n" in captured
    assert f"output: {'a' * 79}\\n" in captured
    assert "q" not in captured
    assert "b" not in captured


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
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                f"STATE={state}",
                "COUNT=0",
                "if [ -f \"$STATE\" ]; then COUNT=$(cat \"$STATE\"); fi",
                "COUNT=$((COUNT + 1))",
                "echo \"$COUNT\" > \"$STATE\"",
                "if [ \"$COUNT\" -lt 3 ]; then",
                "  echo '{\"ok\": false}' > \"$LAST\"",
                "else",
                "  echo '{\"ok\": true}' > \"$LAST\"",
                "fi",
                "echo '{\"event\":\"done\"}'",
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

    log_contents = [
        path.read_text(encoding="utf-8")
        for path in sorted(
            (repo / ".cmoc" / "logs" / "codex_exec" / "call").glob("*.log")
        )
    ]
    assert output.strip() == '{"ok": true}'
    assert state.read_text(encoding="utf-8").strip() == "3"
    assert len(log_contents) == 3
    assert all(
        content.count("## Codex Exec Call") == 1
        for content in log_contents
    )
    attempt_flags = [
        f"attempt: {index}" in content
        for index, content in enumerate(log_contents, 1)
    ]
    assert attempt_flags == [True, True, True]


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
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "echo '{\"ok\": false}' > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
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

    assert "Last validation error: ok must be true." in error.value.detail
    assert "Log:" in error.value.detail
    assert "Last stdout:" in error.value.detail


def test_run_codex_exec_retries_text_semantic_validation_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """非 JSON 出力の意味的失敗も 3 回までリトライする。"""
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
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                f"STATE={state}",
                "COUNT=0",
                "if [ -f \"$STATE\" ]; then COUNT=$(cat \"$STATE\"); fi",
                "COUNT=$((COUNT + 1))",
                "echo \"$COUNT\" > \"$STATE\"",
                "if [ \"$COUNT\" -lt 3 ]; then",
                "  echo 'incomplete report' > \"$LAST\"",
                "else",
                "  echo 'complete report' > \"$LAST\"",
                "fi",
                "echo '{\"event\":\"done\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    def validate(value: str) -> None:
        """complete を含む出力だけを成功にする。"""
        if value.strip() != "complete report":
            raise ValueError("report is incomplete.")

    output = run_codex_exec(
        repo,
        "prompt",
        read_only=True,
        text_validator=validate,
    )

    log_contents = [
        path.read_text(encoding="utf-8")
        for path in sorted(
            (repo / ".cmoc" / "logs" / "codex_exec" / "call").glob("*.log")
        )
    ]
    assert output.strip() == "complete report"
    assert state.read_text(encoding="utf-8").strip() == "3"
    assert len(log_contents) == 3
    assert all(
        content.count("## Codex Exec Call") == 1
        for content in log_contents
    )
    attempt_flags = [
        f"attempt: {index}" in content
        for index, content in enumerate(log_contents, 1)
    ]
    assert attempt_flags == [True, True, True]


def test_run_codex_exec_retries_missing_last_message_without_validator(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """検証なしの非 JSON 呼び出しでも last message 欠落はリトライする。"""
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
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                f"STATE={state}",
                "COUNT=0",
                "if [ -f \"$STATE\" ]; then COUNT=$(cat \"$STATE\"); fi",
                "COUNT=$((COUNT + 1))",
                "echo \"$COUNT\" > \"$STATE\"",
                "if [ \"$COUNT\" -ge 2 ]; then",
                "  echo 'plain text result' > \"$LAST\"",
                "fi",
                "echo '{\"event\":\"done\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    output = run_codex_exec(repo, "prompt", read_only=True)

    log_files = sorted(
        (repo / ".cmoc" / "logs" / "codex_exec" / "call").glob("*.log")
    )
    assert output.strip() == "plain text result"
    assert state.read_text(encoding="utf-8").strip() == "2"
    assert len(log_files) == 2
    assert [
        f"attempt: {index}" in path.read_text(encoding="utf-8")
        for index, path in enumerate(log_files, 1)
    ] == [True, True]


def test_run_codex_exec_reports_text_semantic_validation_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """非 JSON 出力の意味的失敗が続いたら CmocError で詳細を出す。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "echo 'incomplete report' > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    def validate(value: str) -> None:
        """常に semantic validation failure を発生させる。"""
        raise ValueError("report is incomplete.")

    with pytest.raises(CmocError) as error:
        run_codex_exec(
            repo,
            "prompt",
            read_only=True,
            text_validator=validate,
        )

    assert "Last validation error: report is incomplete." in error.value.detail
    assert "Output schema: none" in error.value.detail
    assert "Last stdout:" in error.value.detail


def test_run_codex_exec_requires_schema_for_structured_output(
    tmp_path: Path,
) -> None:
    """Structured Output 扱いの呼び出しは output_schema 未指定を拒否する。"""
    repo = tmp_path / "repo"
    repo.mkdir()

    with pytest.raises(ValueError):
        run_codex_exec(repo, "prompt", read_only=True, expect_json=True)


def test_run_codex_exec_rejects_forbidden_reasoning_effort(
    tmp_path: Path,
) -> None:
    """oracle が禁止する xhigh reasoning effort は起動前に拒否する。"""
    repo = tmp_path / "repo"
    repo.mkdir()

    with pytest.raises(ValueError):
        run_codex_exec(
            repo,
            "prompt",
            read_only=True,
            reasoning_effort="xhigh",
        )


def test_run_codex_exec_allows_high_reasoning_effort(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """品質重視用途向けの high reasoning effort を Codex CLI に渡せる。"""
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
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "echo done > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
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
        reasoning_effort="high",
    )

    args = args_file.read_text(encoding="utf-8").splitlines()
    assert output.strip() == "done"
    assert 'model_reasoning_effort="high"' in args


def test_run_codex_exec_waits_and_resumes_after_quota_exhaustion(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """quota 枯渇時は疎通確認後に --resume 付きで同じ prompt を再実行する。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    args_file = tmp_path / "args.txt"
    prompts_file = tmp_path / "prompts.txt"
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                f"printf '%s\\n' \"$@\" >> {args_file}",
                "PROMPT=\"$(cat)\"",
                f"printf '%s\\n---END---\\n' \"$PROMPT\" >> {prompts_file}",
                "LAST=''",
                "PREV=''",
                "HAS_RESUME=0",
                "for ARG in \"$@\"; do",
                "  if [ \"$ARG\" = \"--resume\" ]; then HAS_RESUME=1; fi",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "if [ \"$PROMPT\" = \"original prompt\" ]; then",
                "  if [ \"$HAS_RESUME\" = 0 ]; then",
                "  echo '{\"session_id\":\"session-1\"}'",
                "  echo '{\"type\":\"error\","
                "\"error\":{\"code\":\"insufficient_quota\"}}'",
                "  echo 'quota limit exhausted' >&2",
                "  exit 1",
                "  fi",
                "fi",
                "if [[ \"$PROMPT\" == *'Codex CLI の疎通確認担当'* ]]; then",
                "  if [[ \"$PROMPT\" != "
                "*'/memo` は読み書き禁止です。'* ]]; then exit 2; fi",
                "  if [[ \"$PROMPT\" != *'ファイル編集は禁止です。'* ]]; then exit 2; fi",
                "  echo ok > \"$LAST\"",
                "  echo '{\"event\":\"poll-ok\"}'",
                "  exit 0",
                "fi",
                "echo resumed > \"$LAST\"",
                "echo '{\"event\":\"resumed\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)

    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setattr("commons.codex.time.sleep", lambda seconds: None)

    calls: list[Path] = []

    def fake_maintain(repo_root: Path) -> bool:
        """quota 復旧経路を含む Codex CLI 直前メンテナンスを記録する。"""
        calls.append(repo_root)
        return False

    monkeypatch.setattr("commons.indexing.maintain_indexes", fake_maintain)

    output = run_codex_exec(repo, "original prompt", read_only=True)

    args = args_file.read_text(encoding="utf-8")
    prompts = prompts_file.read_text(encoding="utf-8")
    captured = capsys.readouterr().out
    log_contents = [
        path.read_text(encoding="utf-8")
        for path in sorted(
            (repo / ".cmoc" / "logs" / "codex_exec" / "call").glob("*.log")
        )
    ]
    assert output.strip() == "resumed"
    assert calls == [repo, repo, repo]
    assert len(log_contents) == 3
    assert all(
        content.count("## Codex Exec Call") == 1
        for content in log_contents
    )
    assert any("quota limit exhausted" in content for content in log_contents)
    assert any("Codex CLI の疎通確認担当" in content for content in log_contents)
    assert any("--resume" in content for content in log_contents)
    assert "original prompt" not in args
    assert "Codex CLI の疎通確認担当" not in args
    assert "--resume\nsession-1" in args
    assert args.count("\n-\n") == 3
    assert "original prompt" in prompts
    assert "Codex CLI の疎通確認担当" in prompts
    assert "/memo` は読み書き禁止です。" in prompts
    assert "quota exhausted; waiting before resume" in captured
    assert "quota poll prompt: あなたは Codex CLI の疎通確認担当です。" in captured
    assert "quota poll output: ok" in captured
    assert "quota restored; resuming codex exec" in captured


def test_run_codex_exec_fails_when_resume_returns_unexpected_error(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """quota 復旧後の resume が想定外エラーなら即時 CmocError にする。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "HAS_RESUME=0",
                "for ARG in \"$@\"; do",
                "  if [ \"$ARG\" = \"--resume\" ]; then HAS_RESUME=1; fi",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "PROMPT=\"$(cat)\"",
                "if [[ \"$PROMPT\" == *'Codex CLI の疎通確認担当'* ]]; then",
                "  if [[ \"$PROMPT\" != "
                "*'/memo` は読み書き禁止です。'* ]]; then exit 2; fi",
                "  if [[ \"$PROMPT\" != *'ファイル編集は禁止です。'* ]]; then exit 2; fi",
                "  echo ok > \"$LAST\"",
                "  exit 0",
                "fi",
                "if [ \"$HAS_RESUME\" = 0 ]; then",
                "  echo '{\"session_id\":\"session-1\"}'",
                "  echo '{\"type\":\"error\","
                "\"error\":{\"code\":\"insufficient_quota\"}}'",
                "  echo 'quota limit exhausted' >&2",
                "  exit 1",
                "fi",
                "echo 'repository failure' >&2",
                "exit 2",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)

    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setattr("commons.codex.time.sleep", lambda seconds: None)

    with pytest.raises(CmocError) as error:
        run_codex_exec(repo, "original prompt", read_only=True)

    assert "codex exec が失敗しました。" in error.value.message
    assert "repository failure" in error.value.detail


def test_run_codex_exec_does_not_treat_plain_limit_error_as_quota(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """quota 明示でない limit 系エラーは待機せず即時失敗する。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "echo 'validation limit exceeded while processing input' >&2",
                "exit 2",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)

    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    with pytest.raises(CmocError) as error:
        run_codex_exec(repo, "original prompt", read_only=True)

    log_files = sorted(
        (repo / ".cmoc" / "logs" / "codex_exec" / "call").glob("*.log")
    )
    assert "codex exec が失敗しました。" in error.value.message
    assert "validation limit exceeded" in error.value.detail
    assert len(log_files) == 1


def test_run_codex_exec_fails_when_quota_poll_returns_unexpected_error(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """quota poll 自体の非 quota エラーは待機継続せず失敗する。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "PROMPT=\"$(cat)\"",
                "if [[ \"$PROMPT\" == *'Codex CLI の疎通確認担当'* ]]; then",
                "  echo 'network failure during poll' >&2",
                "  exit 2",
                "fi",
                "echo '{\"session_id\":\"session-1\"}'",
                "echo '{\"type\":\"error\","
                "\"error\":{\"code\":\"insufficient_quota\"}}'",
                "echo 'quota exhausted' >&2",
                "exit 1",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)

    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setattr("commons.codex.time.sleep", lambda seconds: None)

    with pytest.raises(CmocError) as error:
        run_codex_exec(repo, "original prompt", read_only=True)

    log_files = sorted(
        (repo / ".cmoc" / "logs" / "codex_exec" / "call").glob("*.log")
    )
    assert "codex exec が失敗しました。" in error.value.message
    assert "network failure during poll" in error.value.detail
    assert len(log_files) == 2


def test_run_codex_exec_requires_ok_last_message_for_quota_poll(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """quota poll が 0 終了でも last message が ok 以外なら resume しない。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "PROMPT=\"$(cat)\"",
                "if [[ \"$PROMPT\" == *'Codex CLI の疎通確認担当'* ]]; then",
                "  echo 'not-ok' > \"$LAST\"",
                "  exit 0",
                "fi",
                "echo '{\"session_id\":\"session-1\"}'",
                "echo '{\"type\":\"error\","
                "\"error\":{\"code\":\"insufficient_quota\"}}'",
                "echo 'quota exhausted' >&2",
                "exit 1",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)

    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setattr("commons.codex.time.sleep", lambda seconds: None)

    with pytest.raises(CmocError) as error:
        run_codex_exec(repo, "original prompt", read_only=True)

    log_contents = [
        path.read_text(encoding="utf-8")
        for path in sorted(
            (repo / ".cmoc" / "logs" / "codex_exec" / "call").glob("*.log")
        )
    ]
    assert "quota 復旧確認に失敗しました。" in error.value.message
    assert "quota poll output-last-message was not ok." in error.value.detail
    assert not any("--resume" in content for content in log_contents)


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
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                f"STATE={state}",
                "COUNT=0",
                "if [ -f \"$STATE\" ]; then COUNT=$(cat \"$STATE\"); fi",
                "COUNT=$((COUNT + 1))",
                "echo \"$COUNT\" > \"$STATE\"",
                "echo '{\"ok\":\"not boolean\"}' > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
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
    assert "'not boolean' is not of type 'boolean'" in error.value.detail


def test_run_codex_exec_validates_output_schema_without_expect_json(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """output_schema 指定時は expect_json=False でも cmoc 側で schema 検証する。"""
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
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                f"STATE={state}",
                "COUNT=0",
                "if [ -f \"$STATE\" ]; then COUNT=$(cat \"$STATE\"); fi",
                "COUNT=$((COUNT + 1))",
                "echo \"$COUNT\" > \"$STATE\"",
                "echo '{\"ok\":\"not boolean\"}' > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
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
            output_schema=_BOOLEAN_SCHEMA,
        )

    assert state.read_text(encoding="utf-8").strip() == "3"
    assert "有効な JSON" in error.value.message
    assert "'not boolean' is not of type 'boolean'" in error.value.detail


def test_run_codex_exec_retries_enum_validation_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Structured Output の enum 不一致も cmoc 側 schema 検証でリトライする。"""
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
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                f"STATE={state}",
                "COUNT=0",
                "if [ -f \"$STATE\" ]; then COUNT=$(cat \"$STATE\"); fi",
                "COUNT=$((COUNT + 1))",
                "echo \"$COUNT\" > \"$STATE\"",
                "if [ \"$COUNT\" -eq 1 ]; then",
                "  echo '{\"severity\":\"severe\"}' > \"$LAST\"",
                "else",
                "  echo '{\"severity\":\"fatal\"}' > \"$LAST\"",
                "fi",
                "echo '{\"event\":\"done\"}'",
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
        output_schema=_ENUM_SCHEMA,
    )

    assert output.strip() == '{"severity":"fatal"}'
    assert state.read_text(encoding="utf-8").strip() == "2"


def test_run_codex_exec_validates_json_schema_string_length(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """JSON Schema の文字列長制約も cmoc 側 schema 検証で検査する。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "echo '{\"name\":\"x\"}' > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")
    length_schema: dict[str, object] = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "minLength": 2,
            },
        },
    }

    with pytest.raises(CmocError) as error:
        run_codex_exec(
            repo,
            "prompt",
            read_only=True,
            expect_json=True,
            output_schema=length_schema,
        )

    assert "'x' is too short" in error.value.detail


def test_run_codex_exec_maintains_indexes_before_codex_call(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """通常の Codex CLI 呼び出し直前に INDEX.md メンテナンスを実行する。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    calls: list[Path] = []
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "echo done > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)

    def fake_maintain(repo_root: Path) -> bool:
        """run_codex_exec 直前メンテナンスの呼び出しを記録する。"""
        calls.append(repo_root)
        return False

    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setattr("commons.indexing.maintain_indexes", fake_maintain)

    output = run_codex_exec(repo, "prompt", read_only=True)

    assert output.strip() == "done"
    assert calls == [repo]


def test_run_codex_exec_maintains_indexes_before_each_retry(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """レスポンス検証失敗後の retry でも Codex CLI 直前に INDEX.md を保守する。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    state = tmp_path / "attempts.txt"
    maintain_file = tmp_path / "maintain.txt"
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                f"STATE={state}",
                "COUNT=0",
                "if [ -f \"$STATE\" ]; then COUNT=$(cat \"$STATE\"); fi",
                "COUNT=$((COUNT + 1))",
                "echo \"$COUNT\" > \"$STATE\"",
                f"if [ \"$(wc -l < {maintain_file})\" -lt \"$COUNT\" ]; then",
                "  exit 3",
                "fi",
                "if [ \"$COUNT\" -lt 3 ]; then",
                "  echo 'not-json' > \"$LAST\"",
                "else",
                "  echo '{\"ok\": true}' > \"$LAST\"",
                "fi",
                "echo '{\"event\":\"done\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    calls: list[Path] = []

    def fake_maintain(repo_root: Path) -> bool:
        """Codex CLI retry 直前メンテナンスの呼び出しを記録する。"""
        calls.append(repo_root)
        with maintain_file.open("a", encoding="utf-8") as handle:
            handle.write("maintain\n")
        return False

    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setattr("commons.indexing.maintain_indexes", fake_maintain)

    output = run_codex_exec(
        repo,
        "prompt",
        read_only=True,
        expect_json=True,
        output_schema=_BOOLEAN_SCHEMA,
    )

    assert output.strip() == '{"ok": true}'
    assert calls == [repo, repo, repo]


def test_run_codex_exec_can_skip_index_maintenance(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX 生成や merge conflict 解消用に事前メンテナンスを明示スキップできる。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    codex = fake_bin / "codex"
    codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "LAST=''",
                "PREV=''",
                "for ARG in \"$@\"; do",
                "  if [ \"$PREV\" = \"--output-last-message\" ]; then",
                "    LAST=\"$ARG\"",
                "  fi",
                "  PREV=\"$ARG\"",
                "done",
                "echo done > \"$LAST\"",
                "echo '{\"event\":\"done\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)

    def fail_maintain(repo_root: Path) -> bool:
        """skip 指定時には呼ばれてはいけない fake メンテナンス。"""
        raise AssertionError("maintain_indexes should be skipped")

    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setattr("commons.indexing.maintain_indexes", fail_maintain)

    output = run_codex_exec(
        repo,
        "prompt",
        read_only=True,
        skip_index_maintenance=True,
    )

    assert output.strip() == "done"


def _init_git_repo(tmp_path: Path) -> Path:
    """Codex ラッパー用の最小 git repo を作る。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    (repo / "README.md").write_text("test\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-m", "initial")
    return repo


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """git をテスト repo で実行する。"""
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class _FailingTextIO:
    """テスト用の失敗する text sink。"""

    def __init__(
        self,
        *,
        fail_write: bool = False,
        fail_flush: bool = False,
    ) -> None:
        self._fail_write = fail_write
        self._fail_flush = fail_flush

    def write(self, text: str) -> int:
        if self._fail_write:
            raise BrokenPipeError("console closed")
        return len(text)

    def flush(self) -> None:
        if self._fail_flush:
            raise BrokenPipeError("console closed")

    def isatty(self) -> bool:
        return False


class _RecordingTextIO:
    """テスト用の flush 記録 text sink。"""

    def __init__(self) -> None:
        self.flushed = False

    def write(self, text: str) -> int:
        return len(text)

    def flush(self) -> None:
        self.flushed = True

    def isatty(self) -> bool:
        return False
