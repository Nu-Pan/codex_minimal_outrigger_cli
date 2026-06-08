"""サブコマンド横断テストを意味カテゴリ別に分割したファイル。"""

from .helpers import *


def test_session_join_merges_current_session_branch_and_deletes_it(
    tmp_path: Path,
) -> None:
    """`cmoc session join` は記録済み home branch へ session を merge する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    target_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "feature")

    cmoc_session_join_impl(repo)

    branches = _git(
        repo,
        "branch",
        "--format=%(refname:short)",
    ).stdout.splitlines()
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert _git(repo, "branch", "--show-current").stdout.strip() == target_branch
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "feature\n"
    assert state["session"]["state"] == "joined"
    assert "cmoc/session/2026-05-10_22-21_10_000000123" not in branches


def test_session_join_rejects_null_session_home_branch(
    tmp_path: Path,
) -> None:
    """null home branch の session state では session join しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / (
        "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["session_home_branch"] = None
    state_path.write_text(json.dumps(state), encoding="utf-8")
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", "feature.txt")
    _git(repo, "commit", "-m", "feature")

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    assert "session state ファイルの形式が不正です。" in error.value.message
    assert "session.session_home_branch: None" in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert state_after["session"]["state"] == "active"
    assert state_after["session"]["session_home_branch"] is None


def test_session_join_dirty_worktree_rejects_null_session_home_branch_first(
    tmp_path: Path,
) -> None:
    """dirty 判定前に null home branch state を schema 検証で拒否する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / (
        "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["session_home_branch"] = None
    state_path.write_text(json.dumps(state), encoding="utf-8")
    state_before = json.loads(state_path.read_text(encoding="utf-8"))
    (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    assert "session state ファイルの形式が不正です。" in error.value.message
    assert "session.session_home_branch: None" in error.value.detail
    assert state_after == state_before
    assert state_after["session"]["session_home_branch"] is None


def test_session_join_ensures_cmoc_ignored_before_switch(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """tracked `.cmoc` state を補修 commit してから home branch へ merge する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    state_path = ".cmoc/sessions/2026-05-10_22-21_10_000000123.json"
    _git(repo, "add", "-f", state_path)
    _git(repo, "commit", "-m", "track session state")

    cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    state = json.loads((repo / state_path).read_text(encoding="utf-8"))
    assert captured.err == ""
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert state["session"]["state"] == "joined"
    assert "/.cmoc/" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert home_branch in _git(repo, "branch", "--format=%(refname:short)").stdout


def test_session_join_ensures_cmoc_ignored_after_switch_to_home_branch(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """home branch 側の tracked `.cmoc` も merge 前に補修する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / ".cmoc").mkdir()
    (repo / ".cmoc" / "home.log").write_text("home log\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/home.log")
    _git(repo, "commit", "-m", "track home cmoc log")
    _checkout_session_branch(repo)
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", "feature.txt")
    _git(repo, "commit", "-m", "feature")

    cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    assert captured.err == ""
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "feature\n"
    assert "/.cmoc/" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_session_join_rejects_non_session_branch_before_git_merge(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """通常 branch 上では session join を開始しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    target_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _git(repo, "checkout", "-b", "feature")
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "feature")
    _git(repo, "checkout", target_branch)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    branches = _git(
        repo,
        "branch",
        "--format=%(refname:short)",
    ).stdout.splitlines()
    assert "session branch 上" in error.value.message
    assert f"現在の branch: {target_branch}" in error.value.detail
    assert (repo / "feature.txt").exists() is False
    assert "feature" in branches
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert "手動解消が必要です" not in captured.err


def test_session_join_precondition_failure_does_not_print_manual_resolution(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """merge 開始前の事前条件失敗では merge state 手動解決を案内しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    state["apply"]["apply_branch"] = (
        "cmoc/apply/2026-05-10_22-21_10_000000123/2026-05-10_22-22_10_000000123"
    )
    state["apply"]["oracle_snapshot_commit"] = _git(
        repo,
        "rev-parse",
        "HEAD",
    ).stdout.strip()
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    assert "apply run" in error.value.message
    assert "手動解消が必要です" not in captured.err


def test_session_join_switch_failure_prints_manual_resolution(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """副作用段階の switch 失敗では merge 前でも手動解決を案内する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    home_branch = state["session"]["session_home_branch"]
    original_run_git = session_join_module.run_git

    def fail_switch_to_home_branch(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """home branch への switch 失敗を模擬する。"""
        if args == ["switch", home_branch]:
            raise subprocess.CalledProcessError(
                128,
                ["git", *args],
                output="",
                stderr="fatal: cannot switch branch",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(
        session_join_module,
        "run_git",
        fail_switch_to_home_branch,
    )

    with pytest.raises(subprocess.CalledProcessError):
        cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    assert "手動解消が必要です" in captured.err
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch


def test_session_join_stops_non_conflict_merge_failure_without_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """conflict ではない merge 失敗では Codex を呼ばず手動解決にする。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "feature")
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    original_run_git = session_join_module.run_git
    codex_calls: list[str] = []

    def fail_merge_without_unmerged_paths(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """merge の非 conflict 失敗を模擬する。"""
        if args == ["merge", "--no-ff", session_branch]:
            return subprocess.CompletedProcess(
                ["git", *args],
                128,
                stdout="",
                stderr="fatal: refusing to merge unrelated histories",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    def fake_codex(*args: object, **kwargs: object) -> None:
        """Codex 呼び出しが誤って発生したことを記録する。"""
        del args, kwargs
        codex_calls.append("called")

    monkeypatch.setattr(
        session_join_module,
        "run_git",
        fail_merge_without_unmerged_paths,
    )
    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    captured = capsys.readouterr()
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "merge conflict は検出されませんでした" in error.value.message
    assert "fatal: refusing to merge unrelated histories" in error.value.detail
    assert "手動解消が必要です" in captured.err
    assert codex_calls == []
    assert state["session"]["state"] == "active"
    assert session_branch in branches


def test_session_join_rejects_binary_conflict_without_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """binary conflict は marker 解消対象にせず手動解消にする。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    (repo / "image.bin").write_bytes(b"base\0content\n")
    _git(repo, "add", ".gitignore", "image.bin")
    _git(repo, "commit", "-m", "prepare binary session")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "image.bin").write_bytes(b"session\0content\n")
    _git(repo, "add", "image.bin")
    _git(repo, "commit", "-m", "session binary change")
    _git(repo, "switch", home_branch)
    (repo / "image.bin").write_bytes(b"home\0content\n")
    _git(repo, "add", "image.bin")
    _git(repo, "commit", "-m", "home binary change")
    _git(repo, "switch", session_branch)
    codex_calls: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> None:
        """Codex 呼び出しが誤って発生したことを記録する。"""
        del args, kwargs
        codex_calls.append("called")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "conflict marker を持たない" in error.value.message
    assert "image.bin" in error.value.detail
    assert codex_calls == []
    assert state["session"]["state"] == "active"
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "diff", "--name-only", "--diff-filter=U").stdout == (
        "image.bin\n"
    )


def test_session_join_rejects_modify_delete_conflict_without_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """delete/modify conflict は marker 不在なので手動解消にする。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    (repo / "deleted.txt").write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "deleted.txt")
    _git(repo, "commit", "-m", "prepare modify delete session")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "deleted.txt").write_text("session\n", encoding="utf-8")
    _git(repo, "add", "deleted.txt")
    _git(repo, "commit", "-m", "session modifies file")
    _git(repo, "switch", home_branch)
    (repo / "deleted.txt").unlink()
    _git(repo, "rm", "deleted.txt")
    _git(repo, "commit", "-m", "home deletes file")
    _git(repo, "switch", session_branch)
    codex_calls: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> None:
        """Codex 呼び出しが誤って発生したことを記録する。"""
        del args, kwargs
        codex_calls.append("called")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "conflict marker を持たない" in error.value.message
    assert "deleted.txt" in error.value.detail
    assert codex_calls == []
    assert state["session"]["state"] == "active"
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "diff", "--name-only", "--diff-filter=U").stdout == (
        "deleted.txt\n"
    )


def test_session_join_rejects_codex_change_outside_conflict_paths(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex が conflict 対象外を変更した場合は merge commit しない。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """conflict を解消しつつ、対象外ファイルを誤って変更する。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        (repo_root / ".gitignore").write_text("tampered\n", encoding="utf-8")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "conflict 対象外" in error.value.message
    assert ".gitignore" in error.value.detail
    assert state["session"]["state"] == "active"
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_rewrite_of_auto_merged_file(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """同じ status の非 conflict path でも内容変更は検出する。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """自動 merge 済みファイルを status 変化なしで書き換える。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        (repo_root / "auto.txt").write_text("tampered\n", encoding="utf-8")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "conflict 対象外" in error.value.message
    assert "auto.txt" in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_rewrite_of_auto_merged_special_path(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """改行や tab を含む非 conflict path の内容変更も検出する。"""
    auto_path = "dir/auto\nname\tfile.txt"
    repo = _repo_with_session_join_conflict(tmp_path, auto_path=auto_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """特殊 path の自動 merge 済みファイルを書き換える。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        (repo_root / auto_path).write_text("tampered\n", encoding="utf-8")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "conflict 対象外" in error.value.message
    assert auto_path in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_staged_rewrite_of_auto_merged_memo(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """memo 内容を読まずに staged auto merge の書き換えを検出する。"""
    repo = _repo_with_session_join_conflict(tmp_path, auto_path="memo/note.md")

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """禁止違反として memo を変更し、git add で status を戻す。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        (repo_root / "memo" / "note.md").write_text(
            "tampered\n",
            encoding="utf-8",
        )
        _git(repo_root, "add", "memo/note.md")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "conflict 対象外" in error.value.message
    assert "memo/note.md" in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_allows_oracle_conflict_path_in_codex_guard(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """session join は conflict 対象 oracle path を Codex guard 例外へ渡す。"""
    repo = _repo_with_session_join_oracle_conflict(tmp_path)
    captured_allowed_paths: list[str] = []

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """oracle conflict を解消し、guard 例外対象を記録する。"""
        del prompt
        allowed = kwargs.get("allowed_uncommitted_oracle_paths")
        assert isinstance(allowed, list)
        captured_allowed_paths.extend(allowed)
        (repo_root / "oracles" / "spec.md").write_text(
            "resolved oracle\n",
            encoding="utf-8",
        )

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert captured_allowed_paths == ["oracles/spec.md"]
    assert state["session"]["state"] == "joined"
    assert (repo / "oracles" / "spec.md").read_text(encoding="utf-8") == (
        "resolved oracle\n"
    )


def test_session_join_allows_clean_auto_merged_root_forbidden_file(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """conflict 対象外で自動 merge 済みの README 変更は merge 成果物に含める。"""
    repo = _repo_with_session_join_conflict(tmp_path, auto_path="README.md")

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """本物の Codex CLI なしで conflict 対象だけを解消する。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["session"]["state"] == "joined"
    assert (repo / "README.md").read_text(encoding="utf-8") == "session auto\n"
    assert _git(repo, "status", "--porcelain").stdout == ""


@pytest.mark.parametrize("root_doc_path", ["README.md", "AGENTS.md"])
def test_session_join_rejects_root_doc_file_conflict_without_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    root_doc_path: str,
) -> None:
    """README/AGENTS の conflict は Codex CLI に渡さず手動解決にする。"""
    repo = _repo_with_session_join_root_doc_conflict(tmp_path, root_doc_path)
    codex_calls: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> None:
        """Codex 呼び出しが誤って発生したことを記録する。"""
        del args, kwargs
        codex_calls.append("called")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "Codex CLI に依頼できない禁止領域" in error.value.message
    assert root_doc_path in error.value.detail
    assert codex_calls == []
    assert state["session"]["state"] == "active"
    assert (repo / ".git" / "MERGE_HEAD").exists()


def test_session_join_ignores_markers_outside_conflict_paths(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """conflict 対象外の通常内容にある marker 風文字列では止めない。"""
    repo = _repo_with_session_join_conflict(tmp_path)
    (repo / "literal_markers.txt").write_text(
        "<<<<<<< sample\n"
        "left\n"
        "=======\n"
        "right\n"
        ">>>>>>> sample\n",
        encoding="utf-8",
    )
    _git(repo, "add", "literal_markers.txt")
    _git(repo, "commit", "-m", "add literal marker sample")

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """本物の Codex CLI なしで conflict 対象だけを解消する。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["session"]["state"] == "joined"
    assert (repo / "literal_markers.txt").read_text(encoding="utf-8").startswith(
        "<<<<<<< sample\n"
    )


def test_session_join_rejects_remaining_diff3_base_marker(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """diff3/zdiff3 の base marker が残る場合も merge commit しない。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """base marker だけが残る不完全な conflict 解消を模擬する。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text(
            "resolved\n"
            "||||||| base\n"
            "base text still present\n",
            encoding="utf-8",
        )

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "conflict marker" in error.value.message
    assert "conflict.txt" in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_change_in_forbidden_path(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex が禁止領域を作成した場合も merge commit しない。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """conflict 解消後に禁止 path を誤って作る。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        (repo_root / ".agents").mkdir()
        (repo_root / ".agents" / "note.txt").write_text(
            "forbidden\n",
            encoding="utf-8",
        )

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "conflict 対象外" in error.value.message
    assert ".agents/note.txt" in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_created_merge_commit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex が git add/commit まで進めた場合は cmoc の commit に進まない。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """prompt 違反として merge commit を作成する。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        _git(repo_root, "add", "conflict.txt")
        _git(repo_root, "commit", "--no-edit")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "merge state" in error.value.message
    assert "head:" in error.value.detail
    assert "merge_head:" in error.value.detail
    assert state["session"]["state"] == "active"
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip().startswith(
        "Merge branch"
    )


def test_session_join_rejects_codex_staged_conflict_resolution(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex が git add だけ実行した場合も cmoc の add/commit に進まない。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """prompt 違反として conflict 対象を stage する。"""
        del prompt, kwargs
        (repo_root / "conflict.txt").write_text("resolved\n", encoding="utf-8")
        _git(repo_root, "add", "conflict.txt")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "merge state" in error.value.message
    assert "unmerged_index: changed" in error.value.detail
    assert (repo / ".git" / "MERGE_HEAD").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_aborted_merge(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex が merge state を中止した場合は後続の add/commit に進まない。"""
    repo = _repo_with_session_join_conflict(tmp_path)

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """prompt 違反として merge を abort する。"""
        del prompt, kwargs
        _git(repo_root, "merge", "--abort")

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "merge state" in error.value.message
    assert "merge_head:" in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "home change"


def test_session_join_rejects_codex_switched_branch_after_abort(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex が branch を移動した場合は現在 branch の変化を明示検出する。"""
    repo = _repo_with_session_join_conflict(tmp_path)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()

    def fake_codex(
        repo_root: Path,
        prompt: str,
        **kwargs: object,
    ) -> None:
        """prompt 違反として merge を abort して session branch へ戻る。"""
        del prompt, kwargs
        _git(repo_root, "merge", "--abort")
        _git(repo_root, "switch", session_branch)

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_session_join_impl(repo)

    assert "merge state" in error.value.message
    assert "branch:" in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
@pytest.mark.parametrize(
    "relative_path",
    [
        ".cmoc/state.json",
        ".agents/config.json",
        "memo/note.md",
    ],
)
def test_session_join_forbidden_conflict_paths_exclude_root_docs(
    relative_path: str,
) -> None:
    """session join は編集禁止 path の conflict を Codex に渡さない。"""
    assert session_join_module._is_forbidden_conflict_path(relative_path)


@pytest.mark.parametrize("relative_path", ["README.md", "AGENTS.md"])
def test_session_join_root_docs_are_forbidden_conflict_paths(
    relative_path: str,
) -> None:
    """README/AGENTS の conflict は marker 解消対象にしない。"""
    assert session_join_module._is_forbidden_conflict_path(relative_path)


def test_session_join_conflict_prompt_allows_marker_only_oracle_fix() -> None:
    """conflict 対象 oracle file は marker 解消に限って編集できる。"""
    repo = Path("/repo")

    prompt = _conflict_prompt(repo, ["app.py", "oracles/spec.md"])

    assert "あなたは merge conflict 解消担当です。" in prompt
    assert "cmoc session join" not in prompt
    assert "`/repo/oracles` は編集禁止です。" not in prompt
    assert "`/repo/.cmoc` は編集禁止です。" in prompt
    assert "`/repo/README.md` は編集禁止です。" in prompt
    assert "`/repo/AGENTS.md` は編集禁止です。" in prompt
    assert "['/repo/app.py', '/repo/oracles/spec.md']" in prompt
    assert "['app.py" not in prompt
    assert "conflict marker 解消に限って編集できます" in prompt
    assert "意味的な仕様改訂" in prompt
    assert "conflict 対象外 oracle file の編集は禁止" in prompt
    assert "解決内容と未解決ファイルの有無を報告" in prompt


def test_session_join_conflict_prompt_keeps_root_docs_forbidden() -> None:
    """README/AGENTS は conflict prompt でも編集禁止として指示する。"""
    repo = Path("/repo")

    prompt = _conflict_prompt(repo, ["README.md", "AGENTS.md"])

    assert "`/repo/README.md` は編集禁止です。" in prompt
    assert "`/repo/AGENTS.md` は編集禁止です。" in prompt
    assert "['/repo/README.md', '/repo/AGENTS.md']" in prompt
    assert "root document file は conflict marker 解消に限って編集できます" not in prompt
    assert "conflict 対象外 root document file の編集は禁止" not in prompt


def test_files_with_conflict_markers_checks_requested_paths_only(
    tmp_path: Path,
) -> None:
    """marker 検査は渡された対象一覧だけを見る。"""
    repo = _init_repo(tmp_path)
    conflicted = repo / "conflicted.txt"
    unrelated = repo / "unrelated.txt"
    conflicted.write_text(
        "<<<<<<< HEAD\nleft\n=======\nright\n>>>>>>> branch\n",
        encoding="utf-8",
    )
    unrelated.write_text(
        "<<<<<<< HEAD\nleft\n=======\nright\n>>>>>>> branch\n",
        encoding="utf-8",
    )
    _git(repo, "add", "conflicted.txt", "unrelated.txt")
    _git(repo, "commit", "-m", "add tracked files")

    assert _files_with_conflict_markers(repo, ["conflicted.txt"]) == [
        "conflicted.txt"
    ]
