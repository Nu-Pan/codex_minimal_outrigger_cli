"""INDEX.md メンテナンス処理のテスト。"""

import json
import os
import subprocess
from pathlib import Path

from pytest import MonkeyPatch

from commons.indexing import maintain_indexes


def test_maintain_indexes_generates_routing_entries_and_respects_gitignore(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX.md は直下項目ごとに生成され、gitignore 対象は除外される。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
    (repo / "kept.txt").write_text("kept\n", encoding="utf-8")
    (repo / "ignored.txt").write_text("ignored\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "content")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の Structured Output を返す fake Codex CLI。"""
        return json.dumps(
            {
                "summary": ["kept summary"],
                "read_this_when": ["read kept"],
                "do_not_read_this_when": ["skip kept"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo, commit_changes=False)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert changed is True
    assert "# `kept.txt`" in content
    assert "kept summary" in content
    assert "# `ignored.txt`" not in content


def test_maintain_indexes_retries_invalid_structured_output(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX 生成用 JSON の schema 不一致は run_codex_exec 側でリトライされる。"""
    repo = _init_repo(tmp_path)
    (repo / "target.txt").write_text("target\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "content")
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
                "if [ \"$COUNT\" -eq 1 ]; then",
                "  echo '{\"content_hash\":\"abc\",\"summary\":\"not a list\",\"read_this_when\":[\"read\"],\"do_not_read_this_when\":[\"skip\"]}'",
                "else",
                "  echo '{\"summary\":[\"valid summary\"],\"read_this_when\":[\"read\"],\"do_not_read_this_when\":[\"skip\"]}'",
                "fi",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    changed = maintain_indexes(repo, commit_changes=False)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert changed is True
    assert "valid summary" in content
    assert int(state.read_text(encoding="utf-8").strip()) >= 2


def _init_repo(tmp_path: Path) -> Path:
    """テスト用 git repo を作り、初期 commit を置く。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    (repo / "README.md").write_text("test\n", encoding="utf-8")
    _git(repo, "add", ".")
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
