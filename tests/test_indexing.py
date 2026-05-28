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


def test_maintain_indexes_uses_local_exclude_but_ignores_external_excludes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX 生成対象は `.git/info/exclude` を反映し、global/system は無視する。"""
    global_ignore = tmp_path / "global-excludes"
    global_ignore.write_text("/global-only.txt\n", encoding="utf-8")
    global_config = tmp_path / "global-gitconfig"
    global_config.write_text(
        f"[core]\n\texcludesFile = {global_ignore.as_posix()}\n",
        encoding="utf-8",
    )
    external_ignore = tmp_path / "system-excludes"
    external_ignore.write_text("/system-only.txt\n", encoding="utf-8")
    system_config = tmp_path / "system-gitconfig"
    system_config.write_text(
        f"[core]\n\texcludesFile = {external_ignore.as_posix()}\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", global_config.as_posix())
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", system_config.as_posix())

    repo = _init_repo(tmp_path)
    (repo / ".git" / "info" / "exclude").write_text(
        "/local-only.txt\n",
        encoding="utf-8",
    )
    (repo / ".gitignore").write_text("# repo rules only\n", encoding="utf-8")
    (repo / "global-only.txt").write_text("kept\n", encoding="utf-8")
    (repo / "local-only.txt").write_text("kept\n", encoding="utf-8")
    (repo / "system-only.txt").write_text("kept\n", encoding="utf-8")

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

    content = (repo / "INDEX.md").read_text(encoding="utf-8")
    assert changed is True
    assert "# `global-only.txt`" in content
    assert "# `local-only.txt`" not in content
    assert "# `system-only.txt`" in content


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


def test_maintain_indexes_skips_excluded_index_roots(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """除外 root 配下には INDEX.md を作成・更新しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    nested_oracle = oracle_root / "nested"
    nested_oracle.mkdir(parents=True)
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (nested_oracle / "more.md").write_text("more\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracles")

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

    changed = maintain_indexes(repo, excluded_index_roots=["oracles"])

    assert changed is True
    assert (repo / "INDEX.md").exists()
    assert not (oracle_root / "INDEX.md").exists()
    assert not (nested_oracle / "INDEX.md").exists()


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


def test_maintain_indexes_excludes_symlink_entries(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """symlink は repo 外混入や循環回避のため目次対象から除外する。"""
    repo = _init_repo(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "external.txt").write_text("external\n", encoding="utf-8")
    (repo / "real.txt").write_text("real\n", encoding="utf-8")
    (repo / "linked-file.txt").symlink_to(outside / "external.txt")
    (repo / "linked-dir").symlink_to(outside, target_is_directory=True)
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "symlinks")
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成対象を記録する fake Codex CLI。"""
        purpose = str(kwargs["purpose"])
        purposes.append(purpose)
        return json.dumps(
            {
                "summary": [purpose],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "# `real.txt`" in content
    assert "# `linked-file.txt`" not in content
    assert "# `linked-dir`" not in content
    assert not any("linked-file.txt" in purpose for purpose in purposes)
    assert not any("linked-dir" in purpose for purpose in purposes)


def test_maintain_indexes_ignores_symlink_contents_in_directory_hash(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """directory hash は symlink 先の内容変更に影響されない。"""
    repo = _init_repo(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    external = outside / "external.txt"
    external.write_text("before\n", encoding="utf-8")
    folder = repo / "folder"
    folder.mkdir()
    (folder / "real.txt").write_text("real\n", encoding="utf-8")
    (folder / "external-link.txt").symlink_to(external)
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "folder symlink")

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
    external.write_text("after\n", encoding="utf-8")

    def fail_codex(*args: object, **kwargs: object) -> str:
        """symlink 先の変更だけでは呼ばれてはいけない fake Codex CLI。"""
        raise AssertionError(
            "codex exec should not be called for symlink target changes"
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fail_codex)

    changed = maintain_indexes(repo)
    folder_index = (folder / "INDEX.md").read_text(encoding="utf-8")

    assert changed is False
    assert "# `real.txt`" in folder_index
    assert "# `external-link.txt`" not in folder_index


def test_maintain_indexes_excludes_cyclic_symlink_from_directory_hash(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """循環 symlink は辿らず、通常項目だけを INDEX 化する。"""
    repo = _init_repo(tmp_path)
    folder = repo / "folder"
    folder.mkdir()
    (folder / "real.txt").write_text("real\n", encoding="utf-8")
    (folder / "loop").symlink_to(folder, target_is_directory=True)
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "cyclic symlink")

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
    folder_index = (folder / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "# `real.txt`" in folder_index
    assert "# `loop`" not in folder_index


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


def test_maintain_indexes_excludes_binary_after_initial_chunk(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """先頭付近が UTF-8 でも後続に NUL があるファイルは目次対象から除外する。"""
    repo = _init_repo(tmp_path)
    binary = repo / "late_binary.dat"
    binary.write_bytes(b"a" * 4096 + b"\0")
    (repo / "kept.txt").write_text("kept\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "late binary")

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
    assert "# `late_binary.dat`" not in content


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


def test_maintain_indexes_regenerates_known_cmoc_command_typo(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """hash が最新でも既知の cmoc コマンド名 typo は再生成する。"""
    repo = _init_repo(tmp_path)
    target = repo / "apply_join.md"
    target.write_text("join spec\n", encoding="utf-8")
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
                "# `apply_join.md`",
                "",
                "## Summary",
                "",
                "- cmo apply fork からの合流仕様を扱います。",
                "",
                "## Read this when",
                "",
                "- apply join を確認するとき。",
                "",
                "## Do not read this when",
                "",
                "- unrelated.",
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
    _git(repo, "commit", "-m", "stale command typo index")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """再生成された routing 文を返す。"""
        return json.dumps(
            {
                "summary": ["cmoc apply fork からの合流仕様を扱います。"],
                "read_this_when": ["apply join を確認するとき。"],
                "do_not_read_this_when": ["unrelated."],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "cmo apply fork" not in content
    assert "cmoc apply fork" in content


def test_maintain_indexes_regenerates_non_utf8_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """UTF-8 として読めない既存 INDEX.md は停止せず再生成する。"""
    repo = _init_repo(tmp_path)
    (repo / "target.txt").write_text("target\n", encoding="utf-8")
    (repo / "INDEX.md").write_bytes(b"# broken\n\xff\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "broken index")
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """再生成対象を記録できる Structured Output を返す。"""
        purpose = str(kwargs["purpose"])
        purposes.append(purpose)
        return json.dumps(
            {
                "summary": [purpose],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "# `README.md`" in content
    assert "# `target.txt`" in content
    assert "INDEX entry 生成 README.md" in purposes
    assert "INDEX entry 生成 target.txt" in purposes


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


def test_maintain_indexes_round_trips_special_names_and_multiline_text(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """特殊文字を含む名前と複数行説明文でも INDEX を再利用できる。"""
    repo = _init_repo(tmp_path)
    target = repo / "we`ird\n%.txt"
    target.write_text("target\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "special file name")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """Markdown 境界に見える文字を含む Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["first\n# `ghost`\nsecond"],
                "read_this_when": ["read\r\nwhen"],
                "do_not_read_this_when": ["skip\twhen"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = maintain_indexes(repo)
    content = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "# `we%60ird%0A%25.txt`" in content
    assert "# `we`ird" not in content
    assert "- first # `ghost` second" in content
    assert "read when" in content
    assert "skip when" in content

    def fail_codex(*args: object, **kwargs: object) -> str:
        """特殊文字を含む最新 INDEX では呼ばれてはいけない。"""
        raise AssertionError(
            "codex exec should not be called for escaped current INDEX entries"
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fail_codex)

    assert maintain_indexes(repo) is False


def test_maintain_indexes_regenerates_parent_entry_after_child_rename(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """子の名前変更は親ディレクトリ hash を変え、親 entry を再生成する。"""
    repo = _init_repo(tmp_path)
    folder = repo / "folder"
    folder.mkdir()
    (folder / "before.txt").write_text("same content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "nested content")
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """呼び出し対象を記録できる Structured Output を返す。"""
        purpose = str(kwargs["purpose"])
        purposes.append(purpose)
        return json.dumps(
            {
                "summary": [purpose],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)
    maintain_indexes(repo)

    purposes.clear()
    (folder / "before.txt").rename(folder / "after.txt")

    changed = maintain_indexes(repo)
    root_index = (repo / "INDEX.md").read_text(encoding="utf-8")

    assert changed is True
    assert "INDEX entry 生成 folder" in purposes
    assert "# `folder`" in root_index
    assert "- INDEX entry 生成 folder" in root_index


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


def test_maintain_indexes_commits_ignored_new_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """ignored な新規 INDEX.md もメンテナンス差分として commit する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("INDEX.md\n", encoding="utf-8")
    (repo / "target.txt").write_text("target\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "target.txt")
    _git(repo, "commit", "-m", "ignore index")

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
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout

    assert changed is True
    assert "INDEX.md" in last_commit_paths
    assert _git(repo, "ls-files", "INDEX.md").stdout.strip() == "INDEX.md"


def test_maintain_indexes_stages_literal_index_paths(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """特殊文字を含む INDEX.md path が別 path を巻き込まない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("docsX/\n", encoding="utf-8")
    literal_dir = repo / "docs*"
    ignored_dir = repo / "docsX"
    literal_dir.mkdir()
    ignored_dir.mkdir()
    (literal_dir / "target.txt").write_text("target\n", encoding="utf-8")
    (ignored_dir / "INDEX.md").write_text("user ignored\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "docs*/target.txt")
    _git(repo, "commit", "-m", "special path")

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
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout

    assert changed is True
    assert "docs*/INDEX.md" in last_commit_paths
    assert "docsX/INDEX.md" not in last_commit_paths
    assert _git(repo, "ls-files", "docsX/INDEX.md").stdout.strip() == ""


def test_maintain_indexes_preserves_preexisting_staged_index_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """同じ INDEX.md の既存 staged-only 差分を自動 commit 後も残す。"""
    repo = _init_repo(tmp_path)
    target = repo / "target.txt"
    target.write_text("before\n", encoding="utf-8")
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

    maintain_indexes(repo)
    head_index = (repo / "INDEX.md").read_text(encoding="utf-8")
    (repo / "INDEX.md").write_text(
        "staged note\n" + head_index,
        encoding="utf-8",
    )
    _git(repo, "add", "INDEX.md")
    (repo / "INDEX.md").write_text(head_index, encoding="utf-8")
    target.write_text("after\n", encoding="utf-8")

    changed = maintain_indexes(repo)
    status = _git(repo, "status", "--porcelain").stdout
    staged_index = _git(repo, "diff", "--cached", "--", "INDEX.md").stdout
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout

    assert changed is True
    assert "MM INDEX.md" in status
    assert "+staged note" in staged_index
    assert "INDEX.md" in last_commit_paths


def test_maintain_indexes_does_not_ensure_cmoc_ignore(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX メンテナンスは `.cmoc` の ignore 保証を担当しない。"""
    repo = _init_repo(tmp_path)
    cmoc_log = repo / ".cmoc" / "log.txt"
    cmoc_log.parent.mkdir()
    cmoc_log.write_text("log\n", encoding="utf-8")
    _git(repo, "add", ".cmoc/log.txt")
    _git(repo, "commit", "-m", "tracked cmoc log")

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
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout

    assert changed is True
    assert not (repo / ".gitignore").exists()
    assert _git(repo, "ls-files", ".cmoc/log.txt").stdout.strip() == (
        ".cmoc/log.txt"
    )
    assert "INDEX.md" in last_commit_paths
    assert ".gitignore" not in last_commit_paths
    assert ".cmoc/log.txt" not in last_commit_paths


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
