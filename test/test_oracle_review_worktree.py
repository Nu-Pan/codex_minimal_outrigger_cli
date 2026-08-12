"""oracle review の worktree と INDEX 統合を検証する。

仕様根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md、
{{work-root}}/oracle/doc/app_spec/run_isolation.md、
{{work-root}}/oracle/doc/branch_model.md、
{{work-root}}/oracle/doc/app_spec/indexing.md。
通知根拠: {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md。

この file は 16,000 文字を超えるが、review fork、linked worktree、preflight commit、
差分検証、merge は同じ review worktree lifecycle を検証する一つの責務である。分割
すると、review branch と INDEX 差分の外部契約を複数 file で追う必要があるため、現状
は review worktree 回帰として一箇所に保つ。

分割根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner
from _git_support import make_repo, run_git

import commons.indexing as indexing_module
import commons.runtime_cli as runtime_cli
import commons.runtime_codex_preflight as codex_preflight_module
import commons.runtime_run_lifecycle as lifecycle_module
import sub_commands.oracle.review as review_module
import sub_commands.oracle.review_index as review_index_module
from basic.acp import AgentCallParameter
from cmoc_runtime import CmocError
from commons.runtime_results import CommandResult
from commons.runtime_run_lifecycle import set_run_state, start_editing_run
from main import app


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    """各テスト前後で process-global な indexing preflight 状態を初期化する。

    根拠: {{work-root}}/oracle/doc/dev_rule/test_rule.md
    """
    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


class _FakeCodexResult:
    """oracle review が読む構造化出力だけを保持する fake。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """

    def __init__(self, output_json: dict[str, object]) -> None:
        """Codex CLI を起動せず、テスト用の構造化出力を保持する。"""
        self.output_json = output_json


def _schema_name(parameter: AgentCallParameter) -> str:
    """fake callback が検証する Structured Output schema 名を返す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
    """
    schema_path = parameter.structured_output_schema_path
    if schema_path is None:
        raise AssertionError("oracle review requires a Structured Output schema")
    return schema_path.name


def _review_worktree_from_enumeration(kwargs: dict[str, object]) -> Path:
    """enumeration purpose に含まれる oracle path から隔離 worktree を得る。"""
    prefix = "oracle review enumerate findings for "
    purpose = str(kwargs["purpose"])
    if not purpose.startswith(prefix):
        raise AssertionError(purpose)
    return Path(purpose.removeprefix(prefix)).parent.parent


def test_oracle_review_uses_linked_worktree_branch_and_oracle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree の session branch と oracle を review 対象にする。

    根拠: {{work-root}}/oracle/doc/app_spec/run_isolation.md、
    {{work-root}}/oracle/doc/branch_model.md。
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "gu" / "worktree" / "linked-review"
    run_git(root, "worktree", "add", "-b", "linked-review-home", str(linked), "HEAD")
    (linked / "oracle" / "linked.md").write_text("# linked oracle\n")
    run_git(linked, "add", "oracle/linked.md")
    run_git(linked, "commit", "-m", "linked oracle change")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_head = run_git(linked, "rev-parse", "HEAD").stdout.strip()
    calls: list[str] = []
    agent_call_cwds: list[Path] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """finding 列挙の応答と agent call cwd を記録する。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
        """

        agent_call_cwds.append(parameter.agent_call_cwd)
        calls.append(str(kwargs["purpose"]))
        schema_name = _schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            return _FakeCodexResult({"findings": []})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    assert report_path.is_relative_to(root / ".cmoc" / "gu" / "ar" / "report")
    assert not report_path.is_relative_to(linked)
    rendered = report_path.read_text()
    assert (
        f"run_fork_commit: {session_head}" in rendered
        or f'run_fork_commit: "{session_head}"' in rendered
    )
    assert "`oracle/linked.md`" in rendered
    branch = run_git(linked, "branch", "--show-current").stdout.strip()
    assert branch.startswith("cmoc/session/")
    assert agent_call_cwds
    assert all(path != root for path in agent_call_cwds)
    assert all(
        path.is_relative_to(root / ".cmoc" / "gu" / "worktree")
        for path in agent_call_cwds
    )
    assert Path.cwd() == linked
    assert any("linked.md" in call for call in calls)


def test_oracle_review_forks_from_snapshot_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session branch が進んでも review run は取得済み snapshot から fork する。

    根拠: {{work-root}}/oracle/doc/app_spec/run_isolation.md。
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    snapshot_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    original_create_run_worktree = review_module.create_run_worktree
    start_points: list[str] = []
    forked_commits: list[str] = []

    def advance_session_before_run_creation(
        root_arg: Path, branch: str, worktree: Path, start_point: str
    ) -> Path:
        """run worktree 作成直前に session branch を進めて fork point を検証する。"""
        (root / "README.md").write_text("# session advanced\n")
        run_git(root, "add", "README.md")
        run_git(root, "commit", "-m", "advance session before review run")
        start_points.append(start_point)
        created = original_create_run_worktree(root_arg, branch, worktree, start_point)
        forked_commits.append(run_git(worktree, "rev-parse", "HEAD").stdout.strip())
        return created

    monkeypatch.setattr(
        review_module,
        "create_run_worktree",
        advance_session_before_run_creation,
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """review の構造化出力を空にして、fork point の検証だけを行う。"""
        assert _schema_name(parameter) == "enumerate_finding.json"
        return _FakeCodexResult({"findings": []})

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0, result.output
    assert start_points == [snapshot_commit]
    assert forked_commits == [snapshot_commit]


def test_oracle_review_retries_run_target_collision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """既存 run target と timestamp が衝突しても別の target で隔離する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    collision_id = "2026-07-28_00-00-00_000000000"
    collision_branch = f"cmoc/run/{session_id}/{collision_id}"
    collision_worktree = root / ".cmoc" / "gu" / "worktree" / session_id / collision_id
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        collision_branch,
        str(collision_worktree),
        "HEAD",
    )
    target_ids = iter([collision_id, "2026-07-28_00-00-00_000000001"])
    monkeypatch.setattr(lifecycle_module, "timestamp", lambda: next(target_ids))
    agent_call_cwds: list[Path] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """review の構造化出力を空にし、agent call cwd を記録する。"""
        agent_call_cwds.append(parameter.agent_call_cwd)
        assert _schema_name(parameter) == "enumerate_finding.json"
        return _FakeCodexResult({"findings": []})

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0, result.output
    assert collision_worktree.exists()
    assert run_git(root, "branch", "--list", collision_branch).stdout.strip()
    assert agent_call_cwds
    assert set(agent_call_cwds) == {
        root
        / ".cmoc"
        / "gu"
        / "worktree"
        / session_id
        / "2026-07-28_00-00-00_000000001"
    }


def test_oracle_review_does_not_cleanup_preexisting_target_after_create_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """作成前から存在した target は create failure 後も削除しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    occupied_branch = f"cmoc/run/{session_id}/occupied"
    occupied_worktree = root / ".cmoc" / "gu" / "worktree" / session_id / "occupied"
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        occupied_branch,
        str(occupied_worktree),
        "HEAD",
    )
    monkeypatch.setattr(
        review_module,
        "new_run_target",
        lambda _root, _session_id: (occupied_branch, occupied_worktree),
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """既存 target が cleanup されず review が失敗することだけを確認する。"""
        raise AssertionError("create_run_worktree must fail before Codex execution")

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code != 0
    assert occupied_worktree.is_dir()
    assert run_git(root, "branch", "--list", occupied_branch).stdout.strip()


def test_oracle_review_interrupt_during_run_creation_cleans_resources(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """run worktree 作成後の中断でも review branch と worktree を削除する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    original_create_run_worktree = review_module.create_run_worktree
    created: dict[str, Path | str] = {}

    def create_then_interrupt(
        root_arg: Path,
        branch: str,
        worktree: Path,
        start_point: str,
    ) -> Path:
        """linked worktree 作成直後にユーザー中断を送出する。"""
        created.update(branch=branch, worktree=worktree)
        original_create_run_worktree(root_arg, branch, worktree, start_point)
        raise KeyboardInterrupt()

    monkeypatch.setattr(review_module, "create_run_worktree", create_then_interrupt)
    notifications: list[tuple[str, str]] = []
    monkeypatch.setattr(
        runtime_cli,
        "notify_terminal_result",
        lambda command, _root, state: notifications.append((command, state)),
    )

    result = runner.invoke(
        app,
        ["oracle", "review", "--scope", "full"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    branch = str(created["branch"])
    worktree = Path(str(created["worktree"]))
    assert run_git(root, "branch", "--list", branch).stdout == ""
    assert not worktree.exists()
    assert not worktree.is_symlink()
    assert notifications == [("oracle review", "interrupted")]
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    assert "result: interrupted" in report_path.read_text()


def test_oracle_review_interrupt_during_preconditions_writes_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """run resource 作成前の中断でも interrupted report を保存する。"""
    # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    def interrupt_current_branch(_root: Path) -> str:
        """review 固有事前条件中のユーザー中断を再現する。"""
        raise KeyboardInterrupt()

    monkeypatch.setattr(review_module, "current_branch", interrupt_current_branch)

    result = runner.invoke(
        app,
        ["oracle", "review", "--scope", "full"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    assert "result: interrupted" in report_path.read_text()
    assert run_git(root, "branch", "--list", "cmoc/run/*").stdout == ""


def test_oracle_review_interrupt_during_doctor_writes_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """doctor preprocess 中の中断でも review report を保存する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    def interrupt_doctor(_root: Path) -> None:
        """doctor preprocess 中のユーザー中断を再現する。"""
        raise KeyboardInterrupt()

    monkeypatch.setattr(review_module, "run_doctor_preprocess", interrupt_doctor)

    result = runner.invoke(
        app,
        ["oracle", "review", "--scope", "full"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    report = report_path.read_text()
    assert "result: interrupted" in report
    assert "oracle_count_total: 0" in report
    assert "oracle_count_evaluated: 0" in report


def test_oracle_review_interrupt_after_branch_only_creation_cleans_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """run branch だけ作成された中断でも、存在しない worktree を cleanup しない。

    根拠: {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
    """
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    created: dict[str, Path | str] = {}

    def create_branch_then_interrupt(
        root_arg: Path,
        branch: str,
        worktree: Path,
        start_point: str,
    ) -> Path:
        """linked worktree 追加の部分完了を run branch だけで再現する。"""
        created.update(branch=branch, worktree=worktree)
        run_git(root_arg, "branch", branch, start_point)
        raise KeyboardInterrupt()

    monkeypatch.setattr(
        review_module, "create_run_worktree", create_branch_then_interrupt
    )

    result = runner.invoke(
        app,
        ["oracle", "review", "--scope", "full"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    branch = str(created["branch"])
    worktree = Path(str(created["worktree"]))
    assert run_git(root, "branch", "--list", branch).stdout == ""
    assert not worktree.exists()
    assert not worktree.is_symlink()
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    assert "result: interrupted" in report_path.read_text()


def test_oracle_review_interrupt_during_resource_probe_cleans_resources(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """作成直後の resource probe 中断でも review branch を残さない。

    根拠: {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
    """
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    original_branch_exists = review_module.branch_exists
    interrupted = False
    created_branch: list[str] = []

    def interrupt_during_branch_probe(root_arg: Path, branch: str) -> bool:
        """review resource の所有権確認中の Ctrl+C を再現する。"""
        nonlocal interrupted
        present = original_branch_exists(root_arg, branch)
        if branch.startswith("cmoc/run/") and present and not interrupted:
            interrupted = True
            created_branch.append(branch)
            raise KeyboardInterrupt()
        return present

    monkeypatch.setattr(review_module, "branch_exists", interrupt_during_branch_probe)

    result = runner.invoke(
        app,
        ["oracle", "review", "--scope", "full"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    assert created_branch
    assert run_git(root, "branch", "--list", created_branch[0]).stdout == ""
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    assert "result: interrupted" in report_path.read_text()


def test_oracle_review_keeps_successfully_created_branch_owned_on_false_probe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """成功した worktree 作成後の false probe でも run branch を cleanup する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    created_branch: list[str] = []
    original_branch_exists = review_module.branch_exists

    def false_for_created_branch(root_arg: Path, branch: str) -> bool:
        """作成後の branch probe が false になる状態を再現する。"""
        if branch.startswith("cmoc/run/"):
            created_branch.append(branch)
            return False
        return original_branch_exists(root_arg, branch)

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """finding 列挙を空結果にして cleanup だけを検証する。"""
        assert _schema_name(parameter) == "enumerate_finding.json"
        return _FakeCodexResult({"findings": []})

    monkeypatch.setattr(review_module, "branch_exists", false_for_created_branch)
    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0, result.output
    assert created_branch
    assert run_git(root, "branch", "--list", created_branch[0]).stdout == ""


@pytest.mark.parametrize("interrupt_cleanup_lock", [False, True])
def test_oracle_review_serializes_merge_and_cleanup_with_run_lifecycle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    interrupt_cleanup_lock: bool,
) -> None:
    """review run の merge・cleanup と lock 待機中断を検証する。

    根拠: {{work-root}}/oracle/doc/app_spec/run_isolation.md、
    {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
    """
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    original_lock = review_module.run_lifecycle_lock
    original_cleanup = review_module._cleanup_review_run
    original_merge = review_module.merge_review_branch
    lock_depth = 0
    lock_calls = 0
    merge_lock_depths: list[int] = []
    cleanup_lock_depths: list[int] = []

    @contextmanager
    def tracked_lock(root_arg: Path, session_id: str) -> Iterator[None]:
        """lifecycle lock の保持中に実行された処理を記録する。"""
        nonlocal lock_calls, lock_depth
        lock_calls += 1
        if interrupt_cleanup_lock and lock_calls == 3:
            raise KeyboardInterrupt()
        with original_lock(root_arg, session_id):
            lock_depth += 1
            try:
                yield
            finally:
                lock_depth -= 1

    def tracked_cleanup(*args: object, **kwargs: object) -> object:
        """merge 後の cleanup が lock 内で行われることを検証する。"""
        cleanup_lock_depths.append(lock_depth)
        return original_cleanup(*args, **kwargs)

    def tracked_merge(*args: object, **kwargs: object) -> object:
        """review branch の merge が lock 内で行われることを検証する。"""
        merge_lock_depths.append(lock_depth)
        return original_merge(*args, **kwargs)

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """finding 列挙を空結果にして lifecycle の直列化だけを検証する。"""
        assert _schema_name(parameter) == "enumerate_finding.json"
        review_worktree = _review_worktree_from_enumeration(kwargs)
        (review_worktree / "INDEX.md").write_text("# generated review index\n")
        return _FakeCodexResult({"findings": []})

    monkeypatch.setattr(review_module, "run_lifecycle_lock", tracked_lock)
    monkeypatch.setattr(review_module, "_cleanup_review_run", tracked_cleanup)
    monkeypatch.setattr(review_module, "merge_review_branch", tracked_merge)
    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
    )

    if interrupt_cleanup_lock:
        assert result.exit_code != 0
        assert "oracle review の隔離 run の cleanup に失敗しました。" in result.output
        assert merge_lock_depths == [1]
        assert cleanup_lock_depths == []
    else:
        assert result.exit_code == 0, result.output
        assert merge_lock_depths == [1]
        assert cleanup_lock_depths == [1]


def test_oracle_review_unexpected_base_exception_during_run_creation_cleans_resources(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """run 作成後の非通常例外でも review resource を cleanup して error report を残す。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    original_create_run_worktree = review_module.create_run_worktree
    created: dict[str, Path | str] = {}

    def create_then_exit(
        root_arg: Path,
        branch: str,
        worktree: Path,
        start_point: str,
    ) -> Path:
        """linked worktree 作成後に KeyboardInterrupt 以外の BaseException を送出する。"""
        created.update(branch=branch, worktree=worktree)
        original_create_run_worktree(root_arg, branch, worktree, start_point)
        raise SystemExit("unexpected create failure")

    monkeypatch.setattr(review_module, "create_run_worktree", create_then_exit)

    result = runner.invoke(
        app,
        ["oracle", "review", "--scope", "full"],
        catch_exceptions=False,
    )

    assert result.exit_code != 0
    branch = str(created["branch"])
    worktree = Path(str(created["worktree"]))
    assert run_git(root, "branch", "--list", branch).stdout == ""
    assert not worktree.exists()
    assert not worktree.is_symlink()
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    rendered = report_path.read_text()
    assert "result: error" in rendered
    assert "unexpected create failure" in result.output


def test_oracle_review_reports_unknown_run_branch_as_null_before_target_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """run target 作成前の失敗 report は未確定の branch を null で表す。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    def fail_new_run_target(_root: Path, _session_id: str) -> tuple[str, Path]:
        """run branch が確定する前の失敗を再現する。"""
        raise RuntimeError("run target selection failed")

    monkeypatch.setattr(review_module, "new_run_target", fail_new_run_target)

    result = runner.invoke(
        app,
        ["oracle", "review", "--scope", "full"],
        catch_exceptions=False,
    )

    assert result.exit_code != 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    rendered = report_path.read_text()
    assert "result: error" in rendered
    assert "run_branch: null" in rendered


@pytest.mark.parametrize(
    ("relative_path", "content"),
    [
        ("oracle/uncommitted.md", "# uncommitted\n"),
        ("README.md", "dirty\n"),
    ],
)
def test_oracle_review_rejects_uncommitted_worktree_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    relative_path: str,
    content: str,
) -> None:
    """session fork 後に未コミット差分がある worktree を拒否する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / relative_path).write_text(content)

    result = runner.invoke(app, ["oracle", "review"])

    assert result.exit_code != 0
    assert "git 未コミット差分" in result.output
    assert str(root / relative_path) in result.output
    assert relative_path in result.output


def test_oracle_review_allows_active_editing_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """read-only review は active editing run 中でも実行できる。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md、
    {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md。
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    context = start_editing_run("realization_apply")

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """review の所見列挙を空結果にして lifecycle の許可だけを検証する。"""

        assert _schema_name(parameter) == "enumerate_finding.json"
        return _FakeCodexResult({"findings": []})

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0, result.output
    set_run_state(context, "joinable")
    abandon = runner.invoke(app, ["run", "abandon"], catch_exceptions=False)
    assert abandon.exit_code == 0, abandon.output


def test_oracle_review_merges_review_index_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """review worktree で生成された INDEX.md だけを session に統合する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md、
    {{work-root}}/oracle/doc/app_spec/indexing.md。
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_id = (
        run_git(root, "branch", "--show-current")
        .stdout.strip()
        .removeprefix("cmoc/session/")
    )
    review_worktrees: list[Path] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """finding 検証を空結果にし、review worktree の INDEX を更新する。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md、
        {{work-root}}/oracle/doc/app_spec/indexing.md。
        """

        review_worktree = _review_worktree_from_enumeration(kwargs)
        review_worktrees.append(review_worktree)
        schema_name = _schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            (review_worktree / "INDEX.md").write_text("# generated review index\n")
            return _FakeCodexResult({"findings": []})
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return _FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return _FakeCodexResult({"verdict": "reject", "reason": "no finding"})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert (root / "INDEX.md").read_text() == "# generated review index\n"
    rendered = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    ).read_text()
    assert "run_join_commit: null" not in rendered
    assert review_worktrees
    for review_worktree in review_worktrees:
        assert review_worktree.parent == root / ".cmoc" / "gu" / "worktree" / session_id
    assert not any(
        path.name == ".git"
        for path in (root / ".cmoc" / "gu" / "worktree").rglob(".git")
    )
    assert all(not path.exists() and not path.is_symlink() for path in review_worktrees)


def test_oracle_review_preflight_uses_review_worktree_path_context(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """review agent call の preflight は review worktree context を使う。

    根拠: {{work-root}}/oracle/doc/app_spec/run_isolation.md、
    {{work-root}}/oracle/doc/app_spec/indexing.md。
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    review_worktrees: list[Path] = []

    def fake_update_indexes(
        update_root: Path, codex_exec: object | None = None
    ) -> list[Path]:
        """preflight の INDEX 更新先を記録し、生成結果を返す。

        根拠: {{work-root}}/oracle/doc/app_spec/indexing.md。
        """

        review_worktrees.append(update_root)
        index_path = update_root / "INDEX.md"
        index_path.write_text("# preflight review index\n")
        return [index_path]

    def fake_runtime_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """preflight 中の finding 列挙を空結果に置き換える。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
        """

        schema_name = _schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            return _FakeCodexResult({"findings": []})
        raise AssertionError(schema_name)

    monkeypatch.setattr(indexing_module, "update_indexes", fake_update_indexes)
    monkeypatch.setattr(
        codex_preflight_module, "runtime_run_codex_exec", fake_runtime_run_codex_exec
    )

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert (root / "INDEX.md").read_text() == "# preflight review index\n"
    assert review_worktrees
    assert all(path != root for path in review_worktrees)
    assert all(
        path.is_relative_to(root / ".cmoc" / "gu" / "worktree")
        for path in review_worktrees
    )
    assert (
        run_git(
            root,
            "log",
            "--all",
            "--grep=^cmoc indexing$",
            "-1",
            "--pretty=%s",
        ).stdout.strip()
        == "cmoc indexing"
    )
    rendered = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    ).read_text()
    assert "run_join_commit: null" not in rendered


@pytest.mark.parametrize("index_relative_path", ["INDEX.md", "日本語[1]/INDEX.md"])
def test_oracle_review_resolves_index_conflict_when_session_deleted_index(
    tmp_path: Path, index_relative_path: str
) -> None:
    """session 側で削除された INDEX.md の merge conflict を解決する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
    """

    root = make_repo(tmp_path)
    index_path = root / index_relative_path
    home_branch = run_git(root, "branch", "--show-current").stdout.strip()
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("base\n")
    run_git(root, "add", "--", index_relative_path)
    run_git(root, "commit", "-m", "add index")
    run_git(root, "switch", "-c", "review")
    index_path.write_text("review\n")
    run_git(root, "add", "--", index_relative_path)
    run_git(root, "commit", "-m", "review index")
    run_git(root, "switch", home_branch)
    index_path.unlink()
    run_git(root, "add", "--", index_relative_path)
    run_git(root, "commit", "-m", "delete index")
    merge = subprocess.run(
        ["git", "merge", "--no-ff", "review"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    assert merge.returncode != 0

    resolved = review_module.resolve_review_index_conflicts(root)

    assert resolved is True
    assert not index_path.exists()
    assert run_git(root, "diff", "--name-only", "--diff-filter=U").stdout.strip() == ""
    assert "Merge branch 'review'" in run_git(root, "log", "-1", "--pretty=%B").stdout


def test_oracle_review_aborts_non_index_merge_conflict(
    tmp_path: Path,
) -> None:
    """INDEX.md 以外の merge conflict でも session worktree を復旧する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
    """

    root = make_repo(tmp_path)
    home_branch = run_git(root, "branch", "--show-current").stdout.strip()
    run_git(root, "switch", "-c", "review")
    (root / "README.md").write_text("review\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "review README")
    run_git(root, "switch", home_branch)
    (root / "README.md").write_text("session\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session README")
    session_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()

    with pytest.raises(CmocError, match="review branch の merge に失敗しました"):
        review_module.merge_review_branch(root, "review")

    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == session_commit
    assert run_git(root, "diff", "--name-only", "--diff-filter=U").stdout == ""
    assert run_git(root, "status", "--porcelain").stdout == ""
    assert (root / "README.md").read_text() == "session\n"


def test_oracle_review_restores_interrupted_merge_conflict(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """git merge の中断でも session worktree に conflict state を残さない。

    根拠: {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
    """
    root = make_repo(tmp_path)
    home_branch = run_git(root, "branch", "--show-current").stdout.strip()
    run_git(root, "switch", "-c", "review")
    (root / "README.md").write_text("review\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "review README")
    run_git(root, "switch", home_branch)
    (root / "README.md").write_text("session\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session README")
    session_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    original_run_git = review_index_module.run_git

    # {{work-root}}/oracle/doc/dev_rule/coding_rule.md
    def interrupt_during_merge(
        args: list[str], git_cwd: Path, check: bool = True
    ) -> CommandResult:
        """conflict state 作成直後の Ctrl+C を再現する。"""
        result = original_run_git(args, git_cwd, check=check)
        if args[:2] == ["merge", "--no-ff"]:
            raise KeyboardInterrupt()
        return result

    monkeypatch.setattr(review_index_module, "run_git", interrupt_during_merge)

    with pytest.raises(KeyboardInterrupt):
        review_module.merge_review_branch(root, "review")

    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == session_commit
    assert run_git(root, "diff", "--name-only", "--diff-filter=U").stdout == ""
    assert run_git(root, "status", "--porcelain").stdout == ""
    assert (root / "README.md").read_text() == "session\n"


def test_oracle_review_cleans_untracked_merge_rollback_residue(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """merge abort の失敗で残った未追跡 path も session worktree から除去する。

    根拠: {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
    """
    root = make_repo(tmp_path)
    home_branch = run_git(root, "branch", "--show-current").stdout.strip()
    run_git(root, "switch", "-c", "review")
    (root / "README.md").write_text("review\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "review README")
    run_git(root, "switch", home_branch)
    (root / "README.md").write_text("session\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session README")
    session_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    leftover = root / "merge-leftover.txt"
    original_run_git = review_index_module.run_git

    # {{work-root}}/oracle/doc/dev_rule/coding_rule.md
    def fail_abort_with_leftover(
        args: list[str], git_cwd: Path, check: bool = True
    ) -> CommandResult:
        """merge abort 失敗後に未追跡 path が残る状態を再現する。"""
        result = original_run_git(args, git_cwd, check=check)
        if args == ["merge", "--abort"]:
            leftover.write_text("partial merge output\n")
            return CommandResult(1, result.stdout, result.stderr)
        return result

    monkeypatch.setattr(review_index_module, "run_git", fail_abort_with_leftover)

    with pytest.raises(CmocError, match="review branch の merge に失敗しました"):
        review_module.merge_review_branch(root, "review")

    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == session_commit
    assert run_git(root, "status", "--porcelain").stdout == ""
    assert not leftover.exists()


def test_commit_review_index_changes_accepts_nested_untracked_index(
    tmp_path: Path,
) -> None:
    """未追跡 directory 配下でも INDEX.md だけなら commit する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md、
    {{work-root}}/oracle/doc/app_spec/indexing.md。
    """

    root = make_repo(tmp_path)
    generated_index = root / "generated[1]" / "INDEX.md"
    generated_index.parent.mkdir()
    generated_index.write_text("# generated\n")

    assert review_module.commit_review_index_changes(root) is True
    assert (
        run_git(root, "show", "--format=", "--name-only", "HEAD").stdout.strip()
        == "generated[1]/INDEX.md"
    )


def test_commit_review_index_changes_accepts_generated_index_directory_rename(
    tmp_path: Path,
) -> None:
    """生成済み INDEX.md の親 directory rename を INDEX 差分として commit する。"""

    root = make_repo(tmp_path)
    old_directory = root / "old-directory"
    old_directory.mkdir()
    (old_directory / "INDEX.md").write_text("# generated\n")
    run_git(root, "add", "old-directory/INDEX.md")
    run_git(root, "commit", "-m", "add generated index")

    run_git(root, "mv", "old-directory", "new-directory")

    assert review_module.commit_review_index_changes(root) is True
    assert not old_directory.exists()
    assert (root / "new-directory" / "INDEX.md").exists()
    assert (
        run_git(root, "show", "--format=", "--name-only", "HEAD").stdout.strip()
        == "new-directory/INDEX.md"
    )


def test_review_branch_accepts_index_path_with_git_quoted_parent(
    tmp_path: Path,
) -> None:
    """Git が quote する親 directory 配下の INDEX.md も変更として扱う。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
    """
    root = make_repo(tmp_path)
    index_path = root / "日本語[1]" / "INDEX.md"
    index_path.parent.mkdir()
    index_path.write_text("# generated\n")
    run_git(root, "add", "--", str(index_path.relative_to(root)))
    run_git(root, "commit", "-m", "generated index")

    base_commit = run_git(root, "rev-parse", "HEAD^").stdout.strip()

    assert review_module.review_branch_has_index_changes(root, base_commit) is True


def test_review_branch_rejects_non_index_rename_to_index(
    tmp_path: Path,
) -> None:
    """非 INDEX file から INDEX.md への rename を差分違反として扱う。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
    """
    root = make_repo(tmp_path)
    (root / "README.md").rename(root / "INDEX.md")
    run_git(root, "add", "-A")
    run_git(root, "commit", "-m", "rename non-index to index")
    base_commit = run_git(root, "rev-parse", "HEAD^").stdout.strip()

    with pytest.raises(CmocError, match="INDEX.md 以外の commit 済み差分"):
        review_module.review_branch_has_index_changes(root, base_commit)


@pytest.mark.parametrize("relative_path", [".agents/INDEX.md", "memo/INDEX.md"])
def test_review_branch_rejects_non_generated_index_commit(
    tmp_path: Path,
    relative_path: str,
) -> None:
    """indexing 対象外 directory の INDEX.md commit を統合しない。

    根拠: {{work-root}}/oracle/doc/app_spec/indexing.md。
    """
    root = make_repo(tmp_path)
    index_path = root / relative_path
    index_path.parent.mkdir(parents=True)
    index_path.write_text("unexpected\n")
    run_git(root, "add", "--", relative_path)
    run_git(root, "commit", "-m", "add non-generated index")
    base_commit = run_git(root, "rev-parse", "HEAD^").stdout.strip()

    with pytest.raises(CmocError, match="INDEX.md 以外の commit 済み差分"):
        review_module.review_branch_has_index_changes(root, base_commit)


@pytest.mark.parametrize("change_kind", ["unstaged", "staged", "untracked"])
def test_oracle_review_rejects_non_index_worktree_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    change_kind: str,
) -> None:
    """review worktree が INDEX.md 以外を変更した場合に失敗させる。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md、
    {{work-root}}/oracle/doc/app_spec/indexing.md。
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """finding 列挙時に指定された種類の不正な差分を作る。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
        """

        schema_name = _schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            review_worktree = _review_worktree_from_enumeration(kwargs)
            if change_kind == "untracked":
                (review_worktree / "generated.txt").write_text("unexpected\n")
            else:
                (review_worktree / "README.md").write_text("unexpected\n")
                if change_kind == "staged":
                    run_git(review_worktree, "add", "README.md")
            return _FakeCodexResult({"findings": []})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["oracle", "review", "--scope", "full"])

    assert result.exit_code != 0
    assert "oracle review が INDEX.md 以外の差分を作成しました。" in result.output
    assert (root / "README.md").read_text() == "# repo\n"
    assert not (root / "generated.txt").exists()


@pytest.mark.parametrize("relative_path", [".agents/INDEX.md", "memo/INDEX.md"])
def test_oracle_review_rejects_non_generated_index_worktree_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    relative_path: str,
) -> None:
    """indexing 対象外 directory の INDEX.md を session に統合しない。

    根拠: {{work-root}}/oracle/doc/app_spec/indexing.md。
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """indexing 対象外の INDEX.md を review worktree に作る。"""
        assert _schema_name(parameter) == "enumerate_finding.json"
        review_worktree = _review_worktree_from_enumeration(kwargs)
        unexpected_index = review_worktree / relative_path
        unexpected_index.parent.mkdir(parents=True, exist_ok=True)
        unexpected_index.write_text("unexpected\n")
        return _FakeCodexResult({"findings": []})

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["oracle", "review", "--scope", "full"])

    assert result.exit_code != 0
    assert "oracle review が INDEX.md 以外の差分を作成しました。" in result.output
    assert relative_path in result.output


def test_oracle_review_reports_cleanup_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """隔離 worktree または run branch の削除失敗を成功扱いにしない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """review の列挙を完了させ、cleanup の失敗検査まで進める。"""
        assert _schema_name(parameter) == "enumerate_finding.json"
        return _FakeCodexResult({"findings": []})

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)
    failed_cleanup = CommandResult(1, "", "cleanup failed")

    def fail_remove_worktree(_root: Path, worktree: Path) -> CommandResult:
        """削除 command が失敗しつつ path だけ消えた cleanup を再現する。"""
        worktree.rename(worktree.with_name(f"{worktree.name}.removed"))
        return failed_cleanup

    monkeypatch.setattr(review_module, "remove_worktree", fail_remove_worktree)
    monkeypatch.setattr(
        review_module, "delete_branch", lambda *args, **kwargs: failed_cleanup
    )

    result = runner.invoke(app, ["oracle", "review", "--scope", "full"])

    assert result.exit_code != 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    rendered = report_path.read_text()
    assert "result: error" in rendered
    assert "oracle review の隔離 run の cleanup に失敗しました。" in rendered
    assert "cleanup failed" in rendered
    assert "worktree removal failed: cleanup failed" in result.output
    assert "cleanup failed" in result.output


def test_oracle_review_reports_cleanup_failure_after_outer_interrupt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """外側で Ctrl+C が発生した後の cleanup failure は中断成功ではなくエラーとする。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """review の列挙を完了させ、後続処理の中断検査へ進める。"""
        assert _schema_name(parameter) == "enumerate_finding.json"
        return _FakeCodexResult({"findings": []})

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    def interrupt_after_review(_review_worktree: Path) -> bool:
        """review loop 後の処理で、外側の中断処理を再現する。"""
        raise KeyboardInterrupt()

    monkeypatch.setattr(
        review_module, "commit_review_index_changes", interrupt_after_review
    )
    failed_cleanup = CommandResult(1, "", "cleanup failed")

    def fail_remove_worktree(_root: Path, worktree: Path) -> CommandResult:
        """削除 command が失敗しつつ path だけ消えた cleanup を再現する。"""
        worktree.rename(worktree.with_name(f"{worktree.name}.removed"))
        return failed_cleanup

    monkeypatch.setattr(review_module, "remove_worktree", fail_remove_worktree)
    monkeypatch.setattr(
        review_module, "delete_branch", lambda *args, **kwargs: failed_cleanup
    )

    result = runner.invoke(app, ["oracle", "review", "--scope", "full"])

    assert result.exit_code != 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    rendered = report_path.read_text()
    assert "result: error" in rendered
    assert "cleanup failed" in rendered
    assert "ユーザー中断要求" not in rendered


def test_cleanup_review_run_rejects_remaining_dangling_worktree_symlink(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """cleanup 成功コードでも残った dangling symlink を隔離 run 残存として扱う。"""
    review_worktree = tmp_path / "review-worktree"
    review_worktree.symlink_to(tmp_path / "missing-worktree")

    monkeypatch.setattr(
        review_module,
        "remove_worktree",
        lambda _root, _worktree: CommandResult(0, "", ""),
    )

    cleanup_error = review_module._cleanup_review_run(
        tmp_path,
        review_worktree,
        "cmoc/run/session/run",
        worktree_created=True,
        branch_created=False,
    )

    assert cleanup_error is not None
    assert "path still exists" in cleanup_error.detail
