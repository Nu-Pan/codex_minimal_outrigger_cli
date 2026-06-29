import shutil
import subprocess
from pathlib import Path

from commons.runtime_errors import CmocError
from commons.runtime_results import CommandResult


MANAGED_BRANCH_PREFIXES = ("cmoc/session/", "cmoc/apply/", "cmoc/run/")
CMOC_IGNORE_PATTERN = "/.cmoc/"


def run_git(args: list[str], cwd: Path, check: bool = True) -> CommandResult:
    """git subprocess の失敗を cmoc の利用者向けエラーへそろえる境界。"""
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
    """detached HEAD を cmoc の実行前提違反として扱う branch 取得 helper。"""
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
    """cmoc state や report に記録する現在 HEAD commit を取得する。"""
    return run_git(["rev-parse", "HEAD"], root).stdout.strip()


def require_clean_worktree(root: Path, status: str | None = None) -> None:
    """未コミット差分を許容しない操作の事前条件を共通化する。"""
    if status is None:
        status = run_git(["status", "--short"], root).stdout.strip()
    if status:
        raise CmocError(
            "git 未コミット差分が存在します。",
            ["差分を commit または退避してから再実行してください。"],
            status,
        )


def is_managed_branch(branch: str) -> bool:
    """cmoc が作る branch namespace に入っているかを判定する。"""
    return branch.startswith(MANAGED_BRANCH_PREFIXES)


def branch_exists(root: Path, branch: str) -> bool:
    """git の quiet command を cmoc の boolean 判定へ変換する。"""
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
    """既存 path を除去してから run/apply 用 linked worktree を作る。"""
    expected_worktree = _expected_managed_worktree(root, branch)
    if worktree.resolve() != expected_worktree:
        raise CmocError(
            "run worktree path が cmoc 管理領域と一致しません。",
            ["branch 名と worktree path の対応を確認してください。"],
            f"branch: {branch}\nworktree: {worktree}\nexpected: {expected_worktree}",
        )
    worktree.parent.mkdir(parents=True, exist_ok=True)
    if worktree.exists():
        shutil.rmtree(worktree)
    run_git(["worktree", "add", "-b", branch, str(worktree), start_point], root)
    return worktree


def remove_worktree(root: Path, worktree: Path) -> CommandResult:
    """git worktree remove 失敗時も実体 directory の削除まで試みる。"""
    _require_managed_worktree(root, worktree)
    result = run_git(
        ["worktree", "remove", "--force", str(worktree)], root, check=False
    )
    if result.returncode != 0 and worktree.exists():
        shutil.rmtree(worktree)
    run_git(["worktree", "prune"], root, check=False)
    return result


def delete_branch(root: Path, branch: str, force: bool = False) -> CommandResult:
    """削除失敗を caller が warning 化できる branch 削除 helper。"""
    return run_git(["branch", "-D" if force else "-d", branch], root, check=False)


def _expected_managed_worktree(root: Path, branch: str) -> Path:
    parts = branch.split("/")
    if (
        len(parts) != 4
        or parts[0] != "cmoc"
        or parts[1] not in {"apply", "run"}
        or not parts[2]
        or not parts[3]
    ):
        raise CmocError(
            "run worktree を作成できない branch 名です。",
            ["cmoc apply/run branch 名を確認してください。"],
            f"branch: {branch}",
        )
    return (
        _main_worktree_root(root) / ".cmoc" / "worktrees" / parts[2] / parts[3]
    ).resolve()


def _require_managed_worktree(root: Path, worktree: Path) -> None:
    base = (_main_worktree_root(root) / ".cmoc" / "worktrees").resolve()
    resolved = worktree.resolve()
    try:
        relative = resolved.relative_to(base)
    except ValueError as exc:
        raise _unmanaged_worktree_error(worktree, base) from exc
    # <work-root>/oracle/src/oracle/other/path_model.py
    # work-root deletion is limited to .cmoc/worktrees/<parent-run-id>/<run-id>.
    if len(relative.parts) != 2 or not all(relative.parts):
        raise _unmanaged_worktree_error(worktree, base)


def _unmanaged_worktree_error(worktree: Path, base: Path) -> CmocError:
    return CmocError(
        "cmoc 管理外の worktree は削除できません。",
        ["worktree path と session state file を確認してください。"],
        f"worktree: {worktree}\nmanaged_base: {base}",
    )


def _main_worktree_root(root: Path) -> Path:
    common = run_git(
        ["rev-parse", "--path-format=absolute", "--git-common-dir"], root
    ).stdout.strip()
    return Path(common).parent.resolve()


def _cmoc_ignore_status(root: Path) -> tuple[str, int]:
    """.cmoc の追跡有無と ignore 判定を同じ probe で取得する。"""
    tracked = run_git(["ls-files", "--", ".cmoc"], root).stdout.strip()
    ignored = run_git(
        ["check-ignore", "-q", ".cmoc/.__cmoc_ignore_probe__"],
        root,
        check=False,
    )
    return tracked, ignored.returncode


def with_cmoc_ignore_pattern(content: str) -> str:
    """既存の末尾改行を崩さず .cmoc ignore pattern を追加する。"""
    lines = content.splitlines()
    if CMOC_IGNORE_PATTERN in lines:
        return content
    separator = "\n" if lines and lines[-1] != "" else ""
    newline = "" if content == "" or content.endswith("\n") else "\n"
    return f"{content}{newline}{separator}{CMOC_IGNORE_PATTERN}\n"


def ensure_cmoc_ignored(root: Path) -> None:
    """.gitignore と index を更新できる場面で .cmoc を追跡対象外にする。"""
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


def ensure_cmoc_ignored_in_exclude(root: Path) -> None:
    """clean worktree を保つ必要がある caller 用に git exclude で .cmoc ignore を保証する。

    根拠:
    - <work-root>/oracle/doc/app_spec/sub_command/session_fork.md
    - <work-root>/oracle/doc/app_spec/sub_command/apply_fork.md
    """
    exclude_path = root / run_git(
        ["rev-parse", "--git-path", "info/exclude"], root
    ).stdout.strip()
    content = exclude_path.read_text() if exclude_path.exists() else ""
    if CMOC_IGNORE_PATTERN not in content.splitlines():
        exclude_path.parent.mkdir(parents=True, exist_ok=True)
        newline = "" if content == "" or content.endswith("\n") else "\n"
        exclude_path.write_text(f"{content}{newline}{CMOC_IGNORE_PATTERN}\n")
    tracked, ignored_returncode = _cmoc_ignore_status(root)
    if tracked or ignored_returncode != 0:
        raise CmocError(
            ".cmoc を git 追跡対象外にできませんでした。",
            [".gitignore と git index の状態を確認してください。"],
            f"tracked:\n{tracked}\ncheck-ignore returncode: {ignored_returncode}",
        )


def require_cmoc_ignored(root: Path) -> None:
    """初期化済み repository として .cmoc ignore 状態を検査する。"""
    tracked, ignored_returncode = _cmoc_ignore_status(root)
    if tracked or ignored_returncode != 0:
        raise CmocError(
            ".cmoc が git 追跡対象外に初期化されていません。",
            ["cmoc init を実行してから再実行してください。"],
            f"tracked:\n{tracked}\ncheck-ignore returncode: {ignored_returncode}",
        )


def is_git_ignored(root: Path, path: Path) -> bool:
    """対象 path が git ignore されるかを work root 基準で判定する。"""
    candidate = path if path.is_absolute() else root / path
    rel = candidate.absolute().relative_to(root.absolute())
    return (
        run_git(
            ["check-ignore", "--no-index", "-q", str(rel)],
            root,
            check=False,
        ).returncode
        == 0
    )
