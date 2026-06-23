from pathlib import Path

import typer

from cmoc_runtime import ensure_cmoc_ignored, repo_root, run_git, sync_config


def cmoc_init_impl() -> None:
    """work root を cmoc が扱える初期状態へ同期する。"""
    root = repo_root()
    ensure_cmoc_ignored(root)
    sync_config(root)
    if run_git(["status", "--short"], root).stdout.strip():
        run_git(["add", ".gitignore"], root)
        run_git(["commit", "-m", "cmoc init"], root)
    typer.echo(render_cmoc_init_result(root))


def render_cmoc_init_result(root: Path) -> str:
    """`cmoc init` の成功結果を stdout 用 Markdown にする。"""
    return f"# cmoc init\n- repo_root: `{root}`\n- ignored: `{root / '.cmoc'}`"
