import shutil
import subprocess
from pathlib import Path
from typing import Callable

from commons.runtime_errors import CmocError
from commons.runtime_paths import worktrees_dir
from commons.runtime_results import CommandResult


MANAGED_BRANCH_PREFIXES = ("cmoc/session/", "cmoc/apply/", "cmoc/run/")
CMOC_IGNORE_PATTERN = "/.cmoc/gu/"
# {{work-root}}/oracle/src/oracle/other/cmoc_config.py
# Keep a broad user .cmoc/ rule effective for other children while making the
# tracked repository config reachable while keeping other `.cmoc` data ignored.
CMOC_CONFIG_IGNORE_EXCEPTIONS = (
    "!/.cmoc/",
    "/.cmoc/*",
    "!/.cmoc/gt/",
    "/.cmoc/gt/*",
    "!/.cmoc/gt/ar/",
    "/.cmoc/gt/ar/*",
    "!/.cmoc/gt/ar/config.json",
)
CMOC_IGNORE_PROBE = ".cmoc/gu/.__cmoc_ignore_probe__"


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
        status = _git_status_short(root)
    if status:
        raise CmocError(
            "git 未コミット差分が存在します。",
            ["差分を commit または退避してから再実行してください。"],
            status,
        )


def _git_status_short(root: Path) -> str:
    """porcelain status を返す。"""
    return run_git(["status", "--short"], root).stdout.strip()


def status_path_statuses(
    root: Path,
    *,
    untracked_all: bool = False,
    include_rename_sources: bool = False,
    git: Callable[[list[str], Path], CommandResult] = run_git,
) -> list[tuple[str, Path]]:
    """git status porcelain v1 -z の path を quote なしで返す。"""
    args = ["status", "--porcelain=v1", "-z"]
    if untracked_all:
        args.append("-uall")
    fields = git(args, root).stdout.split("\0")
    paths: list[tuple[str, Path]] = []
    index = 0
    while index < len(fields):
        field = fields[index]
        index += 1
        if not field:
            continue
        status = field[:2]
        paths.append((status, root / field[3:]))
        if status[0] in {"R", "C"} or status[1] in {"R", "C"}:
            if include_rename_sources and index < len(fields) and fields[index]:
                paths.append((status, root / fields[index]))
            index += 1
    return paths


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
    """未使用 path に run/apply 用 linked worktree を作る。"""
    expected_worktree = _expected_managed_worktree(root, branch)
    candidate = _absolute_path(worktree)
    if _first_managed_worktree_symlink(
        root, candidate, expected_worktree
    ) is not None:
        raise CmocError(
            "run worktree path は symlink を含められません。",
            ["branch 名と worktree path の対応を確認してください。"],
            f"branch: {branch}\nworktree: {worktree}\nexpected: {expected_worktree}",
        )
    expected_worktree = expected_worktree.resolve()
    candidate = candidate.resolve()
    if candidate != expected_worktree:
        raise CmocError(
            "run worktree path が cmoc 管理領域と一致しません。",
            ["branch 名と worktree path の対応を確認してください。"],
            f"branch: {branch}\nworktree: {worktree}\nexpected: {expected_worktree}",
        )
    candidate.parent.mkdir(parents=True, exist_ok=True)
    if candidate.exists():
        # {{work-root}}/oracle/doc/branch_model.md
        # A matching path is not evidence of a cmoc-created linked worktree; never delete it implicitly.
        raise CmocError(
            "run worktree path は既に存在します。",
            ["既存の directory または worktree を確認してから再実行してください。"],
            str(candidate),
        )
    run_git(["worktree", "add", "-b", branch, str(candidate), start_point], root)
    return worktree


def remove_worktree(root: Path, worktree: Path) -> CommandResult:
    """登録済み worktree だけを git worktree として削除する。"""
    safe_worktree = _require_managed_worktree(root, worktree)
    result = run_git(
        ["worktree", "remove", "--force", str(safe_worktree)], root, check=False
    )
    if result.returncode != 0 and safe_worktree.exists():
        # git コマンド中の状態変化後も、登録済み path だけを再帰削除する。
        safe_worktree = _require_managed_worktree(root, safe_worktree)
        shutil.rmtree(safe_worktree)
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
    return worktrees_dir(_main_worktree_root(root)) / parts[2] / parts[3]


def _require_managed_worktree(root: Path, worktree: Path) -> Path:
    base = worktrees_dir(_main_worktree_root(root))
    candidate = _absolute_path(worktree)
    if _first_managed_worktree_symlink(root, candidate) is not None:
        raise _unmanaged_worktree_error(worktree, base)
    base = base.resolve()
    resolved = candidate.resolve()
    try:
        relative = resolved.relative_to(base)
    except ValueError as exc:
        raise _unmanaged_worktree_error(worktree, base) from exc
    # {{work-root}}/oracle/src/oracle/other/path_model.py
    # work-root deletion is limited to .cmoc/gu/worktree/{{parent-run-id}}/{{run-id}}.
    if len(relative.parts) != 2 or not all(relative.parts):
        raise _unmanaged_worktree_error(worktree, base)
    # {{work-root}}/oracle/doc/branch_model.md
    # The naming convention is not enough: deletion is limited to Git linked worktrees.
    if candidate.exists() and resolved not in _registered_worktree_paths(root):
        raise _unmanaged_worktree_error(worktree, base)
    return resolved


def _absolute_path(path: Path) -> Path:
    """symlink 検査前に相対 path を絶対 path へ変換する。"""
    return path if path.is_absolute() else Path.cwd() / path


def _first_symlink_component(path: Path) -> Path | None:
    """path を順にたどり、最初に見つかった symlink component を返す。"""
    absolute = _absolute_path(path)
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        if part in {"", "."}:
            continue
        if part == "..":
            current = current.parent
            continue
        current /= part
        if current.is_symlink():
            return current
    return None


def _first_managed_worktree_symlink(root: Path, *paths: Path) -> Path | None:
    """managed base と path の symlink component を探す。"""
    # {{work-root}}/oracle/doc/branch_model.md
    # resolve() だけでは repo 外の実体が managed path に見えるため、canonicalize 前に
    # lexical path の component を検査して、作成・削除の両方で symlink 経由を拒否する。
    for path in (worktrees_dir(_main_worktree_root(root)), *paths):
        if symlink := _first_symlink_component(path):
            return symlink
    return None


def _registered_worktree_paths(root: Path) -> set[Path]:
    output = run_git(["worktree", "list", "--porcelain"], root).stdout
    return {
        Path(line.removeprefix("worktree ")).resolve()
        for line in output.splitlines()
        if line.startswith("worktree ")
    }


def _unmanaged_worktree_error(worktree: Path, base: Path) -> CmocError:
    return CmocError(
        "cmoc 管理外の worktree は削除できません。",
        ["worktree path と session state file を確認してください。"],
        f"worktree: {worktree}\nmanaged_base: {base}",
    )


def git_common_dir(root: Path) -> Path:
    """Git common directory の絶対 path を返す。"""
    common = run_git(
        ["rev-parse", "--path-format=absolute", "--git-common-dir"], root
    ).stdout.strip()
    return Path(common).resolve()


def _main_worktree_root(root: Path) -> Path:
    return git_common_dir(root).parent


def _cmoc_ignore_status(root: Path) -> tuple[str, int]:
    """.cmoc/gu の追跡有無と ignore 判定を取得する。"""
    tracked = run_git(["ls-files", "--", ".cmoc/gu"], root).stdout.strip()
    ignored = run_git(
        ["check-ignore", "-q", CMOC_IGNORE_PROBE],
        root,
        check=False,
    )
    return tracked, ignored.returncode


def with_cmoc_ignore_pattern(content: str) -> str:
    """既存の末尾改行を崩さず cmoc の ignore 規則を追加する。"""
    lines = content.splitlines()
    patterns = []
    if any(line in {".cmoc/", "/.cmoc/"} for line in lines):
        patterns.extend(
            pattern
            for pattern in CMOC_CONFIG_IGNORE_EXCEPTIONS
            if pattern not in lines
        )
    if CMOC_IGNORE_PATTERN not in lines:
        patterns.append(CMOC_IGNORE_PATTERN)
    if not patterns:
        return content
    separator = "\n" if lines and lines[-1] != "" else ""
    newline = "" if content == "" or content.endswith("\n") else "\n"
    added = "\n".join(patterns)
    return f"{content}{newline}{separator}{added}\n"


def ensure_cmoc_ignored(root: Path) -> None:
    """.gitignore と index を更新できる場面で .cmoc/gu を追跡対象外にする。"""
    tracked, ignored_returncode = _cmoc_ignore_status(root)
    gitignore = root / ".gitignore"
    content = gitignore.read_text() if gitignore.exists() else ""
    updated_content = with_cmoc_ignore_pattern(content)
    if updated_content != content:
        gitignore.write_text(updated_content)

    if not tracked and ignored_returncode == 0:
        return

    run_git(["rm", "--cached", "-f", "-r", "--ignore-unmatch", ".cmoc/gu"], root)
    tracked, ignored_returncode = _cmoc_ignore_status(root)
    if tracked or ignored_returncode != 0:
        raise CmocError(
            ".cmoc/gu を git 追跡対象外にできませんでした。",
            [".gitignore と git index の状態を確認してください。"],
            f"tracked:\n{tracked}\ncheck-ignore returncode: {ignored_returncode}",
        )


def ensure_cmoc_ignored_in_exclude(root: Path) -> None:
    """clean worktree を保つ必要がある caller 用に git exclude で .cmoc ignore を保証する。

    根拠:
    - {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    - {{work-root}}/oracle/doc/app_spec/sub_command/apply_fork.md
    """
    exclude_path = root / run_git(
        ["rev-parse", "--git-path", "info/exclude"], root
    ).stdout.strip()
    content = exclude_path.read_text() if exclude_path.exists() else ""
    updated_content = with_cmoc_ignore_pattern(content)
    if updated_content != content:
        exclude_path.parent.mkdir(parents=True, exist_ok=True)
        exclude_path.write_text(updated_content)
    tracked, ignored_returncode = _cmoc_ignore_status(root)
    if tracked or ignored_returncode != 0:
        raise CmocError(
            ".cmoc/gu を git 追跡対象外にできませんでした。",
            [".gitignore と git index の状態を確認してください。"],
            f"tracked:\n{tracked}\ncheck-ignore returncode: {ignored_returncode}",
        )


def require_cmoc_ignored(root: Path) -> None:
    """初期化済み repository として .cmoc/gu ignore 状態を検査する。"""
    tracked, ignored_returncode = _cmoc_ignore_status(root)
    if tracked or ignored_returncode != 0:
        raise CmocError(
            ".cmoc/gu が git 追跡対象外に初期化されていません。",
            ["cmoc doctor を実行してから再実行してください。"],
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


def is_untracked_git_ignored(root: Path, path: Path) -> bool:
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    # oracle/realization file definitions use normal git check-ignore behavior:
    # tracked files remain targets even when they match an ignore pattern.
    candidate = path if path.is_absolute() else root / path
    rel = candidate.absolute().relative_to(root.absolute())
    return (
        run_git(["check-ignore", "-q", str(rel)], root, check=False).returncode == 0
    )


def is_oracle_file_path(root: Path, path: Path) -> bool:
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    # Keep the oracle file definition in one runtime helper because it is used by
    # both Codex access checks and apply/session diff classification.
    # Oracle ownership is defined by the repository path, so tracked symlinks
    # under oracle/ remain oracle files even when their targets are outside root.
    try:
        candidate = path if path.is_absolute() else root / path
        relative = candidate.absolute().relative_to(root.absolute())
    except ValueError:
        return False
    return (
        bool(relative.parts)
        and relative.parts[0] == "oracle"
        and path.name not in {"AGENTS.md", "INDEX.md"}
        and not is_untracked_git_ignored(root, path)
    )
