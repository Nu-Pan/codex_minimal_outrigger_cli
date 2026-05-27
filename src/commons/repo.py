"""git リポジトリと cmoc 作業ディレクトリの共通処理。"""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from .errors import CmocError

SESSION_BRANCH_PREFIX = "cmoc/session/"
APPLY_BRANCH_PREFIX = "cmoc/apply/"
SESSION_STATES = {"active", "joined", "abandoned", "error"}
APPLY_STATES = {"ready", "running", "completed", "error"}


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
    """cmoc 管理ブランチ名か判定する。"""
    return is_session_branch(branch_name) or is_apply_branch(branch_name)


def is_session_branch(branch_name: str) -> bool:
    """`cmoc/session/<session-id>` 形式のブランチ名か判定する。"""
    session_id = branch_name.removeprefix(SESSION_BRANCH_PREFIX)
    return (
        branch_name.startswith(SESSION_BRANCH_PREFIX)
        and bool(session_id)
        and "/" not in session_id
    )


def is_apply_branch(branch_name: str) -> bool:
    """`cmoc/apply/<session-id>/<apply-run-id>` 形式のブランチ名か判定する。"""
    suffix = branch_name.removeprefix(APPLY_BRANCH_PREFIX)
    parts = suffix.split("/")
    return (
        branch_name.startswith(APPLY_BRANCH_PREFIX)
        and len(parts) == 2
        and all(parts)
    )


def session_id_from_branch(branch_name: str) -> str:
    """cmoc 管理ブランチ名から session id を取り出す。"""
    if is_session_branch(branch_name):
        return branch_name.removeprefix(SESSION_BRANCH_PREFIX)
    if is_apply_branch(branch_name):
        return branch_name.removeprefix(APPLY_BRANCH_PREFIX).split("/", 1)[0]
    raise CmocError(
        "cmoc 管理 branch ではありません。",
        [
            "`cmoc session fork` で作成した session branch 上で実行してください。",
            "通常の branch から実行する場合は、先に session を開始してください。",
        ],
        f"現在の branch: {branch_name}",
    )


def apply_worktree_path_from_branch(repo_root: Path, apply_branch: str) -> Path:
    """apply branch 名から管理 worktree path を復元する。"""
    session_id, apply_run_id = apply_branch.removeprefix(
        APPLY_BRANCH_PREFIX
    ).split("/", 1)
    return (
        repo_root
        / ".cmoc"
        / "worktrees"
        / "apply"
        / session_id
        / apply_run_id
    )


def session_state_path(repo_root: Path, session_id: str) -> Path:
    """session state JSON の保存先 path を返す。"""
    return repo_root / ".cmoc" / "sessions" / f"{session_id}.json"


def session_state_repo_root(repo_root: Path, session_id: str) -> Path:
    """session state を保持する main worktree root を返す。"""
    common_dir = run_git(
        repo_root,
        ["rev-parse", "--path-format=absolute", "--git-common-dir"],
    ).stdout.strip()
    common_root = Path(common_dir).parent
    if session_state_path(common_root, session_id).exists():
        return common_root
    if common_root != repo_root:
        return common_root
    return repo_root


def initial_session_state(
    session_home_branch: str,
    session_start_commit: str,
) -> dict[str, object]:
    """`cmoc session fork` 直後の session state を返す。"""
    return {
        "session": {
            "state": "active",
            "session_home_branch": session_home_branch,
            "session_start_commit": session_start_commit,
        },
        "apply": {
            "state": "ready",
            "apply_branch": None,
            "oracle_snapshot_commit": None,
        },
    }


def write_session_state(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
) -> Path:
    """session state JSON を保存する。"""
    path = session_state_path(repo_root, session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = _session_state_payload(state)
    _validate_session_state_schema(payload, path)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    return path


def _session_state_payload(state: dict[str, object]) -> dict[str, object]:
    """永続化対象の session state 固定スキーマだけを返す。"""
    session = state.get("session")
    apply = state.get("apply")
    if not isinstance(session, dict) or not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session/apply セクションを確認してください。",
                "破損した session state を復旧してください。",
            ],
        )
    return {
        "session": {
            "state": session.get("state"),
            "session_home_branch": session.get("session_home_branch"),
            "session_start_commit": session.get("session_start_commit"),
        },
        "apply": {
            "state": apply.get("state"),
            "apply_branch": apply.get("apply_branch"),
            "oracle_snapshot_commit": apply.get("oracle_snapshot_commit"),
        },
    }


def read_session_state(repo_root: Path, session_id: str) -> dict[str, object]:
    """session state JSON を読む。"""
    path = session_state_path(repo_root, session_id)
    if not path.exists():
        raise CmocError(
            "session state ファイルが見つかりませんでした。",
            [
                "`cmoc session fork` で作成した branch 上で実行してください。",
                "session state が失われた場合は、手動で branch と .cmoc/sessions を確認してください。",
            ],
            str(path),
        )
    return _read_existing_session_state(path)


def _read_existing_session_state(path: Path) -> dict[str, object]:
    """存在する session state JSON を読み、固定スキーマを検証する。"""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise CmocError(
            "session state ファイルを読めませんでした。",
            [
                ".cmoc/sessions 配下のファイル権限と状態を確認してください。",
                "破損した session state を復旧または退避してから再実行してください。",
            ],
            f"{path}\n{error}",
        ) from error
    except json.JSONDecodeError as error:
        raise CmocError(
            "session state ファイルの JSON が不正です。",
            [
                ".cmoc/sessions 配下の JSON を確認してください。",
                "破損した session state を復旧または退避してから再実行してください。",
            ],
            f"{path}\n{error}",
        ) from error

    if not isinstance(payload, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の内容を確認してください。",
                "破損した session state を復旧または退避してから再実行してください。",
            ],
            str(path),
        )
    _validate_session_state_schema(payload, path)
    return payload


def _validate_session_state_schema(
    payload: dict[str, object],
    path: Path,
) -> None:
    """session state の固定スキーマと state 不変条件を検証する。"""
    session = payload.get("session")
    apply = payload.get("apply")
    if not isinstance(session, dict) or not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session/apply セクションを確認してください。",
                "破損した session state を復旧または退避してから再実行してください。",
            ],
            str(path),
        )

    session_state = _validate_required_string(
        session,
        "state",
        "session.state",
        path,
    )
    _validate_state_value(session_state, SESSION_STATES, "session.state", path)
    _validate_required_string(
        session,
        "session_home_branch",
        "session.session_home_branch",
        path,
    )
    _validate_required_string(
        session,
        "session_start_commit",
        "session.session_start_commit",
        path,
    )
    apply_state = _validate_required_string(apply, "state", "apply.state", path)
    _validate_state_value(apply_state, APPLY_STATES, "apply.state", path)
    _validate_optional_string(apply, "apply_branch", "apply.apply_branch", path)
    _validate_optional_string(
        apply,
        "oracle_snapshot_commit",
        "apply.oracle_snapshot_commit",
        path,
    )
    _validate_apply_state_invariants(apply, apply_state, path)


def _validate_required_string(
    section: dict[object, object],
    key: str,
    label: str,
    path: Path,
) -> str:
    """必須 string field が session state に存在することを検証する。"""
    value = section.get(key)
    if not isinstance(value, str) or not value:
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                f"{label} を確認してください。",
                "破損した session state を復旧してください。",
            ],
            f"{path}\n{label}: {value}",
        )
    return value


def _validate_state_value(
    value: str,
    allowed_values: set[str],
    label: str,
    path: Path,
) -> None:
    """state field が oracle 定義の列挙値であることを検証する。"""
    if value not in allowed_values:
        choices = "/".join(sorted(allowed_values))
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                f"{label} は {choices} のいずれかである必要があります。",
                "破損した session state を復旧してください。",
            ],
            f"{path}\n{label}: {value}",
        )


def _validate_optional_string(
    section: dict[object, object],
    key: str,
    label: str,
    path: Path,
) -> None:
    """任意 string field が null または string であることを検証する。"""
    value = section.get(key)
    if value is not None and not isinstance(value, str):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                f"{label} を確認してください。",
                "破損した session state を復旧してください。",
            ],
            f"{path}\n{label}: {value}",
        )


def _validate_apply_state_invariants(
    apply: dict[object, object],
    apply_state: str,
    path: Path,
) -> None:
    """apply.state ごとの補助 field 不変条件を検証する。"""
    apply_branch = apply.get("apply_branch")
    oracle_snapshot_commit = apply.get("oracle_snapshot_commit")
    if apply_state == "ready":
        _validate_null_field(apply_branch, "apply.apply_branch", path)
        _validate_null_field(
            oracle_snapshot_commit,
            "apply.oracle_snapshot_commit",
            path,
        )
        return

    if apply_state in {"running", "completed"}:
        _validate_apply_run_fields(apply_branch, oracle_snapshot_commit, path)
        return

    if apply_state == "error" and (
        apply_branch is not None or oracle_snapshot_commit is not None
    ):
        _validate_apply_run_fields(apply_branch, oracle_snapshot_commit, path)


def _validate_null_field(value: object, label: str, path: Path) -> None:
    """ready state で null 初期化される field を検証する。"""
    if value is not None:
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                f"apply.state が ready の場合は {label} を null にしてください。",
                "破損した session state を復旧してください。",
            ],
            f"{path}\n{label}: {value}",
        )


def _validate_apply_run_fields(
    apply_branch: object,
    oracle_snapshot_commit: object,
    path: Path,
) -> None:
    """active apply run の特定に必要な field を検証する。"""
    if not isinstance(apply_branch, str) or not is_apply_branch(apply_branch):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "apply.apply_branch は cmoc apply branch 名である必要があります。",
                "破損した session state を復旧してください。",
            ],
            f"{path}\napply.apply_branch: {apply_branch}",
        )
    if not isinstance(oracle_snapshot_commit, str) or not oracle_snapshot_commit:
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "apply.oracle_snapshot_commit を確認してください。",
                "破損した session state を復旧してください。",
            ],
            f"{path}\napply.oracle_snapshot_commit: {oracle_snapshot_commit}",
        )


def active_session_ids_for_home_branch(
    repo_root: Path,
    session_home_branch: str,
) -> list[str]:
    """指定 home branch に紐づく active session id を列挙する。"""
    session_root = repo_root / ".cmoc" / "sessions"
    if not session_root.exists():
        return []

    session_ids: list[str] = []
    for path in sorted(session_root.glob("*.json")):
        payload = _read_existing_session_state(path)
        session = payload["session"]
        if (
            session.get("state") == "active"
            and session.get("session_home_branch") == session_home_branch
        ):
            session_ids.append(path.stem)
    return session_ids


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


def assert_cmoc_ignored(repo_root: Path) -> None:
    """`.cmoc` が git 追跡対象外であることを副作用なしで検証する。"""
    _assert_cmoc_ignore_guarantee(repo_root)


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
    if not paths:
        return False

    # 呼び出し前から stage 済みの差分を、対象 commit 後の index へ戻す。
    staged_outside_paths = _staged_diff_excluding_paths(repo_root, paths)
    staged_inside_paths = _staged_diff_for_paths(repo_root, paths)
    parent_hash = _head_commit_or_none(repo_root)
    with tempfile.TemporaryDirectory(
        prefix="cmoc-pathspec-index-",
    ) as temp_name:
        env = {"GIT_INDEX_FILE": str(Path(temp_name) / "index")}
        if parent_hash is None:
            run_git(repo_root, ["read-tree", "--empty"], env=env)
        else:
            run_git(repo_root, ["read-tree", "HEAD"], env=env)

        literal_paths = _literal_pathspecs(paths)
        update_paths = [path for path in paths if (repo_root / path).exists()]
        if update_paths:
            run_git(
                repo_root,
                ["add", "-u", "--", *_literal_pathspecs(update_paths)],
                env=env,
            )

        add_paths = [path for path in paths if not path.startswith(".cmoc")]
        if add_paths:
            run_git(
                repo_root,
                ["add", "-f", "--", *_literal_pathspecs(add_paths)],
                env=env,
            )
        if any(path == ".cmoc" or path.startswith(".cmoc/") for path in paths):
            _remove_cmoc_from_index(repo_root, env)

        changed = run_git(
            repo_root,
            ["diff", "--cached", "--quiet", "--", *literal_paths],
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
    _restore_index_after_pathspec_commit(
        repo_root,
        staged_outside_paths + staged_inside_paths,
    )
    return True


def _restore_index_after_init_commit(
    repo_root: Path,
    preexisting_staged_diff: str,
) -> None:
    """init commit 後の index を HEAD ベースに戻し、既存 staged 差分を復元する。"""
    _restore_index_after_internal_commit(
        repo_root,
        preexisting_staged_diff,
        remove_cmoc=True,
    )
    _assert_cmoc_ignore_guarantee(repo_root)


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


def filter_oracle_file_paths(
    repo_root: Path,
    relative_paths: list[str],
) -> list[str]:
    """root 相対 path から仕様上の oracles ファイルだけを返す。"""
    # 削除済み path も判定できるよう、存在確認ではなく path と root .gitignore
    # だけで oracles ファイル定義に合わせる。
    candidates = sorted(
        {
            path
            for path in relative_paths
            if path.startswith("oracles/")
            and Path(path).name != "INDEX.md"
        }
    )
    ignored = _root_gitignored_paths(repo_root, candidates)
    return [path for path in candidates if path not in ignored]


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


def is_implementation_path(repo_root: Path, relative_path: str) -> bool:
    """root 相対 path が実装ファイル列挙対象か判定する。"""
    return (
        not _is_excluded_implementation_path(relative_path)
        and not _is_root_gitignored(repo_root, relative_path)
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
            "--name-status",
            "-M",
            "--diff-filter=DR",
            "--format=",
            f"{base_commit}..HEAD",
        ],
        ["diff", "--name-status", "-M", "--diff-filter=DR", "HEAD"],
        ["diff", "--cached", "--name-status", "-M", "--diff-filter=DR"],
    ]
    for command in commands:
        result = run_git(repo_root, [*command, "--", "."])
        if _deleted_oracle_changes_from_name_status(repo_root, result.stdout):
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


def _deleted_oracle_changes_from_name_status(
    repo_root: Path,
    output: str,
) -> list[str]:
    """`git name-status` から oracle 削除相当の変更を取り出す。"""
    # oracle から非 oracle への rename は、oracle 集合から見れば削除である。
    deleted: list[str] = []
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0]
        if status == "D":
            deleted.extend(filter_oracle_file_paths(repo_root, [parts[1]]))
            continue
        if not status.startswith("R") or len(parts) < 3:
            continue
        source_oracles = filter_oracle_file_paths(repo_root, [parts[1]])
        destination_oracles = filter_oracle_file_paths(repo_root, [parts[2]])
        if source_oracles and not destination_oracles:
            deleted.extend(source_oracles)
    return deleted


def _deleted_implementation_file_paths(
    repo_root: Path,
    output: str,
) -> list[str]:
    """削除 path から実装ファイル列挙対象外のものを除外する。"""
    # 削除済み path は存在確認できないため、path 規則と gitignore だけで判定する。
    relatives = [
        line
        for line in output.splitlines()
        if is_implementation_path(repo_root, line)
    ]
    return relatives


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
    # oracles、root memo、.git、INDEX.md は仕様上の除外対象である。
    path = Path(relative_path)
    return (
        relative_path == "oracles"
        or relative_path.startswith("oracles/")
        or relative_path == "memo"
        or relative_path.startswith("memo/")
        or relative_path == ".git"
        or relative_path.startswith(".git/")
        or path.name == "INDEX.md"
    )


def read_session_start_commit(repo_root: Path, branch_name: str) -> str:
    """cmoc session state から session start commit を読む。"""
    payload = read_session_state(repo_root, session_id_from_branch(branch_name))
    session = payload.get("session")
    if not isinstance(session, dict):
        raise CmocError(
            "session state ファイルに session セクションがありません。",
            ["state JSON の内容を確認してください。"],
            f"branch: {branch_name}",
        )
    start_commit = session.get("session_start_commit")
    if not isinstance(start_commit, str) or not start_commit:
        raise CmocError(
            "session start commit が session state に記録されていません。",
            [
                "差分評価の前に `cmoc session fork` を実行してください。",
                "全 oracle ファイルを評価する場合は `cmoc eval-oracles --full` を実行してください。",
            ],
            f"branch: {branch_name}",
        )
    return start_commit


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
    exclusions = _literal_exclude_pathspecs(paths)
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


def _staged_diff_for_paths(repo_root: Path, paths: list[str]) -> str:
    """指定 pathspec の既存 staged 差分を patch として返す。"""
    result = run_git(
        repo_root,
        [
            "diff",
            "--cached",
            "--binary",
            "--full-index",
            "--",
            *_literal_pathspecs(paths),
        ],
    )
    return result.stdout


def _literal_pathspecs(paths: list[str]) -> list[str]:
    """repo 相対 path を git literal pathspec へ変換する。"""
    return [f":(literal){path}" for path in paths]


def _literal_exclude_pathspecs(paths: list[str]) -> list[str]:
    """repo 相対 path を git literal exclude pathspec へ変換する。"""
    return [f":(exclude,literal){path}" for path in paths]


def _restore_index_after_pathspec_commit(
    repo_root: Path,
    staged_diff: str,
) -> None:
    """pathspec commit 後、既存 staged 差分を index に戻す。"""
    _restore_index_after_internal_commit(
        repo_root,
        staged_diff,
        remove_cmoc=bool(staged_diff),
    )


def _restore_index_after_internal_commit(
    repo_root: Path,
    staged_diff: str,
    *,
    remove_cmoc: bool,
) -> None:
    """内部 commit 後の index を一時 index で復元し、成功後だけ本体へ反映する。"""
    with tempfile.TemporaryDirectory(prefix="cmoc-restore-index-") as temp_name:
        temp_index = Path(temp_name) / "index"
        env = {"GIT_INDEX_FILE": str(temp_index)}
        run_git(repo_root, ["read-tree", "--reset", "HEAD"], env=env)

        if staged_diff:
            result = _apply_staged_diff_to_index(repo_root, staged_diff, env)
            if result.returncode != 0:
                raise CmocError(
                    "事前に stage されていた変更の復元に失敗しました。",
                    [
                        "作業を続ける前に git index の状態を確認してください。",
                        "必要に応じて、以前 stage していた変更をもう一度 stage してください。",
                    ],
                    result.stderr.strip(),
                )

        if remove_cmoc:
            _remove_cmoc_from_index(repo_root, env)
        _replace_git_index(repo_root, temp_index)


def _apply_staged_diff_to_index(
    repo_root: Path,
    staged_diff: str,
    env: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    """保存済み staged patch を指定 index に適用する。"""
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
            env=env,
        )
    finally:
        patch_path.unlink(missing_ok=True)
    return result


def _replace_git_index(repo_root: Path, source_index: Path) -> None:
    """通常 index を復元済み一時 index で置き換える。"""
    index_path = Path(
        run_git(
            repo_root,
            ["rev-parse", "--path-format=absolute", "--git-path", "index"],
        ).stdout.strip()
    )
    index_path.parent.mkdir(parents=True, exist_ok=True)
    os.replace(source_index, index_path)


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
            ".cmoc が git 追跡対象外として初期化されていません。",
            [
                "先に `cmoc init` を実行してください。",
                ".gitignore と git index を確認してください。",
                "追跡済みの .cmoc ファイルは `cmoc init` で index から外してください。",
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
    env = _root_gitignore_git_env()
    with tempfile.TemporaryDirectory(prefix="cmoc-gitignore-") as temp_name:
        temp_root = Path(temp_name)
        shutil.copyfile(gitignore, temp_root / ".gitignore")
        subprocess.run(
            ["git", "init", "-q"],
            cwd=temp_root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )
        # `--stdin` で渡した root 相対 path を Git の ignore 実装に判定させる。
        result = subprocess.run(
            [
                "git",
                "-c",
                f"core.excludesFile={os.devnull}",
                "check-ignore",
                "--no-index",
                "--stdin",
            ],
            cwd=temp_root,
            check=False,
            input="\n".join(relative_paths) + "\n",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
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


def _root_gitignore_git_env() -> dict[str, str]:
    """root `.gitignore` 評価用に外部 Git ignore 設定を遮断した env を返す。"""
    env = dict(os.environ)
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_SYSTEM"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return env


def _is_gitignored(repo_root: Path, relative_path: str) -> bool:
    """実リポジトリ全体の `.gitignore` ルールで ignore 対象か判定する。"""
    # 単一 path の判定も集合判定の実装に揃える。
    return relative_path in _gitignored_paths(repo_root, [relative_path])


def _gitignored_paths(repo_root: Path, relative_paths: list[str]) -> set[str]:
    """実リポジトリ全体の `.gitignore` ルールで ignore 対象を返す。"""
    # nested .gitignore も含め、Git 自身の判定に path 集合をまとめて渡す。
    if not relative_paths:
        return set()
    result = run_git(
        repo_root,
        ["check-ignore", "--no-index", "--stdin"],
        check=False,
        input_text="\n".join(relative_paths) + "\n",
    )
    if result.returncode not in {0, 1}:
        raise CmocError(
            ".gitignore の評価に失敗しました。",
            [
                ".gitignore の構文を確認してからコマンドを再実行してください。",
                "一時的に .gitignore を単純化してから cmoc を再実行してください。",
            ],
            result.stderr.strip(),
        )
    return set(result.stdout.splitlines())


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
