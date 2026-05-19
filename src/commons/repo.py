"""git リポジトリと cmoc 作業ディレクトリの共通処理。"""

import fnmatch
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from .errors import CmocError


def enter_repo_root(start: Path | None = None) -> Path:
    """リポジトリルートを特定し、プロセスの cwd をそこへ移す。"""
    # 起点から repo root を見つけ、以降の git 操作の cwd を固定する。
    repo_root = find_repo_root(start)
    os.chdir(repo_root)
    return repo_root


def find_repo_root(start: Path | None = None) -> Path:
    """カレントから親方向へ `.git` を持つリポジトリルートを探す。"""
    # 指定起点または現在ディレクトリから親方向へ順番に探索する。
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
    # git の現在 branch 名を余分な改行なしで返す。
    result = run_git(repo_root, ["branch", "--show-current"])
    return result.stdout.strip()


def head_commit(repo_root: Path) -> str:
    """HEAD の commit hash を返す。"""
    # HEAD の full hash を git から取得する。
    result = run_git(repo_root, ["rev-parse", "HEAD"])
    return result.stdout.strip()


def is_cmoc_branch(branch_name: str) -> bool:
    """`cmoc_<time-stamp>` 形式のブランチ名か判定する。"""
    # timestamp 区切り数と prefix を先に検査する。
    parts = branch_name.split("_")
    if len(parts) != 5 or parts[0] != "cmoc":
        return False

    # 各 timestamp 要素の桁数、区切り文字、数字性を検査する。
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
    # `.gitignore` に必要な行を保証し、既に tracked な `.cmoc` は index から外す。
    changed = _ensure_cmoc_ignore_rule(repo_root)
    tracked = _tracked_cmoc_paths(repo_root)
    if tracked:
        run_git(repo_root, ["rm", "--cached", "-r", "--", ".cmoc"])
        changed = True

    # gitignore と git index の両面から完了条件を検証する。
    _assert_cmoc_ignore_guarantee(repo_root)
    return changed


def has_uncommitted_changes(repo_root: Path) -> bool:
    """git 未コミット差分が存在するか判定する。"""
    # porcelain 出力が 1 行でもあれば未コミット差分ありとする。
    result = run_git(repo_root, ["status", "--porcelain"])
    return bool(result.stdout.strip())


def assert_no_uncommitted_changes(repo_root: Path) -> None:
    """未コミット差分がある場合は仕様通りエラーにする。"""
    # 未コミット path を利用者に見せるため、bool ではなく一覧を取得する。
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
    # apply 前の許容差分を oracles 配下だけに制限する。
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


def assert_paths_clean(repo_root: Path, paths: list[str]) -> None:
    """指定 pathspec に未コミット差分がないことを確認する。"""
    # init が既存ユーザー差分を自動 commit に混ぜないため、対象 path を先に検査する。
    result = run_git(
        repo_root,
        ["status", "--porcelain", "--untracked-files=all", "--", *paths],
    )
    if result.stdout.strip():
        raise CmocError(
            "Uncommitted initialization target changes exist.",
            [
                "Commit or stash the listed paths before running cmoc init.",
                "Run the command again after initialization targets are "
                "clean.",
            ],
            result.stdout.strip(),
        )


def gitignore_has_cmoc_rule(repo_root: Path) -> bool:
    """作業ツリーの `.gitignore` が `/.cmoc/` 行を既に持つか返す。"""
    # init 開始前からある ignore ルールを、init で発生した差分と区別する。
    gitignore = repo_root / ".gitignore"
    if not gitignore.exists():
        return False
    content = gitignore.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines()]
    return "/.cmoc/" in lines


def commit_cmoc_initialization_changes(
    repo_root: Path,
    had_cmoc_rule: bool,
) -> bool:
    """`cmoc init` が発生させた差分だけを commit する。"""
    # init が追加した `/.cmoc/` だけを、既存 `.gitignore` 差分と分けて stage する。
    if not had_cmoc_rule:
        _stage_gitignore_with_cmoc_rule_from_head(repo_root)

    # tracked `.cmoc` の追跡解除は `ensure_cmoc_ignored()` 済みの index 状態を使う。
    diff = run_git(
        repo_root,
        ["diff", "--cached", "--quiet", "--", ".gitignore", ".cmoc"],
        check=False,
    )
    if diff.returncode == 0:
        return False
    if diff.returncode != 1:
        raise CmocError(
            "Failed to inspect initialization changes.",
            [
                "Inspect git index state and retry cmoc init.",
                "Commit or stash unrelated changes, then run cmoc init again.",
            ],
            diff.stderr.strip(),
        )

    # stage 済みの初期化差分だけを init commit にする。
    run_git(repo_root, ["commit", "-m", "Initialize cmoc"])
    return True


def commit_if_changed(repo_root: Path, paths: list[str], message: str) -> bool:
    """指定パスに差分があれば add して commit する。"""
    # 指定 pathspec に差分が無ければ commit を作らない。
    diff_result = run_git(repo_root, ["status", "--porcelain", "--", *paths])
    if not diff_result.stdout.strip():
        return False

    # 既存ファイルの削除・更新は `git add -u` で拾う。
    update_paths = [path for path in paths if (repo_root / path).exists()]
    if update_paths:
        run_git(repo_root, ["add", "-u", "--", *update_paths])

    # `.cmoc` は追跡対象外なので、新規 add 対象からは外す。
    add_paths = [path for path in paths if not path.startswith(".cmoc")]
    if add_paths:
        run_git(repo_root, ["add", "--", *add_paths])
    run_git(repo_root, ["commit", "-m", message])
    return True


def list_oracle_files(repo_root: Path) -> list[Path]:
    """仕様に従って `oracles` ファイルを列挙する。"""
    # oracles ディレクトリが無い場合は評価対象なしとして扱う。
    oracle_root = repo_root / "oracles"
    if not oracle_root.exists():
        return []

    # INDEX.md と root .gitignore 対象を除いた全ファイルを列挙する。
    candidates: list[Path] = []
    for path in oracle_root.rglob("*"):
        if not path.is_file() or path.name == "INDEX.md":
            continue
        candidates.append(path)

    relatives = [path.relative_to(repo_root).as_posix() for path in candidates]
    ignored = _root_gitignored_paths(repo_root, relatives)
    return sorted(
        path
        for path, relative in zip(candidates, relatives, strict=True)
        if relative not in ignored
    )


def changed_oracle_files(repo_root: Path, base_commit: str) -> list[Path]:
    """部分評価対象となる変更済み oracle ファイルを列挙する。"""
    # base..HEAD の追加・変更・rename などを収集する。
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

    # 未コミットの working tree/staging 変更も部分評価対象に加える。
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

    # untracked oracle ファイルはディレクトリ単位に畳まない形式で収集する。
    status = run_git(
        repo_root,
        ["status", "--porcelain", "--untracked-files=all", "--", "oracles"],
    )
    for line in status.stdout.splitlines():
        if line.startswith("?? "):
            collected.add(repo_root / line[3:])

    # 削除済み、INDEX.md、root .gitignore 対象は評価対象から除外する。
    existing = [
        path
        for path in collected
        if path.exists()
        and path.is_file()
        and path.name != "INDEX.md"
    ]
    relatives = [path.relative_to(repo_root).as_posix() for path in existing]
    ignored = _root_gitignored_paths(repo_root, relatives)
    return sorted(
        path
        for path, relative in zip(existing, relatives, strict=True)
        if relative not in ignored
    )


def has_deleted_oracle_files(repo_root: Path, base_commit: str) -> bool:
    """評価モード切替用に oracle 削除有無を判定する。"""
    # committed、working tree、staging area の削除をすべて切替条件にする。
    commands = [
        ["diff", "--name-only", "--diff-filter=D", f"{base_commit}..HEAD"],
        ["diff", "--name-only", "--diff-filter=D", "HEAD"],
        ["diff", "--cached", "--name-only", "--diff-filter=D"],
    ]
    for command in commands:
        result = run_git(repo_root, [*command, "--", "oracles"])
        if result.stdout.strip():
            return True
    return False


def read_branch_base_commit(repo_root: Path, branch_name: str) -> str:
    """cmoc branch の作成元 commit hash を読む。"""
    # cmoc branch 作成時に記録した base commit ファイルを読む。
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
    # branch 名をファイル名にして `.cmoc/branch` 配下へ配置する。
    return repo_root / ".cmoc" / "branch" / f"{branch_name}.txt"


def changed_paths(repo_root: Path) -> list[str]:
    """未コミット差分のパスを porcelain から取り出す。"""
    # rename 行は新しい path だけを返す。
    result = run_git(repo_root, ["status", "--porcelain"])
    paths: list[str] = []
    for line in result.stdout.splitlines():
        value = line[3:]
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        paths.append(value)
    return paths


def _stage_gitignore_with_cmoc_rule_from_head(repo_root: Path) -> None:
    """HEAD の `.gitignore` に `/.cmoc/` だけを足した blob を stage する。"""
    # HEAD 側の内容を基準にすることで、作業ツリーの既存差分を commit から外す。
    head_text = _head_file_text(repo_root, ".gitignore") or ""
    lines = [line.strip() for line in head_text.splitlines()]
    if "/.cmoc/" in lines:
        return

    # commit 対象にする `.gitignore` 内容を一時ファイル経由で git object 化する。
    prefix = head_text
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    staged_text = f"{prefix}/.cmoc/\n"
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        delete=False,
    ) as staged_file:
        staged_file.write(staged_text)
        staged_path = Path(staged_file.name)
    try:
        blob = run_git(
            repo_root,
            ["hash-object", "-w", str(staged_path)],
        ).stdout.strip()
    finally:
        staged_path.unlink(missing_ok=True)

    # 作った blob を index に直接置き、作業ツリーの `.gitignore` は触らない。
    run_git(
        repo_root,
        ["update-index", "--add", "--cacheinfo", f"100644,{blob},.gitignore"],
    )


def _head_file_text(repo_root: Path, relative_path: str) -> str | None:
    """HEAD 上のファイル内容を返し、存在しなければ None を返す。"""
    # 初回 init のように HEAD に `.gitignore` が無い場合を通常系として扱う。
    result = run_git(
        repo_root,
        ["show", f"HEAD:{relative_path}"],
        check=False,
    )
    if result.returncode == 0:
        return result.stdout
    return None


def _ensure_cmoc_ignore_rule(repo_root: Path) -> bool:
    """`.gitignore` に oracle 指定の `/.cmoc/` 行を追加する。"""
    # 既存 `.gitignore` を読み、必要な ignore 行の重複を避ける。
    gitignore = repo_root / ".gitignore"
    existing = (
        gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    )
    lines = [line.strip() for line in existing.splitlines()]
    if "/.cmoc/" in lines:
        return False

    # 既存内容の末尾改行を整えてから ignore 行を追加する。
    prefix = existing
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    gitignore.write_text(f"{prefix}/.cmoc/\n", encoding="utf-8")
    return True


def _assert_cmoc_ignore_guarantee(repo_root: Path) -> None:
    """`.cmoc` 追跡対象外保証の完了条件を検証する。"""
    # tracked path と ignore probe の両方で保証状態を確認する。
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


def _tracked_cmoc_paths(repo_root: Path) -> list[str]:
    """git index に残っている `.cmoc` 配下パスを返す。"""
    # `git ls-files` の空でない行だけを tracked path として返す。
    result = run_git(repo_root, ["ls-files", "--", ".cmoc"])
    return [line for line in result.stdout.splitlines() if line]


def _is_root_gitignored(repo_root: Path, relative_path: str) -> bool:
    """root `.gitignore` の pattern だけで ignore 対象か判定する。"""
    return relative_path in _root_gitignored_paths(repo_root, [relative_path])


def _root_gitignored_paths(
    repo_root: Path,
    relative_paths: list[str],
) -> set[str]:
    """root `.gitignore` だけを Git の wildmatch semantics で評価する。"""
    # 評価対象または root `.gitignore` が無ければ ignore 対象なしとして返す。
    gitignore = repo_root / ".gitignore"
    if not relative_paths or not gitignore.exists():
        return set()

    # 一時 git repository に root `.gitignore` だけを複製して評価環境を作る。
    with tempfile.TemporaryDirectory(prefix="cmoc-gitignore-") as temp_name:
        temp_root = Path(temp_name)
        shutil.copyfile(gitignore, temp_root / ".gitignore")
        subprocess.run(
            ["git", "init", "-q"],
            cwd=temp_root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # `--stdin` で渡した root 相対 path を Git の ignore 実装に判定させる。
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--stdin"],
            cwd=temp_root,
            check=False,
            input="\n".join(relative_paths) + "\n",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "GIT_CONFIG_GLOBAL": os.devnull},
        )

    # gitignore 評価自体の異常は利用者が復旧できる共通エラーに変換する。
    if result.returncode not in {0, 1}:
        raise CmocError(
            "Failed to evaluate root .gitignore.",
            [
                "Inspect .gitignore syntax and retry the command.",
                "Temporarily simplify root .gitignore, then run cmoc again.",
            ],
            result.stderr.strip(),
        )

    # `git check-ignore` が出力した path だけを ignore 対象集合として返す。
    return set(result.stdout.splitlines())


def _is_gitignored(repo_root: Path, relative_path: str) -> bool:
    """gitignore 対象かを git check-ignore とローカル fallback で判定する。"""
    # tracked 状態に依存しないよう `--no-index` で pattern 一致だけを見る。
    result = run_git(
        repo_root,
        ["check-ignore", "--no-index", "-q", "--", relative_path],
        check=False,
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False

    # git check-ignore 自体が失敗した場合だけ、単純な .gitignore fallback を使う。
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
    # git 呼び出しは全て repo root 起点で実行し、stdout/stderr を呼び出し側で扱う。
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=check,
        text=text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
