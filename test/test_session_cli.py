"""session fork/join/abandon の CLI 外部挙動をまとめて検証する。

このファイルは 16,000 文字を超えるが、責務境界は session branch と session state の
ライフサイクルに閉じている。fork、join、abandon、linked worktree、state cleanup、
dirty worktree 拒否は同じ session 状態遷移の観測点であり、分割すると同じ branch/state
fixture を追う文脈が分散する。現状は session CLI 回帰として一箇所に保つ方が凝集性が高い。

根拠:
- {{work-root}}/oracle/doc/app_spec/oracle_and_realization.md の
  「realization file を扱う判断基準」
- {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
- {{work-root}}/oracle/doc/app_spec/feedback_state.md
- {{work-root}}/oracle/doc/app_spec/session_state.md
- {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
- {{work-root}}/oracle/doc/app_spec/sub_command/session_abandon.md
- {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
"""

import json
import stat
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path

import pytest
from _cli_support import (
    runner,
    seed_search_config,
    terminal_primary_report,
)
from _git_support import (
    RUN_ID,
    SESSION_BRANCH,
    SESSION_ID,
    current_branch,
    make_repo,
    run_git,
)

import cmoc_runtime
import commons.runtime_cli as runtime_cli
import commons.runtime_merge_conflict as merge_conflict_module
import sub_commands.session.abandon as session_module
import sub_commands.session.fork as session_fork_module
import sub_commands.session.join as session_join_module
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError
from commons.runtime_codex_profile import build_codex_override_args
from commons.runtime_refactor import sync_refactor_state, write_refactor_state
from config.cmoc_config import CmocConfig
from main import app


def _seed_remote_tracking_branch(root: Path, branch: str, commit: str) -> None:
    """checkout の推測候補になる remote 設定と追跡 ref を用意する。"""
    # 推測は local の fetch refspec と追跡 ref を使うため、remote の実体は不要。
    run_git(root, "remote", "add", "origin", str(root.parent / "remote.git"))
    run_git(root, "update-ref", f"refs/remotes/origin/{branch}", commit)
    run_git(root, "config", "checkout.defaultRemote", "origin")


def session_state_path(root: Path, session_branch: str) -> Path:
    """managed session branch に対応する永続 state file の path を求める。

    根拠: {{work-root}}/oracle/doc/app_spec/session_state.md
    """

    session_id = session_branch.removeprefix("cmoc/session/")
    return root / ".cmoc" / "gu" / "session" / f"{session_id}.json"


def session_home_branch(root: Path, session_branch: str) -> str:
    """session state から fork 元かつ join 先の home branch を読む。

    根拠: {{work-root}}/oracle/doc/app_spec/session_state.md
    """

    state = json.loads(session_state_path(root, session_branch).read_text())
    return state["session"]["session_home_branch"]


def _seed_session_management_files(root: Path) -> None:
    """session test の clean な管理ファイルを、doctor CLI を実行せず用意する。"""
    # 管理物の検証・修復は各 command 自身の doctor と専用ケースに残す。
    # tracked 管理物も揃え、前処理の修復 commit で検査対象の HEAD を進めない。
    (root / ".gitignore").write_text("/.cmoc/gu/\n")
    seed_search_config(root)
    agents = root / ".agents"
    agents.mkdir()
    (agents / ".gitkeep").touch()
    # state 自身も列挙対象なので、空 state を置いてから entry を同期する。
    write_refactor_state(root, {})
    sync_refactor_state(root)
    run_git(
        root,
        "add",
        ".gitignore",
        ".agents/.gitkeep",
        ".cmoc/gt/config.json",
        ".cmoc/gt/realization/refactor/state.json",
    )
    run_git(root, "commit", "-m", "session seed")


def _seed_active_session(root: Path) -> tuple[str, str]:
    """session 終了の検査に必要な clean session を、fork CLI を実行せず用意する。"""
    # fork の branch/state 作成と fork→join/abandon の連携は専用 test に残す。
    _seed_session_management_files(root)
    return _seed_session_in_worktree(root, root)


def _seed_session_in_worktree(root: Path, work: Path) -> tuple[str, str]:
    """clean な worktree に session を作り、repo-root に state を保存する。"""
    home_branch = current_branch(work)
    fork_commit = run_git(work, "rev-parse", "HEAD").stdout.strip()
    run_git(work, "switch", "-c", SESSION_BRANCH, fork_commit)
    state = cmoc_runtime.SessionState()
    state.session.session_home_branch = home_branch
    state.session.session_fork_commit = fork_commit
    cmoc_runtime.write_state(session_state_path(root, SESSION_BRANCH), state)
    return SESSION_BRANCH, home_branch


def write_abandoned_state(root: Path, session_id: str) -> Path:
    """session fork の session-id collision 用に abandoned state を作る。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    {{work-root}}/oracle/doc/app_spec/session_state.md
    """

    path = root / ".cmoc" / "gu" / "session" / f"{session_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "session": {
                    "state": "abandoned",
                    "session_home_branch": "old-home",
                    "session_fork_commit": "old-commit",
                    "last_joined_apply_fork_commit": None,
                },
                "run": {
                    "state": "ready",
                    "kind": None,
                    "branch": None,
                    "fork_commit": None,
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
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """同じ fork 成功経路で branch/state/report と ignore/log/clean 状態を検証する。"""
    # fork の検査には実 Git の HEAD が必要だが、追跡ファイルの内容は使わない。
    root = committed_repository
    monkeypatch.chdir(root)
    home_branch = current_branch(root)
    seed_search_config(root)

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    branch = current_branch(root)
    assert branch.startswith("cmoc/session/")
    state = json.loads(session_state_path(root, branch).read_text())
    assert state["session"]["state"] == "active"
    assert state["session"]["session_home_branch"] == home_branch
    assert state["session"]["last_joined_apply_fork_commit"] is None
    assert state["session"]["session_fork_commit"]
    assert state["run"] == {
        "state": "ready",
        "kind": None,
        "branch": None,
        "fork_commit": None,
    }
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert (
        subprocess.run(
            ["git", "check-ignore", "-q", ".cmoc/gu/.__cmoc_ignore_probe__"],
            cwd=root,
        ).returncode
        == 0
    )
    assert (
        len(list((root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl"))) == 1
    )
    assert run_git(root, "status", "--short").stdout.strip() == ""
    report = terminal_primary_report(result)
    rendered_report = report.read_text(encoding="utf-8")
    assert report.parent == root / ".cmoc" / "gu" / "report" / "session" / "fork"
    assert f'session_branch: "{branch}"' in rendered_report
    assert f'home_branch: "{home_branch}"' in rendered_report
    assert 'session_state_after: "active"' in rendered_report


def test_session_fork_uses_captured_head_when_home_advances_before_branch_creation(
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """HEAD取得後にhome branchが進んでも、その時点のcommitからforkする。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    """
    root = committed_repository
    monkeypatch.chdir(root)
    seed_search_config(root)
    original_run_git = session_fork_module.run_git
    captured_head = ""
    advanced = False

    def advance_home_before_switch(
        args: list[str], work: Path, check: bool = True
    ) -> cmoc_runtime.CommandResult:
        """session branch作成直前のhome branch更新を再現する。"""
        nonlocal advanced, captured_head
        if not advanced and args[:2] == ["switch", "-c"]:
            # fork 自身の doctor 後の HEAD を観測し、準備用 doctor の再実行を省く。
            captured_head = original_run_git(["rev-parse", "HEAD"], work).stdout.strip()
            # 分岐元の識別には異なる commit だけが必要で、tree の変更は使わない。
            original_run_git(
                ["commit", "--allow-empty", "-m", "advance home branch"], work
            )
            advanced = True
        return original_run_git(args, work, check)

    monkeypatch.setattr(session_fork_module, "run_git", advance_home_before_switch)

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    assert advanced
    session_branch = current_branch(root)
    assert session_branch.startswith("cmoc/session/")
    state = json.loads(session_state_path(root, session_branch).read_text())
    assert state["session"]["session_fork_commit"] == captured_head
    assert run_git(root, "rev-parse", session_branch).stdout.strip() == captured_head


def test_session_fork_rechecks_branch_after_lifecycle_lock(
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """lock 待ち中に branch が切り替わっても state と分岐元を一致させる。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    {{work-root}}/oracle/doc/app_spec/session_state.md
    """
    root = committed_repository
    monkeypatch.chdir(root)
    _seed_session_management_files(root)
    original_home = current_branch(root)
    alternate = "alternate-home"
    run_git(root, "branch", alternate)
    run_git(root, "switch", alternate)
    run_git(root, "commit", "--allow-empty", "-m", "advance alternate home")
    alternate_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    run_git(root, "switch", original_home)

    original_lock = session_fork_module.session_fork_lock

    @contextmanager
    def switch_branch_while_locked(repository: Path) -> Iterator[None]:
        """fork が lock を取得した直後の branch 切替を再現する。"""
        with original_lock(repository):
            run_git(repository, "switch", alternate)
            yield

    monkeypatch.setattr(
        session_fork_module, "session_fork_lock", switch_branch_while_locked
    )

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    session_branch = current_branch(root)
    assert session_branch.startswith("cmoc/session/")
    state = json.loads(session_state_path(root, session_branch).read_text())
    assert state["session"]["session_home_branch"] == alternate
    assert state["session"]["session_fork_commit"] == alternate_commit
    assert run_git(root, "rev-parse", session_branch).stdout.strip() == alternate_commit


def test_session_fork_rolls_back_when_state_save_fails(
    committed_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """state 保存失敗時に branch と state を作成前へ戻す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    """

    root = committed_repository
    monkeypatch.chdir(root)
    home_branch = current_branch(root)
    session_id = "sess_000000_2026-06-27_01-02"
    session_branch = f"cmoc/session/{session_id}"
    monkeypatch.setattr(
        session_fork_module, "new_id", lambda _root, _prefix: session_id
    )

    def fail_write_state(_path: Path, _state: cmoc_runtime.SessionState) -> None:
        """state保存を失敗させ、fork rollback経路を検証する。"""
        raise OSError("state write failed")

    monkeypatch.setattr(session_fork_module, "write_state", fail_write_state)

    result = runner.invoke(app, ["session", "fork"])

    assert session_preprocess == [root]
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
    assert result.stdout == ""
    assert "session fork の作成に失敗しました。" in result.stderr
    assert "session_branch_exists: False" in result.stderr
    assert "session_state_file_exists: False" in result.stderr


def test_session_fork_rollback_does_not_guess_remote_home_branch(
    committed_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """rollback が消えた local home branch を remote から推測しない。

    根拠:
    - {{work-root}}/oracle/doc/branch_model.md
    - {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    """
    root = committed_repository
    monkeypatch.chdir(root)
    home_branch = current_branch(root)
    home_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    _seed_remote_tracking_branch(root, home_branch, home_commit)

    session_id = "sess_000000_2026-06-27_01-02"
    session_branch = f"cmoc/session/{session_id}"
    monkeypatch.setattr(
        session_fork_module, "new_id", lambda _root, _prefix: session_id
    )

    def fail_write_state(_path: Path, _state: cmoc_runtime.SessionState) -> None:
        """rollback 中の remote branch 推測を再現するため local ref を消す。"""
        run_git(root, "branch", "-D", home_branch)
        raise OSError("state write failed")

    monkeypatch.setattr(session_fork_module, "write_state", fail_write_state)

    result = runner.invoke(app, ["session", "fork"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert current_branch(root) == session_branch
    assert (
        cmoc_runtime.run_git(
            ["show-ref", "--verify", f"refs/heads/{home_branch}"],
            root,
            check=False,
        ).returncode
        != 0
    )
    assert (
        cmoc_runtime.run_git(
            ["show-ref", "--verify", f"refs/remotes/origin/{home_branch}"],
            root,
            check=False,
        ).returncode
        == 0
    )
    assert (
        cmoc_runtime.run_git(
            ["show-ref", "--verify", f"refs/heads/{session_branch}"],
            root,
            check=False,
        ).returncode
        == 0
    )
    assert not session_state_path(root, session_branch).exists()
    assert "session fork の作成に失敗しました。" in result.stderr


def test_session_fork_does_not_delete_branch_from_id_collision_race(
    committed_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """branch 作成前に同名 branch が現れても既存 branch を削除しない。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    """
    root = committed_repository
    monkeypatch.chdir(root)
    home_branch = current_branch(root)
    session_id = "sess_000000_2026-06-27_01-02"
    session_branch = f"cmoc/session/{session_id}"
    protected_commit = ""

    def reserve_colliding_id(_root: Path) -> str:
        """session-id 検査後に外部 branch が作られる競合を再現する。"""
        nonlocal protected_commit
        run_git(root, "branch", session_branch)
        protected_commit = run_git(root, "rev-parse", session_branch).stdout.strip()
        return session_id

    monkeypatch.setattr(session_fork_module, "_new_session_id", reserve_colliding_id)

    result = runner.invoke(app, ["session", "fork"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert current_branch(root) == home_branch
    assert run_git(root, "rev-parse", session_branch).stdout.strip() == protected_commit
    assert "session fork の作成に失敗しました。" in result.stderr


def test_session_fork_does_not_overwrite_state_from_id_collision_race(
    committed_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """state file が競合した場合に既存 state を保持する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    """
    root = committed_repository
    monkeypatch.chdir(root)
    session_id = "sess_000000_2026-06-27_01-02"
    session_branch = f"cmoc/session/{session_id}"
    path = write_abandoned_state(root, session_id)
    original = path.read_text()
    monkeypatch.setattr(
        session_fork_module, "_new_session_id", lambda _root: session_id
    )

    result = runner.invoke(app, ["session", "fork"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert path.read_text() == original
    report = terminal_primary_report(result)
    assert "session_state_after: null" in report.read_text(encoding="utf-8")
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch],
            cwd=root,
        ).returncode
        != 0
    )


def test_session_fork_does_not_overwrite_existing_state_on_session_id_collision(
    committed_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """session id衝突時に既存abandoned stateを上書きしないことを検証する。"""
    root = committed_repository
    monkeypatch.chdir(root)
    session_id = "sess_000000_2026-06-27_01-02"
    path = write_abandoned_state(root, session_id)
    original = path.read_text()
    home_branch = current_branch(root)
    monkeypatch.setattr(
        session_fork_module, "new_id", lambda _root, _prefix: session_id
    )

    result = runner.invoke(app, ["session", "fork"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert "発行した session ID の保存先が既に存在します。" in result.stderr
    assert path.read_text() == original
    assert current_branch(root) == home_branch
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", f"cmoc/session/{session_id}"],
            cwd=root,
        ).returncode
        != 0
    )


def test_session_fork_rejects_corrupt_state_without_active_session_message(
    committed_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """壊れたstateをactive session未存在として誤報しないことを検証する。"""
    root = committed_repository
    monkeypatch.chdir(root)
    home_branch = current_branch(root)
    path = root / ".cmoc" / "gu" / "session" / f"{SESSION_ID}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"session": {"session_home_branch": home_branch}, "run": {}}) + "\n"
    )

    result = runner.invoke(app, ["session", "fork"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert "session state file が不正です。" in result.stderr
    assert "active session が既に存在します。" not in result.stderr
    assert current_branch(root) == home_branch


def test_session_fork_uses_linked_worktree_branch_and_head(
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree上のbranchとHEADからsessionをforkすることを検証する。"""
    root = committed_repository
    monkeypatch.chdir(root)
    _seed_session_management_files(root)
    root_branch = current_branch(root)
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    run_git(linked, "commit", "--allow-empty", "-m", "linked change")
    linked_commit = run_git(linked, "rev-parse", "HEAD").stdout.strip()
    monkeypatch.chdir(linked)

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    session_branch = current_branch(linked)
    assert session_branch.startswith("cmoc/session/")
    assert current_branch(root) == root_branch
    state = json.loads(session_state_path(root, session_branch).read_text())
    assert state["session"]["session_home_branch"] == "linked-home"
    assert state["session"]["session_fork_commit"] == linked_commit
    assert run_git(linked, "rev-parse", session_branch).stdout.strip() == linked_commit


def test_session_abandon_switches_home_and_marks_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session abandonがhome branchへ戻りstateをabandonedにすることを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    seed_search_config(root)
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
    assert f"- abandoned_branch: `{session_branch}`" in result.output
    assert "- session_state: `abandoned`" in result.output
    report = terminal_primary_report(result)
    rendered_report = report.read_text(encoding="utf-8")
    assert f'session_branch: "{session_branch}"' in rendered_report
    assert f'home_branch: "{home_branch}"' in rendered_report
    assert 'session_state_after: "abandoned"' in rendered_report


def test_session_abandon_uses_linked_worktree_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree上のsession abandonが対応home branchを使うことを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    _seed_session_management_files(root)
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
    _seed_session_management_files(root)
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    session_branch, home_branch = _seed_session_in_worktree(root, linked)
    gitignore = break_preprocess_invariants(linked)
    run_git(root, "branch", "-D", home_branch)

    result = runner.invoke(app, ["session", "abandon"])

    assert result.exit_code != 0
    assert current_branch(linked) == session_branch
    assert "session home branch が存在しません。" in result.stderr
    assert "/.cmoc/gu/" in gitignore.read_text().splitlines()
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text().splitlines()
    assert run_git(linked, "ls-files", "--", ".cmoc/gu").stdout.splitlines() == []
    assert run_git(linked, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
    assert run_git(linked, "status", "--short").stdout.strip() == ""


def test_session_abandon_requires_existing_home_branch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """home branchが存在しないsession abandonを拒否することを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    session_branch, home_branch = _seed_active_session(root)
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()
    # 前処理の修復と事前条件の順序は linked worktree の専用ケースで検証する。
    # このケースでは local branch と同名 tag を区別する境界を保つ。
    run_git(root, "branch", "-D", home_branch)
    run_git(root, "tag", home_branch, home_commit)

    result = runner.invoke(app, ["session", "abandon"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert result.stdout == ""
    assert "# 失敗: cmoc session abandon" in result.stderr
    assert "- 診断用サブコマンドログ: `" in result.stderr
    assert "ステップ経過時間" not in result.output
    assert "- 経過時間: `" in result.output
    assert "quota 待機時間" not in result.output
    assert "- 終了コード: `1`" in result.output
    assert current_branch(root) == session_branch
    assert "session home branch が存在しません。" in result.stderr
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )


def test_session_abandon_reports_run_cleanup_action_when_run_is_present(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """未joinのrunがある場合に先行するcleanup操作を案内する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    session_branch, _ = _seed_active_session(root)
    path = session_state_path(root, session_branch)
    state = json.loads(path.read_text())
    session_id = session_branch.removeprefix("cmoc/session/")
    state["run"] = {
        "state": "joinable",
        "kind": "realization_refactor",
        "branch": f"cmoc/run/{session_id}/{RUN_ID}",
        "fork_commit": state["session"]["session_fork_commit"],
    }
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    result = runner.invoke(app, ["session", "abandon"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert "先に `cmoc run abandon`" in result.stderr
    assert current_branch(root) == session_branch


def test_session_abandon_report_keeps_known_state_on_dirty_precondition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """dirty worktree拒否でも既知のsession report fieldを保持する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    _, home_branch = _seed_active_session(root)
    session_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (root / "README.md").write_text("dirty\n")

    result = runner.invoke(app, ["session", "abandon"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    rendered_report = terminal_primary_report(result).read_text(encoding="utf-8")
    assert f'home_branch: "{home_branch}"' in rendered_report
    assert f'abandoned_branch_start_commit: "{session_commit}"' in rendered_report
    assert 'session_state_before: "active"' in rendered_report
    assert "session_state_after: null" in rendered_report


def test_session_abandon_does_not_guess_remote_home_branch_after_validation_race(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """home branch の検証後に local ref が消えても remote branch へ切り替えない。

    根拠:
    - {{work-root}}/oracle/doc/branch_model.md
    - {{work-root}}/oracle/doc/app_spec/sub_command/session_abandon.md
    """
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    session_branch, home_branch = _seed_active_session(root)
    state_path = session_state_path(root, session_branch)
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()

    _seed_remote_tracking_branch(root, home_branch, home_commit)

    original_branch_exists = session_module.branch_exists
    home_deleted = False

    def delete_home_after_validation(repository: Path, branch: str) -> bool:
        """home branch の存在確認直後に local ref が消える競合を再現する。"""
        nonlocal home_deleted
        exists = original_branch_exists(repository, branch)
        if branch == home_branch and not home_deleted:
            assert exists
            run_git(repository, "branch", "-D", home_branch)
            home_deleted = True
        return exists

    monkeypatch.setattr(session_module, "branch_exists", delete_home_after_validation)

    result = runner.invoke(app, ["session", "abandon"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert current_branch(root) == session_branch
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == home_commit
    assert (
        cmoc_runtime.run_git(
            ["show-ref", "--verify", f"refs/heads/{home_branch}"],
            root,
            check=False,
        ).returncode
        != 0
    )
    assert (
        cmoc_runtime.run_git(
            ["show-ref", "--verify", f"refs/remotes/origin/{home_branch}"],
            root,
            check=False,
        ).returncode
        == 0
    )
    assert (
        cmoc_runtime.run_git(
            ["show-ref", "--verify", f"refs/heads/{session_branch}"],
            root,
            check=False,
        ).returncode
        == 0
    )
    assert json.loads(state_path.read_text())["session"]["state"] == "active"
    assert "git switch --no-guess" in result.stderr


@pytest.mark.parametrize(
    "cleanup_error",
    [
        CmocError("delete failed", ["next"], "branch delete failed"),
        KeyboardInterrupt(),
    ],
)
def test_session_abandon_rolls_back_state_and_branch_on_cleanup_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    cleanup_error: BaseException,
    session_preprocess: list[Path],
) -> None:
    """cleanup失敗時にsession branchとactive stateを復元することを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    # ignore/tracking の修復は home branch 不在・linked worktree のケースで検証する。
    session_branch, _ = _seed_active_session(root)
    state_path = session_state_path(root, session_branch)
    gitignore = root / ".gitignore"
    original_delete_branch = session_module.delete_branch

    def fake_delete_branch(root: Path, branch: str, force: bool = False) -> None:
        """対象session branchの削除だけを指定exceptionで失敗させる。"""
        if branch == session_branch:
            raise cleanup_error
        return original_delete_branch(root, branch, force)

    monkeypatch.setattr(session_module, "delete_branch", fake_delete_branch)

    result = runner.invoke(app, ["session", "abandon"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert result.stdout == ""
    assert "session abandon の cleanup に失敗しました。" in result.stderr
    assert "`cmoc session abandon` を再実行してください。" in result.stderr
    assert current_branch(root) == session_branch
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )
    state = json.loads(state_path.read_text())
    assert state["session"]["state"] == "active"
    assert "/.cmoc/gu/" in gitignore.read_text().splitlines()
    assert run_git(root, "ls-files", "--", ".cmoc/gu").stdout == ""
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_session_abandon_restores_branch_if_delete_is_interrupted_after_side_effect(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """branch削除後の中断でも元のsession branchとstateを復元する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    session_branch, _ = _seed_active_session(root)
    session_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    state_path = session_state_path(root, session_branch)
    original_delete_branch = session_module.delete_branch

    def delete_then_interrupt(
        repository: Path, branch: str, force: bool = False
    ) -> None:
        """branchを削除した直後にcleanup中断を再現する。"""
        result = original_delete_branch(repository, branch, force)
        assert result.returncode == 0
        raise KeyboardInterrupt()

    monkeypatch.setattr(session_module, "delete_branch", delete_then_interrupt)

    result = runner.invoke(app, ["session", "abandon"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert current_branch(root) == session_branch
    assert run_git(root, "rev-parse", session_branch).stdout.strip() == session_commit
    state = json.loads(state_path.read_text())
    assert state["session"]["state"] == "active"


def test_session_abandon_rollback_does_not_guess_remote_session_branch_after_race(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """rollback中に消えたlocal session branchをremoteから推測しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    session_branch, home_branch = _seed_active_session(root)
    state_path = session_state_path(root, session_branch)
    session_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()

    run_git(root, "switch", home_branch)
    (root / "README.md").write_text("remote target\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "advance remote branch target")
    remote_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    _seed_remote_tracking_branch(root, session_branch, remote_commit)
    run_git(root, "switch", session_branch)

    original_run_git = session_module.run_git
    original_branch_exists = session_module.branch_exists
    original_delete_branch = session_module.delete_branch
    recreated = False
    raced = False

    def record_recreated_branch(
        args: list[str], git_cwd: Path, check: bool = True
    ) -> cmoc_runtime.CommandResult:
        """rollbackのbranch復元を検出する。"""
        nonlocal recreated
        result = original_run_git(args, git_cwd, check)
        if args == ["branch", session_branch, session_commit]:
            recreated = True
        return result

    def remove_recreated_branch(repository: Path, branch: str) -> bool:
        """branch存在確認とcheckoutの間にlocal refが消える競合を再現する。"""
        nonlocal raced
        exists = original_branch_exists(repository, branch)
        if branch == session_branch and recreated and exists and not raced:
            original_run_git(["branch", "-D", branch], repository)
            raced = True
        return exists

    def delete_then_interrupt(
        repository: Path, branch: str, force: bool = False
    ) -> None:
        """session branch削除後の中断を再現する。"""
        result = original_delete_branch(repository, branch, force)
        assert result.returncode == 0
        raise KeyboardInterrupt()

    monkeypatch.setattr(session_module, "run_git", record_recreated_branch)
    monkeypatch.setattr(session_module, "branch_exists", remove_recreated_branch)
    monkeypatch.setattr(session_module, "delete_branch", delete_then_interrupt)

    result = runner.invoke(app, ["session", "abandon"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert raced
    assert current_branch(root) == home_branch
    assert json.loads(state_path.read_text())["session"]["state"] == "active"
    assert (
        cmoc_runtime.run_git(
            ["show-ref", "--verify", f"refs/heads/{session_branch}"],
            root,
            check=False,
        ).returncode
        != 0
    )
    assert (
        cmoc_runtime.run_git(
            ["show-ref", "--verify", f"refs/remotes/origin/{session_branch}"],
            root,
            check=False,
        ).returncode
        == 0
    )


@pytest.mark.parametrize("command", ["abandon", "join"])
def test_session_completion_rejects_missing_state_fields(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    command: str,
    session_preprocess: list[Path],
) -> None:
    """session completionが必須state field欠落を拒否することを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    session_branch, home_branch = _seed_active_session(root)
    path = session_state_path(root, session_branch)
    broken_state = {"session": {"session_home_branch": home_branch}}
    path.write_text(json.dumps(broken_state) + "\n")

    result = runner.invoke(app, ["session", command])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert "session state file が不正です。" in result.stderr
    assert "必須 field" in result.stderr
    assert current_branch(root) == session_branch


@pytest.fixture
def session_preprocess(monkeypatch: pytest.MonkeyPatch) -> list[Path]:
    """session 固有の検査では共通サービスを省き、doctor 呼び出しを記録する。"""
    # fork の失敗検査は HEAD と pre-log の実 exclude 修復だけを使い、設定を準備しない。
    # fork→abandon/join の結合と doctor の修復・順序は正常系・linked worktree と
    # test_doctor_cli.py、collector の受付・保存・drain は test_feedback.py に残す。
    roots: list[Path] = []
    monkeypatch.setattr(runtime_cli, "run_doctor_preprocess", roots.append)
    monkeypatch.setattr(
        runtime_cli, "start_feedback_invocation", lambda *_args: (None, None)
    )
    return roots


@pytest.fixture
def join_repository(cli_repository: Path, session_preprocess: list[Path]) -> Path:
    """前処理を置換した join 固有の検査に、実 Git と追跡済みの基準 file を用意する。"""
    # config・.agents・refactor state と全 file の列挙は前処理の結合検査に残す。
    # .cmoc/gu の ignore は、実 join の clean 検査とログ・state 保存に必要。
    root = cli_repository
    (root / ".gitignore").write_text("/.cmoc/gu/\n")
    (root / "README.md").write_text("# repo\n")
    (root / "oracle").mkdir()
    (root / "oracle" / "spec.md").write_text("# spec\n")
    run_git(root, "add", ".gitignore", "README.md", "oracle/spec.md")
    run_git(root, "commit", "-m", "initial")
    return root


def test_session_join_preserves_repository_local_feedback_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """session join が repository-local feedback state を merge や rollback しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    _seed_active_session(root)
    relative = ".cmoc/gu/feedback/normalization_checkpoint/sentinel.json"
    path = root / relative
    path.parent.mkdir(parents=True)
    content = '{"repository_local":true}\n'
    path.write_text(content)

    joined = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert joined.exit_code == 0, joined.output
    assert path.read_text() == content
    assert run_git(root, "ls-files", "--", relative).stdout == ""


def test_session_join_preserves_work_on_incidental_conflict_marker(
    join_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """付随編集先の未解消 marker で停止し、stderr と保持した作業状態を検査する。"""
    root = join_repository
    target = root / "oracle" / "spec.md"
    related = root / "src"
    related.mkdir()
    added = related / "added.py"
    modified = related / "modified.py"
    deleted = related / "deleted.py"
    renamed = related / "renamed.py"
    moved = related / "moved.py"
    for path in (modified, deleted, renamed):
        path.write_text("previous implementation\n")
    run_git(root, "add", "src")
    run_git(root, "commit", "-m", "add related implementations")
    monkeypatch.chdir(root)
    session_branch, home_branch = _seed_session_in_worktree(root, root)
    target.write_text("session change\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "session change")
    run_git(root, "switch", home_branch)
    target.write_text("home change\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "home change")
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()
    run_git(root, "switch", session_branch)

    class FakeCodexResult:
        """conflict resolution の成功を表す最小 fake result。"""

        output_text = "merge_resolution: resolved\n"
        output_json = None

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        """両側の仕様を保持し、関連実装を整理する agent の結果を再現する。"""
        target.write_text("home change\nsession change\n")
        modified.write_text("related implementation\n")
        deleted.unlink()
        renamed.rename(moved)
        added.write_text("<<<<<<< HEAD\nhome\n=======\nsession\n>>>>>>> branch\n")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"])

    assert session_preprocess == [root]
    assert current_branch(root) == home_branch
    assert result.exit_code != 0
    assert result.stdout == ""
    assert "# 失敗: cmoc session join" in result.stderr
    assert "conflict marker が残っています。" in result.stderr
    assert "src/added.py" in result.stderr
    assert run_git(root, "rev-parse", home_branch).stdout.strip() == home_commit
    assert run_git(root, "branch", "--list", session_branch).stdout.strip()
    state = json.loads(session_state_path(root, session_branch).read_text())
    assert state["session"]["state"] == "active"
    assert target.read_text() == "home change\nsession change\n"
    assert modified.read_text() == "related implementation\n"
    assert not deleted.exists()
    assert not renamed.exists()
    assert moved.read_text() == "previous implementation\n"
    assert added.read_text().startswith("<<<<<<< HEAD\n")


def test_session_join_merges_conflict_and_incidental_changes(
    join_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """競合の内容・mode・削除・改行 path と、一覧外の追加・変更・rename・削除を取り込む。"""
    # 一つの成功経路を共有し、各編集と NUL framing を独立したファイルで検証する。
    # marker が残る失敗時の作業保持は専用ケースで検査する。
    # {{work-root}}/oracle/doc/app_spec/merge_conflict_resolution.md
    root = join_repository
    context_target = root / "oracle" / "spec.md"
    mode_target = root / "oracle" / "mode.md"
    deleted_target = root / "oracle" / "deleted.md"
    delete_modify_target = root / "README.md"
    newline_target = root / "src" / "line\nbreak.txt"
    newline_target.parent.mkdir()
    newline_target.write_text("base\n")
    added = root / "src" / "added.py"
    modified = root / "src" / "modified.py"
    deleted = root / "src" / "deleted.py"
    renamed = root / "src" / "renamed.py"
    moved = root / "src" / "moved.py"
    for target in (modified, deleted, renamed):
        target.write_text("previous implementation\n")
    for target in (mode_target, deleted_target):
        target.write_text("# spec\n")
    run_git(root, "add", "oracle", "src")
    run_git(root, "commit", "-m", "add conflict targets")
    monkeypatch.chdir(root)
    session_branch, home_branch = _seed_session_in_worktree(root, root)
    for target in (context_target, mode_target):
        target.write_text("prefix\nsession change\nsuffix\n")
    deleted_target.write_text("session change\n")
    delete_modify_target.unlink()
    newline_target.write_text("session change\n")
    run_git(root, "add", "oracle", "src", "README.md")
    run_git(root, "commit", "-m", "session change")
    run_git(root, "switch", home_branch)
    for target in (context_target, mode_target):
        target.write_text("prefix\nhome change\nsuffix\n")
    deleted_target.write_text("home change\n")
    delete_modify_target.write_text("home change\n")
    newline_target.write_text("home change\n")
    run_git(root, "add", "oracle", "src", "README.md")
    run_git(root, "commit", "-m", "home change")
    run_git(root, "switch", session_branch)

    class FakeCodexResult:
        """conflict resolution の成功を表す最小 fake result。"""

        output_text = "merge_resolution: resolved\n"
        output_json = None

    def fake_run_codex_exec(parameter: AgentCallParameter, **kwargs: object) -> object:
        """各競合に独立した編集を行い、解消済み結果を返す。"""
        assert set(kwargs) == {"root", "purpose"}
        assert parameter.agent_call_cwd == root
        assert "統合対象" in parameter.prompt
        assert str(newline_target) not in parameter.prompt
        assert set(merge_conflict_module.unmerged_paths(root)) == {
            "README.md",
            "oracle/spec.md",
            "oracle/mode.md",
            "oracle/deleted.md",
            "src/line\nbreak.txt",
        }
        context_target.write_text(
            "prefix\nhome change\nsession change\nchanged suffix\n"
        )
        mode_target.write_text("prefix\nresolved change\nsuffix\n")
        mode_target.chmod(mode_target.stat().st_mode | stat.S_IXUSR)
        deleted_target.unlink()
        delete_modify_target.unlink()
        newline_target.write_text("resolved change\n")
        added.write_text("related implementation\n")
        modified.write_text("related implementation\n")
        deleted.unlink()
        renamed.rename(moved)
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"])

    assert session_preprocess == [root]
    assert result.exit_code == 0, result.output
    assert current_branch(root) == home_branch
    assert run_git(root, "status", "--porcelain").stdout == ""
    assert run_git(root, "ls-files", "--stage", "oracle/mode.md").stdout.startswith(
        "100755 "
    )
    assert (
        run_git(
            root,
            "ls-files",
            "--",
            "oracle/deleted.md",
            "README.md",
            "src/deleted.py",
            "src/renamed.py",
        ).stdout
        == ""
    )
    assert not deleted_target.exists()
    assert not delete_modify_target.exists()
    assert newline_target.read_text() == "resolved change\n"
    expected_contents = {
        "oracle/spec.md": "prefix\nhome change\nsession change\nchanged suffix\n",
        "oracle/mode.md": "prefix\nresolved change\nsuffix\n",
        "src/line\nbreak.txt": "resolved change\n",
        "src/moved.py": "previous implementation\n",
        "src/added.py": "related implementation\n",
        "src/modified.py": "related implementation\n",
    }
    # HEAD の内容を一括取得し、改行 path は NUL、各本文は byte 長で区切る。
    objects = subprocess.run(
        ["git", "cat-file", "--batch", "-z"],
        cwd=root,
        input=b"".join(
            f"HEAD:{relative}\0".encode("utf-8") for relative in expected_contents
        ),
        capture_output=True,
        check=True,
    )
    with BytesIO(objects.stdout) as contents:
        for relative, expected in expected_contents.items():
            header = contents.readline().split()
            assert header[1:2] == [b"blob"], relative
            assert contents.read(int(header[2])) == expected.encode("utf-8"), relative
            assert contents.read(1) == b"\n"
        assert contents.read() == b""


def test_session_join_reads_unmerged_paths_with_newlines(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Git index の path は NUL 区切りで読み、改行を保持する。"""
    root = tmp_path

    def fake_git(args: list[str], _root: Path) -> cmoc_runtime.CommandResult:
        assert args == ["diff", "--name-only", "-z", "--diff-filter=U"]
        return cmoc_runtime.CommandResult(0, "src/line\nbreak.txt\0", "")

    monkeypatch.setattr(merge_conflict_module, "run_git", fake_git)
    assert merge_conflict_module.unmerged_paths(root) == ["src/line\nbreak.txt"]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", False),
        ("Title\n=======\n", False),
        ("inline <<<<<<< HEAD\ninline ||||||| base\ninline >>>>>>> branch\n", False),
        ("<<<<<<< HEAD\nhome\n=======\nsession\n>>>>>>> branch\n", True),
        ("<<<<<<< HEAD\nhome\n========\nsession\n>>>>>>> branch\n", True),
        ("<<<<<<< HEAD\nhome\n", True),
        ("||||||| base\n", True),
        (">>>>>>> branch\n", True),
        ("prefix\r<<<<<<< HEAD\rhome\r", True),
        ("prefix\u2028>>>>>>> branch\u2028", True),
    ],
)
def test_session_join_conflict_marker_detection(text: str, expected: bool) -> None:
    """未解決 marker block の検出は bare Markdown separator を許す。"""
    assert merge_conflict_module._has_conflict_marker_block(text) is expected


def test_session_join_checks_staged_text_conflict_markers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """通常 text だけを検査し、改行を含む付随 path の残存 marker を報告する。"""
    (tmp_path / "directory.md").mkdir()
    (tmp_path / "binary.dat").write_bytes(b"<<<<<<< HEAD\n\xff")
    target = tmp_path / "target.md"
    target.write_text("<<<<<<< HEAD\n")
    (tmp_path / "link.md").symlink_to(target)
    (tmp_path / "plain.md").write_text("Title\n=======\ninline <<<<<<< HEAD\n")
    staged = ["deleted.md", "directory.md", "binary.dat", "link.md", "plain.md"]

    def fake_git(_args: list[str], _root: Path) -> cmoc_runtime.CommandResult:
        return cmoc_runtime.CommandResult(0, "\0".join(staged) + "\0", "")

    monkeypatch.setattr(merge_conflict_module, "run_git", fake_git)
    merge_conflict_module._check_conflict_markers(tmp_path)

    relative = "src/line\nbreak.txt"
    marker = tmp_path / relative
    marker.parent.mkdir()
    marker.write_text("prefix\u2028<<<<<<< HEAD\nhome\n")
    staged.append(relative)

    with pytest.raises(CmocError, match="conflict marker が残っています。") as error:
        merge_conflict_module._check_conflict_markers(tmp_path)
    assert error.value.detail == relative


def test_session_join_uses_linked_worktree_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree上のsession joinが対応home branchを使うことを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    _seed_session_management_files(root)
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
    report = terminal_primary_report(result)
    rendered_report = report.read_text(encoding="utf-8")
    assert f'session_branch: "{session_branch}"' in rendered_report
    assert f'home_branch: "{home_branch}"' in rendered_report
    assert 'session_state_after: "joined"' in rendered_report
    assert "merge_commit:" in rendered_report
    assert "## 事前検証" in rendered_report
    assert "## branch 切替と merge" in rendered_report
    assert "- merge 結果: `completed`" in rendered_report
    assert "- conflict 解消用 agent call: `未実行（conflict なし）`" in rendered_report
    assert "- session state: `active` -> `joined`" in rendered_report
    assert "- cleanup: `completed`" in rendered_report


def test_session_join_preprocesses_linked_worktree_before_preconditions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree の join が固有の事前条件より先に preprocess することを検証する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
    {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    _seed_session_management_files(root)
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
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text().splitlines()
    assert run_git(linked, "ls-files", "--", ".cmoc/gu").stdout.splitlines() == []
    assert run_git(linked, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
    assert run_git(linked, "status", "--short").stdout.strip() == ""


def test_session_join_warns_when_session_branch_cannot_be_deleted(
    join_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """session branch削除失敗をwarningとしてjoin成功に含めることを検証する。"""
    root = join_repository
    monkeypatch.chdir(root)
    session_branch, home_branch = _seed_session_in_worktree(root, root)
    original_run_git = session_join_module.run_git

    # {{work-root}}/oracle/doc/dev_rule/coding_rule.md
    def fake_run_git(args: list[str], git_cwd: Path, check: bool = True) -> object:
        """session branch削除だけを失敗させ、他のGit操作は委譲する。"""
        if args == ["branch", "-d", session_branch]:
            return cmoc_runtime.CommandResult(1, "", "branch is checked out elsewhere")
        return original_run_git(args, git_cwd, check=check)

    monkeypatch.setattr(session_join_module, "run_git", fake_run_git)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert session_preprocess == [root]
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
    join_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """local session branchのreachability確認失敗時に削除しないことを検証する。"""
    root = join_repository
    monkeypatch.chdir(root)
    session_branch, home_branch = _seed_session_in_worktree(root, root)
    original_run_git = session_join_module.run_git
    delete_calls = 0

    # {{work-root}}/oracle/doc/dev_rule/coding_rule.md
    def fake_run_git(args: list[str], git_cwd: Path, check: bool = True) -> object:
        """reachability確認を失敗させ、他のGit操作は委譲する。"""
        nonlocal delete_calls
        if args == ["merge-base", "--is-ancestor", session_branch, "HEAD"]:
            return cmoc_runtime.CommandResult(1, "", "")
        if args == ["branch", "-d", session_branch]:
            delete_calls += 1
        return original_run_git(args, git_cwd, check=check)

    monkeypatch.setattr(session_join_module, "run_git", fake_run_git)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert session_preprocess == [root]
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


def test_session_join_rejects_missing_home_branch_before_remote_guess(
    join_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """local home branch がない場合に同名 remote branch へ join しない。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
    {{work-root}}/oracle/doc/app_spec/session_state.md
    """
    root = join_repository
    monkeypatch.chdir(root)
    session_branch, home_branch = _seed_session_in_worktree(root, root)
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()
    run_git(root, "branch", "-D", home_branch)

    _seed_remote_tracking_branch(root, home_branch, home_commit)

    result = runner.invoke(app, ["session", "join"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert current_branch(root) == session_branch
    assert "git コマンドが失敗しました。" in result.stderr
    assert "git switch --no-guess" in result.stderr
    assert "git コマンドが失敗しました。" not in result.stdout
    assert run_git(root, "branch", "--show-current").stdout.strip() == session_branch
    assert (
        run_git(
            root,
            "show-ref",
            "--verify",
            f"refs/remotes/origin/{home_branch}",
        ).returncode
        == 0
    )
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == home_commit


def test_session_join_handled_failure_is_written_to_stderr(
    join_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """事前条件 error terminal result を stderr へ出力する。"""
    root = join_repository
    monkeypatch.chdir(root)
    _, home_branch = _seed_session_in_worktree(root, root)
    (root / "README.md").write_text("dirty\n")

    result = runner.invoke(app, ["session", "join"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert result.stdout == ""
    assert "# 失敗: cmoc session join" in result.stderr
    assert "git 未コミット差分が存在します。" in result.stderr
    assert "Traceback" not in result.stderr
    rendered_report = terminal_primary_report(result).read_text(encoding="utf-8")
    assert f'home_branch: "{home_branch}"' in rendered_report
    assert 'session_state_before: "active"' in rendered_report


def test_session_join_codex_failure_reports_unresolved_merge(
    join_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """Codex失敗時に残ったmerge conflictの手動完了手順をstderrへ示す。"""
    root = join_repository
    target = root / "README.md"
    monkeypatch.chdir(root)
    session_branch, home_branch = _seed_session_in_worktree(root, root)
    target.write_text("session change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session change")
    run_git(root, "switch", home_branch)
    target.write_text("home change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "home change")
    run_git(root, "switch", session_branch)

    def failing_codex_exec(parameter: object, **kwargs: object) -> object:
        """Codex CLIの既知の失敗を再現する。"""
        raise CmocError(
            "Codex CLI 呼び出しが失敗しました。",
            ["stderr/stdout log を確認して原因を解消してください。"],
            "call log",
        )

    monkeypatch.setattr(session_join_module, "run_codex_exec", failing_codex_exec)

    result = runner.invoke(app, ["session", "join"])

    assert session_preprocess == [root]
    assert result.exit_code != 0
    assert current_branch(root) == home_branch
    assert "Codex CLI 呼び出しが失敗しました。" in result.stderr
    assert "stderr/stdout log を確認して原因を解消してください。" in result.stderr
    rendered_report = terminal_primary_report(result).read_text(encoding="utf-8")
    assert f"- `{target}`" in rendered_report
    assert "- 確定した解消結果: `未確認`" in rendered_report


def test_session_join_conflict_uses_merge_target_worktree_context(
    join_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    session_preprocess: list[Path],
) -> None:
    """linked worktree の oracle 競合で cwd・sandbox・prompt・report を検証する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
    {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    {{work-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py
    {{work-root}}/oracle/src/oracle/other/path_model.py
    """

    # oracle 競合の成功経路を共有し、sandbox・report 専用の Git 準備を繰り返さない。
    # 通常 worktree の内容解消は付随編集と改行 path のケースにも残す。
    # Git の linked metadata と競合解消は実経路を通し、共通サービスを省く。
    # doctor の修復・順序と fork→join の結合は専用の linked worktree test に残す。
    root = join_repository
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    session_branch, home_branch = _seed_session_in_worktree(root, linked)
    target = linked / "oracle" / "spec.md"
    target.write_text("linked session change\n")
    run_git(linked, "add", "oracle/spec.md")
    run_git(linked, "commit", "-m", "linked session change")
    run_git(linked, "switch", home_branch)
    target.write_text("linked home change\n")
    run_git(linked, "add", "oracle/spec.md")
    run_git(linked, "commit", "-m", "linked home change")
    run_git(linked, "switch", session_branch)
    calls: list[str] = []

    class FakeCodexResult:
        """conflict resolution の成功を表す最小 fake result。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
        """

        output_text = "merge_resolution: resolved\n"
        output_json = None

    def fake_run_codex_exec(parameter: AgentCallParameter, **kwargs: object) -> object:
        """Codex wrapper に渡す root・cwd と、path に依存しない sandbox を確認する。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
        {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        """

        calls.append(kwargs["purpose"])
        assert set(kwargs) == {"root", "purpose"}
        assert kwargs["root"] == root
        assert parameter.agent_call_cwd == linked
        assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
        assert f"- {{{{repo-root}}}} = {root}" in parameter.prompt
        assert f"- {{{{work-root}}}} = {linked}" in parameter.prompt
        assert "統合対象" in parameter.prompt
        assert str(target) not in parameter.prompt
        override_args = build_codex_override_args(parameter, CmocConfig())
        assert override_args[override_args.index("--sandbox") + 1] == (
            "workspace-write"
        )
        assert all("permissions" not in arg for arg in override_args)
        assert all(str(target) not in arg for arg in override_args)
        target.write_text("resolved change\nTitle\n=======\n")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert session_preprocess == [linked]
    assert result.exit_code == 0, result.output
    assert calls == ["session join conflict resolution"]
    assert current_branch(linked) == home_branch
    assert target.read_text() == "resolved change\nTitle\n=======\n"
    rendered_report = terminal_primary_report(result).read_text(encoding="utf-8")
    assert f"- `{target}`" in rendered_report
    assert "- conflict 解消用 agent call: `resolved`" in rendered_report
    assert "- 確定した解消結果: `confirmed`" in rendered_report
