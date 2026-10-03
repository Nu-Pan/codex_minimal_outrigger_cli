"""doctor preprocess の修復・一時 index・commit lifecycle を扱う。

この file は 16,000 文字を超えるが、doctor lock、修復対象の同期、一時 index の
退避・合成・復元、および修復 commit は同じ Git common directory と index の
不変条件を共有する一つの lifecycle である。分割すると、失敗時の index 復元と
commit 対象の対応を複数 file で追う必要が生じるため、現状は doctor preprocess
の境界として一箇所に保つ。

根拠: {{work-root}}/oracle/doc/app_spec/oracle_and_realization.md の
「realization file を扱う判断基準」
"""

import fcntl
import hashlib
import importlib
import locale
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Collection, Iterator
from contextlib import ExitStack, contextmanager
from dataclasses import asdict
from pathlib import Path

from oracle.other.document_search import INITIAL_SEARCH_MATERIALS, DocumentSearchConfig

from .runtime_config import sync_config
from .runtime_document_search import DocumentSearch, SearchError, SyncResult
from .runtime_document_search_scope import oracle_doc_scope, scope_identity
from .runtime_document_search_setup import (
    prepare_document_search_materials,
    require_document_search_materials,
)
from .runtime_document_search_worker import verification_condition
from .runtime_errors import CmocError
from .runtime_feedback import (
    ReporterAvailabilityError,
    emit_reporter_unavailable,
    validate_feedback_reporter_availability,
)
from .runtime_feedback_store import uuid7_prefixed
from .runtime_git import (
    ensure_cmoc_ignored,
    git_common_dir,
    require_cmoc_ignored,
    reuse_git_path_queries,
    run_git,
    with_cmoc_ignore_pattern,
)
from .runtime_paths import (
    cmoc_root,
    config_path,
    ensure_work_directories,
    refactor_state_path,
    repo_root,
)
from .runtime_primary_report import update_primary_report_fields
from .runtime_refactor import sync_refactor_state


def _sync_status(result: SyncResult | None, failure: BaseException | None) -> str:
    """終了処理も含めた索引同期の結果を分類する。"""
    if failure is None:
        return result.status if result is not None else "failed"
    if isinstance(failure, KeyboardInterrupt) or (
        isinstance(failure, SearchError) and failure.code == "CANCELLED"
    ):
        return "cancelled"
    return "failed"


def _installation_root(_root: Path) -> Path:
    """現在の cmoc installation を処理対象の work-root と区別して解決する。"""
    return cmoc_root().resolve()


def _check_common_environment() -> None:
    """doctor 自身を起動できる環境と外部の必須実行ファイルを確認する。"""
    if sys.version_info < (3, 12, 3):
        raise CmocError(
            "cmoc の Python 実行環境が要件を満たしません。",
            ["Python 3.12.3 以上の仮想環境を準備してください。"],
            sys.version,
        )
    for module in ("click", "typer", "jsonschema"):
        try:
            importlib.import_module(module)
        except ImportError as exc:
            raise CmocError(
                "cmoc の起動用依存が不足しています。",
                ["cmoc の Python 仮想環境へ依存関係を導入してください。"],
                f"dependency: {module}\nreason: {exc}",
            ) from exc

    for executable in ("git", "codex"):
        path = shutil.which(executable)
        if path is None:
            raise CmocError(
                "必須の外部コマンドが利用できません。",
                [f"{executable} を導入し、PATH から実行できるようにしてください。"],
                f"dependency: {executable}\nreason: executable not found",
            )
        try:
            subprocess.run(
                [path, "--version"], check=True, capture_output=True, timeout=10
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise CmocError(
                "必須の外部コマンドが利用できません。",
                [f"{executable} の導入状態を確認してください。"],
                f"dependency: {executable}\npath: {path}\nreason: {exc}",
            ) from exc


def _synchronize_document_search_index(
    root: Path, installation_root: Path, config: DocumentSearchConfig
) -> SyncResult:
    """doctor の全 oracle/doc 範囲を期限なしで同期し、途中実績も記録する。"""
    scope = oracle_doc_scope()
    sync_id = uuid7_prefixed("dsi_")
    update_primary_report_fields(
        doctor_sync_status="started",
        doctor_sync_id=sync_id,
        doctor_scope_identity=scope_identity(scope),
        doctor_sync_work_root=str(root),
    )
    search: DocumentSearch | None = None
    result: SyncResult | None = None
    try:
        search = DocumentSearch(
            root,
            scope,
            config,
            installation_root=installation_root,
            use_saved_config=True,
        )
        result = search.synchronize(unbounded=True, sync_id=sync_id)
    except BaseException as exc:
        progress = search.sync_progress if search is not None else None
        identity = progress.get("identity") if progress is not None else None
        status = _sync_status(result, exc)
        update_primary_report_fields(
            doctor_sync_status=status,
            doctor_index_identity=identity,
            doctor_sync_result={
                "status": status,
                "identity": identity,
                "progress": progress,
            },
            doctor_sync_progress=progress,
            doctor_sync_failure_code=(
                exc.code if isinstance(exc, SearchError) else type(exc).__name__
            ),
            doctor_sync_failure_reason=str(exc),
        )
        raise
    else:
        assert result is not None and search is not None
        update_primary_report_fields(
            doctor_sync_status=result.status,
            doctor_index_identity=result.identity,
            doctor_sync_result=asdict(result),
            doctor_sync_progress=search.sync_progress,
        )
        return result


def run_doctor_preprocess(
    root: Path,
    *,
    explicit_doctor: bool = False,
    sync_refactor_entries: bool = True,
) -> None:
    """current と main worktree の共通修復を排他実行し、修復差分だけを commit する。"""
    root = root.resolve()
    update_primary_report_fields(
        work_root=str(root),
        config_path=str(config_path(root)),
        config_generation="未確認",
        config_validation="未実行",
        config_saved=False,
        config_additions={},
        search_config="未確認",
        material_condition="未確認",
        common_environment="未実行",
        management_validation="未実行",
        material_validation="未実行",
        material_status="未実行",
        material_models="未実行",
        material_failure="なし",
        material_identity_check="未実行",
        material_runtime_check="未実行",
        material_document_embedding="未実行",
        material_query_embedding="未実行",
        material_remaining_state="未確認",
        doctor_sync_status="not_started",
        doctor_sync_id=None,
        doctor_scope_identity=None,
        doctor_index_identity=None,
        doctor_sync_result=None,
        doctor_sync_progress=None,
    )
    _check_common_environment()
    update_primary_report_fields(common_environment="成功")
    installation_root = _installation_root(root)
    update_primary_report_fields(
        cmoc_root=str(installation_root),
        material_path=str(installation_root / ".cmoc/gu/document_search/materials"),
        material_identity={
            "embedding_sha256": INITIAL_SEARCH_MATERIALS.embedding.sha256,
            "node_llama_cpp": INITIAL_SEARCH_MATERIALS.node_llama_cpp_version,
            "sqlite_vec": INITIAL_SEARCH_MATERIALS.sqlite_vec_version,
        },
    )
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # snapshot 作成から修復 commit と元の index 復元までを同じ Git common
    # directory の lock 内で行い、並行 doctor が共有 index を混ぜないようにする。
    with ExitStack() as locks, ExitStack() as path_queries:
        path_queries.enter_context(reuse_git_path_queries())
        lock_roots = {doctor_lock_path(root): root}
        if explicit_doctor:
            lock_roots[doctor_lock_path(installation_root)] = installation_root
        for lock_path in sorted(lock_roots):
            locks.enter_context(doctor_lock(lock_roots[lock_path]))
        main_root = repo_root(root)
        ensure_work_directories(root)
        repair_roots = [main_root] if main_root == root else [main_root, root]
        if explicit_doctor and installation_root not in repair_roots:
            repair_roots.append(installation_root)
        if not explicit_doctor and installation_root not in repair_roots:
            try:
                require_cmoc_ignored(installation_root)
            except CmocError as exc:
                raise CmocError(
                    "共有検索用コンポーネントの管理領域が非追跡ではありません。",
                    [f"対象 work-root ({root}) で cmoc doctor を実行してください。"],
                    f"cmoc-root: {installation_root}\nreason: {exc.detail}",
                ) from exc

        repairs: list[tuple[Path, Path, bool, bool, bool, set[str]]] = []
        original_indexes: list[tuple[Path, Path]] = []
        try:
            for repair_root in repair_roots:
                include_config = repair_root == root
                include_agents = repair_root == root
                include_gu_ignore = True
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
            update_primary_report_fields(config_validation="失敗")

            def report_config_candidate(
                generated: bool, additions: dict[str, object]
            ) -> None:
                """保存前の補完候補も失敗 report へ残す。"""
                update_primary_report_fields(
                    config_generation="新規ファイル候補"
                    if generated
                    else "既存ファイル",
                    config_additions=additions,
                )

            config_result = sync_config(
                root,
                repair_missing=explicit_doctor,
                on_candidate=report_config_candidate if explicit_doctor else None,
            )
            update_primary_report_fields(
                config_generation="新規生成"
                if config_result.generated
                else "既存ファイル",
                config_additions=config_result.additions,
                config_validation="成功",
                config_saved=config_result.saved,
                search_config=asdict(config_result.config.document_search),
                material_condition=verification_condition(
                    config_result.config.document_search
                ),
            )
            sync_refactor_state(root, sync_entries=sync_refactor_entries)
            update_primary_report_fields(management_validation="成功")
            try:
                assert config_result.config.document_search is not None
                if explicit_doctor:
                    material_result = prepare_document_search_materials(
                        installation_root, config_result.config.document_search
                    )
                else:
                    material_path = require_document_search_materials(
                        installation_root, config_result.config.document_search
                    )
                    material_result = {
                        "status": "verified",
                        "path": str(material_path),
                        "models": "reused",
                    }
            except (
                SearchError,
                OSError,
                ValueError,
                subprocess.SubprocessError,
            ) as exc:
                update_primary_report_fields(
                    material_validation="失敗",
                    material_status="失敗",
                    material_models="未完了",
                    material_failure=str(exc),
                    material_identity_check="未完了",
                    material_runtime_check="未完了",
                    material_document_embedding="未完了",
                    material_query_embedding="未完了",
                    material_remaining_state="現在の条件では準備済みと扱わず、再実行時に照合する",
                )
                action = (
                    "依存・権限・ネットワークを確認して cmoc doctor を再実行してください。"
                    if explicit_doctor
                    else f"対象 work-root ({root}) で cmoc doctor を実行してください。"
                )
                raise CmocError(
                    "検索用コンポーネントの準備状態を確認できません。",
                    [action],
                    f"cmoc-root: {installation_root}\npath: {installation_root / '.cmoc/gu/document_search/materials'}\nreason: {exc}",
                ) from exc
            update_primary_report_fields(
                material_validation="成功",
                material_status=material_result["status"],
                material_models=material_result["models"],
                material_identity_check="成功",
                material_runtime_check="成功",
                material_document_embedding="成功",
                material_query_embedding="成功",
                material_remaining_state="検査時点で利用可能",
            )
            try:
                _synchronize_document_search_index(
                    root, installation_root, config_result.config.document_search
                )
            except SearchError as exc:
                raise CmocError(
                    "文書検索索引の同期に失敗しました。",
                    [
                        f"対象 work-root ({root}) で cmoc doctor を実行してください。"
                        if exc.code in {"NOT_READY", "MODEL_IDENTITY_MISMATCH"}
                        else "文書検索の設定、資材、許可対象ファイルを確認してください。"
                    ],
                    f"work-root: {root}\ncode: {exc.code}\nreason: {exc}",
                ) from exc
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

        # commit hook は Git 設定を変更できるため、修復 commit へ進む前に
        # 問い合わせの再利用を終える。復元と最終検証は最新の配置・設定を読む。
        path_queries.close()
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
        for repair_root in repair_roots:
            require_cmoc_ignored(repair_root)
        _validate_tracked_runtime_files(root)
        ensure_work_directories(root, create_missing=False)


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
            run_git(
                ["restore", "--worktree", "--", ".agents/.gitkeep"],
                root,
                check=False,
            )
            if not gitkeep.exists():
                # git restore は skip-worktree entry を欠落した worktree へ
                # 戻せないため、現在 index の blob を flag を保ったまま checkout
                # する。通常 entry では最初の restore が成功するので実行しない。
                run_git(
                    [
                        "checkout-index",
                        "--force",
                        "--ignore-skip-worktree-bits",
                        "--",
                        ".agents/.gitkeep",
                    ],
                    root,
                    check=False,
                )
            if not gitkeep.exists() and _head_entry(root, ".agents/.gitkeep"):
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
    # 同じ一時 index の対象 entry をまとめて読み、既存の stage と mode を保つ。
    paths = {
        str(path.relative_to(root)): path
        for path in (config_path(root), refactor_state_path(root))
        if str(path.relative_to(root)) not in skip_paths
    }
    if not paths:
        return
    entries = _run_git_with_index(
        ["ls-files", "--stage", "-z", "--", *paths], root, index_path
    )
    metadata: dict[str, tuple[str, str, str]] = {}
    for record in entries.stdout.split("\0"):
        if record:
            fields, relative = record.split("\t", 1)
            mode, blob, stage = fields.split()
            metadata.setdefault(relative, (mode, blob, stage))

    # hash-object --stdin の text input と同じ encoding で比較する。
    # Git 自身が返した object ID の長さから SHA-1 / SHA-256 を区別する。
    encoding = "utf-8" if sys.flags.utf8_mode else locale.getencoding()
    for relative, path in paths.items():
        content = path.read_text()
        existing = metadata.get(relative)
        if existing is not None and existing[2] == "0":
            blob = existing[1]
            if len(blob) in {40, 64}:
                encoded = content.encode(encoding)
                header = b"blob " + str(len(encoded)).encode("ascii") + b"\0"
                algorithm = "sha1" if len(blob) == 40 else "sha256"
                if hashlib.new(algorithm, header + encoded).hexdigest() == blob:
                    continue
        _stage_text(
            root,
            index_path,
            relative,
            content,
            mode=existing[0] if existing is not None else None,
        )


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


def _stage_text(
    root: Path,
    index_path: Path,
    path: str,
    content: str,
    *,
    mode: str | None = None,
) -> None:
    """テキスト内容をblob化して一時indexへ登録する。"""
    blob = _run_git_with_index(
        ["hash-object", "-w", "--stdin"], root, index_path, input_text=content
    ).stdout.strip()
    if mode is None:
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
