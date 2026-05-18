"""git リポジトリと cmoc 作業ディレクトリの共通処理。"""

import fnmatch
import os
import subprocess
from pathlib import Path

from .errors import CmocError


def enter_repo_root(start: Path | None = None) -> Path:
    """リポジトリルートを特定し、プロセスの cwd をそこへ移す。"""
    repo_root = find_repo_root(start)
    os.chdir(repo_root)
    return repo_root


def find_repo_root(start: Path | None = None) -> Path:
    """カレントから親方向へ `.git` を持つリポジトリルートを探す。"""
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise CmocError(
        "Git repository root was not found.",
        [
            "Move into a git-managed repository.",
            "Run `git init` if this directory should be a repository.",
        ],
        f"Start path: {current}",
    )


def current_branch(repo_root: Path) -> str:
    """現在の git ブランチ名を返す。"""
    result = run_git(repo_root, ["branch", "--show-current"])
    return result.stdout.strip()


def head_commit(repo_root: Path) -> str:
    """HEAD の commit hash を返す。"""
    result = run_git(repo_root, ["rev-parse", "HEAD"])
    return result.stdout.strip()


def is_cmoc_branch(branch_name: str) -> bool:
    """`cmoc_<time-stamp>` 形式のブランチ名か判定する。"""
    parts = branch_name.split("_")
    if len(parts) != 5 or parts[0] != "cmoc":
        return False

    date_part, hour_minute_part, second_part, msec_part = parts[1:]
    return (
        len(date_part) == 10
        and date_part[4] == "-"
        and date_part[7] == "-"
        and len(hour_minute_part) == 5
        and hour_minute_part[2] == "-"
        and len(second_part) == 2
        and len(msec_part) == 3
        and date_part.replace("-", "").isdigit()
        and hour_minute_part.replace("-", "").isdigit()
        and second_part.isdigit()
        and msec_part.isdigit()
    )


def ensure_cmoc_ignored(repo_root: Path) -> bool:
    """`.cmoc` が git 追跡対象外であることを機械的に保証する。"""
    changed = _ensure_cmoc_ignore_rule(repo_root)
    tracked = _tracked_cmoc_paths(repo_root)
    if tracked:
        run_git(repo_root, ["rm", "--cached", "-r", "--", ".cmoc"])
        changed = True
    _assert_cmoc_ignore_guarantee(repo_root)
    return changed


def has_uncommitted_changes(repo_root: Path) -> bool:
    """git 未コミット差分が存在するか判定する。"""
    result = run_git(repo_root, ["status", "--porcelain"])
    return bool(result.stdout.strip())


def assert_no_uncommitted_changes(repo_root: Path) -> None:
    """未コミット差分がある場合は仕様通りエラーにする。"""
    paths = changed_paths(repo_root)
    if paths:
        raise CmocError(
            "Uncommitted changes exist.",
            [
                "Commit or stash the current changes.",
                "Run the command again from a clean working tree.",
            ],
            "\n".join(paths),
        )


def assert_only_oracles_uncommitted(repo_root: Path) -> None:
    """未コミット差分が `oracles` 配下だけであることを確認する。"""
    outside = [
        path
        for path in changed_paths(repo_root)
        if not path.startswith("oracles/")
    ]
    if outside:
        raise CmocError(
            "Uncommitted changes outside oracles exist.",
            [
                "Commit or stash non-oracle changes.",
                "Run `cmoc apply` after only oracle changes remain.",
            ],
            "\n".join(outside),
        )


def commit_if_changed(repo_root: Path, paths: list[str], message: str) -> bool:
    """指定パスに差分があれば add して commit する。"""
    diff_result = run_git(repo_root, ["status", "--porcelain", "--", *paths])
    if not diff_result.stdout.strip():
        return False
    update_paths = [path for path in paths if (repo_root / path).exists()]
    if update_paths:
        run_git(repo_root, ["add", "-u", "--", *update_paths])
    add_paths = [path for path in paths if not path.startswith(".cmoc")]
    if add_paths:
        run_git(repo_root, ["add", "--", *add_paths])
    run_git(repo_root, ["commit", "-m", message])
    return True


def list_oracle_files(repo_root: Path) -> list[Path]:
    """仕様に従って `oracles` ファイルを列挙する。"""
    oracle_root = repo_root / "oracles"
    if not oracle_root.exists():
        return []

    files: list[Path] = []
    for path in oracle_root.rglob("*"):
        if not path.is_file() or path.name == "INDEX.md":
            continue
        relative = path.relative_to(repo_root).as_posix()
        if _is_gitignored(repo_root, relative):
            continue
        files.append(path)
    return sorted(files)


def changed_oracle_files(repo_root: Path, base_commit: str) -> list[Path]:
    """部分評価対象となる変更済み oracle ファイルを列挙する。"""
    collected: set[Path] = set()
    committed = run_git(
        repo_root,
        [
            "diff",
            "--name-only",
            "--diff-filter=ACMRT",
            f"{base_commit}..HEAD",
            "--",
            "oracles",
        ],
    )
    for line in committed.stdout.splitlines():
        collected.add(repo_root / line)

    uncommitted = run_git(
        repo_root,
        [
            "diff",
            "--name-only",
            "--diff-filter=ACMRT",
            "HEAD",
            "--",
            "oracles",
        ],
    )
    staged = run_git(
        repo_root,
        [
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=ACMRT",
            "--",
            "oracles",
        ],
    )
    for output in [uncommitted.stdout, staged.stdout]:
        for line in output.splitlines():
            collected.add(repo_root / line)

    status = run_git(repo_root, ["status", "--porcelain", "--", "oracles"])
    for line in status.stdout.splitlines():
        if line.startswith("?? "):
            collected.add(repo_root / line[3:])

    return sorted(
        path
        for path in collected
        if path.exists()
        and path.is_file()
        and path.name != "INDEX.md"
        and not _is_gitignored(
            repo_root,
            path.relative_to(repo_root).as_posix(),
        )
    )


def has_deleted_oracle_files(repo_root: Path, base_commit: str) -> bool:
    """base commit から HEAD までの oracle 削除有無を判定する。"""
    committed = run_git(
        repo_root,
        [
            "diff",
            "--name-only",
            "--diff-filter=D",
            f"{base_commit}..HEAD",
            "--",
            "oracles",
        ],
    )
    if committed.stdout.strip():
        return True
    staged = run_git(
        repo_root,
        [
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=D",
            "--",
            "oracles",
        ],
    )
    if staged.stdout.strip():
        return True
    working = run_git(
        repo_root,
        ["diff", "--name-only", "--diff-filter=D", "HEAD", "--", "oracles"],
    )
    return bool(working.stdout.strip())


def read_branch_base_commit(repo_root: Path, branch_name: str) -> str:
    """cmoc branch の作成元 commit hash を読む。"""
    path = branch_base_commit_path(repo_root, branch_name)
    if not path.exists():
        raise CmocError(
            "cmoc branch base commit file was not found.",
            [
                "Run `cmoc branch` before partial evaluation.",
                "Run `cmoc eval-oracles --full` to evaluate all oracle files.",
            ],
            str(path),
        )
    return path.read_text(encoding="utf-8").strip()


def branch_base_commit_path(repo_root: Path, branch_name: str) -> Path:
    """cmoc branch の作成元 commit 記録ファイルのパスを返す。"""
    return repo_root / ".cmoc" / "branch" / f"{branch_name}.txt"


def changed_paths(repo_root: Path) -> list[str]:
    """未コミット差分のパスを porcelain から取り出す。"""
    result = run_git(repo_root, ["status", "--porcelain"])
    paths: list[str] = []
    for line in result.stdout.splitlines():
        value = line[3:]
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        paths.append(value)
    return paths


def _ensure_cmoc_ignore_rule(repo_root: Path) -> bool:
    """`.gitignore` に oracle 指定の `/.cmoc/` 行を追加する。"""
    gitignore = repo_root / ".gitignore"
    existing = (
        gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    )
    lines = [line.strip() for line in existing.splitlines()]
    if "/.cmoc/" in lines:
        return False

    prefix = existing
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    gitignore.write_text(f"{prefix}/.cmoc/\n", encoding="utf-8")
    return True


def _tracked_cmoc_paths(repo_root: Path) -> list[str]:
    """git index に残っている `.cmoc` 配下パスを返す。"""
    result = run_git(repo_root, ["ls-files", "--", ".cmoc"])
    return [line for line in result.stdout.splitlines() if line]


def _assert_cmoc_ignore_guarantee(repo_root: Path) -> None:
    """`.cmoc` 追跡対象外保証の完了条件を検証する。"""
    tracked = _tracked_cmoc_paths(repo_root)
    probe = ".cmoc/.__cmoc_ignore_probe__"
    ignored = run_git(
        repo_root,
        ["check-ignore", "-q", "--", probe],
        check=False,
    )
    if tracked or ignored.returncode != 0:
        raise CmocError(
            "Failed to guarantee that .cmoc is untracked.",
            [
                "Inspect .gitignore and the git index.",
                "Remove tracked .cmoc files from the index, then run cmoc "
                "again.",
            ],
            "\n".join(tracked) or f"Probe was not ignored: {probe}",
        )


def _is_gitignored(repo_root: Path, relative_path: str) -> bool:
    """gitignore 対象かを git check-ignore とローカル fallback で判定する。"""
    result = run_git(
        repo_root,
        ["check-ignore", "-q", "--", relative_path],
        check=False,
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False

    gitignore = repo_root / ".gitignore"
    if not gitignore.exists():
        return False
    for raw_line in gitignore.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        pattern = line.lstrip("/")
        if (
            fnmatch.fnmatch(relative_path, pattern)
            or relative_path.startswith(pattern.rstrip("/") + "/")
        ):
            return True
    return False


def run_git(
    repo_root: Path,
    args: list[str],
    *,
    check: bool = True,
    text: bool = True,
) -> subprocess.CompletedProcess[str]:
    """git コマンドを cwd 固定で実行する。"""
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=check,
        text=text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
