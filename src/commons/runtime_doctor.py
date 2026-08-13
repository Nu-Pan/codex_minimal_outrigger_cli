"""doctor preprocess の修復・一時 index・commit lifecycle を扱う。

この file は 16,000 文字を超えるが、doctor lock、修復対象の同期、一時 index の
退避・合成・復元、および修復 commit は同じ Git common directory と index の
不変条件を共有する一つの lifecycle である。分割すると、失敗時の index 復元と
commit 対象の対応を複数 file で追う必要が生じるため、現状は doctor preprocess
の境界として一箇所に保つ。

根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import fcntl
import os
import shutil
import subprocess
import tempfile
from collections.abc import Collection, Iterator
from contextlib import contextmanager
from pathlib import Path

from .runtime_config import sync_config
from .runtime_errors import CmocError
from .runtime_feedback import (
    ReporterAvailabilityError,
    emit_reporter_unavailable,
    validate_feedback_reporter_availability,
)
from .runtime_git import (
    ensure_cmoc_ignored,
    git_common_dir,
    require_cmoc_ignored,
    run_git,
    with_cmoc_ignore_pattern,
)
from .runtime_paths import config_path, refactor_state_path, repo_root
from .runtime_refactor import sync_refactor_state


def run_doctor_preprocess(
    root: Path,
    *,
    sync_refactor_entries: bool = True,
) -> None:
    """current と main worktree の共通修復を排他実行し、修復差分だけを commit する。"""
    root = root.resolve()
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # snapshot 作成から修復 commit と元の index 復元までを同じ Git common
    # directory の lock 内で行い、並行 doctor が共有 index を混ぜないようにする。
    with doctor_lock(root):
        main_root = repo_root(root)
        repair_roots = [main_root] if main_root == root else [main_root, root]

        repairs: list[tuple[Path, Path, bool, bool, bool, set[str]]] = []
        original_indexes: list[tuple[Path, Path]] = []
        try:
            for repair_root in repair_roots:
                include_config = repair_root == root
                include_agents = repair_root == root
                include_gu_ignore = repair_root == main_root
                original_index_path = _copy_current_index(repair_root)
                original_indexes.append((repair_root, original_index_path))
                preserved_runtime_paths = (
                    _preexisting_runtime_paths(repair_root, original_index_path)
                    if include_config
                    else set()
                )
                # ensure_cmoc_ignored と _ensure_agents_tracked は通常 index を
                # 変更するため、後続処理の失敗時も元の staged 状態へ戻せるようにする。
                if include_gu_ignore:
                    ensure_cmoc_ignored(repair_root)
                agents_gitkeep_added = (
                    _ensure_agents_tracked(repair_root) if include_agents else False
                )
                repairs.append(
                    (
                        repair_root,
                        original_index_path,
                        agents_gitkeep_added,
                        include_config,
                        include_gu_ignore,
                        preserved_runtime_paths,
                    )
                )

            # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
            # ignore と .agents の保証後に、config と refactor state を current
            # work-root だけで同期する。index には直接触れず、後続の一時 index
            # で他の doctor 修復と同じ commit にまとめる。
            sync_config(root)
            sync_refactor_state(root, sync_entries=sync_refactor_entries)
            # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
            # reporter 固有の不一致は修復や version command を行わず degraded にする。
            try:
                validate_feedback_reporter_availability()
            except ReporterAvailabilityError as exc:
                emit_reporter_unavailable(exc.component, exc.failure_code)
        except BaseException:
            for repair_root, original_index_path in original_indexes:
                try:
                    _restore_index(repair_root, original_index_path)
                finally:
                    original_index_path.unlink(missing_ok=True)
            raise

        for (
            repair_root,
            original_index_path,
            agents_gitkeep_added,
            include_config,
            include_gu_ignore,
            preserved_runtime_paths,
        ) in repairs:
            restored_index_path: Path | None = None
            try:
                restored_index_path = _restored_index(
                    repair_root,
                    original_index_path=original_index_path,
                    include_config=include_config,
                    include_agents=repair_root == root,
                    include_gu_ignore=include_gu_ignore,
                    preserved_runtime_paths=preserved_runtime_paths,
                )
                _commit_doctor_repairs(
                    repair_root,
                    restored_index_path,
                    original_index_path,
                    agents_gitkeep_added,
                    include_config=include_config,
                    include_gu_ignore=include_gu_ignore,
                    preserved_runtime_paths=preserved_runtime_paths,
                )
            except BaseException:
                if restored_index_path is None:
                    _restore_index(repair_root, original_index_path)
                raise
            finally:
                if restored_index_path is not None:
                    restored_index_path.unlink(missing_ok=True)
                original_index_path.unlink(missing_ok=True)
        require_cmoc_ignored(main_root)
        _validate_tracked_runtime_files(root)


@contextmanager
def doctor_lock(root: Path) -> Iterator[None]:
    """Git common directory 単位の doctor 用 process lock を保持する。"""
    lock_path = doctor_lock_path(root)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def doctor_lock_path(root: Path) -> Path:
    """Git common directory 内の doctor lock file path を返す。"""
    return git_common_dir(root) / "cmoc-doctor.lock"


def _ensure_agents_tracked(root: Path) -> bool:
    """.agentsの追跡用placeholderを準備し、追加したかを返す。"""
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # .agents は agent 操作禁止領域なので、tracked file がない場合だけ
    # placeholder を追加して差分が出る余地を小さくする。
    agents = root / ".agents"
    _validate_agents_paths(root)
    agents.mkdir(exist_ok=True)
    tracked = bool(run_git(["ls-files", "--", ".agents"], root).stdout.strip())
    gitkeep = agents / ".gitkeep"
    if tracked:
        # tracked な .gitkeep の unstaged deletion でも、.agents を空のまま残さない。
        if not gitkeep.exists():
            restored = run_git(
                ["restore", "--worktree", "--", ".agents/.gitkeep"],
                root,
                check=False,
            )
            if restored.returncode != 0 and _head_entry(root, ".agents/.gitkeep"):
                run_git(
                    [
                        "restore",
                        "--source=HEAD",
                        "--worktree",
                        "--",
                        ".agents/.gitkeep",
                    ],
                    root,
                )
        return False
    _validate_agents_paths(root)
    if not gitkeep.exists() and _head_entry(root, ".agents/.gitkeep"):
        run_git(
            ["restore", "--source=HEAD", "--worktree", "--", ".agents/.gitkeep"],
            root,
        )
    else:
        gitkeep.touch(exist_ok=True)
    run_git(["add", "-f", ".agents/.gitkeep"], root)
    if not run_git(["ls-files", "--", ".agents"], root).stdout.strip():
        raise CmocError(
            ".agents を git 追跡対象にできませんでした。",
            [".agents/.gitkeep と git index の状態を確認してください。"],
            str(agents),
        )
    return True


def _validate_agents_paths(root: Path) -> None:
    """.agents の doctor 書き込み対象を通常の directory/file に限定する。"""
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # symlink 経由の mkdir/touch は .agents 外へ書き込むため、修復前に拒否する。
    agents = root / ".agents"
    gitkeep = agents / ".gitkeep"
    if agents.is_symlink() or gitkeep.is_symlink():
        path = agents if agents.is_symlink() else gitkeep
        raise CmocError(
            ".agents は symlink 経由で修復できません。",
            [
                ".agents と .agents/.gitkeep を通常の directory/file に戻してから再実行してください。"
            ],
            str(path),
        )
    if agents.exists() and not agents.is_dir():
        raise CmocError(
            ".agents が directory ではありません。",
            [".agents を通常の directory に戻してから再実行してください。"],
            str(agents),
        )
    if gitkeep.exists() and not gitkeep.is_file():
        raise CmocError(
            ".agents/.gitkeep が通常の file ではありません。",
            [".agents/.gitkeep を通常の file に戻してから再実行してください。"],
            str(gitkeep),
        )


def _validate_tracked_runtime_files(root: Path) -> None:
    """同期済み config と refactor state が Git index に存在するか検証する。"""
    expected = {
        str(config_path(root).relative_to(root)),
        str(refactor_state_path(root).relative_to(root)),
    }
    tracked = set(
        run_git(["ls-files", "--", *sorted(expected)], root).stdout.splitlines()
    )
    if tracked != expected:
        raise CmocError(
            "cmoc の追跡対象 state を git index に登録できませんでした。",
            ["config、refactor state、git index、.gitignore を確認してください。"],
            f"expected: {sorted(expected)}\ntracked: {sorted(tracked)}",
        )


def _preexisting_runtime_paths(root: Path, index_path: Path) -> set[str]:
    """doctor 開始前から差分がある runtime path を repair 対象から外す。"""
    # {{work-root}}/oracle/src/oracle/other/cmoc_config.py
    # config は人間が編集するため、既存の staged/unstaged 変更を doctor の
    # repair commit に混ぜない。state も同じ一時 index で扱うため同じ境界にする。
    paths = {
        str(config_path(root).relative_to(root)),
        str(refactor_state_path(root).relative_to(root)),
    }
    return {
        path
        for path in paths
        if _path_changed_before_doctor(root, index_path, path)
        and _index_has_entry(root, index_path, path)
    }


def _path_changed_before_doctor(root: Path, index_path: Path, path: str) -> bool:
    """元 index と worktree のどちらかに doctor 前の差分があるか返す。"""
    staged = _run_git_with_index(
        ["diff", "--cached", "--name-only", "HEAD", "--", path],
        root,
        index_path,
    ).stdout
    unstaged = _run_git_with_index(
        ["diff", "--name-only", "--", path],
        root,
        index_path,
    ).stdout
    return bool(staged.strip() or unstaged.strip())


def _index_has_entry(root: Path, index_path: Path, path: str) -> bool:
    """一時 index に path の entry があるか返す。"""
    return bool(
        _run_git_with_index(
            ["ls-files", "--stage", "--", path],
            root,
            index_path,
            check=False,
        ).stdout.strip()
    )


def _commit_doctor_repairs(
    root: Path,
    restored_index_path: Path,
    original_index_path: Path,
    agents_gitkeep_added: bool,
    *,
    include_config: bool,
    include_gu_ignore: bool,
    preserved_runtime_paths: set[str],
) -> None:
    """doctorの修復差分をcommitし、呼び出し元のGit indexを復元する。"""
    try:
        _commit_doctor_repairs_from_head(
            root,
            agents_gitkeep_added,
            include_config=include_config,
            include_gu_ignore=include_gu_ignore,
            preserved_runtime_paths=preserved_runtime_paths,
        )
    except BaseException:
        _restore_index(root, original_index_path)
        raise
    else:
        _restore_index(root, restored_index_path)


def _restore_index(root: Path, index_path: Path) -> None:
    """一時 index の内容を現在の Git index へ復元する。"""

    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # tree 化では index 固有状態が失われるため、一時 index file 自体を復元する。
    shutil.copyfile(index_path, _current_index_path(root))


def _commit_doctor_repairs_from_head(
    root: Path,
    agents_gitkeep_added: bool,
    *,
    include_config: bool,
    include_gu_ignore: bool,
    preserved_runtime_paths: set[str],
) -> None:
    """HEAD起点の一時indexでdoctor修復だけをcommitする。"""
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # repair commit は doctor の作業差分だけなので、通常 index ではなく
    # HEAD 起点の一時 index で user staged hunks と同一 path 上でも分離する。
    fd, index_name = tempfile.mkstemp(prefix="cmoc-doctor-index-")
    os.close(fd)
    index_path = Path(index_name)
    try:
        _run_git_with_index(["read-tree", "HEAD"], root, index_path)
        if include_gu_ignore:
            _stage_gitignore_repair(root, index_path)
        _stage_agents_gitkeep_repair(root, index_path, agents_gitkeep_added)
        if include_config:
            _stage_tracked_runtime_repair(
                root,
                index_path,
                skip_paths=preserved_runtime_paths,
            )
        if include_gu_ignore:
            _run_git_with_index(
                ["rm", "--cached", "-f", "-r", "--ignore-unmatch", ".cmoc/gu"],
                root,
                index_path,
            )
        paths = _run_git_with_index(
            ["diff", "--cached", "--name-only"], root, index_path
        ).stdout.splitlines()
        if paths:
            _run_git_with_index(
                ["commit", "-m", "cmoc doctor preprocess"], root, index_path
            )
    finally:
        index_path.unlink(missing_ok=True)


def _stage_gitignore_repair(root: Path, index_path: Path) -> None:
    """HEADの.gitignoreへcmoc ignore規則を一時index上で反映する。"""
    head = run_git(["show", "HEAD:.gitignore"], root, check=False)
    head_content = head.stdout if head.returncode == 0 else ""
    repaired = with_cmoc_ignore_pattern(head_content)
    if repaired != head_content:
        _stage_text(root, index_path, ".gitignore", repaired)


def _stage_agents_gitkeep_repair(
    root: Path, index_path: Path, agents_gitkeep_added: bool
) -> None:
    """doctorが追加した.agents placeholderを修復用indexへ載せる。"""
    # 現在 index に doctor が追加した repair を HEAD 起点の index にも載せる。
    # HEAD に既存の .gitkeep があれば、その blob と mode を repair commit に使う。
    if agents_gitkeep_added:
        _stage_agents_gitkeep(root, index_path)


def _restored_index(
    root: Path,
    *,
    original_index_path: Path,
    include_config: bool,
    include_agents: bool,
    include_gu_ignore: bool,
    preserved_runtime_paths: set[str],
) -> Path:
    """doctor 修復を合成した一時 index file を作る。"""
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # 復元対象は path 列挙ではなく index 全体で扱い、rename や unstaged hunk を保つ。
    index_path = _copy_current_index(root)
    try:
        # 修復 commit は HEAD を更新するが、復元 index では利用者の staged deletion を保つ。
        if include_gu_ignore and not _is_staged_deletion_of_head_entry(
            root, original_index_path, ".gitignore"
        ):
            _stage_gitignore_repair_from_index(root, index_path)
        if include_agents:
            _stage_agents_gitkeep_repair_from_index(root, index_path)
        if include_config:
            _stage_tracked_runtime_repair(
                root,
                index_path,
                skip_paths=preserved_runtime_paths,
            )
        if include_gu_ignore:
            _run_git_with_index(
                ["rm", "--cached", "-f", "-r", "--ignore-unmatch", ".cmoc/gu"],
                root,
                index_path,
            )
        _run_git_with_index(["write-tree"], root, index_path)
        return index_path
    except BaseException:
        index_path.unlink(missing_ok=True)
        raise


def _copy_current_index(root: Path) -> Path:
    """現在の Git index を一時 file へ退避し、存在しなければ HEAD から作る。"""

    fd, index_name = tempfile.mkstemp(prefix="cmoc-doctor-restore-index-")
    os.close(fd)
    index_path = Path(index_name)
    try:
        current_index = _current_index_path(root)
        if current_index.exists():
            shutil.copy2(current_index, index_path)
        else:
            # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
            _run_git_with_index(["read-tree", "HEAD"], root, index_path)
            # 修復処理の Git command は通常の index を参照するため、index が
            # 欠落していた場合も HEAD の完全な index を先に復元する。
            shutil.copyfile(index_path, current_index)
        return index_path
    except BaseException:
        index_path.unlink(missing_ok=True)
        raise


def _current_index_path(root: Path) -> Path:
    """Git が現在使用している index file の path を返す。"""

    return root / run_git(["rev-parse", "--git-path", "index"], root).stdout.strip()


def _stage_gitignore_repair_from_index(root: Path, index_path: Path) -> None:
    """現在のindexにある.gitignoreへcmoc ignore規則を反映する。"""
    current = _index_text(root, index_path, ".gitignore")
    repaired = with_cmoc_ignore_pattern(current or "")
    if repaired != (current or ""):
        _stage_text(root, index_path, ".gitignore", repaired)


def _stage_agents_gitkeep_repair_from_index(root: Path, index_path: Path) -> None:
    """.agentsがindexにない場合にplaceholderをindexへ追加する。"""
    agents = _run_git_with_index(
        ["ls-files", "--", ".agents"], root, index_path
    ).stdout.strip()
    if not agents:
        _stage_agents_gitkeep(root, index_path)


def _stage_agents_gitkeep(root: Path, index_path: Path) -> None:
    """既存blobを優先して.agents placeholderを一時indexへ載せる。"""
    # doctor が現在の index に追加した内容を repair commit にも使い、既存の
    # 未追跡 .gitkeep の内容を空 blobへ置き換えない。
    current = run_git(
        ["ls-files", "--stage", "--", ".agents/.gitkeep"],
        root,
        check=False,
    )
    current_fields = current.stdout.split()
    if current.returncode == 0 and len(current_fields) >= 3:
        _stage_blob(
            root,
            index_path,
            ".agents/.gitkeep",
            current_fields[0],
            current_fields[1],
        )
        return
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # HEAD に既存の placeholder がある場合は、復元用 index と repair commit 用
    # index の双方で同じ blob/mode を参照する。新規作成時だけ空 blob にする。
    entry = _head_entry(root, ".agents/.gitkeep")
    if entry is None:
        _stage_text(root, index_path, ".agents/.gitkeep", "")
        return
    mode, blob = entry
    _stage_blob(root, index_path, ".agents/.gitkeep", mode, blob)


def _stage_tracked_runtime_repair(
    root: Path,
    index_path: Path,
    *,
    skip_paths: Collection[str] = (),
) -> None:
    """同期済み config/state を ignore 規則に左右されず一時 index へ載せる。"""
    for path in (config_path(root), refactor_state_path(root)):
        relative = str(path.relative_to(root))
        if relative in skip_paths:
            continue
        _stage_text(root, index_path, relative, path.read_text())


def _is_staged_deletion_of_head_entry(
    root: Path,
    index_path: Path,
    path: str,
) -> bool:
    """元 index が HEAD の tracked path を staged deletion にしているか返す。"""
    if _head_entry(root, path) is None:
        return False
    return not _run_git_with_index(
        ["ls-files", "--stage", "--", path],
        root,
        index_path,
    ).stdout.strip()


def _index_text(root: Path, index_path: Path, path: str) -> str | None:
    """一時indexからpathの内容を読み、未登録ならNoneを返す。"""
    result = _run_git_with_index(["show", f":{path}"], root, index_path, check=False)
    if result.returncode != 0:
        return None
    return result.stdout


def _stage_text(root: Path, index_path: Path, path: str, content: str) -> None:
    """テキスト内容をblob化して一時indexへ登録する。"""
    blob = _run_git_with_index(
        ["hash-object", "-w", "--stdin"], root, index_path, input_text=content
    ).stdout.strip()
    mode = _index_mode(root, index_path, path)
    if mode is None:
        entry = _head_entry(root, path)
        mode = entry[0] if entry else "100644"
    _stage_blob(root, index_path, path, mode, blob)


def _stage_blob(root: Path, index_path: Path, path: str, mode: str, blob: str) -> None:
    """指定blobとmodeを一時indexのpathへ登録する。"""
    _run_git_with_index(
        ["update-index", "--add", "--cacheinfo", mode, blob, path],
        root,
        index_path,
    )


def _run_git_with_index(
    args: list[str],
    root: Path,
    index_path: Path,
    input_text: str | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """指定した一時Git indexでコマンドを実行する。"""
    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = str(index_path)
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        env=env,
        input=input_text,
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        raise CmocError(
            "git コマンドが失敗しました。",
            ["git の状態を確認してから、同じ cmoc コマンドを再実行してください。"],
            f"command: git {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
    return result


def _head_entry(root: Path, path: str) -> tuple[str, str] | None:
    """HEAD treeからpathのmodeとblobを取得する。"""
    result = run_git(["ls-tree", "HEAD", "--", path], root, check=False)
    metadata = result.stdout.split("\t", 1)[0].split()
    if result.returncode != 0 or len(metadata) < 3:
        return None
    return metadata[0], metadata[2]


def _index_mode(root: Path, index_path: Path, path: str) -> str | None:
    """一時indexに登録されたpathのfile modeを返す。"""
    result = _run_git_with_index(
        ["ls-files", "--stage", "--", path], root, index_path, check=False
    )
    if result.returncode != 0 or not result.stdout:
        return None
    return result.stdout.split(maxsplit=1)[0]
