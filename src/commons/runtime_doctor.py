import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from config.cmoc_config import CmocConfig

from commons.runtime_errors import CmocError
from commons.runtime_git import ensure_cmoc_ignored, run_git, with_cmoc_ignore_pattern
from commons.runtime_ollama import ensure_ollama_serves_local_slm
from commons.runtime_paths import repo_root


def run_doctor_preprocess(root: Path, config: CmocConfig | None = None) -> None:
    """current と main worktree の共通修復を行い、修復差分だけを commit する。"""
    root = root.resolve()
    repair_roots = [root]
    main_root = repo_root(root)
    if main_root != root:
        # <work-root>/oracle/doc/app_spec/doctor_preprocess.md
        # サブコマンドログは doctor 開始前に main worktree 側へ作られるため、
        # linked worktree 実行時も両方の .cmoc/local を ignore 対象にする。
        repair_roots.append(main_root)

    repairs: list[tuple[Path, str, bool]] = []
    for repair_root in repair_roots:
        restored_index_tree = _restored_index_tree(repair_root)
        ensure_cmoc_ignored(repair_root)
        agents_gitkeep_added = _ensure_agents_tracked(repair_root)
        repairs.append((repair_root, restored_index_tree, agents_gitkeep_added))

    ensure_ollama_serves_local_slm(root, config)
    for repair_root, restored_index_tree, agents_gitkeep_added in repairs:
        _commit_doctor_repairs(
            repair_root, restored_index_tree, agents_gitkeep_added
        )


def _ensure_agents_tracked(root: Path) -> bool:
    # <work-root>/oracle/doc/app_spec/doctor_preprocess.md
    # .agents は agent 操作禁止領域なので、tracked file がない場合だけ
    # placeholder を追加して差分が出る余地を小さくする。
    agents = root / ".agents"
    agents.mkdir(exist_ok=True)
    if run_git(["ls-files", "--", ".agents"], root).stdout.strip():
        return False
    gitkeep = agents / ".gitkeep"
    gitkeep.touch(exist_ok=True)
    run_git(["add", "-f", ".agents/.gitkeep"], root)
    if not run_git(["ls-files", "--", ".agents"], root).stdout.strip():
        raise CmocError(
            ".agents を git 追跡対象にできませんでした。",
            [".agents/.gitkeep と git index の状態を確認してください。"],
            str(agents),
        )
    return True


def _commit_doctor_repairs(
    root: Path, restored_index_tree: str, agents_gitkeep_added: bool
) -> None:
    _commit_doctor_repairs_from_head(root, agents_gitkeep_added)
    try:
        run_git(["reset", "-q", "HEAD"], root)
    finally:
        run_git(["read-tree", restored_index_tree], root)


def _commit_doctor_repairs_from_head(root: Path, agents_gitkeep_added: bool) -> None:
    # <work-root>/oracle/doc/app_spec/doctor_preprocess.md
    # repair commit は doctor の作業差分だけなので、通常 index ではなく
    # HEAD 起点の一時 index で user staged hunks と同一 path 上でも分離する。
    fd, index_name = tempfile.mkstemp(prefix="cmoc-doctor-index-")
    os.close(fd)
    index_path = Path(index_name)
    try:
        _run_git_with_index(["read-tree", "HEAD"], root, index_path)
        _stage_gitignore_repair(root, index_path)
        _stage_agents_gitkeep_repair(root, index_path, agents_gitkeep_added)
        _run_git_with_index(
            ["rm", "--cached", "-r", "--ignore-unmatch", ".cmoc/local"],
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
    head = run_git(["show", "HEAD:.gitignore"], root, check=False)
    head_content = head.stdout if head.returncode == 0 else ""
    repaired = with_cmoc_ignore_pattern(head_content)
    if repaired != head_content:
        _stage_text(root, index_path, ".gitignore", repaired)


def _stage_agents_gitkeep_repair(
    root: Path, index_path: Path, agents_gitkeep_added: bool
) -> None:
    # 現在 index に doctor が追加した repair を HEAD 起点の index にも載せる。
    # HEAD に既存の .agents file があっても、それを repair commit から落とさない。
    if agents_gitkeep_added:
        _stage_text(root, index_path, ".agents/.gitkeep", "")


def _restored_index_tree(root: Path) -> str:
    # <work-root>/oracle/doc/app_spec/doctor_preprocess.md
    # 復元対象は path 列挙ではなく index 全体で扱う。rename や同一 path の
    # unstaged hunk を壊さず、doctor 優先の修復だけを合成した tree を戻す。
    index_path = _copy_current_index(root)
    try:
        _stage_gitignore_repair_from_index(root, index_path)
        _stage_agents_gitkeep_repair_from_index(root, index_path)
        _run_git_with_index(
            ["rm", "--cached", "-r", "--ignore-unmatch", ".cmoc/local"],
            root,
            index_path,
        )
        return _run_git_with_index(["write-tree"], root, index_path).stdout.strip()
    finally:
        index_path.unlink(missing_ok=True)


def _copy_current_index(root: Path) -> Path:
    fd, index_name = tempfile.mkstemp(prefix="cmoc-doctor-restore-index-")
    os.close(fd)
    index_path = Path(index_name)
    current_index = root / run_git(
        ["rev-parse", "--git-path", "index"], root
    ).stdout.strip()
    if current_index.exists():
        shutil.copy2(current_index, index_path)
    else:
        _run_git_with_index(["read-tree", "HEAD"], root, index_path)
    return index_path


def _stage_gitignore_repair_from_index(root: Path, index_path: Path) -> None:
    current = _index_text(root, index_path, ".gitignore")
    repaired = with_cmoc_ignore_pattern(current or "")
    if repaired != (current or ""):
        _stage_text(root, index_path, ".gitignore", repaired)


def _stage_agents_gitkeep_repair_from_index(root: Path, index_path: Path) -> None:
    agents = _run_git_with_index(
        ["ls-files", "--", ".agents"], root, index_path
    ).stdout.strip()
    if not agents:
        _stage_text(root, index_path, ".agents/.gitkeep", "")


def _index_text(root: Path, index_path: Path, path: str) -> str | None:
    result = _run_git_with_index(["show", f":{path}"], root, index_path, check=False)
    if result.returncode != 0:
        return None
    return result.stdout


def _stage_text(root: Path, index_path: Path, path: str, content: str) -> None:
    blob = _run_git_with_index(
        ["hash-object", "-w", "--stdin"], root, index_path, input_text=content
    ).stdout.strip()
    _run_git_with_index(
        ["update-index", "--add", "--cacheinfo", "100644", blob, path],
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

