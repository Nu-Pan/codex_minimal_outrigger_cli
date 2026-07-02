from pathlib import Path
from tempfile import NamedTemporaryFile

import typer

from cmoc_runtime import (
    ensure_cmoc_ignored,
    ensure_cmoc_ignored_in_exclude,
    repo_root,
    run_cli_subcommand,
    run_git,
    sync_config,
    with_cmoc_ignore_pattern,
    work_root,
)

# ログ作成前の .cmoc ignore 保証による副作用を、利用者の .gitignore 復元ロジックから見分ける。
_PRE_LOG_GITIGNORE_STATES: dict[Path, tuple[bool, str | None]] = {}


def cmoc_init_impl() -> None:
    """CLI runtime を通して init を実行する。"""
    run_cli_subcommand(
        _cmoc_init_body,
        pre_log_check=ensure_cmoc_ignored_before_init_log,
        command_name="init",
        command_argv=["cmoc", "init"],
        use_work_root_runtime=True,
    )


def _cmoc_init_body() -> None:
    """work root を cmoc が扱える初期状態へ同期する。"""
    root = work_root()
    config_root = repo_root()
    gitignore = root / ".gitignore"
    pre_log_gitignore = _PRE_LOG_GITIGNORE_STATES.pop(root.resolve(), None)
    head_gitignore = _git_show(root, "HEAD:.gitignore")
    index_gitignore = _git_show(root, ":0:.gitignore")
    if pre_log_gitignore is None:
        had_worktree_gitignore = gitignore.exists()
        worktree_gitignore = gitignore.read_text() if had_worktree_gitignore else None
    else:
        had_worktree_gitignore, worktree_gitignore = pre_log_gitignore
    staged_patch = run_git(
        [
            "diff",
            "--cached",
            "--binary",
            "--",
            ".",
            ":(exclude).gitignore",
            ":(exclude).cmoc",
        ],
        root,
    ).stdout
    _write_or_remove(gitignore, head_gitignore)
    if staged_patch:
        # init commit に実行前から staged だった利用者差分を混ぜない。
        run_git(["restore", "--staged", "--", "."], root)
    try:
        ensure_cmoc_ignored(root)
        _ensure_agents_tracked(root)
        if config_root.resolve() != root.resolve():
            ensure_cmoc_ignored_in_exclude(config_root)
        sync_config(config_root)
        run_git(["add", ".gitignore"], root)
        diff = run_git(
            ["diff", "--cached", "--quiet", "--", ".gitignore", ".cmoc", ".agents"],
            root,
            check=False,
        )
        if diff.returncode == 1:
            run_git(["commit", "-m", "cmoc init"], root)
    finally:
        _restore_staged_patch(root, staged_patch)
        _restore_gitignore_state(
            root,
            gitignore,
            head_gitignore,
            index_gitignore,
            had_worktree_gitignore,
            worktree_gitignore,
        )
    typer.echo(render_cmoc_init_result(root))

def ensure_cmoc_ignored_before_init_log(root: Path) -> None:
    gitignore = root / ".gitignore"
    state_key = root.resolve()
    _PRE_LOG_GITIGNORE_STATES[state_key] = (
        gitignore.exists(),
        gitignore.read_text() if gitignore.exists() else None,
    )
    try:
        ensure_cmoc_ignored(root)
        log_root = repo_root()
        if log_root.resolve() != root.resolve():
            # <work-root>/oracle/doc/app_spec/misc_spec.md requires
            # <repo-root>/.cmoc to be ignored before init writes logs there.
            ensure_cmoc_ignored_in_exclude(log_root)
    except BaseException:
        _PRE_LOG_GITIGNORE_STATES.pop(state_key, None)
        raise


def _ensure_agents_tracked(root: Path) -> None:
    # <work-root>/oracle/doc/app_spec/sub_command/init.md requires init to
    # create a tracked placeholder when .agents has no tracked files.
    agents = root / ".agents"
    agents.mkdir(exist_ok=True)
    if run_git(["ls-files", "--", ".agents"], root).stdout.strip():
        return
    gitkeep = agents / ".gitkeep"
    gitkeep.touch(exist_ok=True)
    run_git(["add", "-f", ".agents/.gitkeep"], root)


def _git_show(root: Path, spec: str) -> str | None:
    result = run_git(["show", spec], root, check=False)
    return result.stdout if result.returncode == 0 else None


def _write_or_remove(path: Path, content: str | None) -> None:
    if content is None:
        path.unlink(missing_ok=True)
        return
    path.write_text(content)


def _restore_gitignore_state(
    root: Path,
    path: Path,
    head_content: str | None,
    index_content: str | None,
    had_worktree_content: bool,
    worktree_content: str | None,
) -> None:
    current_head = _git_show(root, "HEAD:.gitignore")
    if index_content is None and head_content is not None:
        run_git(["rm", "--cached", "--ignore-unmatch", ".gitignore"], root)
    elif index_content is not None:
        restored_index = with_cmoc_ignore_pattern(index_content)
        if restored_index != current_head:
            with NamedTemporaryFile("w", delete=False) as f:
                f.write(restored_index)
                temp_path = Path(f.name)
            try:
                blob = run_git(
                    ["hash-object", "-w", str(temp_path)], root
                ).stdout.strip()
                run_git(
                    [
                        "update-index",
                        "--add",
                        "--cacheinfo",
                        "100644",
                        blob,
                        ".gitignore",
                    ],
                    root,
                )
            finally:
                temp_path.unlink(missing_ok=True)
    if had_worktree_content and worktree_content is not None:
        path.write_text(with_cmoc_ignore_pattern(worktree_content))
    elif head_content is not None or index_content is not None:
        restored_content = current_head or index_content or head_content or ""
        path.write_text(with_cmoc_ignore_pattern(restored_content))


def _restore_staged_patch(root: Path, patch: str) -> None:
    if not patch:
        return
    with NamedTemporaryFile("w", delete=False) as f:
        f.write(patch)
        patch_path = Path(f.name)
    try:
        run_git(["apply", "--cached", str(patch_path)], root)
    finally:
        patch_path.unlink(missing_ok=True)


def render_cmoc_init_result(root: Path) -> str:
    """`cmoc init` の成功結果を stdout 用 Markdown にする。"""
    return f"# cmoc init\n- work_root: `{root}`\n- ignored: `{root / '.cmoc'}`"
