"""Git repository の状態・worktree・path 分類を扱う共通境界。

この file は 16,000 文字を超えるが、Git command、branch/worktree、ignore、
oracle/realization file の分類は、同じ repository path・Git index・安全性の不変条件を
共有する一つの境界である。分割すると、path の正規化と Git 状態検証を各 module で
重複して追う必要が生じるため、現状は Git 境界として一箇所に保つ。

根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import os
import shutil
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

from .runtime_errors import CmocError
from .runtime_paths import worktrees_dir
from .runtime_results import CommandResult

MANAGED_BRANCH_PREFIXES = ("cmoc/session/", "cmoc/run/")
CMOC_IGNORE_PATTERN = "/.cmoc/gu/"
# {{work-root}}/oracle/src/oracle/other/cmoc_config.py
# 他の child には広い user .cmoc/ rule を効かせつつ、追跡対象の repository config を
# 到達可能にし、その他の `.cmoc` data は ignore されたままにする。
CMOC_CONFIG_IGNORE_EXCEPTIONS = (
    "!/.cmoc/",
    "/.cmoc/*",
    "!/.cmoc/gt/",
    "/.cmoc/gt/*",
    "!/.cmoc/gt/ar/",
    "/.cmoc/gt/ar/*",
    "!/.cmoc/gt/ar/config.json",
    "!/.cmoc/gt/ar/realization/",
    "/.cmoc/gt/ar/realization/*",
    "!/.cmoc/gt/ar/realization/refactor/",
    "/.cmoc/gt/ar/realization/refactor/*",
    "!/.cmoc/gt/ar/realization/refactor/state.json",
)
CMOC_IGNORE_PROBE = ".cmoc/gu/.__cmoc_ignore_probe__"
_CODEX_SNAPSHOT_EXCLUDED_PREFIXES = (
    Path(".cmoc/gu/ar/log"),
    Path(".cmoc/gu/ar/schema"),
)
_FILE_INVENTORY_EXCLUDED_ROOT_NAMES = frozenset(
    {".git", ".agents", ".codex", ".cmoc", "memo"}
)
_FILE_INVENTORY_EXCLUDED_FILE_NAMES = frozenset({"AGENTS.md", "INDEX.md"})
_FileClassification = Literal["oracle", "realization"]


@dataclass(frozen=True)
class WorktreeArtifact:
    """作業成果物 1 path の復元可能な filesystem 状態。"""

    kind: str
    content: bytes | str | None
    mode: int


@dataclass(frozen=True)
class WorktreeSnapshot:
    """Codex call の前後で比較する非 ignore 作業成果物の状態。"""

    root: Path
    entries: tuple[tuple[str, WorktreeArtifact], ...]

    def changed_paths(self, other: "WorktreeSnapshot") -> frozenset[str]:
        """2 snapshot 間で filesystem 状態が異なる repository 相対 path を返す。"""
        if self.root != other.root:
            raise ValueError("worktree snapshot roots do not match")
        before = dict(self.entries)
        after = dict(other.entries)
        return frozenset(
            path
            for path in before.keys() | after.keys()
            if before.get(path) != after.get(path)
        )


def capture_worktree_snapshot(root: Path) -> WorktreeSnapshot:
    """追跡済みまたは非 ignore の作業成果物を復元可能な形で取得する。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # Codex call の log と schema store は Git ignore 対象なので snapshot へ含めず、
    # agent が扱う非 ignore の作業成果物だけを固定する。
    root = root.absolute()
    fields = run_git(
        ["ls-files", "-z", "--cached", "--others", "--exclude-standard"], root
    ).stdout.split("\0")
    entries: dict[str, WorktreeArtifact] = {}
    for field in fields:
        if not field:
            continue
        relative = Path(field)
        if relative.is_absolute() or ".." in relative.parts:
            raise CmocError(
                "作業成果物の snapshot を取得できません。",
                ["repository の Git index と path を確認してください。"],
                f"invalid path: {field!r}",
            )
        if any(
            relative == prefix or prefix in relative.parents
            for prefix in _CODEX_SNAPSHOT_EXCLUDED_PREFIXES
        ):
            continue
        artifact_path, artifact = _read_worktree_artifact(root, relative)
        if artifact is not None:
            entries[artifact_path] = artifact
    return WorktreeSnapshot(root, tuple(sorted(entries.items())))


def restore_worktree_snapshot(snapshot: WorktreeSnapshot) -> None:
    """現在の作業成果物を指定 snapshot と同じ filesystem 状態へ戻す。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # Structured Output 補正 turn が変動させた path だけを初回 call 完了時へ戻す。
    frozen = dict(snapshot.entries)
    seen: set[frozenset[str]] = set()
    while True:
        current = capture_worktree_snapshot(snapshot.root)
        changed = snapshot.changed_paths(current)
        if not changed:
            return
        if changed in seen:
            raise CmocError(
                "補正 turn が変更した作業成果物を復元できませんでした。",
                ["run worktree の差分を確認してから同じコマンドを再実行してください。"],
                f"remaining paths: {sorted(changed)!r}",
            )
        seen.add(changed)
        ordered = sorted(changed, key=lambda item: (len(Path(item).parts), item))
        for relative in ordered:
            _remove_worktree_artifact(snapshot.root, Path(relative))
        for relative in ordered:
            artifact = frozen.get(relative)
            if artifact is not None:
                _write_worktree_artifact(snapshot.root, Path(relative), artifact)


def _read_worktree_artifact(
    root: Path, relative: Path
) -> tuple[str, WorktreeArtifact | None]:
    """symlink の親をたどらず、最初の filesystem object を読み取る。"""
    candidate = root
    for index, part in enumerate(relative.parts):
        candidate /= part
        try:
            metadata = candidate.lstat()
        except FileNotFoundError:
            return str(relative), None
        is_last = index == len(relative.parts) - 1
        if not is_last and stat.S_ISDIR(metadata.st_mode):
            continue
        artifact_relative = candidate.relative_to(root)
        mode = stat.S_IMODE(metadata.st_mode)
        if stat.S_ISREG(metadata.st_mode):
            artifact = WorktreeArtifact("file", candidate.read_bytes(), mode)
        elif stat.S_ISLNK(metadata.st_mode):
            artifact = WorktreeArtifact("symlink", os.readlink(candidate), mode)
        elif stat.S_ISDIR(metadata.st_mode):
            artifact = WorktreeArtifact("directory", None, mode)
        else:
            raise CmocError(
                "作業成果物の snapshot を取得できません。",
                ["特殊 file を repository の作業成果物から取り除いてください。"],
                f"unsupported path: {artifact_relative}",
            )
        return str(artifact_relative), artifact
    return str(relative), None


def _remove_worktree_artifact(root: Path, relative: Path) -> None:
    """root 外の symlink をたどらず、補正 turn 後の object を取り除く。"""
    candidate = root
    for part in relative.parts:
        candidate /= part
        try:
            metadata = candidate.lstat()
        except FileNotFoundError:
            return
        if not stat.S_ISDIR(metadata.st_mode):
            if stat.S_ISLNK(metadata.st_mode) or stat.S_ISREG(metadata.st_mode):
                candidate.unlink()
            else:
                raise CmocError(
                    "補正 turn が変更した作業成果物を復元できませんでした。",
                    ["run worktree の差分を確認してください。"],
                    f"unsupported path: {candidate.relative_to(root)}",
                )
            return
    shutil.rmtree(candidate)


def _write_worktree_artifact(
    root: Path, relative: Path, artifact: WorktreeArtifact
) -> None:
    """snapshot の object を symlink のない親 directory 配下へ復元する。"""
    parent = root
    for part in relative.parts[:-1]:
        parent /= part
        try:
            metadata = parent.lstat()
        except FileNotFoundError:
            parent.mkdir()
            continue
        if not stat.S_ISDIR(metadata.st_mode):
            raise CmocError(
                "補正 turn が変更した作業成果物を復元できませんでした。",
                ["run worktree の差分を確認してください。"],
                f"non-directory parent: {parent.relative_to(root)}",
            )
    path = root / relative
    if artifact.kind == "file":
        assert isinstance(artifact.content, bytes)
        path.write_bytes(artifact.content)
        path.chmod(artifact.mode)
    elif artifact.kind == "symlink":
        assert isinstance(artifact.content, str)
        path.symlink_to(artifact.content)
    elif artifact.kind == "directory":
        path.mkdir(exist_ok=True)
        path.chmod(artifact.mode)
    else:
        raise AssertionError(f"unknown worktree artifact kind: {artifact.kind}")


def literal_pathspec(path: str) -> str:
    """Git が repository path を wildcard として解釈しない pathspec を返す。"""
    return f":(literal){path}"


def run_git(args: list[str], git_cwd: Path, check: bool = True) -> CommandResult:
    """git subprocess の失敗を cmoc の利用者向けエラーへそろえる境界。"""
    # {{work-root}}/oracle/doc/dev_rule/coding_rule.md
    # Git の実行場所は subprocess API の cwd とは異なる内部役割名で扱う。
    result = subprocess.run(
        ["git", *args],
        cwd=git_cwd,
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
    """未使用 path に run 用 linked worktree を作る。"""
    expected_worktree = expected_run_worktree(root, branch)
    candidate = _absolute_path(worktree)
    if _first_managed_worktree_symlink(root, candidate, expected_worktree) is not None:
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
        # path が一致しても cmoc 作成の linked worktree とは限らないため、暗黙に削除しない。
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


def expected_run_worktree(root: Path, branch: str) -> Path:
    """run branch 名から許可された run worktree path を求める。"""
    parts = branch.split("/")
    # {{work-root}}/oracle/doc/branch_model.md
    # dot component は run-root の2階層配置を崩すため、path component として許可しない。
    if (
        len(parts) != 4
        or parts[0] != "cmoc"
        or parts[1] != "run"
        or not parts[2]
        or not parts[3]
        or parts[2] in {".", ".."}
        or parts[3] in {".", ".."}
    ):
        raise CmocError(
            "run worktree を作成できない branch 名です。",
            ["cmoc run branch 名を確認してください。"],
            f"branch: {branch}",
        )
    return worktrees_dir(_main_worktree_root(root)) / parts[2] / parts[3]


def _require_managed_worktree(root: Path, worktree: Path) -> Path:
    """削除対象が管理領域内の登録済みworktreeであることを検証する。"""
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
    # work-root の削除は .cmoc/gu/worktree/{{parent-run-id}}/{{run-id}} に限定する。
    if len(relative.parts) != 2 or not all(relative.parts):
        raise _unmanaged_worktree_error(worktree, base)
    # {{work-root}}/oracle/doc/branch_model.md
    # 命名規則だけでは不十分であり、削除は対応する Git linked worktree に限定する。
    expected_branch = f"cmoc/run/{relative.parts[0]}/{relative.parts[1]}"
    registered_branch = _registered_worktree_branches(root).get(resolved)
    if registered_branch != expected_branch:
        raise _unmanaged_worktree_error(worktree, base)
    if candidate.exists() and not _has_linked_worktree_metadata(root, candidate):
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


def _registered_worktree_branches(root: Path) -> dict[Path, str]:
    """Git に登録された worktree と checkout branch の対応を返す。"""
    output = run_git(["worktree", "list", "--porcelain"], root).stdout
    registered: dict[Path, str] = {}
    worktree: Path | None = None
    for line in output.splitlines():
        if line.startswith("worktree "):
            worktree = Path(line.removeprefix("worktree ")).resolve()
        elif worktree is not None and line.startswith("branch refs/heads/"):
            registered[worktree] = line.removeprefix("branch refs/heads/")
    return registered


def _has_linked_worktree_metadata(root: Path, worktree: Path) -> bool:
    """worktree path と Git linked worktree metadata の相互参照を検証する。"""
    # {{work-root}}/oracle/src/oracle/other/path_model.py
    # linked worktree の root は直下に .git file を持つ。Git の登録だけでは、
    # worktree directory が置換された stale entry と区別できないため、metadata の
    # 相互参照まで確認して fallback の再帰削除を許可する。
    dot_git = worktree / ".git"
    if not worktree.is_dir() or dot_git.is_symlink() or not dot_git.is_file():
        return False
    try:
        gitdir_line = dot_git.read_text().strip()
        prefix = "gitdir: "
        if (
            not gitdir_line.startswith(prefix)
            or "\n" in gitdir_line
            or "\r" in gitdir_line
        ):
            return False
        gitdir = Path(gitdir_line.removeprefix(prefix))
        if not gitdir.is_absolute():
            gitdir = worktree / gitdir
        gitdir = gitdir.resolve()
        relative_gitdir = gitdir.relative_to(git_common_dir(root) / "worktrees")
        if not relative_gitdir.parts:
            return False
        metadata_gitdir = gitdir / "gitdir"
        if metadata_gitdir.is_symlink() or not metadata_gitdir.is_file():
            return False
        back_reference = Path(metadata_gitdir.read_text().strip())
        if not back_reference.is_absolute():
            back_reference = gitdir / back_reference
        return back_reference.resolve() == dot_git.resolve()
    except (OSError, UnicodeError, ValueError):
        return False


def _unmanaged_worktree_error(worktree: Path, base: Path) -> CmocError:
    """管理外worktreeを拒否するための共通エラーを作る。"""
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
    """linked worktreeからmain worktreeのrootを求める。"""
    return git_common_dir(root).parent


def _git_info_exclude_path(root: Path) -> Path:
    """Git の repository-local info/exclude path を返す。"""
    return (
        root / run_git(["rev-parse", "--git-path", "info/exclude"], root).stdout.strip()
    )


def _global_git_ignore_paths(root: Path) -> list[Path]:
    """Git が読む global excludes file の path を返す。"""
    configured = run_git(
        ["config", "--path", "--get-all", "core.excludesFile"],
        root,
        check=False,
    )
    if configured.returncode == 0:
        paths: list[Path] = []
        for line in configured.stdout.splitlines():
            if line:
                path = Path(line)
                resolved = path if path.is_absolute() else root / path
                # {{work-root}}/oracle/doc/app_spec/misc_spec.md
                # 同じ ignore source の検証結果を一度の列挙内で再利用する。
                if resolved not in paths:
                    paths.append(resolved)
        return paths
    config_home = os.environ.get("XDG_CONFIG_HOME")
    base = Path(config_home) if config_home else Path.home() / ".config"
    return [base / "git" / "ignore"]


def _validate_git_ignore_sources(
    root: Path,
    candidate: Path,
    *,
    strict_local: bool = False,
) -> None:
    """git check-ignore が読む ignore file を非通常 file でないと確認する。"""
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    root = root.absolute()
    relative = candidate.absolute().relative_to(root)
    validate_local = _validate_ignore_path if strict_local else _reject_non_file_path
    validate_local(root / ".gitignore", ".gitignore")
    validate_local(_git_info_exclude_path(root), "Git info/exclude")

    directory = root
    for part in relative.parts[:-1]:
        directory /= part
        try:
            mode = directory.lstat().st_mode
        except FileNotFoundError:
            break
        if not stat.S_ISDIR(mode):
            break
        _reject_non_file_path(directory / ".gitignore", "Git nested .gitignore")

    for path in _global_git_ignore_paths(root):
        _validate_global_git_ignore_path(path)


def _validate_global_git_ignore_path(path: Path) -> None:
    """global excludes の特殊 file を検証し、無害な /dev/null だけ許可する。"""
    if path.resolve() == Path(os.devnull).resolve():
        return
    _reject_non_file_path(path, "Git global excludes file")


def _git_ignore_error(command: list[str], result: CommandResult) -> CmocError:
    """check-ignore の判定不能を分類エラーへ変換する。"""
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    # file の分類条件を満たすか不明なまま、ignore されていない扱いにしてはならない。
    return CmocError(
        "Git ignore 判定に失敗しました。",
        ["Git repository と ignore source を確認してください。"],
        f"command: git {' '.join(command)}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}",
    )


def _check_git_ignore(root: Path, relative: Path, *, no_index: bool) -> bool:
    """check-ignore が受け付ける literal な repository 相対 path を判定する。"""
    args = ["check-ignore"]
    if no_index:
        args.append("--no-index")
    # check-ignore は :(literal) magic を受け付けないため、pathspec magic として
    # 解釈されない ./ を付けて path 名をそのまま渡す。
    command_args = [*args, "-q", "--", f"./{relative}"]
    result = run_git(command_args, root, check=False)
    if result.returncode not in {0, 1}:
        raise _git_ignore_error(command_args, result)
    return result.returncode == 0


def _cmoc_ignore_status(root: Path) -> tuple[str, int]:
    """.cmoc/gu の追跡有無と ignore 判定を取得する。"""
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # git check-ignore は repository-local、nested、global の ignore file を読むため、
    # FIFO などの非通常 file を拒否してからコマンドを実行する。
    _validate_git_ignore_sources(
        root,
        root / CMOC_IGNORE_PROBE,
        strict_local=True,
    )
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
    patterns: list[str] = []
    if any(line in {".cmoc/", "/.cmoc/"} for line in lines):
        patterns.extend(
            pattern for pattern in CMOC_CONFIG_IGNORE_EXCEPTIONS if pattern not in lines
        )
    if CMOC_IGNORE_PATTERN not in lines:
        patterns.append(CMOC_IGNORE_PATTERN)
    if not patterns:
        return content
    separator = "\n" if lines and lines[-1] != "" else ""
    newline = "" if content == "" or content.endswith("\n") else "\n"
    added = "\n".join(patterns)
    return f"{content}{newline}{separator}{added}\n"


def _reject_symlinked_path(path: Path, description: str) -> None:
    """cmoc が更新する ignore file を symlink 経由で扱わない。"""
    # Path.write_text() は symlink を追従するため、修復対象外への書き込みを防ぐ。
    if _first_symlink_component(path) is not None:
        raise CmocError(
            f"{description} は symlink 経由で更新できません。",
            ["ignore file の symlink を通常の file に戻してから再実行してください。"],
            str(path),
        )


def _reject_non_file_path(path: Path, description: str) -> None:
    """ignore file の読み書きを通常 file に限定する。"""
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # FIFO や device を read_text/write_text すると doctor が停止または block するため、
    # symlink 検査後に既存 path の種別を検証する。
    if path.exists() and not path.is_file():
        raise CmocError(
            f"{description} は通常の file ではありません。",
            [f"{description} を通常の file に戻してから再実行してください。"],
            str(path),
        )


def _validate_ignore_path(path: Path, description: str) -> None:
    """ignore file の symlink と非通常 file をまとめて拒否する。"""
    _reject_symlinked_path(path, description)
    _reject_non_file_path(path, description)


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
    - {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    exclude_path = _git_info_exclude_path(root)
    _validate_ignore_path(exclude_path, "Git info/exclude")
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
    """対象 path が owning repository で git ignore されるか判定する。"""
    candidate = path if path.is_absolute() else root / path
    repository = _repository_context_for_path(root, candidate)
    if repository is None:
        return False
    rel = candidate.absolute().relative_to(repository.absolute())
    _validate_git_ignore_sources(repository, candidate)
    return _check_git_ignore(repository, rel, no_index=True)


def is_untracked_git_ignored(root: Path, path: Path) -> bool:
    """未追跡 path が owning repository の通常 ignore 判定に一致するか返す。"""
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    # oracle/realization file の定義は通常の git check-ignore 挙動を使う。
    # ignore pattern に一致しても、追跡済み file は対象に残す。
    candidate = path if path.is_absolute() else root / path
    repository = _repository_context_for_path(root, candidate)
    if repository is None:
        return False
    return _is_untracked_git_ignored_in_repository(repository, candidate)


def _is_untracked_git_ignored_in_repository(repository: Path, candidate: Path) -> bool:
    """検証済み owning repository で単一候補の通常 ignore 判定を行う。"""
    rel = candidate.absolute().relative_to(repository.absolute())
    _validate_git_ignore_sources(repository, candidate)
    return _check_git_ignore(repository, rel, no_index=False)


def enumerate_oracle_and_realization_files(
    root: Path,
) -> tuple[list[Path], list[Path]]:
    """work root の oracle file と realization file を一括列挙する。

    根拠: {{work-root}}/oracle/doc/app_spec/misc_spec.md
    """
    # 常時対象外 root と検証済み Git metadata だけを事前 pruning し、ignored
    # directory も含む残りの tree から regular file と symlink を収集する。
    work_root = root.absolute()
    candidates_by_repository: dict[Path, list[Path]] = {}
    _collect_file_inventory_candidates(
        work_root,
        work_root,
        work_root,
        candidates_by_repository,
    )

    # Git ignore は owning repository ごとに source を一度検証し、候補全件を
    # 一括判定する。候補数を増やしても subprocess 数を増やさない。
    included: list[Path] = []
    for repository, candidates in sorted(
        candidates_by_repository.items(), key=lambda item: item[0].as_posix()
    ):
        _validate_git_ignore_sources(repository, repository)
        ignored = _batch_untracked_git_ignored(repository, candidates)
        for candidate in candidates:
            if candidate in ignored:
                continue
            if not _is_regular_file(candidate):
                raise _file_inventory_error(
                    candidate,
                    "symlink が untracked かつ ignored ではありません。",
                )
            included.append(candidate)

    # Git 判定後の regular file を repository path だけで分類する。
    oracle_files: list[Path] = []
    realization_files: list[Path] = []
    for candidate in included:
        classification = _file_classification(work_root, candidate)
        if classification == "oracle":
            oracle_files.append(candidate)
        elif classification == "realization":
            realization_files.append(candidate)
    return sorted(oracle_files), sorted(realization_files)


def _collect_file_inventory_candidates(
    work_root: Path,
    directory: Path,
    owning_repository: Path,
    candidates_by_repository: dict[Path, list[Path]],
) -> None:
    """directory 直下を lstat し、pruning 後の候補 path を収集する。"""
    # 同じ directory の `.git` を他 entry より先に検証し、直下の file にも
    # 最内側の repository context を適用する。
    entries = _lstat_directory_entries(directory)
    current_repository = owning_repository
    nested_git_metadata: Path | None = None
    if directory != work_root:
        git_entry = next(
            ((path, mode) for path, mode in entries if path.name == ".git"), None
        )
        if git_entry is not None:
            git_path, git_mode = git_entry
            _require_inventory_entry_kind(git_path, git_mode)
            if _is_git_worktree_root(directory):
                current_repository = directory
                nested_git_metadata = git_path

    for path, mode in entries:
        is_root_exclusion = (
            directory == work_root and path.name in _FILE_INVENTORY_EXCLUDED_ROOT_NAMES
        )
        if is_root_exclusion or path == nested_git_metadata:
            _require_inventory_entry_kind(path, mode)
            continue

        if stat.S_ISDIR(mode):
            _collect_file_inventory_candidates(
                work_root,
                path,
                current_repository,
                candidates_by_repository,
            )
        elif stat.S_ISREG(mode) or stat.S_ISLNK(mode):
            candidates_by_repository.setdefault(current_repository, []).append(path)
        else:
            raise _file_inventory_error(
                path, "directory、regular file、または symlink ではありません。"
            )


def _lstat_directory_entries(directory: Path) -> list[tuple[Path, int]]:
    """directory entry を symlink 非追跡で検証して path 順に返す。"""
    try:
        with os.scandir(directory) as iterator:
            entries = [
                (Path(entry.path), entry.stat(follow_symlinks=False).st_mode)
                for entry in iterator
            ]
    except OSError as exc:
        raise _file_inventory_error(
            directory, f"directory を走査できません: {exc}"
        ) from exc
    return sorted(entries, key=lambda item: item[0].name)


def _require_inventory_entry_kind(path: Path, mode: int) -> None:
    """列挙領域と pruning 境界を directory または regular file に限定する。"""
    if stat.S_ISDIR(mode) or stat.S_ISREG(mode):
        return
    raise _file_inventory_error(path, "directory または regular file ではありません。")


def _is_git_worktree_root(directory: Path) -> bool:
    """directory 直下の `.git` が実際の working tree metadata か確認する。"""
    result = run_git(
        ["rev-parse", "--path-format=absolute", "--show-toplevel"],
        directory,
        check=False,
    )
    if result.returncode != 0:
        return False
    reported = result.stdout.strip()
    return bool(reported) and Path(reported).resolve() == directory.resolve()


def _repository_context_for_path(root: Path, candidate: Path) -> Path | None:
    """単一 path を所有する最内側の検証済み Git working tree を返す。"""
    work_root = root.absolute()
    absolute_candidate = candidate.absolute()
    try:
        relative_candidate = absolute_candidate.relative_to(work_root)
    except ValueError:
        return None
    if ".." in relative_candidate.parts:
        return None

    # {{work-root}}/oracle/doc/app_spec/misc_spec.md
    # symlink の親を通る path は参照先を repository context や分類へ混入させるため、
    # 最終 component の symlink path だけを扱う ignore 判定と区別して拒否する。
    parent = work_root
    for part in relative_candidate.parts[:-1]:
        parent /= part
        try:
            metadata = parent.lstat()
        except FileNotFoundError:
            break
        except OSError as exc:
            raise _file_inventory_error(
                parent, f"path を検証できません: {exc}"
            ) from exc
        if stat.S_ISLNK(metadata.st_mode):
            return None
    if absolute_candidate == work_root:
        return work_root

    # 深い ancestor から調べ、nested repository の metadata 自体は分類しない。
    directory = absolute_candidate.parent
    while directory != work_root:
        metadata_path = directory / ".git"
        try:
            mode = metadata_path.lstat().st_mode
        except FileNotFoundError:
            directory = directory.parent
            continue
        except OSError as exc:
            raise _file_inventory_error(
                metadata_path, f"Git metadata を検証できません: {exc}"
            ) from exc
        _require_inventory_entry_kind(metadata_path, mode)
        if _is_git_worktree_root(directory):
            if (
                absolute_candidate == metadata_path
                or metadata_path in absolute_candidate.parents
            ):
                return None
            return directory
        directory = directory.parent
    return work_root


def _batch_untracked_git_ignored(repository: Path, candidates: list[Path]) -> set[Path]:
    """候補を通常の index-aware な check-ignore で一括判定する。"""
    if not candidates:
        return set()

    encoded_candidates: dict[bytes, Path] = {}
    for candidate in candidates:
        relative = candidate.relative_to(repository).as_posix()
        encoded_candidates[os.fsencode(f"./{relative}")] = candidate
    payload = b"".join(path + b"\0" for path in encoded_candidates)
    result = subprocess.run(
        ["git", "check-ignore", "--stdin", "-z"],
        cwd=repository,
        input=payload,
        capture_output=True,
    )
    if result.returncode not in {0, 1}:
        raise _git_ignore_error(
            ["check-ignore", "--stdin", "-z"],
            CommandResult(
                result.returncode,
                result.stdout.decode(errors="replace"),
                result.stderr.decode(errors="replace"),
            ),
        )

    ignored: set[Path] = set()
    for output_path in result.stdout.split(b"\0"):
        if not output_path:
            continue
        matched_candidate = encoded_candidates.get(output_path)
        if matched_candidate is None:
            raise CmocError(
                "Git ignore 判定に失敗しました。",
                ["Git repository と候補 path を確認してください。"],
                f"unexpected check-ignore output: {os.fsdecode(output_path)!r}",
            )
        ignored.add(matched_candidate)
    return ignored


def _file_classification(root: Path, candidate: Path) -> _FileClassification | None:
    """対象外条件適用後の repository path を oracle/realization に分類する。"""
    try:
        relative = candidate.absolute().relative_to(root.absolute())
    except ValueError:
        return None
    if (
        not relative.parts
        or ".." in relative.parts
        or candidate.name in _FILE_INVENTORY_EXCLUDED_FILE_NAMES
    ):
        return None
    if relative.parts[0] == "oracle":
        return "oracle"
    if relative.parts[0] in _FILE_INVENTORY_EXCLUDED_ROOT_NAMES:
        return None
    return "realization"


def _is_regular_file(path: Path) -> bool:
    """path 自身が symlink 非追跡で regular file か返す。"""
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except OSError:
        return False


def _path_exists_without_following_symlinks(path: Path) -> bool:
    """dangling symlink を含め、path entry 自身が存在するか返す。"""
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    except OSError:
        return True
    return True


def _file_inventory_error(path: Path, reason: str) -> CmocError:
    """oracle/realization file 列挙の path 種別エラーを構築する。"""
    return CmocError(
        "oracle/realization file を列挙できません。",
        ["対象 path を directory または regular file に戻して再実行してください。"],
        f"path: {path}\nreason: {reason}",
    )


def is_realization_file_path(
    root: Path,
    path: Path,
    *,
    branch: str | None = None,
) -> bool:
    """repository path と Git 状態から realization file か判定する。

    apply worktree が無い復旧経路では branch の tree を追跡状態の正本にする。
    根拠:
    {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    """
    candidate = path if path.is_absolute() else root / path
    if _file_classification(root, candidate) != "realization":
        return False
    repository = _repository_context_for_path(root, candidate)
    if repository is None:
        return False
    relative = candidate.absolute().relative_to(root.absolute())
    if branch and not _path_exists_without_following_symlinks(candidate):
        # Gitlink は tree entry だが filesystem 上は directory なので、file 定義に
        # 含めず regular blob entry だけを branch の fallback として採用する。
        # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
        # branch の blob は削除された path の追跡状態を補うが、現在の directory や
        # FIFO などの特殊 file を file として扱う根拠にはならない。
        branch_entries = run_git(
            [
                "ls-tree",
                "-r",
                "-z",
                branch,
                "--",
                literal_pathspec(relative.as_posix()),
            ],
            root,
        ).stdout.split("\0")
        for entry in branch_entries:
            metadata, separator, entry_path = entry.partition("\t")
            metadata_fields = metadata.split()
            if separator and entry_path == relative.as_posix():
                try:
                    entry_mode = int(metadata_fields[0], 8)
                except (IndexError, ValueError):
                    continue
                if stat.S_ISREG(entry_mode):
                    return True
        return False
    if not _is_regular_file(candidate):
        return False
    return not _is_untracked_git_ignored_in_repository(repository, candidate)


def is_oracle_file_path(root: Path, path: Path) -> bool:
    """repository pathと追跡状態からoracle fileに該当するか判定する。"""
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    # oracle file の定義は Codex access check と apply/session の差分分類の両方から
    # 使うため、一つの runtime helper に集約する。
    # {{work-root}}/oracle/doc/app_spec/misc_spec.md
    # 列挙対象と同じく、symlink を追跡せず regular file だけを分類する。
    candidate = path if path.is_absolute() else root / path
    if _file_classification(root, candidate) != "oracle" or not _is_regular_file(
        candidate
    ):
        return False
    repository = _repository_context_for_path(root, candidate)
    return repository is not None and not _is_untracked_git_ignored_in_repository(
        repository, candidate
    )
