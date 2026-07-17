"""session fork/join/abandon の CLI 外部挙動をまとめて検証する。

このファイルは 16,000 文字を超えるが、責務境界は session branch と session state の
ライフサイクルに閉じている。fork、join、abandon、linked worktree、state cleanup、
dirty worktree 拒否は同じ session 状態遷移の観測点であり、分割すると同じ branch/state
fixture を追う文脈が分散する。現状は session CLI 回帰として一箇所に保つ方が凝集性が高い。
根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import json
import subprocess
from collections.abc import Iterator
from pathlib import Path

import pytest
from _cli_support import runner
from _git_support import current_branch, make_repo, run_git
from _ollama_support import run_doctor

import cmoc_runtime
import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.session.abandon as session_module
import sub_commands.session.fork as session_fork_module
import sub_commands.session.join as session_join_module
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError
from commons.runtime_codex_profile import build_codex_override_args
from config.cmoc_config import CmocConfig
from main import app


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    """テスト間で process-global な preflight 状態を持ち越さない。

    根拠: {{work-root}}/oracle/doc/dev_rule/test_rule.md
    """

    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


def session_state_path(root: Path, session_branch: str) -> Path:
    """managed session branch に対応する永続 state file の path を求める。

    根拠: {{work-root}}/oracle/doc/app_spec/session_state.md
    """

    session_id = session_branch.removeprefix("cmoc/session/")
    return root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"


def session_home_branch(root: Path, session_branch: str) -> str:
    """session state から fork 元かつ join 先の home branch を読む。

    根拠: {{work-root}}/oracle/doc/app_spec/session_state.md
    """

    state = json.loads(session_state_path(root, session_branch).read_text())
    return state["session"]["session_home_branch"]


def write_abandoned_state(root: Path, session_id: str) -> Path:
    """session fork の session-id collision 用に abandoned state を作る。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    {{work-root}}/oracle/doc/app_spec/session_state.md
    """

    path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "session": {
                    "state": "abandoned",
                    "session_home_branch": "old-home",
                    "session_start_commit": "old-commit",
                    "last_joined_apply_oracle_snapshot_commit": None,
                    "joined_at": None,
                },
                "apply": {
                    "state": "ready",
                    "apply_branch": None,
                    "oracle_snapshot_commit": None,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    return path


def break_preprocess_invariants(work: Path) -> Path:
    """doctor preprocess が修復すべき ignore/tracking 破損状態を commit する。

    根拠: {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    """

    gitignore = work / ".gitignore"
    gitignore.write_text(
        "\n".join(
            line for line in gitignore.read_text().splitlines() if line != "/.cmoc/gu/"
        )
        + "\n"
    )
    tracked_probe = work / ".cmoc" / "gu" / "tracked-probe"
    tracked_probe.parent.mkdir(parents=True, exist_ok=True)
    tracked_probe.write_text("tracked\n")
    run_git(work, "add", ".gitignore")
    run_git(work, "add", "-f", ".cmoc/gu/tracked-probe")
    run_git(work, "rm", ".agents/.gitkeep")
    run_git(work, "commit", "-m", "break preprocess invariants")
    return gitignore


def test_session_fork_creates_session_branch_and_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session forkがbranchとactive stateを作ることを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    home_branch = current_branch(root)
    doctor_result = run_doctor(root)
    assert doctor_result.exit_code == 0

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    branch = current_branch(root)
    assert branch.startswith("cmoc/session/")
    state = json.loads(session_state_path(root, branch).read_text())
    assert state["session"]["state"] == "active"
    assert state["session"]["session_home_branch"] == home_branch
    assert state["session"]["last_joined_apply_oracle_snapshot_commit"] is None
    assert state["session"]["joined_at"] is None
    assert state["apply"]["state"] == "ready"


def test_session_fork_rolls_back_when_state_save_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """state 保存失敗時に branch と state を作成前へ戻す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    home_branch = current_branch(root)
    session_id = "2026-06-27_01-02_03_000000000"
    session_branch = f"cmoc/session/{session_id}"
    monkeypatch.setattr(session_fork_module, "timestamp", lambda: session_id)

    def fail_write_state(_path: Path, _state: cmoc_runtime.SessionState) -> None:
        """state保存を失敗させ、fork rollback経路を検証する。"""
        raise OSError("state write failed")

    monkeypatch.setattr(session_fork_module, "write_state", fail_write_state)

    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code != 0
    assert current_branch(root) == home_branch
    assert not session_state_path(root, session_branch).exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch],
            cwd=root,
        ).returncode
        != 0
    )
    assert "session fork の作成に失敗しました。" in result.stdout
    assert "session_branch_exists: False" in result.stdout
    assert "session_state_file_exists: False" in result.stdout


def test_session_fork_does_not_overwrite_existing_state_on_session_id_collision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session id衝突時に既存abandoned stateを上書きしないことを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    session_id = "2026-06-27_01-02_03_000000000"
    path = write_abandoned_state(root, session_id)
    original = path.read_text()
    home_branch = current_branch(root)
    monkeypatch.setattr(session_fork_module, "timestamp", lambda: session_id)
    monkeypatch.setattr(session_fork_module, "MAX_SESSION_ID_ATTEMPTS", 2)

    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code != 0
    assert "一意な session-id を生成できませんでした。" in result.stdout
    assert path.read_text() == original
    assert current_branch(root) == home_branch
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", f"cmoc/session/{session_id}"],
            cwd=root,
        ).returncode
        != 0
    )


def test_session_fork_retries_session_id_collision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session id衝突後に次のtimestampでforkを再試行することを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    collision_id = "2026-06-27_01-02_03_000000000"
    next_id = "2026-06-27_01-02_03_000000001"
    old_path = write_abandoned_state(root, collision_id)
    original = old_path.read_text()
    ids = iter([collision_id, next_id])
    monkeypatch.setattr(session_fork_module, "timestamp", lambda: next(ids))

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == f"cmoc/session/{next_id}"
    assert old_path.read_text() == original
    assert (root / ".cmoc" / "gu" / "ar" / "session" / f"{next_id}.json").is_file()
    assert f"- session_branch: `cmoc/session/{next_id}`" in result.output


def test_session_fork_rejects_corrupt_state_without_active_session_message(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """壊れたstateをactive session未存在として誤報しないことを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    home_branch = current_branch(root)
    path = root / ".cmoc" / "gu" / "ar" / "session" / "broken.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"session": {"session_home_branch": home_branch}, "apply": {}})
        + "\n"
    )

    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code != 0
    assert "session state file が不正です。" in result.stdout
    assert "active session が既に存在します。" not in result.stdout
    assert current_branch(root) == home_branch


def test_session_fork_initializes_cmoc_ignore_before_logging(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session forkがlog作成前にcmoc ignoreを初期化することを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    home_branch = current_branch(root)

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    branch = current_branch(root)
    assert branch.startswith("cmoc/session/")
    assert session_home_branch(root, branch) == home_branch
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert (
        subprocess.run(
            ["git", "check-ignore", "-q", ".cmoc/gu/.__cmoc_ignore_probe__"],
            cwd=root,
        ).returncode
        == 0
    )
    assert (
        len(
            list((root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl"))
        )
        == 1
    )
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_session_fork_uses_linked_worktree_branch_and_head(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree上のbranchとHEADからsessionをforkすることを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    root_branch = current_branch(root)
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    (linked / "README.md").write_text("# linked\n")
    run_git(linked, "add", "README.md")
    run_git(linked, "commit", "-m", "linked change")
    linked_commit = run_git(linked, "rev-parse", "HEAD").stdout.strip()
    monkeypatch.chdir(linked)

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    session_branch = current_branch(linked)
    assert session_branch.startswith("cmoc/session/")
    assert current_branch(root) == root_branch
    state = json.loads(session_state_path(root, session_branch).read_text())
    assert state["session"]["session_home_branch"] == "linked-home"
    assert state["session"]["session_start_commit"] == linked_commit
    assert run_git(linked, "rev-parse", session_branch).stdout.strip() == linked_commit


def test_session_abandon_switches_home_and_marks_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session abandonがhome branchへ戻りstateをabandonedにすることを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    state_path = session_state_path(root, session_branch)
    home_branch = session_home_branch(root, session_branch)
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()

    result = runner.invoke(app, ["session", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == home_branch
    assert run_git(root, "rev-parse", home_branch).stdout.strip() == home_commit
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["session"]["state"] == "abandoned"
    assert state["session"]["joined_at"] is None
    assert f"- abandoned_branch: `{session_branch}`" in result.output
    assert "- session_state: `abandoned`" in result.output


def test_session_abandon_uses_linked_worktree_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree上のsession abandonが対応home branchを使うことを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    root_branch = current_branch(root)
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(linked)
    state_path = session_state_path(root, session_branch)
    home_branch = session_home_branch(root, session_branch)
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()

    result = runner.invoke(app, ["session", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == root_branch
    assert current_branch(linked) == home_branch
    assert run_git(root, "rev-parse", home_branch).stdout.strip() == home_commit
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["session"]["state"] == "abandoned"
    assert state["session"]["joined_at"] is None
    assert f"- abandoned_branch: `{session_branch}`" in result.output


def test_session_abandon_preprocesses_linked_worktree_before_preconditions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree の abandon が固有の事前条件より先に preprocess することを検証する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_abandon.md
    {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(linked)
    home_branch = session_home_branch(root, session_branch)
    gitignore = break_preprocess_invariants(linked)
    run_git(root, "branch", "-D", home_branch)

    result = runner.invoke(app, ["session", "abandon"])

    assert result.exit_code != 0
    assert current_branch(linked) == session_branch
    assert "session home branch が存在しません。" in result.stdout
    assert "/.cmoc/gu/" in gitignore.read_text().splitlines()
    assert run_git(linked, "ls-files", "--", ".cmoc/gu").stdout == ""
    assert run_git(linked, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
    assert run_git(linked, "status", "--short").stdout.strip() == ""


def test_session_abandon_requires_existing_home_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """home branchが存在しないsession abandonを拒否することを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()
    gitignore = root / ".gitignore"
    gitignore.write_text(
        "\n".join(
            line for line in gitignore.read_text().splitlines() if line != "/.cmoc/gu/"
        )
        + "\n"
    )
    tracked_probe = root / ".cmoc" / "gu" / "tracked-probe"
    tracked_probe.parent.mkdir(parents=True, exist_ok=True)
    tracked_probe.write_text("tracked\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "add", "-f", ".cmoc/gu/tracked-probe")
    run_git(root, "commit", "-m", "track cmoc probe on session")
    run_git(root, "branch", "-D", home_branch)
    run_git(root, "tag", home_branch, home_commit)

    result = runner.invoke(app, ["session", "abandon"])

    assert result.exit_code != 0
    assert "完了 session abandon" in result.output
    assert "- サブコマンドログ: `" in result.output
    assert "- ステップ経過時間[2/4 事前条件を確認]: `" in result.output
    assert "- 経過時間: `" in result.output
    assert "- quota 待機時間: `" in result.output
    assert "- 終了コード: `1`" in result.output
    assert current_branch(root) == session_branch
    assert "session home branch が存在しません。" in result.stdout
    assert "session home branch が存在しません。" not in result.stderr
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )
    assert "/.cmoc/gu/" in gitignore.read_text().splitlines()
    assert run_git(root, "ls-files", "--", ".cmoc/gu").stdout == ""


@pytest.mark.parametrize(
    "cleanup_error",
    [
        CmocError("delete failed", ["next"], "branch delete failed"),
        KeyboardInterrupt(),
    ],
)
def test_session_abandon_rolls_back_state_and_branch_on_cleanup_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, cleanup_error: BaseException
) -> None:
    """cleanup失敗時にsession branchとactive stateを復元することを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    state_path = session_state_path(root, session_branch)
    gitignore = root / ".gitignore"
    gitignore.write_text(
        "\n".join(
            line for line in gitignore.read_text().splitlines() if line != "/.cmoc/gu/"
        )
        + "\n"
    )
    tracked_probe = root / ".cmoc" / "gu" / "tracked-probe"
    tracked_probe.parent.mkdir(parents=True, exist_ok=True)
    tracked_probe.write_text("tracked\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "add", "-f", ".cmoc/gu/tracked-probe")
    run_git(root, "commit", "-m", "track cmoc probe on session")
    original_delete_branch = session_module.delete_branch

    def fake_delete_branch(root: Path, branch: str, force: bool = False) -> None:
        """対象session branchの削除だけを指定exceptionで失敗させる。"""
        if branch == session_branch:
            raise cleanup_error
        return original_delete_branch(root, branch, force)

    monkeypatch.setattr(session_module, "delete_branch", fake_delete_branch)

    result = runner.invoke(app, ["session", "abandon"])

    assert result.exit_code != 0
    assert "session abandon の cleanup に失敗しました。" in result.stdout
    assert "`cmoc session abandon` を再実行してください。" in result.stdout
    assert "session abandon の cleanup に失敗しました。" not in result.stderr
    assert current_branch(root) == session_branch
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )
    state = json.loads(state_path.read_text())
    assert state["session"]["state"] == "active"
    assert state["session"]["joined_at"] is None
    assert "/.cmoc/gu/" in gitignore.read_text().splitlines()
    assert run_git(root, "ls-files", "--", ".cmoc/gu").stdout == ""
    assert run_git(root, "status", "--short").stdout.strip() == ""


@pytest.mark.parametrize("command", ["abandon", "join"])
def test_session_completion_rejects_missing_state_fields(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, command: str
) -> None:
    """session completionが必須state field欠落を拒否することを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    path = session_state_path(root, session_branch)
    broken_state = {
        "session": {"session_home_branch": session_home_branch(root, session_branch)}
    }
    path.write_text(json.dumps(broken_state) + "\n")

    result = runner.invoke(app, ["session", command])

    assert result.exit_code != 0
    assert "session state file が不正です。" in result.stdout
    assert "必須 field" in result.stdout
    assert current_branch(root) == session_branch


def test_session_join_resolves_oracle_conflict_with_repo_write_sandbox(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """oracle conflict 解消時の REPO_WRITE sandbox と prompt 境界を検証する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
    {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    {{work-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py
    """

    root = make_repo(tmp_path)
    target = root / "oracle" / "spec.md"
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    target.write_text("session change\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "session change")
    run_git(root, "switch", home_branch)
    target.write_text("home change\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "home change")
    run_git(root, "switch", session_branch)
    calls: list[str] = []
    modes: list[FileAccessMode] = []

    class FakeCodexResult:
        """conflict resolution の成功を表す最小 fake result。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
        """

        output_json = None

    def fake_run_codex_exec(parameter: AgentCallParameter, **kwargs: object) -> object:
        """Codex 呼び出しを置換し、path 別 override がないことを検証する。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
        {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        """

        calls.append(kwargs["purpose"])
        modes.append(parameter.file_access_mode)
        assert set(kwargs) == {"root", "cwd", "purpose"}
        assert str(target) in parameter.prompt
        override_args = build_codex_override_args(
            parameter,
            CmocConfig(),
        )
        assert override_args[override_args.index("--sandbox") + 1] == (
            "workspace-write"
        )
        assert all("permissions" not in arg for arg in override_args)
        assert all(str(target) not in arg for arg in override_args)
        target.write_text("resolved change\nTitle\n=======\n")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert current_branch(root) == home_branch
    assert target.read_text() == "resolved change\nTitle\n=======\n"
    assert calls == ["session join conflict resolution"]
    assert modes == [FileAccessMode.REPO_WRITE]


def test_session_join_handles_conflict_path_containing_newline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """改行を含むconflict pathをNUL framingで解消できることを検証する。"""
    root = make_repo(tmp_path)
    target = root / "src" / "line\nbreak.txt"
    target.parent.mkdir()
    target.write_text("base\n")
    run_git(root, "add", "src/line\nbreak.txt")
    run_git(root, "commit", "-m", "add newline path")
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    target.write_text("session change\n")
    run_git(root, "add", "src/line\nbreak.txt")
    run_git(root, "commit", "-m", "session change")
    run_git(root, "switch", home_branch)
    target.write_text("home change\n")
    run_git(root, "add", "src/line\nbreak.txt")
    run_git(root, "commit", "-m", "home change")
    run_git(root, "switch", session_branch)

    class FakeCodexResult:
        """conflict resolution成功を表す最小結果double。"""

        output_json = None

    def fake_run_codex_exec(parameter: AgentCallParameter, **kwargs: object) -> object:
        """conflict pathをpromptに含め、解消済み内容を書き込む。"""
        assert set(kwargs) == {"root", "cwd", "purpose"}
        assert str(target) in parameter.prompt
        target.write_text("resolved change\n")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == home_branch
    assert target.read_text() == "resolved change\n"
    assert run_git(root, "diff", "--name-only", "-z", "--diff-filter=U").stdout == ""


def test_session_join_reports_unmerged_path_as_absolute(tmp_path: Path) -> None:
    """unmerged pathを絶対pathでerror detailへ出すことを検証する。"""
    root = tmp_path
    target = root / "src" / "unmerged.py"
    target.parent.mkdir()

    def fake_git(args: list[str], cwd: Path) -> cmoc_runtime.CommandResult:
        """unmerged pathをNUL区切りで返すGit double。"""
        if args == ["diff", "--name-only", "-z", "--diff-filter=U"]:
            return cmoc_runtime.CommandResult(0, "src/unmerged.py\0", "")
        return cmoc_runtime.CommandResult(0, "", "")

    def fake_codex_exec(parameter: object, **kwargs: object) -> object:
        """Codex呼び出しが不要な経路のための最小double。"""
        return object()

    with pytest.raises(CmocError) as error:
        session_join_module.resolve_session_join_conflict(
            root, fake_codex_exec, fake_git
        )

    assert error.value.summary == "unmerged path が残っています。"
    assert error.value.detail == str(target)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Title\n=======\n", False),
        ("<<<<<<< HEAD\nhome\n=======\nsession\n>>>>>>> branch\n", True),
        ("<<<<<<< HEAD\nhome\n========\nsession\n>>>>>>> branch\n", True),
        ("<<<<<<< HEAD\nhome\n", True),
        ("||||||| base\n", True),
        (">>>>>>> branch\n", True),
    ],
)
def test_session_join_conflict_marker_detection(text: str, expected: bool) -> None:
    """conflict marker blockの残存判定が各入力に一致することを検証する。"""
    assert session_join_module._has_conflict_marker_block(text) is expected


def test_session_join_uses_linked_worktree_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree上のsession joinが対応home branchを使うことを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    root_branch = current_branch(root)
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(linked)
    home_branch = session_home_branch(root, session_branch)
    (linked / "README.md").write_text("linked session change\n")
    run_git(linked, "add", "README.md")
    run_git(linked, "commit", "-m", "linked session change")

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == root_branch
    assert current_branch(linked) == home_branch
    assert (linked / "README.md").read_text() == "linked session change\n"
    state = json.loads(session_state_path(root, session_branch).read_text())
    assert state["session"]["state"] == "joined"
    assert state["session"]["joined_at"] is None


def test_session_join_preprocesses_linked_worktree_before_preconditions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree の join が固有の事前条件より先に preprocess することを検証する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
    {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(linked)
    home_branch = session_home_branch(root, session_branch)
    gitignore = break_preprocess_invariants(linked)
    run_git(root, "branch", "-D", home_branch)

    result = runner.invoke(app, ["session", "join"])

    assert result.exit_code != 0
    assert current_branch(linked) == session_branch
    assert "git コマンドが失敗しました。" in result.stderr
    assert "git コマンドが失敗しました。" not in result.stdout
    assert "/.cmoc/gu/" in gitignore.read_text().splitlines()
    assert run_git(linked, "ls-files", "--", ".cmoc/gu").stdout == ""
    assert run_git(linked, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
    assert run_git(linked, "status", "--short").stdout.strip() == ""


def test_session_join_stages_delete_conflict_resolution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Codexが解決した削除をstageしてsession joinできることを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    (root / "README.md").unlink()
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session deletes readme")
    run_git(root, "switch", home_branch)
    (root / "README.md").write_text("home change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "home changes readme")
    run_git(root, "switch", session_branch)

    class FakeCodexResult:
        """conflict resolution成功を表す最小結果double。"""

        output_json = None

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        """conflict対象を削除して解消済み結果を返す。"""
        (root / "README.md").unlink()
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == home_branch
    assert not (root / "README.md").exists()
    assert run_git(root, "diff", "--name-only", "--diff-filter=U").stdout == ""


def test_session_join_warns_when_session_branch_cannot_be_deleted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session branch削除失敗をwarningとしてjoin成功に含めることを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    original_run_git = session_join_module.run_git

    def fake_run_git(args: list[str], cwd: Path, check: bool = True) -> object:
        """session branch削除だけを失敗させ、他のGit操作は委譲する。"""
        if args == ["branch", "-d", session_branch]:
            return cmoc_runtime.CommandResult(1, "", "branch is checked out elsewhere")
        return original_run_git(args, cwd, check=check)

    monkeypatch.setattr(session_join_module, "run_git", fake_run_git)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == home_branch
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )
    assert "- deleted_session_branch: `False`" in result.output
    assert f"session branch was not deleted: {session_branch}" in result.output


def test_session_join_does_not_delete_when_local_branch_reachability_check_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """local session branchのreachability確認失敗時に削除しないことを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    original_run_git = session_join_module.run_git
    delete_calls = 0

    def fake_run_git(args: list[str], cwd: Path, check: bool = True) -> object:
        """reachability確認を失敗させ、他のGit操作は委譲する。"""
        nonlocal delete_calls
        if args == ["merge-base", "--is-ancestor", session_branch, "HEAD"]:
            return cmoc_runtime.CommandResult(1, "", "")
        if args == ["branch", "-d", session_branch]:
            delete_calls += 1
        return original_run_git(args, cwd, check=check)

    monkeypatch.setattr(session_join_module, "run_git", fake_run_git)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == home_branch
    assert delete_calls == 0
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )
    assert "- deleted_session_branch: `False`" in result.output
    assert f"session branch was not deleted: {session_branch}" in result.output


def test_session_join_error_report_is_written_to_stdout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """事前条件error reportをstdoutへ出力することを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "README.md").write_text("dirty\n")

    result = runner.invoke(app, ["session", "join"])

    assert result.exit_code != 0
    assert "完了 session join" in result.stdout
    assert "# ERROR" in result.stdout
    assert "git 未コミット差分が存在します。" in result.stdout
    assert "# ERROR" not in result.stderr
    assert "git 未コミット差分が存在します。" not in result.stderr


def test_session_join_unexpected_error_after_merge_is_written_to_stderr(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """merge後の予期せぬconflict error reportをstderrへ出力することを検証する。"""
    root = make_repo(tmp_path)
    target = root / "README.md"
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    target.write_text("session change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session change")
    run_git(root, "switch", home_branch)
    target.write_text("home change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "home change")
    run_git(root, "switch", session_branch)

    class FakeCodexResult:
        """conflict resolution結果だけを提供する最小double。"""

        output_json = None

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        """未解決markerを残した結果を返し、後段errorを発生させる。"""
        target.write_text("<<<<<<< HEAD\nhome\n========\nsession\n>>>>>>> branch\n")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"])

    assert result.exit_code != 0
    assert current_branch(root) == home_branch
    assert "# ERROR" not in result.stdout
    assert "conflict marker が残っています。" not in result.stdout
    assert "# ERROR" in result.stderr
    assert "conflict marker が残っています。" in result.stderr


def test_session_join_conflict_uses_repo_root_for_codex_storage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree の conflict 解消で Codex storage は repo root、cwd は linked worktree になることを検証する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
    {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    {{work-root}}/oracle/src/oracle/other/path_model.py
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(linked)
    home_branch = session_home_branch(root, session_branch)
    target = linked / "oracle" / "spec.md"
    target.write_text("linked session change\n")
    run_git(linked, "add", "oracle/spec.md")
    run_git(linked, "commit", "-m", "linked session change")
    run_git(linked, "switch", home_branch)
    target.write_text("linked home change\n")
    run_git(linked, "add", "oracle/spec.md")
    run_git(linked, "commit", "-m", "linked home change")
    run_git(linked, "switch", session_branch)
    seen: dict[str, Path] = {}

    class FakeCodexResult:
        """conflict resolution の成功を表す最小 fake result。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
        """

        output_json = None

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        """Codex wrapper に渡された repo root と linked-worktree cwd を記録する。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
        {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        """

        seen["root"] = kwargs["root"]
        seen["cwd"] = kwargs["cwd"]
        target.write_text("resolved change\nTitle\n=======\n")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert seen == {"root": root, "cwd": linked}
    assert current_branch(linked) == home_branch
    assert target.read_text() == "resolved change\nTitle\n=======\n"
