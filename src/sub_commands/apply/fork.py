import json
import os
import shutil
from pathlib import Path
from typing import Callable

from acp.builder.apply.fork.file_finding_enumeration import (
    build_apply_fork_file_finding_enumeration_parameter,
)
from acp.builder.apply.fork.finding_application import (
    build_apply_fork_finding_application_parameter,
)
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from basic.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from cmoc_runtime import (
    ApplyPart,
    CliRunResult,
    CmocError,
    SessionState,
    create_run_worktree,
    current_branch,
    current_subcommand_logger,
    ensure_cmoc_ignored_in_exclude,
    head_commit,
    is_git_ignored,
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
from sub_commands.apply._runtime import (
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
        console_output=False,
    )


def _cmoc_apply_fork_body(
    scope: str,
    codex_exec: CodexExec,
) -> CliRunResult:
    """Codex CLI による apply loop を isolated apply worktree 上で実行する。"""
    if scope not in {"rolling", "session", "full"}:
        raise CmocError("scope が不正です。", ["rolling, session, full のいずれかを指定してください。"], scope)
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
                run_finding_application_with_forbidden_rollback(
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
                        root,
                        apply_worktree,
                        {"findings": findings},
                        config,
                        codex_exec,
                    )
                    run_git(["add", "."], apply_worktree)
                    run_git(["commit", "-m", commit_message], apply_worktree)
            else:
                pending_targets = dedupe_apply_targets(pending_targets)
                result_label = "unconverged" if pending_targets else "converged"
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
        state.apply.state = "completed"
        write_state(path, state)
    except BaseException as exc:
        delete_apply_process_id(root, session_id)
        state.apply.state = "error"
        write_state(path, state)
        if report_path is None:
            report_path = write_apply_fork_error_report(
                root, branch, state, finding_counts, apply_worktree, config, codex_exec
            )
        setattr(exc, "cmoc_stdout", str(report_path.resolve()))
        setattr(exc, "cmoc_error_to_stderr", True)
        raise
    # <work-root>/oracle/doc/app_spec/sub_command/apply_fork.md は stdout を
    # 作成した report の full path だけに限定している。
    return CliRunResult(
        returncode=2 if result_label == "unconverged" else 0,
        stdout=str(report_path.resolve()),
    )


def forbidden_apply_diff(worktree: Path) -> str:
    """apply fork 中の編集禁止対象差分を porcelain status で返す。"""
    return run_git(
        ["status", "--short", "--", "oracle", ".agents", "memo"],
        worktree,
    ).stdout.strip()


def rollback_forbidden_apply_diff(worktree: Path) -> None:
    """編集禁止対象に発生した未コミット差分だけを HEAD へ戻す。"""
    tracked_paths: list[str] = []
    untracked_paths: list[str] = []
    for line in forbidden_apply_diff(worktree).splitlines():
        status = line[:2]
        path_text = line[3:]
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        if path_text.startswith("agents/") and (worktree / f".{path_text}").exists():
            path_text = f".{path_text}"
        if status == "??":
            untracked_paths.append(path_text)
        else:
            tracked_paths.append(path_text)
    if tracked_paths:
        run_git(
            [
                "restore",
                "--staged",
                "--worktree",
                "--",
                *[f":(literal){path}" for path in tracked_paths],
            ],
            worktree,
        )
    for path_text in untracked_paths:
        path = worktree / path_text
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def run_finding_application_with_forbidden_rollback(
    root: Path,
    apply_worktree: Path,
    findings: list[dict],
    config: CmocConfig,
    codex_exec: CodexExec,
) -> None:
    """所見リスト適用を行い、編集禁止対象差分が出た場合は戻して 1 回再実行する。"""
    parameter = build_apply_fork_finding_application_parameter(findings)
    for attempt in range(2):
        codex_exec(
            parameter,
            root=root,
            cwd=apply_worktree,
            config=config,
            purpose="apply fork finding application",
        )
        forbidden_diff = forbidden_apply_diff(apply_worktree)
        if not forbidden_diff:
            return
        rollback_forbidden_apply_diff(apply_worktree)
        if attempt == 0:
            continue
        raise CmocError(
            "apply fork 中に編集禁止対象へ差分が発生しました。",
            ["該当差分をロールバックしました。apply を abandon してから再実行してください。"],
            forbidden_diff,
        )


def generate_apply_commit_message(
    root: Path,
    apply_worktree: Path,
    applied_findings: dict,
    config: CmocConfig,
    codex_exec: CodexExec,
) -> str:
    """所見リスト適用後の差分に対する commit subject を Codex CLI で生成する。"""
    raw_diff = run_git(["diff"], apply_worktree).stdout
    findings_text = json.dumps(applied_findings, ensure_ascii=False, indent=2)
    prompt = [
        StructDoc("Role", "- あなたは git commit message の作成担当です"),
        StructDoc(
            "Goal",
            """
            - 以下の所見リストと git diff から、git commit subject を 1 行だけ生成すること
            - 出力は commit subject 本文だけにすること
            - 先頭に箇条書き記号、引用符、Markdown、コードブロックを付けないこと
            - 72 文字程度を目安に、人間が変更内容を理解できる具体的な文にすること
            """,
        ),
        StructDoc("Applied findings", StructCodeBlock("json", findings_text)),
        StructDoc("Git diff", StructCodeBlock("diff", raw_diff)),
    ]
    result = codex_exec(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.READONLY,
            render_as_markdown(prompt),
            None,
        ),
        root=root,
        cwd=apply_worktree,
        config=config,
        purpose="apply fork commit message",
    )
    return sanitize_commit_message(result.output_text, applied_findings)


def sanitize_commit_message(message: str, applied_findings: dict) -> str:
    """Codex 出力を commit subject として使える 1 行へ丸める。"""
    for line in message.splitlines():
        subject = line.strip().strip("`").strip("\"'")
        if not subject:
            continue
        for prefix in ("- ", "* ", "commit message:", "Commit message:"):
            if subject.startswith(prefix):
                subject = subject.removeprefix(prefix).strip()
        if subject:
            return subject[:120]
    findings = applied_findings.get("findings")
    if isinstance(findings, list):
        for finding in findings:
            if isinstance(finding, dict):
                title = finding.get("title")
                if isinstance(title, str) and title.strip():
                    return f"Apply findings: {title.strip()}"[:120]
    return "Apply cmoc finding"


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
        build_apply_fork_file_finding_enumeration_parameter(target),
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


def changed_worktree_paths(root: Path) -> list[Path]:
    """worktree 上の変更 path を absolute path として返す。"""
    paths: list[Path] = []
    # <work-root>/oracle/doc/app_spec/sub_command/apply_fork.md requires changed
    # realization files to be requeued; default status can collapse untracked
    # directories into one non-file path.
    for line in run_git(["status", "--short", "-uall"], root).stdout.splitlines():
        path_text = line[3:]
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        paths.append(root / path_text)
    return paths


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
        if ".git" in rel_parts or ".agents" in rel_parts or rel_parts[0] == "memo":
            continue
        if not include_oracle and rel_parts[0] == "oracle":
            continue
        # `<work-root>/oracle/doc/app_spec/misc_spec.md` は実装ファイル列挙に
        # binary 除外を置かないため、file 種別だけでは対象から落とさない。
        if path.name == "INDEX.md":
            continue
        if is_git_ignored(root, path):
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
    """最後に join した apply の merge commit を永続 state ではなく git 履歴から解決する。"""
    snapshot = state.session.last_joined_apply_oracle_snapshot_commit
    if not snapshot:
        return None
    merges = run_git(
        ["rev-list", "--first-parent", "--merges", "--reverse", f"{snapshot}..HEAD"],
        root,
    ).stdout.splitlines()
    joined: str | None = None
    for merge_commit in merges:
        parents = run_git(["show", "-s", "--format=%P", merge_commit], root).stdout.split()
        if any(
            run_git(
                ["merge-base", "--is-ancestor", snapshot, parent],
                root,
                check=False,
            ).returncode
            == 0
            for parent in parents[1:]
        ):
            joined = merge_commit
    return joined
