import fcntl
import os
import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from commons.runtime_config import sync_config
from commons.runtime_errors import CmocError
from commons.runtime_git import (
    ensure_cmoc_ignored,
    git_common_dir,
    run_git,
    with_cmoc_ignore_pattern,
)
from commons.runtime_ollama import ensure_ollama_serves_local_slm
from commons.runtime_paths import config_path, refactor_state_path, repo_root
from commons.runtime_refactor import sync_refactor_state
from config.cmoc_config import CmocConfig


def run_doctor_preprocess(
    root: Path,
    config: CmocConfig | None = None,
    *,
    sync_refactor_entries: bool = True,
) -> None:
    """current と main worktree の共通修復を排他実行し、修復差分だけを commit する。"""
    root = root.resolve()
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # snapshot 作成から修復 commit と元の index 復元までを同じ Git common
    # directory の lock 内で行い、並行 doctor が共有 index を混ぜないようにする。
    with doctor_lock(root):
        repair_roots = [root]
        main_root = repo_root(root)
        if main_root != root:
            # サブコマンドログは doctor 開始前に main worktree 側へ作られるため、
            # linked worktree 実行時も両方の .cmoc/gu を ignore 対象にする。
            repair_roots.append(main_root)

        # config は worktree ごとの設定なので current work-root だけを同期する。
        # index にはまだ触れず、後続の一時 index で他の doctor 修復と同じ
        # commit にまとめる。
        synced_config = sync_config(root)
        sync_refactor_state(root, sync_entries=sync_refactor_entries)

        repairs: list[tuple[Path, str, bool, bool]] = []
        original_indexes: list[tuple[Path, str]] = []
        try:
            for repair_root in repair_roots:
                include_config = repair_root == root
                original_index_tree = _current_index_tree(repair_root)
                original_indexes.append((repair_root, original_index_tree))
                # ensure_cmoc_ignored と _ensure_agents_tracked は通常 index を
                # 変更するため、Ollama 失敗時も元の staged 状態へ戻せるようにする。
                ensure_cmoc_ignored(repair_root)
                agents_gitkeep_added = _ensure_agents_tracked(repair_root)
                repairs.append(
                    (
                        repair_root,
                        original_index_tree,
                        agents_gitkeep_added,
                        include_config,
                    )
                )

            # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
            # 初回 doctor が作る .gitignore も realization file 集合へ含め、doctor
            # 完了時点で refactor entry と実 file を一致させる。
            sync_refactor_state(root, sync_entries=sync_refactor_entries)
            ensure_ollama_serves_local_slm(root, config or synced_config)
        except BaseException:
            for repair_root, original_index_tree in original_indexes:
                _restore_index(repair_root, original_index_tree)
            raise

        for (
            repair_root,
            original_index_tree,
            agents_gitkeep_added,
            include_config,
        ) in repairs:
            restored_index_tree = _restored_index_tree(
                repair_root,
                include_config=include_config,
            )
            _commit_doctor_repairs(
                repair_root,
                restored_index_tree,
                original_index_tree,
                agents_gitkeep_added,
                include_config=include_config,
            )
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
    agents.mkdir(exist_ok=True)
    if run_git(["ls-files", "--", ".agents"], root).stdout.strip():
        return False
    gitkeep = agents / ".gitkeep"
    if (
        not gitkeep.exists()
        and not gitkeep.is_symlink()
        and _head_entry(root, ".agents/.gitkeep")
    ):
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


def _commit_doctor_repairs(
    root: Path,
    restored_index_tree: str,
    original_index_tree: str,
    agents_gitkeep_added: bool,
    *,
    include_config: bool,
) -> None:
    """doctorの修復差分をcommitし、呼び出し元のGit indexを復元する。"""
    try:
        _commit_doctor_repairs_from_head(
            root,
            agents_gitkeep_added,
            include_config=include_config,
        )
    except BaseException:
        _restore_index(root, original_index_tree)
        raise
    else:
        _restore_index(root, restored_index_tree)


def _restore_index(root: Path, restored_index_tree: str) -> None:
    """指定した tree へ Git index を戻す。"""
    try:
        run_git(["reset", "-q", "HEAD"], root)
    finally:
        run_git(["read-tree", restored_index_tree], root)


def _current_index_tree(root: Path) -> str:
    """現在の Git index を tree object として保存する。"""
    index_path = _copy_current_index(root)
    try:
        return _run_git_with_index(["write-tree"], root, index_path).stdout.strip()
    finally:
        index_path.unlink(missing_ok=True)


def _commit_doctor_repairs_from_head(
    root: Path,
    agents_gitkeep_added: bool,
    *,
    include_config: bool,
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
        _stage_gitignore_repair(root, index_path)
        _stage_agents_gitkeep_repair(root, index_path, agents_gitkeep_added)
        if include_config:
            _stage_tracked_runtime_repair(root, index_path)
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


def _restored_index_tree(root: Path, *, include_config: bool) -> str:
    """doctor修復後に戻すべきGit index treeを一時indexから作る。"""
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # 復元対象は path 列挙ではなく index 全体で扱う。rename や同一 path の
    # unstaged hunk を壊さず、doctor 優先の修復だけを合成した tree を戻す。
    index_path = _copy_current_index(root)
    try:
        _stage_gitignore_repair_from_index(root, index_path)
        _stage_agents_gitkeep_repair_from_index(root, index_path)
        if include_config:
            _stage_tracked_runtime_repair(root, index_path)
        _run_git_with_index(
            ["rm", "--cached", "-f", "-r", "--ignore-unmatch", ".cmoc/gu"],
            root,
            index_path,
        )
        return _run_git_with_index(["write-tree"], root, index_path).stdout.strip()
    finally:
        index_path.unlink(missing_ok=True)


def _copy_current_index(root: Path) -> Path:
    """現在のGit indexを一時ファイルへコピーして返す。"""
    fd, index_name = tempfile.mkstemp(prefix="cmoc-doctor-restore-index-")
    os.close(fd)
    index_path = Path(index_name)
    current_index = (
        root / run_git(["rev-parse", "--git-path", "index"], root).stdout.strip()
    )
    if current_index.exists():
        shutil.copy2(current_index, index_path)
    else:
        _run_git_with_index(["read-tree", "HEAD"], root, index_path)
    return index_path


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
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # HEAD に既存の placeholder がある場合は、復元用 index と repair commit 用
    # index の双方で同じ blob/mode を参照する。新規作成時だけ空 blob にする。
    entry = _head_entry(root, ".agents/.gitkeep")
    if entry is None:
        _stage_text(root, index_path, ".agents/.gitkeep", "")
        return
    mode, blob = entry
    _stage_blob(root, index_path, ".agents/.gitkeep", mode, blob)


def _stage_tracked_runtime_repair(root: Path, index_path: Path) -> None:
    """同期済み config/state を ignore 規則に左右されず一時 index へ載せる。"""
    for path in (config_path(root), refactor_state_path(root)):
        _stage_text(root, index_path, str(path.relative_to(root)), path.read_text())


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
