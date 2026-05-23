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
        "Git リポジトリのルートが見つかりませんでした。",
        [
            "git 管理下のリポジトリへ移動してください。",
            "このディレクトリをリポジトリにする場合は `git init` を実行してください。",
        ],
        f"開始パス: {current}",
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
            "未コミットの変更があります。",
            [
                "現在の変更を commit または stash してください。",
                "作業ツリーを clean にしてからコマンドを再実行してください。",
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
            "oracles 以外に未コミットの変更があります。",
            [
                "oracle 以外の変更を commit または stash してください。",
                "未コミット変更が oracle だけになってから `cmoc apply` を実行してください。",
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
            "初期化対象パスに未コミットの変更があります。",
            [
                "`cmoc init` を実行する前に、表示されたパスを commit または stash してください。",
                "初期化対象パスを clean にしてからコマンドを再実行してください。",
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


def staged_diff_from_head(repo_root: Path) -> str:
    """現在 stage 済みの差分を HEAD 基準の patch として返す。"""
    # init commit 後に利用者の stage 済み差分だけを復元するため事前保存する。
    result = run_git(
        repo_root,
        ["diff", "--cached", "--binary", "--full-index"],
    )
    return result.stdout


def commit_cmoc_initialization_changes(
    repo_root: Path,
    had_cmoc_rule: bool,
    preexisting_staged_diff: str,
    message: str = "Initialize cmoc",
) -> bool:
    """`.cmoc` ignore 保証が発生させた差分だけを commit する。"""
    # 一時 index だけで初期化差分の tree を作り、通常 index の既存 stage と分離する。
    parent_hash = _head_commit_or_none(repo_root)
    with tempfile.TemporaryDirectory(prefix="cmoc-init-index-") as temp_name:
        env = {"GIT_INDEX_FILE": str(Path(temp_name) / "index")}
        if parent_hash is None:
            run_git(repo_root, ["read-tree", "--empty"], env=env)
        else:
            run_git(repo_root, ["read-tree", "HEAD"], env=env)
        if not had_cmoc_rule:
            _stage_gitignore_with_cmoc_rule_from_head(repo_root, env)
        _remove_cmoc_from_index(repo_root, env)

        diff = run_git(
            repo_root,
            ["diff", "--cached", "--quiet", "--", ".gitignore", ".cmoc"],
            check=False,
            env=env,
        )
        if diff.returncode == 0:
            return False
        if diff.returncode != 1:
            raise CmocError(
                "初期化差分の検査に失敗しました。",
                [
                    "git index の状態を確認してから `cmoc init` を再実行してください。",
                    "無関係な変更を commit または stash してから `cmoc init` を再実行してください。",
                ],
                diff.stderr.strip(),
            )

        tree_hash = run_git(repo_root, ["write-tree"], env=env).stdout.strip()

    commit_args = ["commit-tree", tree_hash, "-m", message]
    if parent_hash is not None:
        commit_args[2:2] = ["-p", parent_hash]
    commit_hash = run_git(
        repo_root,
        commit_args,
    ).stdout.strip()
    update_ref_args = ["update-ref", "HEAD", commit_hash]
    if parent_hash is not None:
        update_ref_args.append(parent_hash)
    run_git(repo_root, update_ref_args)
    _restore_index_after_init_commit(repo_root, preexisting_staged_diff)
    return True


def commit_if_changed(repo_root: Path, paths: list[str], message: str) -> bool:
    """指定パスに差分があれば add して commit する。"""
    # 指定 pathspec に差分が無ければ commit を作らない。
    diff_result = run_git(repo_root, ["status", "--porcelain", "--", *paths])
    if not diff_result.stdout.strip():
        return False

    # 呼び出し前から stage 済みの無関係差分を、対象 commit へ混ぜない。
    staged_outside_paths = _staged_diff_excluding_paths(repo_root, paths)
    parent_hash = _head_commit_or_none(repo_root)
    with tempfile.TemporaryDirectory(
        prefix="cmoc-pathspec-index-",
    ) as temp_name:
        env = {"GIT_INDEX_FILE": str(Path(temp_name) / "index")}
        if parent_hash is None:
            run_git(repo_root, ["read-tree", "--empty"], env=env)
        else:
            run_git(repo_root, ["read-tree", "HEAD"], env=env)

        update_paths = [path for path in paths if (repo_root / path).exists()]
        if update_paths:
            run_git(repo_root, ["add", "-u", "--", *update_paths], env=env)

        add_paths = [path for path in paths if not path.startswith(".cmoc")]
        if add_paths:
            run_git(repo_root, ["add", "--", *add_paths], env=env)
        if any(path == ".cmoc" or path.startswith(".cmoc/") for path in paths):
            _remove_cmoc_from_index(repo_root, env)

        changed = run_git(
            repo_root,
            ["diff", "--cached", "--quiet", "--", *paths],
            check=False,
            env=env,
        )
        if changed.returncode == 0:
            return False
        if changed.returncode != 1:
            raise CmocError(
                "pathspec commit 用差分の検査に失敗しました。",
                [
                    "git index の状態を確認してから cmoc を再実行してください。",
                    "無関係な変更を commit または stash してから cmoc を再実行してください。",
                ],
                changed.stderr.strip(),
            )

        tree_hash = run_git(repo_root, ["write-tree"], env=env).stdout.strip()

    commit_args = ["commit-tree", tree_hash, "-m", message]
    if parent_hash is not None:
        commit_args[2:2] = ["-p", parent_hash]
    commit_hash = run_git(repo_root, commit_args).stdout.strip()
    update_ref_args = ["update-ref", "HEAD", commit_hash]
    if parent_hash is not None:
        update_ref_args.append(parent_hash)
    run_git(repo_root, update_ref_args)
    _restore_index_after_pathspec_commit(repo_root, staged_outside_paths)
    return True


def _restore_index_after_init_commit(
    repo_root: Path,
    preexisting_staged_diff: str,
) -> None:
    """init commit 後の index を HEAD ベースに戻し、既存 staged 差分を復元する。"""
    # 作業ツリーは触らず index だけを新しい HEAD に合わせる。
    run_git(repo_root, ["read-tree", "--reset", "HEAD"])
    if not preexisting_staged_diff:
        return

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        delete=False,
    ) as patch_file:
        patch_file.write(preexisting_staged_diff)
        patch_path = Path(patch_file.name)
    try:
        result = run_git(
            repo_root,
            ["apply", "--cached", "--3way", str(patch_path)],
            check=False,
        )
    finally:
        patch_path.unlink(missing_ok=True)
    if result.returncode == 0:
        _remove_cmoc_from_index(repo_root, {})
        _assert_cmoc_ignore_guarantee(repo_root)
        return

    raise CmocError(
        "事前に stage されていた変更の復元に失敗しました。",
        [
            "作業を続ける前に git index の状態を確認してください。",
            "必要に応じて、以前 stage していた変更をもう一度 stage してください。",
        ],
        result.stderr.strip(),
    )


def _head_commit_or_none(repo_root: Path) -> str | None:
    """HEAD が存在すれば commit hash を返し、未作成なら None を返す。"""
    # rev-parse で HEAD の存在確認と commit hash 取得を同時に行う。
    result = run_git(
        repo_root,
        ["rev-parse", "--verify", "HEAD"],
        check=False,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


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


def list_implementation_files(repo_root: Path) -> list[Path]:
    """仕様に従って実装ファイルを列挙する。"""
    # repo root 配下の全ファイルから、仕様上の除外対象だけを落とす。
    candidates: list[Path] = []
    for path in repo_root.rglob("*"):
        if not path.is_file() or path.name == "INDEX.md":
            continue
        relative = path.relative_to(repo_root).as_posix()
        if _is_excluded_implementation_path(relative):
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
    # base..HEAD の履歴上で起きた追加・変更・rename などを収集する。
    collected: set[Path] = set()
    committed = run_git(
        repo_root,
        [
            "log",
            "--name-status",
            "-M",
            "--diff-filter=ACMRT",
            "--format=",
            f"{base_commit}..HEAD",
            "--",
            "oracles",
        ],
    )
    for line in committed.stdout.splitlines():
        parts = line.split("\t")
        if not parts:
            continue
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) >= 3:
            collected.add(repo_root / parts[2])
        elif len(parts) >= 2:
            collected.add(repo_root / parts[1])

    # 未コミットの working tree/staging 変更も部分評価対象に加える。
    uncommitted = run_git(
        repo_root,
        [
            "diff",
            "--name-status",
            "-M",
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
            "--name-status",
            "-M",
            "--diff-filter=ACMRT",
            "--",
            "oracles",
        ],
    )
    for output in [uncommitted.stdout, staged.stdout]:
        collected.update(_changed_paths_from_name_status(repo_root, output))

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
        and path.relative_to(repo_root).as_posix().startswith("oracles/")
        and path.name != "INDEX.md"
    ]
    relatives = [path.relative_to(repo_root).as_posix() for path in existing]
    ignored = _root_gitignored_paths(repo_root, relatives)
    return sorted(
        path
        for path, relative in zip(existing, relatives, strict=True)
        if relative not in ignored
    )


def changed_implementation_files(
    repo_root: Path,
    base_commit: str,
) -> list[Path]:
    """部分適用対象となる変更済み実装ファイルを列挙する。"""
    # base..HEAD と未コミット差分から、実装ファイルだけを抽出する。
    collected: set[Path] = set()
    commands = [
        [
            "log",
            "--name-status",
            "-M",
            "--diff-filter=ACMRT",
            "--format=",
            f"{base_commit}..HEAD",
            "--",
            ".",
        ],
        [
            "diff",
            "--name-status",
            "-M",
            "--diff-filter=ACMRT",
            "HEAD",
            "--",
            ".",
        ],
        [
            "diff",
            "--cached",
            "--name-status",
            "-M",
            "--diff-filter=ACMRT",
            "--",
            ".",
        ],
    ]
    for command in commands:
        collected.update(
            _changed_paths_from_name_status(
                repo_root,
                run_git(repo_root, command).stdout,
            )
        )

    # 未追跡ファイルもディレクトリ単位に畳まず収集する。
    status = run_git(
        repo_root,
        ["status", "--porcelain", "--untracked-files=all", "--", "."],
    )
    for line in status.stdout.splitlines():
        if line.startswith("?? "):
            collected.add(repo_root / line[3:])

    existing = [
        path
        for path in collected
        if _is_implementation_file(repo_root, path)
    ]
    relatives = [path.relative_to(repo_root).as_posix() for path in existing]
    ignored = _root_gitignored_paths(repo_root, relatives)
    return sorted(
        path
        for path, relative in zip(existing, relatives, strict=True)
        if relative not in ignored
    )


def _changed_paths_from_name_status(repo_root: Path, output: str) -> set[Path]:
    """`git diff --name-status` から変更後 path を取り出す。"""
    # rename/copy を考慮しながら git 出力を path 集合へ変換する。
    paths: set[Path] = set()
    for line in output.splitlines():
        parts = line.split("\t")
        if not parts:
            continue
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) >= 3:
            paths.add(repo_root / parts[2])
        elif len(parts) >= 2:
            paths.add(repo_root / parts[1])
    return paths


def has_deleted_oracle_files(repo_root: Path, base_commit: str) -> bool:
    """評価モード切替用に oracle 削除有無を判定する。"""
    # committed 履歴、working tree、staging area の削除をすべて切替条件にする。
    commands = [
        [
            "log",
            "--name-only",
            "-M",
            "--diff-filter=D",
            "--format=",
            f"{base_commit}..HEAD",
        ],
        ["diff", "--name-only", "-M", "--diff-filter=D", "HEAD"],
        ["diff", "--cached", "--name-only", "-M", "--diff-filter=D"],
    ]
    for command in commands:
        result = run_git(repo_root, [*command, "--", "oracles"])
        if _deleted_oracle_file_paths(repo_root, result.stdout):
            return True
    return False


def has_deleted_implementation_files(
    repo_root: Path,
    base_commit: str,
) -> bool:
    """適用モード切替用に実装ファイル削除有無を判定する。"""
    # committed 履歴、working tree、staging area の削除をすべて切替条件にする。
    commands = [
        [
            "log",
            "--name-only",
            "-M",
            "--diff-filter=D",
            "--format=",
            f"{base_commit}..HEAD",
        ],
        ["diff", "--name-only", "-M", "--diff-filter=D", "HEAD"],
        ["diff", "--cached", "--name-only", "-M", "--diff-filter=D"],
    ]
    for command in commands:
        result = run_git(repo_root, [*command, "--", "."])
        if _deleted_implementation_file_paths(repo_root, result.stdout):
            return True
    return False


def _deleted_oracle_file_paths(repo_root: Path, output: str) -> list[str]:
    """削除 path から oracle 列挙対象外のものを除外する。"""
    # INDEX.md と root .gitignore 対象は oracle ファイル削除として扱わない。
    relatives = [
        line
        for line in output.splitlines()
        if line.startswith("oracles/") and Path(line).name != "INDEX.md"
    ]
    ignored = _root_gitignored_paths(repo_root, relatives)
    return [relative for relative in relatives if relative not in ignored]


def _deleted_implementation_file_paths(
    repo_root: Path,
    output: str,
) -> list[str]:
    """削除 path から実装ファイル列挙対象外のものを除外する。"""
    # 削除済み path は存在確認できないため、path 規則と gitignore だけで判定する。
    relatives = [
        line
        for line in output.splitlines()
        if not _is_excluded_implementation_path(line)
    ]
    ignored = _root_gitignored_paths(repo_root, relatives)
    return [relative for relative in relatives if relative not in ignored]


def _is_implementation_file(repo_root: Path, path: Path) -> bool:
    """実装ファイル列挙対象の既存ファイルか判定する。"""
    # Path が repo 外を指すケースは対象外にする。
    try:
        relative = path.relative_to(repo_root).as_posix()
    except ValueError:
        return False
    return (
        path.exists()
        and path.is_file()
        and not _is_excluded_implementation_path(relative)
    )


def _is_excluded_implementation_path(relative_path: str) -> bool:
    """実装ファイル列挙から機械的に除外する path か判定する。"""
    # oracles、.git、INDEX.md は仕様上の除外対象である。
    path = Path(relative_path)
    return (
        relative_path == "oracles"
        or relative_path.startswith("oracles/")
        or relative_path == ".git"
        or relative_path.startswith(".git/")
        or path.name == "INDEX.md"
    )


def read_branch_base_commit(repo_root: Path, branch_name: str) -> str:
    """cmoc branch の作成元 commit hash を読む。"""
    # cmoc branch 作成時に記録した base commit ファイルを読む。
    path = branch_base_commit_path(repo_root, branch_name)
    if not path.exists():
        raise CmocError(
            "cmoc branch の作成元 commit ファイルが見つかりませんでした。",
            [
                "差分評価の前に `cmoc branch` を実行してください。",
                "全 oracle ファイルを評価する場合は `cmoc eval-oracles --full` を実行してください。",
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


def _staged_diff_excluding_paths(repo_root: Path, paths: list[str]) -> str:
    """指定 pathspec 以外の既存 staged 差分を patch として返す。"""
    # pathspec magic の exclude で、今回 commit する対象だけを復元対象から外す。
    exclusions = [f":(exclude){path}" for path in paths]
    result = run_git(
        repo_root,
        [
            "diff",
            "--cached",
            "--binary",
            "--full-index",
            "--",
            ".",
            *exclusions,
        ],
    )
    return result.stdout


def _restore_index_after_pathspec_commit(
    repo_root: Path,
    staged_diff: str,
) -> None:
    """pathspec commit 後、対象外の既存 staged 差分だけを index に戻す。"""
    # 作業ツリーは触らず index だけを新しい HEAD に合わせる。
    run_git(repo_root, ["read-tree", "--reset", "HEAD"])
    if not staged_diff:
        return

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        delete=False,
    ) as patch_file:
        patch_file.write(staged_diff)
        patch_path = Path(patch_file.name)
    try:
        result = run_git(
            repo_root,
            ["apply", "--cached", "--3way", str(patch_path)],
            check=False,
        )
    finally:
        patch_path.unlink(missing_ok=True)
    if result.returncode == 0:
        _remove_cmoc_from_index(repo_root, {})
        return

    raise CmocError(
        "事前に stage されていた変更の復元に失敗しました。",
        [
            "作業を続ける前に git index の状態を確認してください。",
            "必要に応じて、以前 stage していた変更をもう一度 stage してください。",
        ],
        result.stderr.strip(),
    )


def _stage_gitignore_with_cmoc_rule_from_head(
    repo_root: Path,
    env: dict[str, str],
) -> None:
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
            env=env,
        ).stdout.strip()
    finally:
        staged_path.unlink(missing_ok=True)

    # 作った blob を index に直接置き、作業ツリーの `.gitignore` は触らない。
    run_git(
        repo_root,
        ["update-index", "--add", "--cacheinfo", f"100644,{blob},.gitignore"],
        env=env,
    )


def _remove_cmoc_from_index(repo_root: Path, env: dict[str, str]) -> None:
    """指定 index から `.cmoc` 配下の tracked entries を取り除く。"""
    # 対象 index に残っている `.cmoc` entries を NUL 区切りで取得する。
    tracked = run_git(
        repo_root,
        ["ls-files", "-z", "--", ".cmoc"],
        env=env,
    ).stdout
    if tracked:
        run_git(
            repo_root,
            ["update-index", "--force-remove", "-z", "--stdin"],
            input_text=tracked,
            env=env,
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
            ".cmoc を git 追跡対象外にする保証に失敗しました。",
            [
                ".gitignore と git index を確認してください。",
                "追跡済みの .cmoc ファイルを index から外してから cmoc を再実行してください。",
            ],
            "\n".join(tracked) or f"probe が ignore されませんでした: {probe}",
        )


def _tracked_cmoc_paths(repo_root: Path) -> list[str]:
    """git index に残っている `.cmoc` 配下パスを返す。"""
    # `git ls-files` の空でない行だけを tracked path として返す。
    result = run_git(repo_root, ["ls-files", "--", ".cmoc"])
    return [line for line in result.stdout.splitlines() if line]


def _is_root_gitignored(repo_root: Path, relative_path: str) -> bool:
    """root `.gitignore` の pattern だけで ignore 対象か判定する。"""
    # 単一 path の判定も集合判定の実装に揃える。
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
            "root .gitignore の評価に失敗しました。",
            [
                ".gitignore の構文を確認してからコマンドを再実行してください。",
                "一時的に root .gitignore を単純化してから cmoc を再実行してください。",
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
    input_text: str | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """git コマンドを cwd 固定で実行する。"""
    # git 呼び出しは全て repo root 起点で実行し、stdout/stderr を呼び出し側で扱う。
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=check,
        text=text,
        input=input_text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, **env} if env is not None else None,
    )
