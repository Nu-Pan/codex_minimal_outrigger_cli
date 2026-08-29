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
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner, terminal_primary_report
from _git_support import current_branch, make_repo, run_git

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
    assert state["session"]["last_joined_apply_fork_commit"] is None
    assert state["session"]["session_fork_commit"]
    assert state["run"] == {
        "state": "ready",
        "kind": None,
        "branch": None,
        "fork_commit": None,
    }
    report = terminal_primary_report(result)
    rendered_report = report.read_text(encoding="utf-8")
    assert report.parent == root / ".cmoc" / "gu" / "ar" / "report" / "session" / "fork"
    assert f'session_branch: "{branch}"' in rendered_report
    assert f'home_branch: "{home_branch}"' in rendered_report
    assert 'session_state_after: "active"' in rendered_report


def test_session_fork_uses_captured_head_when_home_advances_before_branch_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """HEAD取得後にhome branchが進んでも、その時点のcommitからforkする。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    """
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    original_run_git = session_fork_module.run_git
    captured_head = original_run_git(["rev-parse", "HEAD"], root).stdout.strip()
    advanced = False

    def advance_home_before_switch(
        args: list[str], work: Path, check: bool = True
    ) -> cmoc_runtime.CommandResult:
        """session branch作成直前のhome branch更新を再現する。"""
        nonlocal advanced
        if not advanced and args[:2] == ["switch", "-c"]:
            (work / "README.md").write_text("advanced home\n")
            original_run_git(["add", "README.md"], work)
            original_run_git(["commit", "-m", "advance home branch"], work)
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
    assert result.stdout == ""
    assert "session fork の作成に失敗しました。" in result.stderr
    assert "session_branch_exists: False" in result.stderr
    assert "session_state_file_exists: False" in result.stderr


def test_session_fork_does_not_delete_branch_from_id_collision_race(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """branch 作成前に同名 branch が現れても既存 branch を削除しない。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    """
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    home_branch = current_branch(root)
    session_id = "2026-06-27_01-02_03-000000000"
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

    assert result.exit_code != 0
    assert current_branch(root) == home_branch
    assert run_git(root, "rev-parse", session_branch).stdout.strip() == protected_commit
    assert "session fork の作成に失敗しました。" in result.stderr


def test_session_fork_does_not_overwrite_state_from_id_collision_race(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """state file が競合した場合に既存 state を保持する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    """
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    session_id = "2026-06-27_01-02_03-000000000"
    session_branch = f"cmoc/session/{session_id}"
    path = write_abandoned_state(root, session_id)
    original = path.read_text()
    monkeypatch.setattr(
        session_fork_module, "_new_session_id", lambda _root: session_id
    )

    result = runner.invoke(app, ["session", "fork"])

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
    assert "一意な session-id を生成できませんでした。" in result.stderr
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
        json.dumps({"session": {"session_home_branch": home_branch}, "run": {}}) + "\n"
    )

    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code != 0
    assert "session state file が不正です。" in result.stderr
    assert "active session が既に存在します。" not in result.stderr
    assert current_branch(root) == home_branch


def test_session_fork_initializes_cmoc_ignore_and_writes_log(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session forkがcmoc ignoreを初期化し、サブコマンドlogを保存する。"""
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
    assert state["session"]["session_fork_commit"] == linked_commit
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
    assert "session home branch が存在しません。" in result.stderr
    assert "/.cmoc/gu/" not in gitignore.read_text().splitlines()
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text().splitlines()
    assert run_git(linked, "ls-files", "--", ".cmoc/gu").stdout.splitlines() == [
        ".cmoc/gu/tracked-probe"
    ]
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
    assert "/.cmoc/gu/" in gitignore.read_text().splitlines()
    assert run_git(root, "ls-files", "--", ".cmoc/gu").stdout == ""


def test_session_abandon_report_keeps_known_state_on_dirty_precondition(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """dirty worktree拒否でも既知のsession report fieldを保持する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    session_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (root / "README.md").write_text("dirty\n")

    result = runner.invoke(app, ["session", "abandon"])

    assert result.exit_code != 0
    rendered_report = terminal_primary_report(result).read_text(encoding="utf-8")
    assert f'home_branch: "{home_branch}"' in rendered_report
    assert f'abandoned_branch_start_commit: "{session_commit}"' in rendered_report
    assert 'session_state_before: "active"' in rendered_report
    assert "session_state_after: null" in rendered_report


def test_session_abandon_does_not_guess_remote_home_branch_after_validation_race(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """home branch の検証後に local ref が消えても remote branch へ切り替えない。

    根拠:
    - {{work-root}}/oracle/doc/branch_model.md
    - {{work-root}}/oracle/doc/app_spec/sub_command/session_abandon.md
    """
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

    remote = tmp_path / "remote.git"
    subprocess.run(
        ["git", "init", "--bare", str(remote)],
        text=True,
        capture_output=True,
        check=True,
    )
    run_git(root, "remote", "add", "origin", str(remote))
    run_git(root, "push", "origin", f"{home_commit}:refs/heads/{home_branch}")
    run_git(root, "config", "checkout.defaultRemote", "origin")

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
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """branch削除後の中断でも元のsession branchとstateを復元する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
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

    assert result.exit_code != 0
    assert current_branch(root) == session_branch
    assert run_git(root, "rev-parse", session_branch).stdout.strip() == session_commit
    state = json.loads(state_path.read_text())
    assert state["session"]["state"] == "active"


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
    assert "session state file が不正です。" in result.stderr
    assert "必須 field" in result.stderr
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
        assert set(kwargs) == {"root", "purpose"}
        assert parameter.agent_call_cwd == root
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


def test_session_join_preserves_repository_local_feedback_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """session join が repository-local feedback state を merge や rollback しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    fork = runner.invoke(app, ["session", "fork"], catch_exceptions=False)
    assert fork.exit_code == 0, fork.output
    relative = ".cmoc/gu/ar/feedback/normalization_checkpoint/sentinel.json"
    path = root / relative
    path.parent.mkdir(parents=True)
    content = '{"repository_local":true}\n'
    path.write_text(content)

    joined = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert joined.exit_code == 0, joined.output
    assert path.read_text() == content
    assert run_git(root, "ls-files", "--", relative).stdout == ""


def test_session_join_rejects_non_conflict_changes_from_conflict_agent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """conflict agent が対象外 file を変更した merge を拒否する。"""
    root = make_repo(tmp_path)
    target = root / "oracle" / "spec.md"
    extra = root / "src" / "extra.py"
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
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()
    run_git(root, "switch", session_branch)

    class FakeCodexResult:
        """conflict resolution の成功を表す最小 fake result。"""

        output_json = None

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        """対象外 file の変更を含む conflict agent の結果を再現する。"""
        target.write_text("resolved change\n")
        extra.parent.mkdir(exist_ok=True)
        extra.write_text("extra\n")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"])

    assert result.exit_code != 0
    assert current_branch(root) == home_branch
    assert "conflict 解消以外の差分が残っています。" in result.stderr
    assert "src/extra.py" in result.stderr
    assert run_git(root, "rev-parse", home_branch).stdout.strip() == home_commit


@pytest.mark.parametrize("change_kind", ["context", "mode", "delete"])
def test_session_join_rejects_extra_conflict_file_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, change_kind: str
) -> None:
    """conflict marker 解消以外の conflict file 変更を merge しない。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md の
    「oracle file 規定と conflict 解消の優先順位」
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
    session_content = (
        "session change\n"
        if change_kind == "delete"
        else "prefix\nsession change\nsuffix\n"
    )
    home_content = (
        "home change\n" if change_kind == "delete" else "prefix\nhome change\nsuffix\n"
    )
    target.write_text(session_content)
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "session change")
    run_git(root, "switch", home_branch)
    target.write_text(home_content)
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "home change")
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()
    run_git(root, "switch", session_branch)

    class FakeCodexResult:
        """conflict resolution の成功を表す最小 fake result。"""

        output_json = None

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        """conflict marker 外の変更、file mode 変更、または file 削除を再現する。"""
        if change_kind == "delete":
            target.unlink()
            return FakeCodexResult()
        target.write_text(
            "prefix\nresolved change\n"
            + ("changed suffix\n" if change_kind == "context" else "suffix\n")
        )
        if change_kind == "mode":
            target.chmod(target.stat().st_mode | stat.S_IXUSR)
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"])

    assert result.exit_code != 0
    assert current_branch(root) == home_branch
    expected_summary = (
        "conflict 対象 file の不要な差分が残っています。"
        if change_kind in {"context", "delete"}
        else "conflict 解消以外の差分が残っています。"
    )
    assert expected_summary in result.stderr
    assert str(target) in result.stderr
    assert run_git(root, "rev-parse", home_branch).stdout.strip() == home_commit


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
        assert set(kwargs) == {"root", "purpose"}
        assert parameter.agent_call_cwd == root
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
    root = make_repo(tmp_path)
    target = root / "src" / "unmerged.py"
    target.parent.mkdir()

    # {{work-root}}/oracle/doc/dev_rule/coding_rule.md
    def fake_git(args: list[str], git_cwd: Path) -> cmoc_runtime.CommandResult:
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


def test_session_join_stages_conflict_path_as_literal_pathspec(tmp_path: Path) -> None:
    """特殊文字を含む conflict path を literal pathspec として stage する。"""
    root = make_repo(tmp_path)
    target = root / "src" / "[ab].txt"
    target.parent.mkdir()
    target.write_text("<<<<<<< HEAD\nhome\n=======\nsession\n>>>>>>> branch\n")
    unmerged_calls = 0
    add_calls: list[list[str]] = []

    def fake_git(args: list[str], git_cwd: Path) -> cmoc_runtime.CommandResult:
        """conflict 解消で呼ばれる Git 操作を記録する。"""
        nonlocal unmerged_calls
        if args == ["diff", "--name-only", "-z", "--diff-filter=U"]:
            unmerged_calls += 1
            output = "src/[ab].txt\0" if unmerged_calls == 1 else ""
            return cmoc_runtime.CommandResult(0, output, "")
        if args == ["status", "--porcelain=v1", "-z", "-uall"]:
            return cmoc_runtime.CommandResult(0, "", "")
        if args[:2] == ["add", "--"]:
            add_calls.append(args)
        return cmoc_runtime.CommandResult(0, "", "")

    def fake_codex_exec(_parameter: object, **_kwargs: object) -> object:
        """conflict marker を対象 path 内だけで解消する。"""
        target.write_text("resolved\n")
        return object()

    session_join_module.resolve_session_join_conflict(root, fake_codex_exec, fake_git)

    assert add_calls == [["add", "--", ":(literal)src/[ab].txt"]]


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
    report = terminal_primary_report(result)
    rendered_report = report.read_text(encoding="utf-8")
    assert f'session_branch: "{session_branch}"' in rendered_report
    assert f'home_branch: "{home_branch}"' in rendered_report
    assert 'session_state_after: "joined"' in rendered_report
    assert "merge_commit:" in rendered_report


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
    assert "/.cmoc/gu/" not in gitignore.read_text().splitlines()
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text().splitlines()
    assert run_git(linked, "ls-files", "--", ".cmoc/gu").stdout.splitlines() == [
        ".cmoc/gu/tracked-probe"
    ]
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

    # {{work-root}}/oracle/doc/dev_rule/coding_rule.md
    def fake_run_git(args: list[str], git_cwd: Path, check: bool = True) -> object:
        """session branch削除だけを失敗させ、他のGit操作は委譲する。"""
        if args == ["branch", "-d", session_branch]:
            return cmoc_runtime.CommandResult(1, "", "branch is checked out elsewhere")
        return original_run_git(args, git_cwd, check=check)

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
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """local home branch がない場合に同名 remote branch へ join しない。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
    {{work-root}}/oracle/doc/app_spec/session_state.md
    """
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()
    run_git(root, "branch", "-D", home_branch)

    remote = tmp_path / "remote.git"
    subprocess.run(
        ["git", "init", "--bare", str(remote)],
        text=True,
        capture_output=True,
        check=True,
    )
    run_git(root, "remote", "add", "origin", str(remote))
    run_git(root, "push", "origin", f"{home_commit}:refs/heads/{home_branch}")
    run_git(root, "config", "checkout.defaultRemote", "origin")

    result = runner.invoke(app, ["session", "join"])

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
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """事前条件 error terminal result を stderr へ出力する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "README.md").write_text("dirty\n")

    result = runner.invoke(app, ["session", "join"])

    assert result.exit_code != 0
    assert result.stdout == ""
    assert "# 失敗: cmoc session join" in result.stderr
    assert "git 未コミット差分が存在します。" in result.stderr
    assert "Traceback" not in result.stderr


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
    assert "# 失敗" not in result.stdout
    assert "conflict marker が残っています。" not in result.stdout
    assert "# 失敗: cmoc session join" in result.stderr
    assert "conflict marker が残っています。" in result.stderr


def test_session_join_conflict_uses_main_worktree_path_context(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree の conflict 解消でも main worktree context を使用する。

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

    def fake_run_codex_exec(parameter: AgentCallParameter, **kwargs: object) -> object:
        """Codex wrapper に渡された repo root と agent call cwd を記録する。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
        {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        """

        seen["root"] = kwargs["root"]
        seen["agent_call_cwd"] = parameter.agent_call_cwd
        assert "cwd" not in kwargs
        target.write_text("resolved change\nTitle\n=======\n")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert seen == {"root": root, "agent_call_cwd": root}
    assert current_branch(linked) == home_branch
    assert target.read_text() == "resolved change\nTitle\n=======\n"
