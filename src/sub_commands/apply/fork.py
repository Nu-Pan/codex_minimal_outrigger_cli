"""apply fork の branch/worktree 作成から Codex 適用 loop までを扱う。

このファイルは 16,000 文字を超えるが、責務境界は一つの apply run を開始し、
対象列挙、Codex によるレビュー・修正、commit、state 更新まで進める制御に閉じている。
apply state、worktree、再キュー、commit subject は同じ loop の失敗時復旧条件を
共有するため、分割すると fork 中の読み取り文脈がかえって分散する。
現状は apply fork の orchestration として一箇所に保つ方が凝集性が高い。

根拠: {{work-root}}/oracle/doc/app_spec/sub_command/apply_fork.md
"""

import os
from dataclasses import replace
from pathlib import Path

import typer

from acp.builder.apply.fork.file_review_and_fix import (
    build_apply_fork_file_review_and_fix_parameter,
)
from cmoc_runtime import (
    ApplyPart,
    CliRunResult,
    CmocError,
    SessionState,
    branch_exists,
    create_run_worktree,
    current_branch,
    current_subcommand_logger,
    delete_branch,
    ensure_cmoc_ignored_in_exclude,
    head_commit,
    is_oracle_file_path,
    is_untracked_git_ignored,
    load_config,
    load_state_for_branch,
    pushd,
    remove_worktree,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    run_codex_exec,
    run_git,
    start_subcommand_step,
    timestamp,
    work_root,
    worktrees_dir,
    write_state,
)
from commons.indexing import enable_indexing_preflight
from commons.runtime_apply import (
    apply_process_tracking,
    apply_run_lock,
    delete_apply_process_id,
    read_apply_process_id,
    stop_child_process_group,
    write_apply_process_id,
)
from commons.runtime_codex_exec import changed_worktree_paths
from commons.runtime_results import CodexExecCallable
from config.cmoc_config import CmocConfig
from sub_commands.apply.fork_report import (
    write_apply_fork_error_report,
    write_apply_fork_report,
)


def cmoc_apply_fork_impl(scope: str) -> None:
    """CLI runtime を通して apply fork を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_apply_fork_body,
        scope,
        run_codex_exec,
        command_name="apply fork",
        command_argv=["cmoc", "apply", "fork", "--scope", scope],
        total_steps=6,
    )


def _cmoc_apply_fork_body(
    scope: str,
    codex_exec: CodexExecCallable,
) -> CliRunResult:
    """Codex CLI による apply loop を isolated apply worktree 上で実行する。"""
    root = repo_root()
    current_root = work_root()
    branch = current_branch(current_root)
    session_id, _, _ = load_state_for_branch(root, branch)
    if not branch.startswith("cmoc/session/"):
        raise CmocError(
            "apply fork は session branch 上で実行してください。", [], branch
        )
    ensure_cmoc_ignored_in_exclude(current_root)
    require_clean_worktree(current_root)
    config = load_config(current_root)
    # {{work-root}}/oracle/doc/app_spec/sub_command/apply_fork.md
    # lifecycle lock の保持中に mutable state を読み直す。そうしないと二つの caller が
    # どちらも ready を観測し、異なる apply run を公開できてしまう。
    finding_counts: list[int] = []
    result_label = "error"
    report_path: Path | None = None
    apply_branch: str | None = None
    apply_worktree: Path | None = None
    state_published = False
    branch_preexisting = False
    worktree_preexisting = False
    interrupted = False
    try:
        with apply_run_lock(root, session_id):
            session_id, path, state = load_state_for_branch(root, branch)
            if state.session.state != "active" or state.apply.state != "ready":
                raise CmocError(
                    "apply fork の事前条件を満たしていません。", [], str(path)
                )
            run_id = timestamp()
            apply_branch = f"cmoc/apply/{session_id}/{run_id}"
            oracle_snapshot_commit = head_commit(current_root)
            apply_worktree = worktrees_dir(root) / session_id / run_id
            branch_preexisting = branch_exists(root, apply_branch)
            worktree_preexisting = (
                apply_worktree.exists() or apply_worktree.is_symlink()
            )
            if branch_preexisting or worktree_preexisting:
                raise CmocError(
                    "apply run の branch または worktree が既に存在します。",
                    ["既存の apply resource を確認してから再実行してください。"],
                    f"apply_branch: {apply_branch}\napply_worktree: {apply_worktree}",
                )
            start_subcommand_step(2, "run の隔離実行を開始", "start isolated run")
            state.apply = ApplyPart(
                state="running",
                apply_branch=apply_branch,
                oracle_snapshot_commit=oracle_snapshot_commit,
            )
            # cleanup target を作成前に公開する。lifecycle lock により、abandon が PID や
            # worktree のない running state を観測することを防ぐ。
            state_published = True
            write_state(path, state)
            create_run_worktree(
                current_root, apply_branch, apply_worktree, oracle_snapshot_commit
            )
            write_apply_process_id(root, session_id, os.getpid())
        assert apply_worktree is not None
        with apply_process_tracking(root, session_id), pushd(apply_worktree):
            try:
                start_subcommand_step(
                    3,
                    "調査待ちファイルリストを初期化",
                    "initialize pending files",
                )
                findings: list[dict] = []
                pending_targets = enumerate_apply_targets(
                    apply_worktree, scope, session_id, state
                )
                start_subcommand_step(4, "apply ループ", "apply loop")
                for _apply_loop in range(config.apply_fork.num_apply_files):
                    pending_targets = dedupe_apply_targets(pending_targets)
                    if not pending_targets:
                        result_label = "converged"
                        break
                    start_subcommand_step(
                        "4/6, 1/4", "調査対象を pop", "pop pending target"
                    )
                    target = pending_targets.pop(0)
                    start_subcommand_step(
                        "4/6, 2/4",
                        "対象ファイルをレビュー・修正",
                        "review and fix target",
                    )
                    findings = review_and_fix_apply_target(
                        apply_worktree,
                        target,
                        config,
                        codex_exec,
                        log_root=root,
                    )
                    finding_counts.append(len(findings))
                    start_subcommand_step(
                        "4/6, 3/4",
                        "結果と差分を調査待ちへ反映",
                        "update pending targets",
                    )
                    changed = changed_worktree_paths(apply_worktree)
                    if changed and not findings:
                        changed_paths = "\n".join(
                            str(path.relative_to(apply_worktree)) for path in changed
                        )
                        raise CmocError(
                            "ファイル単位レビュー・修正が、所見なしで差分を生成しました。",
                            [
                                "apply worktree の差分を確認し、apply abandon で破棄してから再実行してください。"
                            ],
                            changed_paths,
                        )
                    if findings:
                        pending_targets.append(target)
                    if not changed:
                        continue
                    pending_targets.extend(
                        normalize_apply_targets(
                            apply_worktree,
                            set(changed),
                            include_oracle=False,
                        )
                    )
                    start_subcommand_step(
                        "4/6, 4/4", "差分を commit", "commit agent changes"
                    )
                    commit_message = generate_apply_commit_message(
                        apply_worktree,
                        {"findings": findings},
                    )
                    run_git(["add", "."], apply_worktree)
                    run_git(["commit", "-m", commit_message], apply_worktree)
                else:
                    pending_targets = dedupe_apply_targets(pending_targets)
                    result_label = "unconverged" if pending_targets else "converged"
                report_path = _complete_apply_fork_run(
                    root,
                    session_id,
                    path,
                    state,
                    apply_worktree,
                    branch,
                    finding_counts,
                    result_label,
                    config,
                    codex_exec,
                    interrupted=False,
                )
            except KeyboardInterrupt:
                # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
                # 新規 agent call を止め、実行中の処理単位だけを破棄して、既に
                # commit 済みの単位を未収束の部分結果として確定する。
                interrupted = True
                result_label = "unconverged"
                _record_apply_fork_interruption()
                _stop_interrupted_apply_children(root, session_id)
                _discard_uncommitted_apply_changes(apply_worktree)
                report_path = _complete_apply_fork_run(
                    root,
                    session_id,
                    path,
                    state,
                    apply_worktree,
                    branch,
                    finding_counts,
                    result_label,
                    config,
                    codex_exec,
                    interrupted=True,
                )
    except BaseException as exc:
        # {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
        # 中断された Codex call はこの apply process より長く生存し得る。
        # error state の abandon が cleanup 前に停止できるよう child identity を保持する。
        if state_published:
            error_state_saved = False
            try:
                with apply_run_lock(root, session_id):
                    _session_id, path, state = load_state_for_branch(root, branch)
                    if state.apply.state != "ready":
                        state.apply.state = "error"
                        write_state(path, state)
                        error_state_saved = True
                        if report_path is None:
                            report_path = write_apply_fork_error_report(
                                root,
                                branch,
                                state,
                                finding_counts,
                                apply_worktree or root,
                                config,
                                codex_exec,
                                allow_codex_summary=not interrupted,
                            )
                        tracked_process = read_apply_process_id(root, session_id)
                        if not tracked_process or not tracked_process.child_processes:
                            delete_apply_process_id(root, session_id)
                        if report_path is not None:
                            setattr(exc, "cmoc_stdout", str(report_path.resolve()))
            except BaseException as recovery_error:
                if not error_state_saved:
                    rollback_failures = _rollback_apply_setup(
                        root,
                        session_id,
                        apply_branch,
                        apply_worktree,
                        branch_preexisting,
                        worktree_preexisting,
                    )
                    for failure in rollback_failures:
                        exc.add_note(f"apply resource rollback failed: {failure}")
                    if not rollback_failures:
                        try:
                            # 即時 rollback では abandon が扱う active run が残らない。
                            state.apply = ApplyPart()
                            write_state(path, state)
                        except BaseException as reset_error:
                            exc.add_note(f"apply state reset failed: {reset_error}")
                exc.add_note(f"apply run recovery failed: {recovery_error}")
        raise
    # {{work-root}}/oracle/doc/app_spec/sub_command/apply_fork.md は生成した report path を
    # stdout に出すことを求める。common runtime log はその前後に出力する。
    return CliRunResult(
        returncode=2 if result_label == "unconverged" else 0,
        stdout=str(report_path.resolve()),
    )


def _complete_apply_fork_run(
    root: Path,
    session_id: str,
    state_path: Path,
    state: SessionState,
    apply_worktree: Path,
    session_branch: str,
    finding_counts: list[int],
    result_label: str,
    config: CmocConfig,
    codex_exec: CodexExecCallable,
    *,
    interrupted: bool,
) -> Path:
    """state・report・PID を一つの apply 完了境界で確定する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/apply_fork.md
    # {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
    # completed 公開中は report と PID 解放まで cleanup と競合させない。
    with apply_run_lock(root, session_id):
        start_subcommand_step(5, "apply state を更新", "update apply state")
        state.apply.state = "completed"
        write_state(state_path, state)
        start_subcommand_step(6, "作業結果をレポート", "write apply report")
        report_path = write_apply_fork_report(
            root,
            apply_worktree,
            session_branch,
            state,
            finding_counts,
            result_label,
            config,
            codex_exec,
            interrupted=interrupted,
            allow_codex_summary=not interrupted,
        )
        delete_apply_process_id(root, session_id)
    return report_path


def _record_apply_fork_interruption() -> None:
    """中断要求を console とサブコマンドログの双方へ記録する。"""
    typer.echo(
        "# ユーザー中断要求を受け付けました\n"
        "- 確定済みの部分結果で apply fork を未収束として完了します。"
    )
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "user_interruption",
            command="apply fork",
            result="unconverged",
        )


def _stop_interrupted_apply_children(root: Path, session_id: str) -> None:
    """中断された処理単位の Codex process group を停止する。"""
    process = read_apply_process_id(root, session_id)
    if process is None:
        return
    logger = current_subcommand_logger()
    for child in process.child_processes:
        warning = stop_child_process_group(child)
        if warning and logger is not None:
            logger.event(
                "user_interruption_cleanup_warning",
                command="apply fork",
                warning=warning,
            )


def _discard_uncommitted_apply_changes(apply_worktree: Path) -> None:
    """中断時点の未確定な staged/unstaged/untracked 差分を破棄する。"""
    run_git(["reset", "--hard", "HEAD"], apply_worktree)
    run_git(["clean", "-fd"], apply_worktree)


def _rollback_apply_setup(
    root: Path,
    session_id: str,
    apply_branch: str | None,
    apply_worktree: Path | None,
    branch_preexisting: bool,
    worktree_preexisting: bool,
) -> list[str]:
    """error state を保存できない初期化失敗で作成済み resource を戻す。"""
    failures: list[str] = []
    # {{work-root}}/oracle/doc/app_spec/sub_command/apply_fork.md
    # 保存済み error state が無い場合は abandon が cleanup 対象を特定できない。
    if apply_worktree is not None and not worktree_preexisting:
        try:
            result = remove_worktree(root, apply_worktree)
            if result.returncode != 0 and apply_worktree.exists():
                failures.append(
                    f"worktree: {result.stderr.strip() or result.returncode}"
                )
        except BaseException as error:
            failures.append(f"worktree: {error}")
    if apply_branch is not None and not branch_preexisting:
        try:
            result = delete_branch(root, apply_branch, force=True)
            if result.returncode != 0 and branch_exists(root, apply_branch):
                failures.append(f"branch: {result.stderr.strip() or result.returncode}")
        except BaseException as error:
            failures.append(f"branch: {error}")
    try:
        delete_apply_process_id(root, session_id)
    except BaseException as error:
        failures.append(f"process tracking: {error}")
    return failures


def generate_apply_commit_message(
    apply_worktree: Path,
    applied_findings: dict,
) -> str:
    """所見リスト適用後の差分に対する commit subject を機械的に生成する。"""
    findings = applied_findings.get("findings")
    if isinstance(findings, list):
        for finding in findings:
            if isinstance(finding, dict):
                title = finding.get("title")
                if isinstance(title, str) and title.strip():
                    return commit_subject(f"Apply finding: {title.strip()}")
    paths = run_git(["diff", "--name-only"], apply_worktree).stdout.splitlines()
    if paths:
        suffix = " and more" if len(paths) > 3 else ""
        return commit_subject(f"Update {', '.join(paths[:3])}{suffix}")
    return "Apply cmoc finding"


def commit_subject(text: str) -> str:
    """git commit subject として扱う 1 行へ丸める。"""
    return " ".join(text.split())[:120] or "Apply cmoc finding"


def review_and_fix_apply_target(
    apply_worktree: Path,
    target: Path,
    config: CmocConfig,
    codex_exec: CodexExecCallable,
    log_root: Path | None = None,
) -> list[dict]:
    """対象ファイルを起点に所見調査・修正・検証を同一 call で行う。"""
    logger = current_subcommand_logger()
    result = codex_exec(
        replace(
            build_apply_fork_file_review_and_fix_parameter(target), cwd=apply_worktree
        ),
        root=log_root or apply_worktree,
        cwd=apply_worktree,
        config=config,
        purpose=f"apply fork review and fix for {target}",
        subcommand_logger=logger,
    )
    return list((result.output_json or {}).get("findings", []))


def dedupe_apply_targets(targets: list[Path]) -> list[Path]:
    """最初に現れた要素だけを残して調査待ちファイルリストの重複を削除する。"""
    deduped: list[Path] = []
    seen: set[Path] = set()
    for target in targets:
        lexical = target.absolute()
        if lexical in seen:
            continue
        seen.add(lexical)
        deduped.append(target)
    return deduped


def normalize_apply_targets(
    root: Path, candidates: set[Path], include_oracle: bool = True
) -> list[Path]:
    """apply finding 列挙対象として扱える file だけに正規化する。"""
    targets: list[Path] = []
    seen_repository_paths: set[Path] = set()
    for path in sorted(
        {
            (candidate if candidate.is_absolute() else root / candidate).absolute()
            for candidate in candidates
        }
    ):
        if not path.exists() or not path.is_file():
            continue
        try:
            rel_parts = path.relative_to(root.absolute()).parts
        except ValueError:
            continue
        if not rel_parts:
            continue
        if rel_parts[0] in {".git", ".agents", ".codex", ".cmoc", "memo"}:
            continue
        if rel_parts[0] == "oracle":
            if not include_oracle or not is_oracle_file_path(root, path):
                continue
        elif path.name in {"AGENTS.md", "INDEX.md"}:
            continue
        elif is_untracked_git_ignored(root, path):
            continue
        # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
        # oracle/ と realization/ は同じ実体を指す symlink でも別 file である。
        repository_path = path.relative_to(root.absolute())
        if repository_path in seen_repository_paths:
            continue
        seen_repository_paths.add(repository_path)
        targets.append(path)
    return targets


def enumerate_apply_targets(
    root: Path,
    scope: str,
    session_id: str,
    state: SessionState | None = None,
) -> list[Path]:
    """apply scope と session state から finding 列挙対象 file を決める。"""
    if scope == "full":
        candidates = list(root.rglob("*"))
    elif scope == "session":
        base = (
            state.session.session_start_commit
            if state and state.session.session_start_commit
            else "HEAD"
        )
        changed = run_git(
            ["diff", "--name-only", base, "HEAD"], root
        ).stdout.splitlines()
        candidates = [root / path for path in changed]
    elif state and (
        previous_join := previous_apply_join_commit(root, state, session_id)
    ):
        changed = run_git(
            ["diff", "--name-only", previous_join, "HEAD"],
            root,
        ).stdout.splitlines()
        candidates = [root / path for path in changed]
    elif state and state.session.session_start_commit:
        changed = run_git(
            ["diff", "--name-only", state.session.session_start_commit, "HEAD"], root
        ).stdout.splitlines()
        candidates = [root / path for path in changed]
    else:
        candidates = list((root / "oracle").rglob("*")) + [
            path for path in root.rglob("*") if path.is_file() and path.suffix == ".py"
        ]
    return normalize_apply_targets(root, set(candidates))


def previous_apply_join_commit(
    root: Path, state: SessionState, session_id: str
) -> str | None:
    """最後に join した同一 session の apply merge commit を git 履歴から解決する。"""
    snapshot = state.session.last_joined_apply_oracle_snapshot_commit
    if not snapshot:
        return None
    merges = run_git(
        ["rev-list", "--first-parent", "--merges", "--reverse", f"{snapshot}..HEAD"],
        root,
    ).stdout.splitlines()
    for merge_commit in merges:
        subject = run_git(
            ["show", "-s", "--format=%s", merge_commit], root
        ).stdout.strip()
        if f"'cmoc/apply/{session_id}/" not in subject:
            continue
        parents = run_git(
            ["show", "-s", "--format=%P", merge_commit], root
        ).stdout.split()
        if any(
            run_git(
                ["merge-base", "--is-ancestor", snapshot, parent],
                root,
                check=False,
            ).returncode
            == 0
            for parent in parents[1:]
        ):
            return merge_commit
    return None
