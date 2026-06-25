from pathlib import Path
from tempfile import NamedTemporaryFile

import typer

from cmoc_runtime import ensure_cmoc_ignored, repo_root, run_git, sync_config


def cmoc_init_impl() -> None:
    """repo root を cmoc が扱える初期状態へ同期する。"""
    root = repo_root()
    gitignore = root / ".gitignore"
    head_gitignore = _git_show(root, "HEAD:.gitignore")
    index_gitignore = _git_show(root, ":0:.gitignore")
    worktree_gitignore = gitignore.read_text() if gitignore.exists() else None
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
        sync_config(root)
        run_git(["add", ".gitignore"], root)
        diff = run_git(
            ["diff", "--cached", "--quiet", "--", ".gitignore", ".cmoc"],
            root,
            check=False,
        )
        if diff.returncode == 1:
            run_git(["commit", "-m", "cmoc init"], root)
    finally:
        _restore_staged_patch(root, staged_patch)
        _restore_gitignore_state(
            root, gitignore, head_gitignore, index_gitignore, worktree_gitignore
        )
    typer.echo(render_cmoc_init_result(root))


def _git_show(root: Path, spec: str) -> str | None:
    result = run_git(["show", spec], root, check=False)
    return result.stdout if result.returncode == 0 else None


def _write_or_remove(path: Path, content: str | None) -> None:
    if content is None:
        path.unlink(missing_ok=True)
        return
    path.write_text(content)


def _with_cmoc_ignore(content: str) -> str:
    lines = content.splitlines()
    if "/.cmoc/" in lines:
        return content
    separator = "\n" if lines and lines[-1] != "" else ""
    newline = "" if content == "" or content.endswith("\n") else "\n"
    return f"{content}{newline}{separator}/.cmoc/\n"


def _restore_gitignore_state(
    root: Path,
    path: Path,
    head_content: str | None,
    index_content: str | None,
    worktree_content: str | None,
) -> None:
    current_head = _git_show(root, "HEAD:.gitignore")
    if index_content is None and head_content is not None:
        run_git(["rm", "--cached", "--ignore-unmatch", ".gitignore"], root)
    elif index_content is not None:
        restored_index = _with_cmoc_ignore(index_content)
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
    if worktree_content is not None:
        path.write_text(_with_cmoc_ignore(worktree_content))


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
    return f"# cmoc init\n- repo_root: `{root}`\n- ignored: `{root / '.cmoc'}`"
