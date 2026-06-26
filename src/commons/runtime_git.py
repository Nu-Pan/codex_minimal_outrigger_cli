import shutil
import subprocess
from pathlib import Path

from commons.runtime_errors import CmocError
from commons.runtime_results import CommandResult


MANAGED_BRANCH_PREFIXES = ("cmoc/session/", "cmoc/apply/", "cmoc/run/")
CMOC_IGNORE_PATTERN = "/.cmoc/"


def run_git(args: list[str], cwd: Path, check: bool = True) -> CommandResult:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
    )
    command_result = CommandResult(result.returncode, result.stdout, result.stderr)
    if check and result.returncode != 0:
        raise CmocError(
            "git コマンドが失敗しました。",
            ["git の状態を確認してから、同じ cmoc コマンドを再実行してください。"],
            f"command: git {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
    return command_result


def current_branch(root: Path) -> str:
    result = run_git(["branch", "--show-current"], root)
    branch = result.stdout.strip()
    if not branch:
        raise CmocError(
            "detached HEAD 上では実行できません。",
            ["通常の local branch に checkout してから再実行してください。"],
            "git branch --show-current が空文字を返しました。",
        )
    return branch


def head_commit(root: Path) -> str:
    return run_git(["rev-parse", "HEAD"], root).stdout.strip()


def require_clean_worktree(root: Path, status: str | None = None) -> None:
    if status is None:
        status = run_git(["status", "--short"], root).stdout.strip()
    if status:
        raise CmocError(
            "git 未コミット差分が存在します。",
            ["差分を commit または退避してから再実行してください。"],
            status,
        )


def is_managed_branch(branch: str) -> bool:
    return branch.startswith(MANAGED_BRANCH_PREFIXES)


def branch_exists(root: Path, branch: str) -> bool:
    return (
        run_git(
            ["show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
            root,
            check=False,
        ).returncode
        == 0
    )


def create_run_worktree(
    root: Path, branch: str, worktree: Path, start_point: str = "HEAD"
) -> Path:
    worktree.parent.mkdir(parents=True, exist_ok=True)
    if worktree.exists():
        shutil.rmtree(worktree)
    run_git(["worktree", "add", "-b", branch, str(worktree), start_point], root)
    return worktree


def remove_worktree(root: Path, worktree: Path) -> CommandResult:
    result = run_git(
        ["worktree", "remove", "--force", str(worktree)], root, check=False
    )
    if result.returncode != 0 and worktree.exists():
        shutil.rmtree(worktree)
    run_git(["worktree", "prune"], root, check=False)
    return result


def delete_branch(root: Path, branch: str, force: bool = False) -> CommandResult:
    return run_git(["branch", "-D" if force else "-d", branch], root, check=False)


def _cmoc_ignore_status(root: Path) -> tuple[str, int]:
    tracked = run_git(["ls-files", "--", ".cmoc"], root).stdout.strip()
    ignored = run_git(
        ["check-ignore", "-q", ".cmoc/.__cmoc_ignore_probe__"],
        root,
        check=False,
    )
    return tracked, ignored.returncode


def with_cmoc_ignore_pattern(content: str) -> str:
    lines = content.splitlines()
    if CMOC_IGNORE_PATTERN in lines:
        return content
    separator = "\n" if lines and lines[-1] != "" else ""
    newline = "" if content == "" or content.endswith("\n") else "\n"
    return f"{content}{newline}{separator}{CMOC_IGNORE_PATTERN}\n"


def ensure_cmoc_ignored(root: Path) -> None:
    tracked, ignored_returncode = _cmoc_ignore_status(root)
    gitignore = root / ".gitignore"
    content = gitignore.read_text() if gitignore.exists() else ""
    updated_content = with_cmoc_ignore_pattern(content)
    if updated_content != content:
        gitignore.write_text(updated_content)

    if not tracked and ignored_returncode == 0:
        return

    run_git(["rm", "--cached", "-r", "--ignore-unmatch", ".cmoc"], root)
    tracked, ignored_returncode = _cmoc_ignore_status(root)
    if tracked or ignored_returncode != 0:
        raise CmocError(
            ".cmoc を git 追跡対象外にできませんでした。",
            [".gitignore と git index の状態を確認してください。"],
            f"tracked:\n{tracked}\ncheck-ignore returncode: {ignored_returncode}",
        )


def require_cmoc_ignored(root: Path) -> None:
    tracked, ignored_returncode = _cmoc_ignore_status(root)
    if tracked or ignored_returncode != 0:
        raise CmocError(
            ".cmoc が git 追跡対象外に初期化されていません。",
            ["cmoc init を実行してから再実行してください。"],
            f"tracked:\n{tracked}\ncheck-ignore returncode: {ignored_returncode}",
        )


def is_git_ignored(root: Path, path: Path) -> bool:
    rel = path.resolve().relative_to(root)
    return run_git(["check-ignore", "--no-index", "-q", str(rel)], root, check=False).returncode == 0
