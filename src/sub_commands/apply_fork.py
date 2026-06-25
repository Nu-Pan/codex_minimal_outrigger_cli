import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable

import typer

from acp.builder.apply.fork.file_finding_enumeration import (
    build_apply_fork_file_finding_enumeration_parameter,
)
from acp.builder.apply.fork.finding_application import (
    build_apply_fork_finding_application_parameter,
)
from acp.builder.apply.fork.refine_finding import (
    build_apply_fork_refine_finding_parameter,
)
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from basic.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from cmoc_runtime import (
    ApplyPart,
    CmocError,
    SessionState,
    create_run_worktree,
    current_branch,
    current_subcommand_logger,
    ensure_cmoc_ignored,
    head_commit,
    is_binary,
    is_git_ignored,
    load_config,
    load_state_for_branch,
    pushd,
    repo_root,
    require_clean_worktree,
    run_git,
    timestamp,
    worktrees_dir,
    write_state,
)
from config.cmoc_config import CmocConfig


CodexExec = Callable[..., object]


def cmoc_apply_fork_impl(
    scope: str,
    codex_exec: CodexExec,
    enumerate_targets: Callable[..., list[Path]],
    enumerate_findings_for_targets: Callable[..., list[dict]],
    related_paths: Callable[[Path, list[dict]], list[Path]],
    ensure_no_forbidden_diff: Callable[[Path], None],
    changed_paths: Callable[[Path], list[Path]],
    generate_commit_message: Callable[[Path, Path, dict, CmocConfig], str],
    normalize_targets: Callable[[Path, set[Path]], list[Path]],
    write_report: Callable[[Path, Path, str, SessionState, list[int], str, CmocConfig], Path],
    write_error_report: Callable[[Path, str, SessionState, list[int], Path], Path],
) -> int:
    """Codex CLI による apply loop を isolated apply worktree 上で実行する。"""
    if scope not in {"rolling", "session", "full"}:
        raise CmocError("scope が不正です。", ["rolling, session, full のいずれかを指定してください。"], scope)
    root = repo_root()
    branch = current_branch(root)
    session_id, path, state = load_state_for_branch(root, branch)
    if not branch.startswith("cmoc/session/"):
        raise CmocError("apply fork は session branch 上で実行してください。", [], branch)
    if state.session.state != "active" or state.apply.state != "ready":
        raise CmocError("apply fork の事前条件を満たしていません。", [], str(path))
    require_clean_worktree(root)
    ensure_cmoc_ignored(root)
    run_id = timestamp()
    apply_branch = f"cmoc/apply/{session_id}/{run_id}"
    oracle_snapshot_commit = head_commit(root)
    apply_worktree = worktrees_dir(root) / session_id / run_id
    create_run_worktree(root, apply_branch, apply_worktree, "HEAD")
    state.apply = ApplyPart(
        state="running",
        apply_branch=apply_branch,
        oracle_snapshot_commit=oracle_snapshot_commit,
        apply_process_id=os.getpid(),
    )
    write_state(path, state)
    config = load_config(root)
    finding_counts: list[int] = []
    result_label = "error"
    report_path: Path | None = None
    try:
        with pushd(apply_worktree):
            findings: list[dict] = []
            dirty_targets = enumerate_targets(apply_worktree, scope, state)
            for _apply_loop in range(config.apply_fork.num_apply_loop):
                if not dirty_targets:
                    result_label = "unconverged" if findings else "converged"
                    break
                findings = enumerate_findings_for_targets(
                    apply_worktree,
                    dirty_targets,
                    config,
                    log_root=root,
                )
                for _ in range(config.apply_fork.num_improve_findings_loop):
                    refined = codex_exec(
                        build_apply_fork_refine_finding_parameter({"findings": findings}),
                        root=root,
                        cwd=apply_worktree,
                        config=config,
                        purpose="apply fork refine findings",
                    ).output_json
                    next_findings = list((refined or {}).get("findings", []))
                    if next_findings == findings:
                        break
                    findings = next_findings
                finding_counts.append(len(findings))
                if not findings:
                    result_label = "converged"
                    break
                next_dirty = set(related_paths(apply_worktree, findings))
                for finding in findings:
                    codex_exec(
                        build_apply_fork_finding_application_parameter(
                            json.dumps(finding, ensure_ascii=False, indent=2)
                        ),
                        root=root,
                        cwd=apply_worktree,
                        config=config,
                        purpose="apply fork finding application",
                    )
                    ensure_no_forbidden_diff(apply_worktree)
                    changed = changed_paths(apply_worktree)
                    next_dirty.update(changed)
                    if changed:
                        commit_message = generate_commit_message(
                            root,
                            apply_worktree,
                            finding,
                            config,
                        )
                        run_git(["add", "."], apply_worktree)
                        run_git(["commit", "-m", commit_message], apply_worktree)
                dirty_targets = normalize_targets(apply_worktree, next_dirty)
            else:
                result_label = "unconverged"
            report_path = write_report(
                root,
                apply_worktree,
                branch,
                state,
                finding_counts,
                result_label,
                config,
            )
        state.apply.state = "completed"
        state.apply.apply_process_id = None
        write_state(path, state)
    except BaseException:
        state.apply.state = "error"
        state.apply.apply_process_id = None
        write_state(path, state)
        if report_path is None:
            write_error_report(root, branch, state, finding_counts, apply_worktree)
        raise
    typer.echo(
        "\n".join(
            [
                "# cmoc apply fork",
                f"- scope: `{scope}`",
                f"- apply_branch: `{apply_branch}`",
                f"- apply_worktree: `{apply_worktree}`",
                f"- oracle_snapshot_commit: `{oracle_snapshot_commit}`",
                f"- findings: `{len(findings)}`",
                f"- result: `{state.apply.state}`",
                f"- result_label: `{result_label}`",
                f"- report: `{report_path}`",
            ]
        )
    )
    return 2 if result_label == "unconverged" else 0


def ensure_no_forbidden_apply_diff(worktree: Path) -> None:
    """apply fork 中に編集禁止対象へ差分が出ていないことを確認する。"""
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
    codex_exec: CodexExec,
) -> str:
    """適用した finding ごとの commit subject を Codex CLI で生成する。"""
    raw_diff = run_git(["diff"], apply_worktree).stdout
    finding_text = json.dumps(finding, ensure_ascii=False, indent=2)
    prompt = [
        StructDoc("Role", "- あなたは git commit message の作成担当です"),
        StructDoc(
            "Goal",
            """
            - 以下の所見と git diff から、git commit subject を 1 行だけ生成すること
            - 出力は commit subject 本文だけにすること
            - 先頭に箇条書き記号、引用符、Markdown、コードブロックを付けないこと
            - 72 文字程度を目安に、人間が変更内容を理解できる具体的な文にすること
            """,
        ),
        StructDoc("Finding", StructCodeBlock("json", finding_text)),
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
    return sanitize_commit_message(result.output_text, finding)


def sanitize_commit_message(message: str, finding: dict) -> str:
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
    title = finding.get("title")
    if isinstance(title, str) and title.strip():
        return f"Apply finding: {title.strip()}"[:120]
    return "Apply cmoc finding"


def enumerate_apply_findings(
    root: Path,
    scope: str,
    config: CmocConfig,
    codex_exec: CodexExec,
    log_root: Path | None = None,
) -> list[dict]:
    """scope から apply finding 列挙対象を決めて finding を収集する。"""
    return enumerate_apply_findings_for_targets(
        root,
        enumerate_apply_targets(root, scope),
        config,
        codex_exec,
        log_root=log_root,
    )


def enumerate_apply_findings_for_targets(
    root: Path,
    targets: list[Path],
    config: CmocConfig,
    codex_exec: CodexExec,
    log_root: Path | None = None,
) -> list[dict]:
    """対象ファイルごとの apply finding 列挙を並列実行する。"""
    logger = current_subcommand_logger()

    def enumerate_one(target: Path) -> list[dict]:
        result = codex_exec(
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
    """worktree 上の変更 path を absolute path として返す。"""
    paths: list[Path] = []
    for line in run_git(["status", "--short"], root).stdout.splitlines():
        path_text = line[3:]
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        paths.append(root / path_text)
    return paths


def related_apply_paths(root: Path, findings: list[dict]) -> list[Path]:
    """finding に含まれる path 情報を apply dirty target 候補へ変換する。"""
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
    """apply finding 列挙対象として扱える通常テキスト file だけに正規化する。"""
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
    elif state and state.session.last_joined_apply_oracle_snapshot_commit:
        changed = run_git(
            [
                "diff",
                "--name-only",
                state.session.last_joined_apply_oracle_snapshot_commit,
                "HEAD",
            ],
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
