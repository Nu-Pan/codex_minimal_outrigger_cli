"""INDEX.md メンテナンス処理のテスト。"""

import hashlib
import json
import os
import subprocess
from pathlib import Path

from pytest import MonkeyPatch

from commons.indexing import _INDEX_OUTPUT_SCHEMA
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
    codex_kwargs: list[dict[str, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の Structured Output を返す fake Codex CLI。"""
        codex_kwargs.append(kwargs)
        return json.dumps(
            {
                "summary": ["kept summary"],
                "read_this_when": ["read kept"],
                "do_not_read_this_when": ["skip kept"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert changed is True
    assert "# `kept.txt`" in content
    assert "kept summary" in content
    assert "# `ignored.txt`" not in content
    assert codex_kwargs
    assert all(
        kwargs["output_schema"] == _INDEX_OUTPUT_SCHEMA
        for kwargs in codex_kwargs
    )
    assert all(kwargs["model"] == "gpt-5.4-mini" for kwargs in codex_kwargs)
    assert all(
        kwargs["reasoning_effort"] == "medium" for kwargs in codex_kwargs
    )


def test_maintain_indexes_creates_empty_index_for_empty_directory(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """空の配置対象ディレクトリにも空の INDEX.md を新規作成する。"""
    repo = _init_repo(tmp_path)
    empty = repo / "empty"
    empty.mkdir()

    def fake_codex(*args: object, **kwargs: object) -> str:
        """root INDEX の既存ファイル向け Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)

    assert changed is True
    assert (empty / "INDEX.md").exists()
    assert (empty / "INDEX.md").read_text(encoding="utf-8") == ""


def test_maintain_indexes_includes_build_and_tmp_as_entries(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """build/tmp は配置対象からは除外しても親 INDEX の目次対象には含める。"""
    repo = _init_repo(tmp_path)
    build = repo / "build"
    tmp = repo / "tmp"
    build.mkdir()
    tmp.mkdir()
    (build / "artifact.txt").write_text("artifact\n", encoding="utf-8")
    (tmp / "scratch.txt").write_text("scratch\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "generated dirs")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の最小 Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert "# `build`" in content
    assert "# `tmp`" in content
    assert not (build / "INDEX.md").exists()
    assert not (tmp / "INDEX.md").exists()


def test_maintain_indexes_excludes_non_utf8_binary_without_nul(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """NUL を含まない非 UTF-8 バイナリも INDEX 目次対象から除外する。"""
    repo = _init_repo(tmp_path)
    binary = repo / "image.bin"
    binary.write_bytes(bytes([0xFF, 0xD8, 0xFF, 0xE0, 0x7F, 0x01]))
    (repo / "kept.txt").write_text("kept\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "binary")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の最小 Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert "# `kept.txt`" in content
    assert "# `image.bin`" not in content


def test_maintain_indexes_keeps_utf8_when_sample_ends_mid_character(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """sample 末尾で UTF-8 文字が途中切れしてもテキストとして扱う。"""
    repo = _init_repo(tmp_path)
    target = repo / "partial_boundary.md"
    target.write_bytes(b"a" * 4094 + "あ".encode("utf-8") + b"\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "utf8 boundary")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の最小 Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert "# `partial_boundary.md`" in content


def test_maintain_indexes_places_index_in_nested_memo_directory(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """配置除外の memo は repo root 直下だけに限定する。"""
    repo = _init_repo(tmp_path)
    nested_memo = repo / "docs" / "memo"
    nested_memo.mkdir(parents=True)
    (nested_memo / "note.md").write_text("note\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "nested memo")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の最小 Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    maintain_indexes(repo)

    assert (nested_memo / "INDEX.md").exists()


def test_maintain_indexes_regenerates_malformed_current_entry(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """hash が最新でも必須セクションが欠ける既存エントリは再生成する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    target = repo / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    readme_digest = hashlib.sha256(
        (repo / "README.md").read_bytes()
    ).hexdigest()
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (repo / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## Summary",
                "",
                "- readme summary",
                "",
                "## Read this when",
                "",
                "- read readme",
                "",
                "## Do not read this when",
                "",
                "- skip readme",
                "",
                "## hash",
                "",
                f"- {readme_digest}",
                "",
                "# `target.txt`",
                "",
                "## Summary",
                "",
                "- stale summary",
                "",
                "## hash",
                "",
                f"- {digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "malformed index")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """再生成されたことを識別できる Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["regenerated summary"],
                "read_this_when": ["read regenerated"],
                "do_not_read_this_when": ["skip regenerated"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "regenerated summary" in content
    assert "## Read this when" in content
    assert "## Do not read this when" in content


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
                (
                    "  printf '%s\\n' > \"$LAST\" "
                    "'{\"content_hash\":\"abc\","
                    "\"summary\":\"not a list\","
                    "\"read_this_when\":[\"read\"],"
                    "\"do_not_read_this_when\":[\"skip\"]}'"
                ),
                "else",
                (
                    "  printf '%s\\n' > \"$LAST\" "
                    "'{\"summary\":[\"valid summary\"],"
                    "\"read_this_when\":[\"read\"],"
                    "\"do_not_read_this_when\":[\"skip\"]}'"
                ),
                "fi",
                "echo '{\"event\":\"done\"}'",
            ]
        ),
        encoding="utf-8",
    )
    codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ['PATH']}")

    changed = maintain_indexes(repo)

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert changed is True
    assert "valid summary" in content
    assert int(state.read_text(encoding="utf-8").strip()) >= 2


def test_maintain_indexes_does_not_call_codex_when_index_is_current(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX.md が最新なら機械的チェックだけで済ませ、Codex CLI を呼ばない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    target = repo / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    readme_digest = hashlib.sha256(
        (repo / "README.md").read_bytes()
    ).hexdigest()
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (repo / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## Summary",
                "",
                "- readme summary",
                "",
                "## Read this when",
                "",
                "- read readme",
                "",
                "## Do not read this when",
                "",
                "- skip readme",
                "",
                "## hash",
                "",
                f"- {readme_digest}",
                "",
                "# `target.txt`",
                "",
                "## Summary",
                "",
                "- target summary",
                "",
                "## Read this when",
                "",
                "- read target",
                "",
                "## Do not read this when",
                "",
                "- skip target",
                "",
                "## hash",
                "",
                f"- {digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "content")

    def fail_codex(*args: object, **kwargs: object) -> str:
        """最新 INDEX では呼ばれてはいけない fake Codex CLI。"""
        raise AssertionError(
            "codex exec should not be called for a fresh INDEX.md"
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fail_codex)

    changed = maintain_indexes(repo)

    assert changed is False


def test_maintain_indexes_reuses_current_index_with_empty_sections(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """schema 上有効な空配列由来の既存 INDEX は再生成しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    target = repo / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    readme_digest = hashlib.sha256(
        (repo / "README.md").read_bytes()
    ).hexdigest()
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (repo / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## Summary",
                "",
                "- readme summary",
                "",
                "## Read this when",
                "",
                "- read readme",
                "",
                "## Do not read this when",
                "",
                "- skip readme",
                "",
                "## hash",
                "",
                f"- {readme_digest}",
                "",
                "# `target.txt`",
                "",
                "## Summary",
                "",
                "",
                "## Read this when",
                "",
                "",
                "## Do not read this when",
                "",
                "",
                "## hash",
                "",
                f"- {digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    original_content = (repo / "INDEX.md").read_text(encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "current empty index sections")

    def fail_codex(*args: object, **kwargs: object) -> str:
        """空セクションの最新 INDEX では呼ばれてはいけない fake Codex CLI。"""
        raise AssertionError(
            "codex exec should not be called for empty INDEX sections"
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fail_codex)

    changed = maintain_indexes(repo)

    assert changed is False
    assert (repo / "INDEX.md").read_text(encoding="utf-8") == original_content


def test_maintain_indexes_commits_only_maintenance_paths(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """自動コミットは INDEX.md などメンテナンス差分だけを対象にする。"""
    repo = _init_repo(tmp_path)
    (repo / "target.txt").write_text("target\n", encoding="utf-8")
    (repo / "user_work.txt").write_text("user work\n", encoding="utf-8")
    _git(repo, "add", "target.txt")
    _git(repo, "commit", "-m", "target")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の最小 Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    status = _git(repo, "status", "--porcelain").stdout
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout

    assert changed is True
    assert "?? user_work.txt" in status
    assert "INDEX.md" in last_commit_paths
    assert "user_work.txt" not in last_commit_paths


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
