from pathlib import Path
from tempfile import NamedTemporaryFile

import typer

from cmoc_runtime import ensure_cmoc_ignored, repo_root, run_git, sync_config


def cmoc_init_impl() -> None:
    """work root を cmoc が扱える初期状態へ同期する。"""
    root = repo_root()
    staged_patch = run_git(["diff", "--cached", "--binary"], root).stdout
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
    typer.echo(render_cmoc_init_result(root))


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
