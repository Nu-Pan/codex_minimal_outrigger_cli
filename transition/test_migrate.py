"""移設によるデータ損失、中断後の取り違え、文書 ID の破壊を検出する。"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import migrate
import pytest


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    """実行コードと文書を含む、移設前の最小 tree を用意する。"""
    root = tmp_path / "repository"
    package = root / "referenece/src/oracle"
    package.mkdir(parents=True)
    (package / "builder.py").write_bytes(
        b"# exact prompt builder\r\nVALUE = 'oracle'\r\n"
    )
    (package / "schema.json").write_text('{"type": "object"}', encoding="utf-8")
    (package / "builder.py").chmod(0o750)
    (root / "spec").mkdir()
    (root / "spec/example.md").write_text("# 仕様\n", encoding="utf-8")
    (root / "oracle/test").mkdir()
    (root / "transition").mkdir()
    return root


def test_plan_is_read_only_and_move_preserves_all_source_bytes(
    repository: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """計画は読み取りだけを行い、移設は内容と権限を保持する。"""
    before = {name: migrate._fingerprint(repository / name) for name in migrate._MOVES}
    migrate._plan(repository)
    assert "referenece/src -> reference/src" in capsys.readouterr().out
    assert not (repository / "transition/work").exists()
    migrate._move(repository)
    for source, target in migrate._MOVES.items():
        assert not (repository / source).exists()
        assert migrate._fingerprint(repository / target) == before[source]
    assert not (repository / "oracle").exists()
    migrate._move(repository)
    migrate._verify_move(repository)


def test_target_collision_stops_before_any_move(repository: Path) -> None:
    """一部の移設先が衝突しても、他の tree を先行移設しない。"""
    (repository / "spec").mkdir()
    (repository / "spec/keep.md").write_text("keep", encoding="utf-8")
    with pytest.raises(migrate.MigrationError):
        migrate._move(repository)
    assert (repository / "spec/keep.md").read_text() == "keep"
    assert (repository / "referenece/src/oracle/builder.py").is_file()
    assert not (repository / "reference").exists()
    assert not (repository / "transition/work").exists()


@pytest.mark.parametrize("entry", ["symlink", "fifo", "AGENTS.md", ".git"])
def test_move_refuses_special_and_protected_entries(
    repository: Path, entry: str
) -> None:
    """保護対象・特殊ファイルを含む tree を移動しない。"""
    path = repository / "referenece/src" / entry
    if entry == "symlink":
        path.symlink_to(repository / "spec", target_is_directory=True)
    elif entry == "fifo":
        os.mkfifo(path)
    else:
        path.write_text("protected", encoding="utf-8")
    with pytest.raises(migrate.MigrationError):
        migrate._move(repository)
    assert (repository / "spec").is_dir()
    assert not (repository / "reference").exists()


@pytest.mark.parametrize("relative", ["oracle/test/contract.py", "oracle/extra.md"])
def test_unmapped_sources_are_not_silently_discarded(
    repository: Path, relative: str
) -> None:
    """行き先のない資料を残したまま移設成功としない。"""
    (repository / relative).write_text("human intent", encoding="utf-8")
    with pytest.raises(migrate.MigrationError, match="No migration destination"):
        migrate._move(repository)
    assert not (repository / "transition/work").exists()


@pytest.mark.parametrize("parent", ["reference", "transition/work"])
def test_move_does_not_follow_destination_or_receipt_symlinks(
    repository: Path, parent: str, tmp_path: Path
) -> None:
    """移設先と receipt の親が外部へのリンクでも書き込まない。"""
    external = tmp_path / "external"
    external.mkdir()
    (repository / parent).symlink_to(external, target_is_directory=True)
    with pytest.raises(migrate.MigrationError, match="Symlink"):
        migrate._move(repository)
    assert not list(external.iterdir())
    assert (repository / "referenece/src").is_dir()


def test_invalid_destination_parent_stops_before_writing_receipt(
    repository: Path,
) -> None:
    """移設先の親が通常ファイルなら、準備記録も作る前に停止する。"""
    (repository / "reference").write_text("keep", encoding="utf-8")
    with pytest.raises(migrate.MigrationError, match="parent directory"):
        migrate._move(repository)
    assert not (repository / "transition/work").exists()
    assert (repository / "reference").read_text() == "keep"


def test_interrupted_move_can_resume_without_losing_the_completed_tree(
    repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """二つ目の rename に失敗しても、同じ入力から残りを再開できる。"""
    rename = Path.rename

    def interrupted(path: Path, target: Path) -> Path:
        if path == repository / "spec":
            raise OSError("simulated interruption")
        return rename(path, target)

    with monkeypatch.context() as patch:
        patch.setattr(Path, "rename", interrupted)
        with pytest.raises(OSError, match="interruption"):
            migrate._move(repository)
    assert (repository / "reference/src/oracle/builder.py").is_file()
    with pytest.raises(migrate.MigrationError, match="incomplete"):
        migrate._verify_move(repository)
    migrate._move(repository)
    migrate._verify_move(repository)


@pytest.mark.parametrize("change", ["content", "permission", "extra_file"])
def test_receipt_detects_changes_and_move_does_not_erase_them(
    repository: Path, change: str
) -> None:
    """人間の後続編集を、中断した移設の再開で上書きしない。"""
    migrate._move(repository)
    path = repository / "reference/src/oracle/builder.py"
    if change == "content":
        path.write_text("human edit", encoding="utf-8")
    elif change == "permission":
        path.chmod(0o600)
    else:
        (path.parent / "new.py").write_text("new", encoding="utf-8")
    edited = migrate._fingerprint(repository / "reference/src")
    with pytest.raises(migrate.MigrationError, match="Tree changed"):
        migrate._move(repository)
    assert migrate._fingerprint(repository / "reference/src") == edited


def test_path_rewrite_previews_and_updates_literals_without_changing_package_names(
    repository: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """差分提示は読取専用とし、明示 path だけを改行・権限を保って置換する。"""
    builder = repository / "referenece/src/oracle/builder.py"
    before = (
        "import oracle\r\n"
        "DOC = '{{work-root}}/spec/example.md'\r\n"
        "SRC = '{{cmoc-root}}/referenece/src/oracle/builder.py'\r\n"
        "REL = './referenece/src'\r\n"
        f"ABS = '{repository.as_posix()}/spec'\r\n"
    )
    builder.write_bytes(before.encode())
    (repository / "pyproject.toml").write_text(
        'where = ["src", "referenece/src"]\n', encoding="utf-8"
    )
    (repository / "src").mkdir()
    (repository / "src/example.py").write_text(
        '# {{repo-root}}/spec/example.md\nPATH = "referenece/src"\n', encoding="utf-8"
    )
    migrate._move(repository)
    capsys.readouterr()
    moved = repository / "reference/src/oracle/builder.py"
    migrate._rewrite_paths(repository, apply=False)
    preview = capsys.readouterr().out
    assert "--- reference/src/oracle/builder.py" in preview
    assert "Would rewrite paths in 3 files" in preview
    assert moved.read_bytes() == before.encode()
    migrate._verify_move(repository)
    migrate._rewrite_paths(repository, apply=True)
    expected = before.replace("spec", "spec").replace("referenece/src", "reference/src")
    assert moved.read_bytes() == expected.encode()
    assert moved.stat().st_mode & 0o777 == 0o750
    assert (repository / "pyproject.toml").read_text() == (
        'where = ["src", "reference/src"]\n'
    )
    assert (repository / "src/example.py").read_text() == (
        '# {{repo-root}}/spec/example.md\nPATH = "reference/src"\n'
    )
    with pytest.raises(migrate.MigrationError, match="Tree changed"):
        migrate._verify_move(repository)
    capsys.readouterr()
    migrate._rewrite_paths(repository, apply=True)
    assert "Rewrote paths in 0 files" in capsys.readouterr().out


def test_path_rewrite_rebases_markdown_links_from_the_old_file_location(
    repository: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """参照元・先の移設を反映し、anchor・query・同一 tree のリンクを保持する。"""
    (repository / "README.md").write_text(
        "# Root\n\n[仕様](spec/example.md#section)\n", encoding="utf-8"
    )
    (repository / "with space.md").write_text("# Space\n", encoding="utf-8")
    (repository / "spec/sibling.md").write_text("# Sibling\n", encoding="utf-8")
    (repository / "spec/example.md").write_text(
        "# 仕様\n\n[Root](../../README.md#summary)\n"
        "[Builder](../src/oracle/builder.py)\n"
        '[Space](<../../with space.md?q=1#part> "title")\n'
        "[Sibling](sibling.md)\n[ref]: ../../README.md\n",
        encoding="utf-8",
    )
    (repository / "referenece/src/guide.md").write_text(
        "[仕様](../doc/example.md)\n", encoding="utf-8"
    )
    migrate._move(repository)
    migrate._rewrite_paths(repository, apply=True)
    assert (repository / "README.md").read_text() == (
        "# Root\n\n[仕様](spec/example.md#section)\n"
    )
    expected = (
        "# 仕様\n\n[Root](../README.md#summary)\n"
        "[Builder](../reference/src/oracle/builder.py)\n"
        '[Space](<../with%20space.md?q=1#part> "title")\n'
        "[Sibling](sibling.md)\n[ref]: ../README.md\n"
    )
    assert (repository / "spec/example.md").read_text() == expected
    assert (repository / "reference/src/guide.md").read_text() == (
        "[仕様](../../spec/example.md)\n"
    )
    capsys.readouterr()
    migrate._rewrite_paths(repository, apply=True)
    assert "Rewrote paths in 0 files; 0 review/skip notices" in capsys.readouterr().out
    assert (repository / "spec/example.md").read_text() == expected


def test_path_rewrite_keeps_ambiguous_and_unmapped_paths_for_review(
    repository: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """外部 URL・動的 path・移設先未定の path と複数候補のリンクを独断で直さない。"""
    content = (
        "# 仕様\n\nhttps://example.org/spec/example.md\n"
        "/another/repository/referenece/src/file.py\n"
        'root / "oracle" / "src"\n'
        'join(root, "oracle", "doc")\n'
        "oracle\\src\\file.py\n"
        "oracle/test\n"
        "myspec specument referenece/src_extra\n"
        "[ambiguous](../src/oracle/builder.py)\n"
    )
    (repository / "spec/example.md").write_text(content, encoding="utf-8")
    (repository / "src/oracle").mkdir(parents=True)
    (repository / "src/oracle/builder.py").write_text("other", encoding="utf-8")
    migrate._move(repository)
    migrate._rewrite_paths(repository, apply=True)
    assert (repository / "spec/example.md").read_text() == content
    output = capsys.readouterr().out
    assert "Old or constructed path remains" in output
    assert "Relative link has two possible targets" in output


def test_path_rewrite_does_not_treat_a_nested_relative_link_as_root_relative(
    repository: Path,
) -> None:
    """Markdown の行き先に含まれる同名 directory を root の移設対象と混同しない。"""
    nested = repository / "spec/spec"
    nested.mkdir(parents=True)
    (nested / "nested.md").write_text("# Nested\n", encoding="utf-8")
    content = "# 仕様\n\n[Nested](spec/nested.md)\n"
    (repository / "spec/example.md").write_text(content, encoding="utf-8")
    migrate._move(repository)
    migrate._rewrite_paths(repository, apply=True)
    assert (repository / "spec/example.md").read_text() == content


def test_path_rewrite_leaves_excluded_and_binary_files_untouched(
    repository: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """移行記録・人間の作業領域・保護対象・バイナリを読替え対象にしない。"""
    migrate._move(repository)
    protected = [
        repository / "AGENTS.md",
        repository / "memo/notes.md",
        repository / "transition/README.md",
        repository / "spec/AGENTS.md",
        repository / "src/.agents/notes.md",
        repository / "src/__pycache__/cache.txt",
    ]
    for path in protected:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("spec", encoding="utf-8")
    binary = repository / "reference/src/data.bin"
    binary.write_bytes(b"\0spec")
    invalid = repository / "reference/src/non_utf8.txt"
    invalid.write_bytes(b"\xffreferenece/src")
    migrate._rewrite_paths(repository, apply=True)
    assert all(path.read_text() == "spec" for path in protected)
    assert binary.read_bytes() == b"\0spec"
    assert invalid.read_bytes() == b"\xffreferenece/src"
    assert "2 review/skip notices" in capsys.readouterr().out


def test_path_rewrite_preflights_all_files_before_writing(repository: Path) -> None:
    """後ろの対象に symlink があっても、先の文書だけを先行書換えしない。"""
    (repository / "spec/example.md").write_text("referenece/src", encoding="utf-8")
    migrate._move(repository)
    (repository / "bin").mkdir()
    (repository / "bin/link").symlink_to(repository / "spec/example.md")
    with pytest.raises(migrate.MigrationError, match="symlink"):
        migrate._rewrite_paths(repository, apply=True)
    assert (repository / "spec/example.md").read_text() == "referenece/src"


def test_interrupted_path_rewrite_can_resume(
    repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """一部を書換えた後に失敗しても、完了部分を再変換せず残りを再開できる。"""
    (repository / "spec/example.md").write_text("referenece/src", encoding="utf-8")
    (repository / "referenece/src/oracle/builder.py").write_text(
        'PATH = "spec"\n', encoding="utf-8"
    )
    migrate._move(repository)
    replace = migrate._replace_text

    def interrupt(path: Path, content: str) -> None:
        if path.suffix == ".py":
            raise OSError("simulated interruption")
        replace(path, content)

    with monkeypatch.context() as patch:
        patch.setattr(migrate, "_replace_text", interrupt)
        with pytest.raises(OSError, match="interruption"):
            migrate._rewrite_paths(repository, apply=True)
    assert (repository / "spec/example.md").read_text() == "reference/src"
    migrate._rewrite_paths(repository, apply=True)
    assert (repository / "spec/example.md").read_text() == "reference/src"
    assert (repository / "reference/src/oracle/builder.py").read_text() == (
        'PATH = "spec"\n'
    )


@pytest.mark.parametrize("apply", [False, True])
def test_path_rewrite_requires_relocation(repository: Path, apply: bool) -> None:
    """移設を済ませず本文だけ新配置へ向ける操作は受け付けない。"""
    with pytest.raises(migrate.MigrationError, match="No move receipt"):
        migrate._rewrite_paths(repository, apply=apply)
    assert not (repository / "spec").exists()


def test_number_specs_preserves_existing_ids_and_code_examples(
    repository: Path,
) -> None:
    """採番は本文の改行と既存 ID を保持し、コード例は変更しない。"""
    migrate._move(repository)
    path = repository / "spec/example.md"
    source = (
        "# [SPEC-000000] 既存\r\n\r\n"
        "## 新規\r\n\r\n"
        "Setext\r\n======\r\n\r\n"
        "```markdown\r\n# [SPEC-000001] 例\r\n```\r\n"
    )
    path.write_bytes(source.encode("utf-8"))
    migrate._number_specs(repository)
    expected = source.replace("## 新規", "## [SPEC-000001] 新規").replace(
        "Setext\r\n", "[SPEC-000002] Setext\r\n"
    )
    assert path.read_bytes() == expected.encode("utf-8")
    migrate._number_specs(repository)
    assert path.read_bytes() == expected.encode("utf-8")
    assert not (repository / "decision").exists()


@pytest.mark.parametrize(
    "invalid", ["# [SPEC-000000] 重複\n", "> # ネスト\n", "# [DECI-000001] 違う区分\n"]
)
def test_numbering_validates_all_documents_before_writing(
    repository: Path, invalid: str
) -> None:
    """後ろの文書が不正なら、先に読んだ文書にも採番を書き込まない。"""
    migrate._move(repository)
    first = repository / "spec/example.md"
    original = "# [SPEC-000000] 既存\n\n## 未採番\n"
    first.write_text(original, encoding="utf-8")
    (repository / "spec/z.md").write_text(invalid, encoding="utf-8")
    with pytest.raises(migrate.MigrationError):
        migrate._number_specs(repository)
    assert first.read_text(encoding="utf-8") == original


def test_numbering_write_failure_preserves_document(
    repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """置換直前の失敗で元文書を失わず、後から採番を再実行できる。"""
    migrate._move(repository)
    path = repository / "spec/example.md"
    before = path.read_bytes()

    def fail_replace(path: Path, target: Path) -> Path:
        raise OSError("simulated write failure")

    with monkeypatch.context() as patch:
        patch.setattr(Path, "replace", fail_replace)
        with pytest.raises(OSError, match="write failure"):
            migrate._number_specs(repository)
    assert path.read_bytes() == before
    assert list(path.parent.iterdir()) == [path]
    migrate._number_specs(repository)
    assert path.read_text(encoding="utf-8").startswith("# [SPEC-000000]")


def _write_documents(repository: Path) -> Path:
    (repository / "decision").mkdir()
    (repository / "decision/intent.md").write_text(
        "# [DECI-000000] 人間意図\n", encoding="utf-8"
    )
    (repository / "spec").mkdir()
    spec = repository / "spec/generated.md"
    spec.write_text(
        "# [SPEC-000000] 仕様\n\n意図は [DECI-000000] に従う。\n\n"
        "`[DECI-example]` はコード例。\n\n```markdown\n# [SPEC-example] 例\n```\n",
        encoding="utf-8",
    )
    return spec


def test_doc_check_resolves_references_but_ignores_code_examples(
    repository: Path,
) -> None:
    """本文の参照を照合し、コード例のダミー ID は参照扱いしない。"""
    _write_documents(repository)
    migrate._check_docs(repository)


@pytest.mark.parametrize("state", ["absent", "empty_directory", "blank_file"])
@pytest.mark.parametrize("missing_reference", [False, True])
def test_doc_check_allows_empty_decision_but_rejects_missing_references(
    repository: Path, state: str, missing_reference: bool
) -> None:
    """decision が空でも spec を検査し、存在しない決定への参照は見逃さない。"""
    if state != "absent":
        (repository / "decision").mkdir()
    if state == "blank_file":
        (repository / "decision/intent.md").write_text(" \n\t\n", encoding="utf-8")
    (repository / "spec").mkdir()
    content = "# [SPEC-000000] 既存仕様\n"
    if missing_reference:
        content += "\n決定は [DECI-000000] に従う。\n"
    (repository / "spec/initial.md").write_text(content, encoding="utf-8")
    if missing_reference:
        with pytest.raises(migrate.MigrationError, match=r"Unresolved \[DECI-000000\]"):
            migrate._check_docs(repository)
    else:
        migrate._check_docs(repository)


def test_doc_check_still_requires_spec_documents(repository: Path) -> None:
    """decision を空にできても、初期材料である spec の欠落は成功としない。"""
    (repository / "spec").mkdir()
    with pytest.raises(migrate.MigrationError, match="No Markdown documents found"):
        migrate._check_docs(repository)


@pytest.mark.parametrize(
    "addition, error",
    [
        ("\n## 見出し\n", "Expected a leading"),
        ("\n## [SPEC-000000] 重複\n", "Duplicate"),
        ("\n参照は [DECI-missing]。\n", "Unresolved"),
    ],
)
def test_doc_check_reports_invalid_definitions_and_references(
    repository: Path, addition: str, error: str
) -> None:
    """不足・重複した定義と参照切れを、それぞれ検出する。"""
    path = _write_documents(repository)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(addition)
    with pytest.raises(migrate.MigrationError, match=error):
        migrate._check_docs(repository)


def test_cli_uses_its_own_repository_and_reports_failure(
    repository: Path, tmp_path: Path
) -> None:
    """別の cwd から移設・パス更新を実行でき、未完了は非ゼロと理由を返す。"""
    script = repository / "transition/migrate.py"
    shutil.copyfile(Path(migrate.__file__), script)

    def run(command: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), command],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            timeout=10,
        )

    result = run("plan")
    assert result.returncode == 0
    assert "referenece/src -> reference/src" in result.stdout
    result = run("verify-move")
    assert result.returncode == 1
    assert "No move receipt" in result.stderr
    original = "# 仕様\n\n`referenece/src/oracle/builder.py`\n"
    (repository / "spec/example.md").write_text(original, encoding="utf-8")
    result = run("move")
    assert result.returncode == 0, result.stderr
    result = run("plan-paths")
    assert result.returncode == 0, result.stderr
    assert "--- spec/example.md" in result.stdout
    assert (repository / "spec/example.md").read_text() == original
    result = run("rewrite-paths")
    assert result.returncode == 0, result.stderr
    assert (repository / "spec/example.md").read_text() == (
        "# 仕様\n\n`reference/src/oracle/builder.py`\n"
    )
