"""apply fork の branch/worktree 作成から Codex 適用 loop までを扱う。

このファイルは 16,000 文字を超えるが、責務境界は一つの apply run を開始し、
対象列挙、Codex による finding 適用、commit、state 更新まで進める制御に閉じている。
apply state、worktree、再キュー、commit subject は同じ loop の失敗時復旧条件を
共有するため、分割すると fork 中の読み取り文脈がかえって分散する。
現状は apply fork の orchestration として一箇所に保つ方が凝集性が高い。
"""

import os
from dataclasses import replace
from pathlib import Path
from typing import Callable

from acp.builder.apply.fork.file_finding_enumeration import (
    build_apply_fork_file_finding_enumeration_parameter,
)
from acp.builder.apply.fork.finding_application import (
    build_apply_fork_finding_application_parameter,
)
from commons.runtime_codex_exec import changed_worktree_paths
from cmoc_runtime import (
    ApplyPart,
    CliRunResult,
    CmocError,
    SessionState,
    apply_branch_session_id,
    create_run_worktree,
    current_branch,
    current_subcommand_logger,
    ensure_cmoc_ignored_in_exclude,
    head_commit,
    is_untracked_git_ignored,
    load_config,
    load_state_for_branch,
    pushd,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    run_codex_exec,
    run_git,
    timestamp,
    work_root,
    worktrees_dir,
    write_state,
)
from config.cmoc_config import CmocConfig
from sub_commands.apply.fork_report import (
    write_apply_fork_error_report,
    write_apply_fork_report,
)
from commons.runtime_apply import (
    apply_process_tracking,
    delete_apply_process_id,
    write_apply_process_id,
)
from commons.indexing import enable_indexing_preflight


CodexExec = Callable[..., object]


def cmoc_apply_fork_impl(scope: str) -> None:
    """CLI runtime を通して apply fork を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_apply_fork_body,
        scope,
        run_codex_exec,
        command_name="apply fork",
        command_argv=["cmoc", "apply", "fork", "--scope", scope],
    )


def _cmoc_apply_fork_body(
    scope: str,
    codex_exec: CodexExec,
) -> CliRunResult:
    """Codex CLI による apply loop を isolated apply worktree 上で実行する。"""
    root = repo_root()
    current_root = work_root()
    branch = current_branch(current_root)
    session_id, path, state = load_state_for_branch(root, branch)
    if not branch.startswith("cmoc/session/"):
        raise CmocError("apply fork は session branch 上で実行してください。", [], branch)
    if state.session.state != "active" or state.apply.state != "ready":
        raise CmocError("apply fork の事前条件を満たしていません。", [], str(path))
    ensure_cmoc_ignored_in_exclude(current_root)
    require_clean_worktree(current_root)
    config = load_config(root)
    run_id = timestamp()
    apply_branch = f"cmoc/apply/{session_id}/{run_id}"
    oracle_snapshot_commit = head_commit(current_root)
    apply_worktree = worktrees_dir(root) / session_id / run_id
    create_run_worktree(current_root, apply_branch, apply_worktree, "HEAD")
    write_apply_process_id(root, session_id, os.getpid())
    state.apply = ApplyPart(
        state="running",
        apply_branch=apply_branch,
        oracle_snapshot_commit=oracle_snapshot_commit,
    )
    write_state(path, state)
    finding_counts: list[int] = []
    result_label = "error"
    report_path: Path | None = None
    try:
        with apply_process_tracking(root, session_id), pushd(apply_worktree):
            findings: list[dict] = []
            pending_targets = enumerate_apply_targets(apply_worktree, scope, state)
            for _apply_loop in range(config.apply_fork.num_apply_files):
                pending_targets = dedupe_apply_targets(pending_targets)
                if not pending_targets:
                    result_label = "converged"
                    break
                target = pending_targets.pop(0)
                findings = enumerate_apply_findings_for_target(
                    apply_worktree,
                    target,
                    config,
                    codex_exec,
                    log_root=root,
                )
                finding_counts.append(len(findings))
                if not findings:
                    continue
                pending_targets.append(target)
                run_finding_application(
                    root,
                    apply_worktree,
                    findings,
                    config,
                    codex_exec,
                )
                changed = changed_worktree_paths(apply_worktree)
                if not changed:
                    continue
                pending_targets.extend(
                    normalize_apply_targets(
                        apply_worktree,
                        set(changed),
                        include_oracle=False,
                    )
                )
                if changed:
                    commit_message = generate_apply_commit_message(
                        apply_worktree,
                        {"findings": findings},
                    )
                    run_git(["add", "."], apply_worktree)
                    run_git(["commit", "-m", commit_message], apply_worktree)
            else:
                pending_targets = dedupe_apply_targets(pending_targets)
                result_label = "unconverged" if pending_targets else "converged"
            state.apply.state = "completed"
            write_state(path, state)
            report_path = write_apply_fork_report(
                root,
                apply_worktree,
                branch,
                state,
                finding_counts,
                result_label,
                config,
                codex_exec,
            )
        delete_apply_process_id(root, session_id)
    except BaseException as exc:
        delete_apply_process_id(root, session_id)
        state.apply.state = "error"
        write_state(path, state)
        if report_path is None:
            report_path = write_apply_fork_error_report(
                root, branch, state, finding_counts, apply_worktree, config, codex_exec
            )
        setattr(exc, "cmoc_stdout", str(report_path.resolve()))
        raise
    # <work-root>/oracle/doc/app_spec/sub_command/apply_fork.md requires the
    # generated report path on stdout; common runtime logs are emitted around it.
    return CliRunResult(
        returncode=2 if result_label == "unconverged" else 0,
        stdout=str(report_path.resolve()),
    )


def run_finding_application(
    root: Path,
    apply_worktree: Path,
    findings: list[dict],
    config: CmocConfig,
    codex_exec: CodexExec,
) -> None:
    """所見リスト適用を Codex に依頼する。"""
    parameter = replace(
        build_apply_fork_finding_application_parameter(findings),
        cwd=apply_worktree,
    )
    codex_exec(
        parameter,
        root=root,
        cwd=apply_worktree,
        config=config,
        purpose="apply fork finding application",
    )


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


def enumerate_apply_findings_for_target(
    root: Path,
    target: Path,
    config: CmocConfig,
    codex_exec: CodexExec,
    log_root: Path | None = None,
) -> list[dict]:
    """対象ファイルを起点に apply finding を列挙する。"""
    logger = current_subcommand_logger()
    result = codex_exec(
        replace(build_apply_fork_file_finding_enumeration_parameter(target), cwd=root),
        root=log_root or root,
        cwd=root,
        config=config,
        purpose=f"apply fork enumerate findings for {target}",
        subcommand_logger=logger,
    )
    return list((result.output_json or {}).get("findings", []))


def dedupe_apply_targets(targets: list[Path]) -> list[Path]:
    """最初に現れた要素だけを残して調査待ちファイルリストの重複を削除する。"""
    deduped: list[Path] = []
    seen: set[Path] = set()
    for target in targets:
        resolved = target.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        deduped.append(target)
    return deduped


def normalize_apply_targets(
    root: Path, candidates: set[Path], include_oracle: bool = True
) -> list[Path]:
    """apply finding 列挙対象として扱える file だけに正規化する。"""
    targets: list[Path] = []
    for path in sorted({candidate.resolve() for candidate in candidates}):
        if not path.exists() or not path.is_file():
            continue
        try:
            rel_parts = path.relative_to(root.resolve()).parts
        except ValueError:
            continue
        if not rel_parts:
            continue
        if rel_parts[0] in {".git", ".agents", ".cmoc", ".codex", "memo"}:
            continue
        if not include_oracle and rel_parts[0] == "oracle":
            continue
        # `<work-root>/oracle/doc/app_spec/misc_spec.md` は実装ファイル列挙に
        # binary 除外を置かないため、file 種別だけでは対象から落とさない。
        if path.name in {"AGENTS.md", "INDEX.md"}:
            continue
        if is_untracked_git_ignored(root, path):
            continue
        targets.append(path)
    return targets


def enumerate_apply_targets(
    root: Path, scope: str, state: SessionState | None = None
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
        changed = run_git(["diff", "--name-only", base, "HEAD"], root).stdout.splitlines()
        candidates = [root / path for path in changed]
    elif state and (base := previous_apply_join_commit(root, state)):
        changed = run_git(
            ["diff", "--name-only", base, "HEAD"],
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


def previous_apply_join_commit(root: Path, state: SessionState) -> str | None:
    """最後に join した同一 session の apply merge commit を git 履歴から解決する。"""
    snapshot = state.session.last_joined_apply_oracle_snapshot_commit
    if not snapshot:
        return None
    try:
        session_id = apply_branch_session_id(current_branch(root))
    except CmocError:
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
