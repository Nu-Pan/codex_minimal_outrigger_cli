import json
import threading
from concurrent.futures import ThreadPoolExecutor
from contextvars import ContextVar
from pathlib import Path

import typer

from acp.builder.apply.fork.file_finding_enumeration import (
    build_apply_fork_file_finding_enumeration_parameter,
)
from acp.builder.apply.fork.change_summary import (
    build_apply_fork_change_summary_parameter,
)
from cmoc_runtime import (
    CmocError,
    SessionState,
    SubcommandLogger,
    console_timestamp,
    current_subcommand_logger,
    current_branch,
    ensure_cmoc_ignored,
    is_binary,
    is_git_ignored,
    load_config,
    load_state_for_branch,
    logs_dir,
    render_error,
    reports_dir,
    repo_root,
    require_clean_worktree,
    reset_current_subcommand_logger,
    format_duration,
    run_codex_exec as runtime_run_codex_exec,
    run_codex_tui as runtime_run_codex_tui,
    run_git,
    set_current_subcommand_logger,
    timestamp,
    write_state,
    work_root,
)
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from basic.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from config.cmoc_config import CmocConfig
from sub_commands.init import cmoc_init_impl
from sub_commands.indexing import (
    build_index_entry_impl,
    commit_index_updates_impl,
    cmoc_indexing_impl,
    index_target_hash,
    indexable_children,
    parse_index_entries,
    render_index_entry,
    target_content_for_indexing,
    update_indexes_impl,
)
from sub_commands.apply import (
    cmoc_apply_abandon_impl,
    cmoc_apply_fork_impl,
    cmoc_apply_join_impl,
    collect_apply_join_unexpected_changes as collect_apply_join_unexpected_changes_impl,
    is_expected_apply_change as is_expected_apply_change_impl,
    is_expected_session_change as is_expected_session_change_impl,
    resolve_index_conflicts as resolve_index_conflicts_impl,
    restore_path_from_commit as restore_path_from_commit_impl,
    revert_unexpected_changes as revert_unexpected_changes_impl,
    worktree_for_branch as worktree_for_branch_impl,
    worktree_for_branch_optional as worktree_for_branch_optional_impl,
)
from sub_commands.session import (
    cmoc_session_abandon_impl,
    cmoc_session_fork_impl,
    cmoc_session_join_impl,
)
from sub_commands.review import (
    apply_finding_merge_operations as apply_finding_merge_operations_impl,
    cmoc_review_oracle_impl,
    commit_review_index_changes as commit_review_index_changes_impl,
    enumerate_review_all_oracle_files as enumerate_review_all_oracle_files_impl,
    enumerate_review_oracle_targets as enumerate_review_oracle_targets_impl,
    merge_review_branch as merge_review_branch_impl,
    path_display as path_display_impl,
    render_finding_section as render_finding_section_impl,
    render_review_oracle_report as render_review_oracle_report_impl,
    resolve_review_index_conflicts as resolve_review_index_conflicts_impl,
    run_review_oracle_loop as run_review_oracle_loop_impl,
)
from sub_commands.tui import cmoc_tui_impl


app = typer.Typer(no_args_is_help=True)
session_app = typer.Typer(no_args_is_help=True)
apply_app = typer.Typer(no_args_is_help=True)
review_app = typer.Typer(no_args_is_help=True)
app.add_typer(session_app, name="session")
app.add_typer(apply_app, name="apply")
app.add_typer(review_app, name="review")
_INDEXING_LOCK = threading.Lock()
_INDEXING_ACTIVE: ContextVar[bool] = ContextVar("INDEXING_ACTIVE", default=False)


def run_codex_exec(parameter: AgentCallParameter, **kwargs):
    purpose = str(kwargs.get("purpose", "codex exec"))
    if not _INDEXING_ACTIVE.get() and not should_skip_indexing_before_codex(purpose):
        root = kwargs.get("root") or repo_root()
        with _INDEXING_LOCK:
            token = _INDEXING_ACTIVE.set(True)
            try:
                commit_index_updates(root, update_indexes(root))
            finally:
                _INDEXING_ACTIVE.reset(token)
    return runtime_run_codex_exec(parameter, **kwargs)


def run_codex_tui(parameter: AgentCallParameter, **kwargs):
    return runtime_run_codex_tui(parameter, **kwargs)


def should_skip_indexing_before_codex(purpose: str) -> bool:
    return purpose.startswith("indexing index entry") or "conflict resolution" in purpose


def _run(handler) -> None:
    logger = None
    logger_token = None
    try:
        current_root = work_root()
        require_current_directory_is_work_root(current_root)
        root = command_log_root(repo_root(), current_root)
        logger = SubcommandLogger(root, handler.__name__)
        logger_token = set_current_subcommand_logger(logger)
        logger.event("command_invoked", argv=[])
        typer.echo(f"# {console_timestamp()} (1/3) start {handler.__name__}")
        typer.echo(f"- sub_command_log: `{logger.path}`")
        logger.event("step_started", step="execute")
        typer.echo(f"# {console_timestamp()} (2/3) execute {handler.__name__}")
        handler_result = handler()
        returncode = handler_result if isinstance(handler_result, int) else 0
        if logger:
            logger.event(
                "command_finished",
                returncode=returncode,
                elapsed_sec=logger.elapsed(),
                quota_wait_sec=logger.quota_wait_sec,
            )
            _emit_completion_summary(logger, handler.__name__, returncode)
        if returncode:
            raise typer.Exit(returncode)
    except typer.Exit:
        raise
    except BaseException as exc:
        if logger:
            logger.event(
                "command_finished",
                returncode=1,
                elapsed_sec=logger.elapsed(),
                quota_wait_sec=logger.quota_wait_sec,
                error=str(exc),
            )
            _emit_completion_summary(logger, handler.__name__, 1)
        typer.echo(render_error(exc))
        raise typer.Exit(1) from exc
    finally:
        if logger_token is not None:
            reset_current_subcommand_logger(logger_token)


def _emit_completion_summary(
    logger: SubcommandLogger, handler_name: str, returncode: int
) -> None:
    elapsed = logger.elapsed()
    typer.echo(f"# {console_timestamp()} (3/3) completed {handler_name}")
    typer.echo(f"- sub_command_log: `{logger.path}`")
    typer.echo(f"- step_execute_elapsed: `{format_duration(elapsed)}`")
    typer.echo(f"- elapsed: `{format_duration(elapsed)}`")
    typer.echo(f"- quota_wait: `{format_duration(logger.quota_wait_sec)}`")
    typer.echo(f"- returncode: `{returncode}`")


def require_current_directory_is_work_root(root: Path) -> None:
    if Path.cwd().resolve() == root.resolve():
        return
    raise CmocError(
        "cmoc は work root で実行してください。",
        ["git repository の root directory へ移動してから再実行してください。"],
        f"cwd: {Path.cwd().resolve()}\nwork_root: {root.resolve()}",
    )


def command_log_root(root: Path, current_root: Path | None = None) -> Path:
    branch = current_branch(current_root or root)
    if branch.startswith("cmoc/apply/"):
        parts = branch.split("/")
        if len(parts) >= 4:
            return worktree_for_branch(root, f"cmoc/session/{parts[2]}")
    return root


@app.command()
def init() -> None:
    def handler() -> None:
        cmoc_init_impl()

    _run(handler)


@app.command()
def tui() -> None:
    def handler() -> None:
        root = repo_root()
        current_root = work_root()
        cmoc_tui_impl(
            run_codex_exec,
            run_codex_tui,
            root=root,
            work_root=current_root,
            config=load_config(root),
        )

    _run(handler)


@session_app.command("fork")
def session_fork() -> None:
    def handler() -> None:
        cmoc_session_fork_impl()

    _run(handler)


@session_app.command("join")
def session_join() -> None:
    def handler() -> None:
        cmoc_session_join_impl(run_codex_exec, run_git)

    _run(handler)


@session_app.command("abandon")
def session_abandon() -> None:
    def handler() -> None:
        cmoc_session_abandon_impl()

    _run(handler)


@apply_app.command("fork")
def apply_fork(scope: str = typer.Option("rolling", "--scope", "-s")) -> None:
    def handler() -> None:
        return cmoc_apply_fork_impl(
            scope,
            run_codex_exec,
            enumerate_apply_targets,
            enumerate_apply_findings_for_targets,
            related_apply_paths,
            ensure_no_forbidden_apply_diff,
            changed_worktree_paths,
            generate_apply_commit_message,
            normalize_apply_targets,
            write_apply_fork_report,
            write_apply_fork_error_report,
        )

    _run(handler)


def write_apply_fork_report(
    root: Path,
    apply_worktree: Path,
    session_branch: str,
    state: SessionState,
    finding_counts: list[int],
    result_label: str,
    config: CmocConfig,
) -> Path:
    apply_branch = state.apply.apply_branch or ""
    fork_commit = state.apply.oracle_snapshot_commit or ""
    raw_diff = run_git(["diff", f"{fork_commit}..HEAD"], apply_worktree).stdout if fork_commit else run_git(["diff", "HEAD"], apply_worktree).stdout
    if raw_diff.strip():
        summary = run_codex_exec(
            build_apply_fork_change_summary_parameter(raw_diff),
            root=root,
            cwd=apply_worktree,
            config=config,
            purpose="apply fork change summary",
        ).output_json
        changes = list((summary or {}).get("changes", []))
        if not changes:
            changes = [
                {
                    "category": "変更要約なし",
                    "summary": "変更差分はありますが、構造化された変更要約は空でした。",
                    "changed_paths": [],
                }
            ]
    else:
        changes = [
            {
                "category": "変更なし",
                "summary": "apply fork による実装差分はありません。",
                "changed_paths": [],
            }
        ]
    report_dir = reports_dir(root, "apply/fork")
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"{timestamp()}.md"
    path.write_text(
        render_apply_fork_report(
            root,
            session_branch,
            state,
            apply_branch,
            fork_commit,
            apply_worktree,
            result_label,
            finding_counts,
            changes,
        )
    )
    return path


def write_apply_fork_error_report(
    root: Path,
    session_branch: str,
    state: SessionState,
    finding_counts: list[int],
    apply_worktree: Path,
) -> Path:
    report_dir = reports_dir(root, "apply/fork")
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"{timestamp()}.md"
    path.write_text(
        render_apply_fork_report(
            root,
            session_branch,
            state,
            state.apply.apply_branch or "",
            state.apply.oracle_snapshot_commit or "",
            apply_worktree,
            "error",
            finding_counts,
            [{"category": "エラー", "summary": "apply fork が途中で失敗しました。", "changed_paths": []}],
        )
    )
    return path


def render_apply_fork_report(
    root: Path,
    session_branch: str,
    state: SessionState,
    apply_branch: str,
    apply_fork_commit: str,
    apply_worktree: Path,
    result_label: str,
    finding_counts: list[int],
    changes: list[dict],
) -> str:
    result_text = {
        "converged": "収束: 検出された所見リストが空によりループを終了しました。",
        "unconverged": "未収束: まだ所見が残っている可能性があります。",
        "error": "エラー: 途中でエラーが起きてループを正常に終了出来ませんでした。",
    }.get(result_label, result_label)
    count_lines = "\n".join(f"- loop {idx}: {count}" for idx, count in enumerate(finding_counts, 1)) or "- loop 1: 0"
    change_lines = "\n".join(
        [
            f"- {change.get('category')}: {change.get('summary')} ({', '.join(change.get('changed_paths', [])) or 'no paths'})"
            for change in changes
        ]
    )
    return "\n".join(
        [
            "---",
            f"cmoc_session_branch: {session_branch}",
            f"cmoc_session_fork_commit: {state.session.session_start_commit}",
            f"cmoc_apply_branch: {apply_branch}",
            f"cmoc_apply_fork_commit: {apply_fork_commit}",
            f"cmoc_apply_worktree: {apply_worktree}",
            f"result: {result_label}",
            "---",
            "# cmoc apply fork report",
            "## Result",
            result_text,
            "## Finding Count",
            count_lines,
            "## Change Summary",
            change_lines,
            "",
        ]
    )


def ensure_no_forbidden_apply_diff(worktree: Path) -> None:
    forbidden_diff = run_git(
        ["status", "--short", "--", "oracle", ".agents", "memo", ".gitignore"],
        worktree,
    ).stdout.strip()
    if forbidden_diff:
        raise CmocError(
            "apply fork 中に編集禁止対象へ差分が発生しました。",
            ["該当差分を確認し、apply を abandon してから再実行してください。"],
            forbidden_diff,
        )


def generate_apply_commit_message(
    root: Path,
    apply_worktree: Path,
    finding: dict,
    config: CmocConfig,
) -> str:
    raw_diff = run_git(["diff"], apply_worktree).stdout
    finding_text = json.dumps(finding, ensure_ascii=False, indent=2)
    prompt = [
        StructDoc(
            "Role",
            "- あなたは git commit message の作成担当です",
        ),
        StructDoc(
            "Goal",
            """
            - 以下の所見と git diff から、git commit subject を 1 行だけ生成すること
            - 出力は commit subject 本文だけにすること
            - 先頭に箇条書き記号、引用符、Markdown、コードブロックを付けないこと
            - 72 文字程度を目安に、人間が変更内容を理解できる具体的な文にすること
            """,
        ),
        StructDoc(
            "Finding",
            StructCodeBlock("json", finding_text),
        ),
        StructDoc(
            "Git diff",
            StructCodeBlock("diff", raw_diff),
        ),
    ]
    result = run_codex_exec(
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
    return sanitize_commit_message(result.output_text, finding)


def sanitize_commit_message(message: str, finding: dict) -> str:
    for line in message.splitlines():
        subject = line.strip().strip("`").strip("\"'")
        if not subject:
            continue
        for prefix in ("- ", "* ", "commit message:", "Commit message:"):
            if subject.startswith(prefix):
                subject = subject.removeprefix(prefix).strip()
        if subject:
            return subject[:120]
    title = finding.get("title")
    if isinstance(title, str) and title.strip():
        return f"Apply finding: {title.strip()}"[:120]
    return "Apply cmoc finding"


def enumerate_apply_findings(root: Path, scope: str, config: CmocConfig, log_root: Path | None = None) -> list[dict]:
    return enumerate_apply_findings_for_targets(
        root,
        enumerate_apply_targets(root, scope),
        config,
        log_root=log_root,
    )


def enumerate_apply_findings_for_targets(
    root: Path,
    targets: list[Path],
    config: CmocConfig,
    log_root: Path | None = None,
) -> list[dict]:
    logger = current_subcommand_logger()

    def enumerate_one(target: Path) -> list[dict]:
        result = run_codex_exec(
            build_apply_fork_file_finding_enumeration_parameter(target),
            root=log_root or root,
            cwd=root,
            config=config,
            purpose=f"apply fork enumerate findings for {target}",
            subcommand_logger=logger,
        )
        return list((result.output_json or {}).get("findings", []))

    findings: list[dict] = []
    with ThreadPoolExecutor(max_workers=config.num_parallel) as executor:
        for target_findings in executor.map(enumerate_one, targets):
            findings.extend(target_findings)
    return findings


def changed_worktree_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for line in run_git(["status", "--short"], root).stdout.splitlines():
        path_text = line[3:]
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        paths.append(root / path_text)
    return paths


def related_apply_paths(root: Path, findings: list[dict]) -> list[Path]:
    paths: list[Path] = []
    for finding in findings:
        for key in ("oracle_path", "realization_path", "path"):
            value = finding.get(key)
            if isinstance(value, str) and value:
                paths.append(Path(value) if Path(value).is_absolute() else root / value)
        for evidence in finding.get("evidences", []):
            if isinstance(evidence, dict) and isinstance(evidence.get("path"), str):
                value = evidence["path"]
                paths.append(Path(value) if Path(value).is_absolute() else root / value)
        for value in finding.get("changed_paths", []):
            if isinstance(value, str):
                paths.append(Path(value) if Path(value).is_absolute() else root / value)
    return paths


def normalize_apply_targets(root: Path, candidates: set[Path]) -> list[Path]:
    targets: list[Path] = []
    for path in sorted({candidate.resolve() for candidate in candidates}):
        if not path.exists() or not path.is_file():
            continue
        try:
            rel_parts = path.relative_to(root.resolve()).parts
        except ValueError:
            continue
        if ".git" in rel_parts or ".agents" in rel_parts or "memo" in rel_parts:
            continue
        if path.name == "INDEX.md" or path.name.startswith(".") or is_binary(path):
            continue
        if is_git_ignored(root, path):
            continue
        targets.append(path)
    return targets


def enumerate_apply_targets(root: Path, scope: str, state: SessionState | None = None) -> list[Path]:
    if scope == "full":
        candidates = list(root.rglob("*"))
    elif scope == "session":
        base = state.session.session_start_commit if state and state.session.session_start_commit else "HEAD"
        changed = run_git(["diff", "--name-only", base, "HEAD"], root).stdout.splitlines()
        candidates = [root / path for path in changed]
    elif state and state.session.last_joined_apply_commit:
        changed = run_git(
            ["diff", "--name-only", state.session.last_joined_apply_commit, "HEAD"],
            root,
        ).stdout.splitlines()
        candidates = [root / path for path in changed]
    elif state and state.session.session_start_commit:
        changed = run_git(["diff", "--name-only", state.session.session_start_commit, "HEAD"], root).stdout.splitlines()
        candidates = [root / path for path in changed]
    else:
        candidates = list((root / "oracle").rglob("*")) + [
            path for path in root.rglob("*") if path.is_file() and path.suffix == ".py"
        ]
    return normalize_apply_targets(root, set(candidates))


@apply_app.command("join")
def apply_join(force_resolve: bool = typer.Option(False, "--force-resolve")) -> None:
    def handler() -> None:
        cmoc_apply_join_impl(force_resolve)

    _run(handler)


def collect_apply_join_unexpected_changes(root: Path, state: SessionState, apply_branch: str, session_branch: str) -> dict[str, list[str]]:
    return collect_apply_join_unexpected_changes_impl(root, state, apply_branch, session_branch)


def is_expected_apply_change(root: Path, path: str) -> bool:
    return is_expected_apply_change_impl(root, path)


def is_expected_session_change(path: str) -> bool:
    return is_expected_session_change_impl(path)


def revert_unexpected_changes(root: Path, unexpected: dict[str, list[str]], state: SessionState) -> None:
    revert_unexpected_changes_impl(root, unexpected, state)


def restore_path_from_commit(root: Path, commit: str, path: str) -> None:
    restore_path_from_commit_impl(root, commit, path)


def resolve_index_conflicts(root: Path) -> bool:
    return resolve_index_conflicts_impl(root)


@apply_app.command("abandon")
def apply_abandon() -> None:
    def handler() -> None:
        cmoc_apply_abandon_impl()

    _run(handler)


def worktree_for_branch(root: Path, branch: str) -> Path:
    return worktree_for_branch_impl(root, branch)


def worktree_for_branch_optional(root: Path, branch: str) -> Path | None:
    return worktree_for_branch_optional_impl(root, branch)


@review_app.command("oracle")
def review_oracle(scope: str = typer.Option("session", "--scope", "-s")) -> None:
    def handler() -> None:
        cmoc_review_oracle_impl(
            scope,
            run_codex_exec,
            enumerate_review_all_oracle_files,
            enumerate_review_oracle_targets,
            run_review_oracle_loop,
            commit_review_index_changes,
            merge_review_branch,
            render_review_oracle_report,
        )

    _run(handler)


def commit_review_index_changes(review_worktree: Path) -> bool:
    return commit_review_index_changes_impl(review_worktree)


def merge_review_branch(root: Path, review_branch: str) -> str:
    return merge_review_branch_impl(root, review_branch)


def resolve_review_index_conflicts(root: Path) -> bool:
    return resolve_review_index_conflicts_impl(root)


def enumerate_review_oracle_targets(root: Path, scope: str, state: SessionState) -> list[Path]:
    return enumerate_review_oracle_targets_impl(root, scope, state)


def enumerate_review_all_oracle_files(root: Path) -> list[Path]:
    return enumerate_review_all_oracle_files_impl(root)


def run_review_oracle_loop(
    log_root: Path,
    worktree: Path,
    oracle_files: list[Path],
    config: CmocConfig,
    codex_exec=None,
) -> list[dict]:
    return run_review_oracle_loop_impl(log_root, worktree, oracle_files, config, codex_exec or run_codex_exec)


def apply_finding_merge_operations(findings: list[dict], operations: list[dict], next_id: int) -> list[dict]:
    return apply_finding_merge_operations_impl(findings, operations, next_id)


def render_review_oracle_report(
    root: Path,
    scope: str,
    session_branch: str,
    session_id: str,
    state: SessionState,
    oracle_count_total: int,
    oracle_files: list[Path],
    findings: list[dict],
    review_branch: str | None,
    review_fork_commit: str | None,
    review_join_commit: str | None,
) -> str:
    return render_review_oracle_report_impl(
        root,
        scope,
        session_branch,
        session_id,
        state,
        oracle_count_total,
        oracle_files,
        findings,
        review_branch,
        review_fork_commit,
        review_join_commit,
    )


def render_finding_section(findings: list[dict]) -> str:
    return render_finding_section_impl(findings)


def path_display(root: Path, path: Path) -> str:
    return path_display_impl(root, path)


@app.command()
def indexing() -> None:
    def handler() -> None:
        cmoc_indexing_impl(update_indexes, commit_index_updates)

    _run(handler)


def commit_index_updates(root: Path, updated: list[Path]) -> None:
    commit_index_updates_impl(root, updated)


def update_indexes(root: Path) -> list[Path]:
    return update_indexes_impl(root, build_index_entry)


def build_index_entry(root: Path, path: Path, digest: str | None = None) -> str:
    return build_index_entry_impl(root, path, run_codex_exec, digest=digest)


def main() -> None:
    app(prog_name="cmoc")


if __name__ == "__main__":
    main()
