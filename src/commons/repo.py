"""git リポジトリと cmoc 作業ディレクトリの共通処理。"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

from .errors import CmocError
from .timestamps import is_timestamp

SESSION_BRANCH_PREFIX = "cmoc/session/"
APPLY_BRANCH_PREFIX = "cmoc/apply/"
REVIEW_BRANCH_PREFIX = "cmoc/review/"
SESSION_STATES = {"active", "joined", "abandoned", "error"}
APPLY_STATES = {"ready", "running", "completed", "error"}
SESSION_STATE_KEYS = {
    "state",
    "session_home_branch",
    "session_start_commit",
    "last_joined_apply_oracle_snapshot_commit",
}
APPLY_STATE_KEYS = {"state", "apply_branch", "oracle_snapshot_commit"}
CMOC_IGNORE_PROBE_PATH = ".cmoc/.__cmoc_ignore_probe__"


def enter_repo_root(start: Path | None = None) -> Path:
    """リポジトリルートを特定し、プロセスの cwd をそこへ移す。"""
    # 起点から repo root を見つけ、以降の git 操作の cwd を固定する。
    repo_root = find_repo_root(start)
    os.chdir(repo_root)
    return repo_root


def find_repo_root(start: Path | None = None) -> Path:
    """カレントから親方向へ worktree root を探す。"""
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


def main_worktree_repo_root(worktree_root: Path) -> Path:
    """worktree root から main worktree の repo root を返す。"""
    git_entry = worktree_root / ".git"
    if git_entry.is_dir():
        return worktree_root
    if not git_entry.exists():
        if _is_path_under_cmoc_worktrees(worktree_root):
            try:
                nearest_worktree = find_repo_root(worktree_root)
            except CmocError:
                nearest_worktree = worktree_root
            if nearest_worktree != worktree_root:
                return main_worktree_repo_root(nearest_worktree)
        return worktree_root

    result = run_git(
        worktree_root,
        ["rev-parse", "--path-format=absolute", "--git-common-dir"],
        check=False,
    )
    if result.returncode != 0:
        return _main_worktree_repo_root_from_git_file(git_entry) or worktree_root

    common_dir = result.stdout.strip()
    if not common_dir:
        return worktree_root
    common_path = Path(common_dir)
    if not common_path.is_absolute():
        common_path = worktree_root / common_path
    if common_path.name == ".git":
        return common_path.parent.resolve()
    return worktree_root


def _is_path_under_cmoc_worktrees(path: Path) -> bool:
    """path が `.cmoc/worktrees` 配下を指していれば True を返す。"""
    parts = path.parts
    marker = (".cmoc", "worktrees")
    return any(
        parts[index : index + len(marker)] == marker
        for index in range(0, len(parts) - len(marker) + 1)
    )


def _main_worktree_repo_root_from_git_file(git_entry: Path) -> Path | None:
    """linked worktree の `.git` file から main worktree root を復元する。"""
    if not git_entry.is_file():
        return None
    try:
        content = git_entry.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    prefix = "gitdir:"
    if not content.lower().startswith(prefix):
        return None
    git_dir = Path(content[len(prefix) :].strip())
    if not git_dir.is_absolute():
        git_dir = (git_entry.parent / git_dir).resolve()
    parts = git_dir.parts
    marker = (".git", "worktrees")
    for index in range(0, len(parts) - len(marker)):
        if parts[index : index + len(marker)] == marker:
            return Path(*parts[: index + 1]).parent.resolve()
    return None


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
    return (
        is_session_branch(branch_name)
        or is_apply_branch(branch_name)
        or is_review_branch(branch_name)
    )


def is_cmoc_reserved_branch(branch_name: str) -> bool:
    """cmoc が予約している branch namespace 配下か判定する。"""
    return (
        branch_name.startswith(SESSION_BRANCH_PREFIX)
        or branch_name.startswith(APPLY_BRANCH_PREFIX)
        or branch_name.startswith(REVIEW_BRANCH_PREFIX)
    )


def is_session_branch(branch_name: str) -> bool:
    """`cmoc/session/<session-id>` 形式のブランチ名か判定する。"""
    session_id = branch_name.removeprefix(SESSION_BRANCH_PREFIX)
    return (
        branch_name.startswith(SESSION_BRANCH_PREFIX)
        and is_timestamp(session_id)
    )


def is_apply_branch(branch_name: str) -> bool:
    """`cmoc/apply/<session-id>/<apply-run-id>` 形式のブランチ名か判定する。"""
    suffix = branch_name.removeprefix(APPLY_BRANCH_PREFIX)
    parts = suffix.split("/")
    return (
        branch_name.startswith(APPLY_BRANCH_PREFIX)
        and len(parts) == 2
        and all(is_timestamp(part) for part in parts)
    )


def is_review_branch(branch_name: str) -> bool:
    """`cmoc/review/<session-id>/<review-run-id>` 形式のブランチ名か判定する。"""
    suffix = branch_name.removeprefix(REVIEW_BRANCH_PREFIX)
    parts = suffix.split("/")
    return (
        branch_name.startswith(REVIEW_BRANCH_PREFIX)
        and len(parts) == 2
        and all(is_timestamp(part) for part in parts)
    )


def session_id_from_branch(branch_name: str) -> str:
    """cmoc 管理ブランチ名から session id を取り出す。"""
    if is_session_branch(branch_name):
        return branch_name.removeprefix(SESSION_BRANCH_PREFIX)
    if is_apply_branch(branch_name):
        return branch_name.removeprefix(APPLY_BRANCH_PREFIX).split("/", 1)[0]
    if is_review_branch(branch_name):
        return branch_name.removeprefix(REVIEW_BRANCH_PREFIX).split("/", 1)[0]
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
    return repo_root / ".cmoc" / "worktrees" / session_id / apply_run_id


def worktree_path_for_branch(repo_root: Path, branch_name: str) -> Path | None:
    """指定 branch が checkout されている worktree path を返す。"""
    result = run_git(repo_root, ["worktree", "list", "--porcelain"])
    current_worktree: Path | None = None
    target_ref = f"refs/heads/{branch_name}"
    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            current_worktree = None
            continue
        if line.startswith("worktree "):
            current_worktree = Path(line.removeprefix("worktree "))
            continue
        if line == f"branch {target_ref}" and current_worktree is not None:
            return current_worktree
    return None


def session_state_path(repo_root: Path, session_id: str) -> Path:
    """session state JSON の保存先 path を返す。"""
    return repo_root / ".cmoc" / "sessions" / f"{session_id}.json"


def apply_process_id_path(repo_root: Path, session_id: str) -> Path:
    """running apply process id の runtime-only 保存先 path を返す。"""
    return repo_root / ".cmoc" / "runtime" / "apply" / f"{session_id}.pid"


def write_apply_process_id(
    repo_root: Path,
    session_id: str,
    process_id: int,
    apply_branch: str | None = None,
) -> Path:
    """running apply process 情報を session state 外の runtime file に保存する。"""
    path = apply_process_id_path(repo_root, session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "format": "cmoc-apply-process-v1",
        "process_id": process_id,
        "proc_start_time": process_start_time(process_id),
        "cmdline": process_cmdline(process_id),
        "repo_root": str(repo_root.resolve()),
        "session_id": session_id,
        "apply_branch": apply_branch,
    }
    path.write_text(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def read_apply_process_id(repo_root: Path, session_id: str) -> int | None:
    """runtime file から running apply process id を読む。"""
    record = read_apply_process_record(repo_root, session_id)
    if record is None:
        return None
    process_id = record.get("process_id")
    if not isinstance(process_id, int):
        raise _invalid_apply_process_id_error(
            apply_process_id_path(repo_root, session_id),
            process_id,
        )
    return process_id


def read_apply_process_record(
    repo_root: Path,
    session_id: str,
) -> dict[str, object] | None:
    """runtime file から running apply process record を読む。"""
    path = apply_process_id_path(repo_root, session_id)
    if not path.exists():
        return None
    try:
        raw_value = _read_utf8_text(
            path,
            "apply process id ファイルを読めませんでした。",
            [
                ".cmoc/runtime/apply 配下のファイル権限と状態を確認してください。",
                "手動で apply process の状態を確認してから再実行してください。",
            ],
        ).strip()
    except FileNotFoundError:
        return None
    try:
        parsed = json.loads(raw_value)
    except json.JSONDecodeError:
        parsed = None
    if isinstance(parsed, dict):
        process_id = parsed.get("process_id")
        if not isinstance(process_id, int) or process_id <= 0:
            raise _invalid_apply_process_id_error(path, process_id)
        return parsed
    try:
        process_id = int(raw_value)
    except ValueError as error:
        raise _invalid_apply_process_id_error(path, raw_value) from error
    if process_id <= 0:
        raise _invalid_apply_process_id_error(path, process_id)
    return {
        "format": "legacy-pid-only",
        "process_id": process_id,
    }


def process_start_time(process_id: int) -> int | None:
    """Linux procfs から process starttime(clock ticks) を返す。"""
    try:
        content = Path(f"/proc/{process_id}/stat").read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        fields_after_comm = content.rsplit(") ", 1)[1].split()
    except IndexError:
        return None
    if len(fields_after_comm) < 20:
        return None
    try:
        return int(fields_after_comm[19])
    except ValueError:
        return None


def process_cmdline(process_id: int) -> list[str] | None:
    """Linux procfs から process cmdline を argv list として返す。"""
    try:
        content = Path(f"/proc/{process_id}/cmdline").read_bytes()
    except OSError:
        return None
    if not content:
        return []
    return [
        value.decode("utf-8", errors="replace")
        for value in content.rstrip(b"\0").split(b"\0")
    ]


def _invalid_apply_process_id_error(
    path: Path,
    process_id: object,
) -> CmocError:
    """apply process runtime file の形式不正を CmocError 化する。"""
    return CmocError(
        "apply process id ファイルの形式が不正です。",
        [
            ".cmoc/runtime/apply 配下の pid ファイルを確認してください。",
            "手動で apply process の状態を確認してから再実行してください。",
        ],
        f"{path}\nprocess_id: {process_id}",
    )


def clear_apply_process_id(repo_root: Path, session_id: str) -> None:
    """runtime-only apply process id file を削除する。"""
    path = apply_process_id_path(repo_root, session_id)
    try:
        path.unlink()
    except FileNotFoundError:
        return


def session_state_root(repo_root: Path) -> Path:
    """session state を置く main worktree repo root を返す。"""
    return main_worktree_repo_root(repo_root)


def session_state_repo_root(repo_root: Path, session_id: str) -> Path:
    """session state を保持する repo root を返す。

    通常 worktree からも linked worktree からも main worktree を返す。
    cmoc 管理 apply worktree も git common dir から main worktree へ解決する。
    """
    return session_state_root(repo_root)


def _owning_repo_root_from_apply_worktree_path(
    repo_root: Path,
    session_id: str,
) -> Path | None:
    """cmoc apply worktree path から所有元 repo root を復元する。"""
    parts = repo_root.resolve().parts
    markers = (
        (".cmoc", "worktrees", session_id),
        (".cmoc", "worktrees", "apply", session_id),
    )
    for marker in markers:
        for index in range(0, len(parts) - len(marker)):
            if parts[index : index + len(marker)] != marker:
                continue
            if len(parts) == index + len(marker) + 1:
                return Path(*parts[:index])
    return None


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
            "last_joined_apply_oracle_snapshot_commit": None,
        },
        "apply": {
            "state": "ready",
            "apply_branch": None,
            "oracle_snapshot_commit": None,
        },
    }


def resolve_session_home_branch(
    repo_root: Path,
    state: dict[str, object],
    session_branch: str,
) -> str:
    """null 初期値の session home branch を session branch から復元する。"""
    session = state.get("session")
    if not isinstance(session, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session セクションを確認して復旧してください。",
                "復旧できない場合は、対象 session を破棄して新しい session でやり直してください。",
            ],
        )
    existing = session.get("session_home_branch")
    if isinstance(existing, str) and existing:
        return existing
    start_commit = session.get("session_start_commit")
    if not isinstance(start_commit, str) or not start_commit:
        raise CmocError(
            "session home branch を特定できませんでした。",
            [
                "session state の session.session_start_commit を確認してください。",
                "state が壊れている場合は、手動で session state を復旧してください。",
            ],
            f"session.session_start_commit: {start_commit}",
        )

    candidates = _session_home_branch_candidates(
        repo_root,
        session_branch,
        start_commit,
    )
    if not candidates:
        raise CmocError(
            "session home branch を特定できませんでした。",
            [
                "session fork 元の local branch が削除されていないか確認してください。",
                "必要な branch を復元してから再実行してください。",
            ],
            f"session_start_commit: {start_commit}",
        )
    if len(candidates) == 1:
        return candidates[0]

    checked_out = set(_checked_out_local_branches(repo_root))
    checked_out_candidates = [
        branch for branch in candidates if branch in checked_out
    ]
    if len(checked_out_candidates) == 1:
        return checked_out_candidates[0]

    exact_tip_candidates = [
        branch
        for branch in candidates
        if _branch_head(repo_root, branch) == start_commit
    ]
    if len(exact_tip_candidates) == 1:
        return exact_tip_candidates[0]

    raise CmocError(
        "session home branch を一意に特定できませんでした。",
        [
            "session fork 元の local branch だけを残してから再実行してください。",
            "判断できる場合は session state の session.session_home_branch を復旧してください。",
        ],
        "\n".join(candidates),
    )


def _session_home_branch_candidates(
    repo_root: Path,
    session_branch: str,
    start_commit: str,
) -> list[str]:
    """session_start_commit から分岐した通常 local branch 候補を返す。"""
    candidates: list[str] = []
    for branch in _local_non_cmoc_branches(repo_root):
        merge_base = run_git(
            repo_root,
            ["merge-base", branch, session_branch],
            check=False,
        )
        if merge_base.returncode != 0:
            continue
        if merge_base.stdout.strip() == start_commit:
            candidates.append(branch)
    return candidates


def _local_non_cmoc_branches(repo_root: Path) -> list[str]:
    """cmoc 管理ではない local branch 名を列挙する。"""
    result = run_git(
        repo_root,
        ["for-each-ref", "--format=%(refname:short)", "refs/heads"],
    )
    return sorted(
        branch
        for branch in result.stdout.splitlines()
        if branch and not is_cmoc_branch(branch)
    )


def _checked_out_local_branches(repo_root: Path) -> list[str]:
    """worktree で checkout されている local branch 名を列挙する。"""
    result = run_git(repo_root, ["worktree", "list", "--porcelain"])
    branches: list[str] = []
    for line in result.stdout.splitlines():
        if not line.startswith("branch refs/heads/"):
            continue
        branch = line.removeprefix("branch refs/heads/")
        if branch and not is_cmoc_branch(branch):
            branches.append(branch)
    return branches


def _branch_head(repo_root: Path, branch: str) -> str | None:
    """branch の HEAD commit を返す。"""
    result = run_git(
        repo_root,
        ["rev-parse", "--verify", branch],
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def write_session_state(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
) -> Path:
    """session state JSON を保存する。"""
    path = session_state_path(repo_root, session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = _session_state_payload(state, path)
    _validate_session_state_schema(payload, path)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    return path


def _session_state_payload(
    state: dict[str, object],
    path: Path,
) -> dict[str, object]:
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
    _validate_required_keys(session, SESSION_STATE_KEYS, "session", path)
    _validate_required_keys(
        apply,
        APPLY_STATE_KEYS,
        "apply",
        path,
    )
    return {
        "session": {
            "state": session.get("state"),
            "session_home_branch": session.get("session_home_branch"),
            "session_start_commit": session.get("session_start_commit"),
            "last_joined_apply_oracle_snapshot_commit": session.get(
                "last_joined_apply_oracle_snapshot_commit"
            ),
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
        payload = json.loads(
            _read_utf8_text(
                path,
                "session state ファイルを読めませんでした。",
                [
                    ".cmoc/sessions 配下のファイル権限と状態を確認してください。",
                    "破損した session state を復旧または退避してから再実行してください。",
                ],
            )
        )
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
    _validate_exact_keys(payload, {"session", "apply"}, "root", path)
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
    _validate_exact_keys(session, SESSION_STATE_KEYS, "session", path)
    _validate_exact_keys(
        apply,
        APPLY_STATE_KEYS,
        "apply",
        path,
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
    _validate_optional_string(
        session,
        "last_joined_apply_oracle_snapshot_commit",
        "session.last_joined_apply_oracle_snapshot_commit",
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
    _validate_apply_state_invariants(apply, apply_state, path, path.stem)


def _validate_required_keys(
    section: dict[object, object],
    required_keys: set[str],
    label: str,
    path: Path,
) -> None:
    """永続化元 state が固定スキーマの定義済み key を持つことを検証する。"""
    missing = required_keys - set(section)
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                f"{label} セクションの不足 field を確認してください。",
                "破損した session state を復旧してください。",
            ],
            f"{path}\nmissing {label} fields: {missing_text}",
        )


def _validate_exact_keys(
    section: dict[object, object],
    expected_keys: set[str],
    label: str,
    path: Path,
    *,
    optional_keys: set[str] | None = None,
) -> None:
    """読み込んだ永続 state の key 集合が固定スキーマと一致することを検証する。"""
    actual_keys = set(section)
    allowed_keys = expected_keys | (optional_keys or set())
    if expected_keys <= actual_keys <= allowed_keys:
        return
    missing = expected_keys - actual_keys
    extra = actual_keys - allowed_keys
    detail_parts: list[str] = [str(path)]
    if missing:
        detail_parts.append(f"missing {label} fields: {', '.join(sorted(missing))}")
    if extra:
        detail_parts.append(f"unknown {label} fields: {', '.join(sorted(extra))}")
    raise CmocError(
        "session state ファイルの形式が不正です。",
        [
            f"{label} セクションの field 集合を確認してください。",
            "破損した session state を復旧してください。",
        ],
        "\n".join(detail_parts),
    )


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
    session_id: str,
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

    if apply_state == "running":
        _validate_apply_run_fields(apply_branch, oracle_snapshot_commit, path)
        _validate_apply_branch_session_id(apply_branch, session_id, path)
        return

    if apply_state == "completed":
        _validate_apply_run_fields(apply_branch, oracle_snapshot_commit, path)
        _validate_apply_branch_session_id(apply_branch, session_id, path)
        return

    if apply_state == "error" and (
        apply_branch is not None or oracle_snapshot_commit is not None
    ):
        _validate_apply_run_fields(apply_branch, oracle_snapshot_commit, path)
        _validate_apply_branch_session_id(apply_branch, session_id, path)


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


def _validate_apply_branch_session_id(
    apply_branch: object,
    session_id: str,
    path: Path,
) -> None:
    """apply branch がこの session state に属することを検証する。"""
    if not isinstance(apply_branch, str):
        return
    branch_session_id = session_id_from_branch(apply_branch)
    if branch_session_id == session_id:
        return
    raise CmocError(
        "session state ファイルの形式が不正です。",
        [
            "apply.apply_branch は同じ session の apply branch である必要があります。",
            "破損した session state を復旧してください。",
        ],
        "\n".join(
            [
                str(path),
                f"session id: {session_id}",
                f"apply branch session id: {branch_session_id}",
                f"apply.apply_branch: {apply_branch}",
            ]
        ),
    )


def active_session_ids_for_home_branch(
    repo_root: Path,
    session_home_branch: str,
) -> list[str]:
    """指定 home branch に紐づく active session id を列挙する。

    active session の一意性は state file と session branch の両方で守る。
    片方だけが残る状態は新規 session 作成を進めず、手動復旧を促す。
    """
    session_branch_names = _session_branch_names(repo_root)
    session_branch_ids = {
        branch_name.removeprefix(SESSION_BRANCH_PREFIX)
        for branch_name in session_branch_names
    }
    session_root = session_state_root(repo_root) / ".cmoc" / "sessions"
    if not session_root.exists():
        if session_branch_ids:
            _raise_session_state_branch_mismatch(
                "session state がない session branch が存在します。",
                session_branch_names,
            )
        return []

    session_ids: list[str] = []
    state_session_ids: set[str] = set()
    for path in sorted(session_root.glob("*.json")):
        payload = _read_existing_session_state(path)
        session = payload["session"]
        session_id = path.stem
        state_session_ids.add(session_id)
        if (
            session.get("state") == "active"
            and session_id not in session_branch_ids
        ):
            _raise_session_state_branch_mismatch(
                "active session state に対応する session branch が存在しません。",
                [f"{SESSION_BRANCH_PREFIX}{session_id}"],
            )
        if (
            session.get("state") == "active"
            and (
                session.get("session_home_branch") == session_home_branch
                or _active_session_home_branch_matches(
                    repo_root,
                    session_id,
                    session,
                    session_home_branch,
                )
            )
        ):
            session_ids.append(session_id)
    orphan_branch_ids = sorted(session_branch_ids - state_session_ids)
    if orphan_branch_ids:
        _raise_session_state_branch_mismatch(
            "session state がない session branch が存在します。",
            [
                f"{SESSION_BRANCH_PREFIX}{session_id}"
                for session_id in orphan_branch_ids
            ],
        )
    return session_ids


def _active_session_home_branch_matches(
    repo_root: Path,
    session_id: str,
    session: dict[str, object],
    session_home_branch: str,
) -> bool:
    """home branch が null の active session を復元し、判定不能なら止める。"""
    if session.get("session_home_branch") is not None:
        return False
    start_commit = session.get("session_start_commit")
    if not isinstance(start_commit, str) or not start_commit:
        _raise_unresolved_active_session_home_branch(
            session_id,
            "session.session_start_commit が不正です。",
            [f"session.session_start_commit: {start_commit}"],
        )
    session_branch = f"{SESSION_BRANCH_PREFIX}{session_id}"
    candidates = _session_home_branch_candidates(
        repo_root,
        session_branch,
        start_commit,
    )
    if len(candidates) == 1:
        return candidates[0] == session_home_branch
    detail_items = [
        f"session branch: {session_branch}",
        f"session_start_commit: {start_commit}",
    ]
    if candidates:
        detail_items.extend(f"candidate: {branch}" for branch in candidates)
    else:
        detail_items.append("candidate: (none)")
    _raise_unresolved_active_session_home_branch(
        session_id,
        "session home branch を一意に特定できませんでした。",
        detail_items,
    )


def _raise_unresolved_active_session_home_branch(
    session_id: str,
    reason: str,
    detail_items: list[str],
) -> None:
    """home branch 未確定の active session を fail closed にする。"""
    raise CmocError(
        "home branch 未確定の active session が存在します。",
        [
            "この状態では active session の一意性を判定できないため、新しい session は開始できません。",
            "既存 session を join/abandon するか、session state の session.session_home_branch を復旧してください。",
        ],
        "\n".join([f"session id: {session_id}", reason, *detail_items]),
    )


def _session_branch_names(repo_root: Path) -> list[str]:
    """local session branch 名を列挙する。"""
    result = run_git(
        repo_root,
        [
            "for-each-ref",
            "--format=%(refname:short)",
            f"refs/heads/{SESSION_BRANCH_PREFIX}",
        ],
    )
    return sorted(
        branch_name
        for branch_name in result.stdout.splitlines()
        if is_session_branch(branch_name)
    )


def _raise_session_state_branch_mismatch(
    message: str,
    detail_items: list[str],
) -> None:
    """session state と branch の不整合を fail closed にする。"""
    raise CmocError(
        message,
        [
            ".cmoc/sessions と refs/heads/cmoc/session を確認してください。",
            "不整合を復旧または不要な session branch を削除してから再実行してください。",
        ],
        "\n".join(detail_items),
    )


def ensure_cmoc_ignored(repo_root: Path) -> bool:
    """`.cmoc` が git 追跡対象外であることを機械的に保証する。"""
    # `.gitignore` に必要な行を保証し、既に tracked な `.cmoc` は index から外す。
    changed = _ensure_cmoc_ignore_rule(repo_root)
    tracked = _tracked_cmoc_paths(repo_root)
    if tracked:
        _remove_cmoc_from_index(repo_root, env={})
        changed = True

    # gitignore と git index の両面から完了条件を検証する。
    _assert_cmoc_ignore_guarantee(repo_root)
    return changed


def ensure_cmoc_ignored_and_committed(
    repo_root: Path,
    message: str = "Initialize cmoc",
) -> bool:
    """`.cmoc` ignore 保証で発生した内部差分を commit まで完了する。"""
    had_cmoc_rule = gitignore_has_cmoc_rule(repo_root)
    preexisting_staged_diff = staged_diff_from_head(repo_root)
    changed = ensure_cmoc_ignored(repo_root)
    if not changed:
        return False
    return commit_cmoc_initialization_changes(
        repo_root,
        had_cmoc_rule,
        preexisting_staged_diff,
        message,
    )


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
    _raise_uncommitted_changes(paths)


def assert_no_uncommitted_changes_outside_cmoc(repo_root: Path) -> None:
    """`.cmoc` 管理領域以外に未コミット差分がないことを確認する。"""
    paths = [
        path
        for path in changed_paths(repo_root)
        if not _is_cmoc_managed_path(path)
    ]
    _raise_uncommitted_changes(paths)


def _raise_uncommitted_changes(paths: list[str]) -> None:
    """未コミット path 一覧が空でなければ共通エラーを送出する。"""
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
    """作業ツリーの `.gitignore` が有効な `/.cmoc/` 専用行を持つか返す。"""
    # init 開始前から guarantee 済みの ignore ルールを、init 差分と区別する。
    gitignore = repo_root / ".gitignore"
    if not gitignore.exists():
        return False
    content = _read_gitignore_text(gitignore)
    return _gitignore_content_has_effective_cmoc_rule(content)


def staged_diff_from_head(repo_root: Path) -> str:
    """現在 stage 済みの差分を HEAD 基準の patch として返す。"""
    # init commit 後に利用者の stage 済み差分だけを復元するため事前保存する。
    # `.cmoc` は init の完了条件として必ず index から外すため復元対象にしない。
    result = run_git(
        repo_root,
        [
            "diff",
            "--cached",
            "--binary",
            "--full-index",
            "--",
            ".",
            ":(exclude,literal).cmoc",
        ],
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
        if parent_hash is None:
            _stage_worktree_gitignore(repo_root, env)
        elif not had_cmoc_rule:
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
    with tempfile.TemporaryDirectory(prefix="cmoc-restore-index-") as temp_name:
        restored_index = Path(temp_name) / "index"
        _write_restored_index_after_internal_commit(
            repo_root,
            restored_index,
            commit_hash,
            preexisting_staged_diff,
            remove_cmoc=True,
        )
        _assert_cmoc_ignore_guarantee(
            repo_root,
            env={"GIT_INDEX_FILE": str(restored_index)},
        )
        update_ref_args = ["update-ref", "HEAD", commit_hash]
        if parent_hash is not None:
            update_ref_args.append(parent_hash)
        run_git(repo_root, update_ref_args)
        _replace_git_index(repo_root, restored_index)
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

        add_paths = [path for path in paths if not _is_cmoc_managed_path(path)]
        if add_paths:
            run_git(
                repo_root,
                ["add", "-f", "--", *_literal_pathspecs(add_paths)],
                env=env,
            )
        if any(_is_cmoc_managed_path(path) for path in paths):
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
    with tempfile.TemporaryDirectory(prefix="cmoc-restore-index-") as temp_name:
        restored_index = Path(temp_name) / "index"
        staged_diff = staged_outside_paths + staged_inside_paths
        _write_restored_index_after_internal_commit(
            repo_root,
            restored_index,
            commit_hash,
            staged_diff,
            remove_cmoc=bool(staged_diff),
        )
        update_ref_args = ["update-ref", "HEAD", commit_hash]
        if parent_hash is not None:
            update_ref_args.append(parent_hash)
        run_git(repo_root, update_ref_args)
        _replace_git_index(repo_root, restored_index)
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


def _is_cmoc_managed_path(relative_path: str) -> bool:
    """`.cmoc` 管理領域そのもの、またはその配下なら True を返す。"""
    return relative_path == ".cmoc" or relative_path.startswith(".cmoc/")


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


def filter_oracle_file_paths_at_commit(
    repo_root: Path,
    commit_hash: str,
    relative_paths: list[str],
) -> list[str]:
    """指定 commit の root `.gitignore` で oracles ファイルだけを返す。"""
    candidates = sorted(
        {
            path
            for path in relative_paths
            if path.startswith("oracles/")
            and Path(path).name != "INDEX.md"
        }
    )
    ignored = root_gitignored_paths_at_commit(repo_root, commit_hash, candidates)
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


def filter_apply_implementation_file_paths(
    repo_root: Path,
    relative_paths: list[str],
) -> list[str]:
    """root 相対 path から apply の調査対象になる実装ファイルだけを返す。"""
    candidates = sorted(
        {
            path
            for path in relative_paths
            if not _is_excluded_implementation_path(path)
            and not _is_forbidden_apply_investigation_path(path)
        }
    )
    ignored = _root_gitignored_paths(repo_root, candidates)
    return [path for path in candidates if path not in ignored]


def filter_apply_implementation_file_paths_at_commit(
    repo_root: Path,
    commit_hash: str,
    relative_paths: list[str],
) -> list[str]:
    """指定 commit の root `.gitignore` で apply 実装調査対象だけを返す。"""
    candidates = sorted(
        {
            path
            for path in relative_paths
            if not _is_excluded_implementation_path(path)
            and not _is_forbidden_apply_investigation_path(path)
        }
    )
    ignored = root_gitignored_paths_at_commit(repo_root, commit_hash, candidates)
    return [path for path in candidates if path not in ignored]


def is_apply_implementation_path(repo_root: Path, relative_path: str) -> bool:
    """root 相対 path が apply の調査対象になる実装ファイルか判定する。"""
    return (
        not _is_forbidden_apply_investigation_path(relative_path)
        and is_implementation_path(repo_root, relative_path)
    )


def root_gitignored_paths(
    repo_root: Path,
    relative_paths: list[str],
) -> set[str]:
    """root `.gitignore` の pattern に一致する path 集合を返す。"""
    return _root_gitignored_paths(repo_root, relative_paths)


def root_gitignored_paths_at_commit(
    repo_root: Path,
    commit_hash: str,
    relative_paths: list[str],
) -> set[str]:
    """指定 commit の root `.gitignore` pattern に一致する path 集合を返す。"""
    if not relative_paths:
        return set()
    result = run_git(
        repo_root,
        ["show", f"{commit_hash}:.gitignore"],
        check=False,
    )
    if result.returncode != 0:
        return set()
    return _root_gitignored_paths_from_content(relative_paths, result.stdout)


def changed_oracle_files(repo_root: Path, base_commit: str) -> list[Path]:
    """部分評価対象となる変更済み oracle ファイルを列挙する。"""
    # base..HEAD の履歴上で起きた追加・変更・rename などを収集する。
    collected: set[Path] = set()
    committed = run_git(
        repo_root,
        [
            "log",
            "--name-status",
            "-z",
            "-M",
            "--diff-filter=ACMRT",
            "--format=",
            f"{base_commit}..HEAD",
            "--",
            "oracles",
        ],
    )
    collected.update(_changed_paths_from_name_status(repo_root, committed.stdout))

    # 未コミットの working tree/staging 変更も部分評価対象に加える。
    uncommitted = run_git(
        repo_root,
        [
            "diff",
            "--name-status",
            "-z",
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
            "-z",
            "-M",
            "--diff-filter=ACMRT",
            "--",
            "oracles",
        ],
    )
    for output in [uncommitted.stdout, staged.stdout]:
        collected.update(_changed_paths_from_name_status(repo_root, output))

    # 未追跡 oracle ファイルは Git の ignore 判定を通さず、oracle
    # ファイル列挙候補と tracked path の差分として収集する。
    collected.update(_untracked_oracle_files(repo_root))

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
            "-z",
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
            "-z",
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
            "-z",
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

    # 未追跡実装ファイルは Git の ignore 判定を通さず、仕様上の実装
    # ファイル列挙候補と tracked path の差分として収集する。
    collected.update(_untracked_implementation_files(repo_root))

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
    return {
        repo_root / paths[-1]
        for status, paths in git_name_status_entries(output)
        if status[:1] in {"A", "C", "M", "R", "T"} and paths
    }


def _untracked_oracle_files(repo_root: Path) -> set[Path]:
    """Git ignore に隠れたものも含め、未追跡 oracle ファイルを返す。"""
    return _untracked_files_from_candidates(
        repo_root,
        list_oracle_files(repo_root),
        ["oracles"],
    )


def _untracked_implementation_files(repo_root: Path) -> set[Path]:
    """Git ignore に隠れたものも含め、未追跡実装ファイルを返す。"""
    return _untracked_files_from_candidates(
        repo_root,
        list_implementation_files(repo_root),
        ["."],
    )


def _untracked_files_from_candidates(
    repo_root: Path,
    candidates: list[Path],
    pathspecs: list[str],
) -> set[Path]:
    """仕様上の候補集合から Git 追跡済み path を除いた集合を返す。"""
    tracked = set(
        git_name_only_paths(
            run_git(
                repo_root,
                ["ls-files", "-z", "--", *pathspecs],
            ).stdout
        )
    )
    return {
        path
        for path in candidates
        if path.relative_to(repo_root).as_posix() not in tracked
    }


def has_deleted_oracle_files(repo_root: Path, base_commit: str) -> bool:
    """評価モード切替用に oracle 削除有無を判定する。"""
    # committed 履歴、working tree、staging area の削除をすべて切替条件にする。
    commands = [
        [
            "log",
            "--name-status",
            "-z",
            "-M",
            "--diff-filter=DR",
            "--format=",
            f"{base_commit}..HEAD",
        ],
        ["diff", "--name-status", "-z", "-M", "--diff-filter=DR", "HEAD"],
        ["diff", "--cached", "--name-status", "-z", "-M", "--diff-filter=DR"],
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
            "--name-status",
            "-z",
            "-M",
            "--diff-filter=DR",
            "--format=",
            f"{base_commit}..HEAD",
        ],
        ["diff", "--name-status", "-z", "-M", "--diff-filter=DR", "HEAD"],
        ["diff", "--cached", "--name-status", "-z", "-M", "--diff-filter=DR"],
    ]
    for command in commands:
        result = run_git(repo_root, [*command, "--", "."])
        if _deleted_implementation_changes_from_name_status(
            repo_root,
            result.stdout,
        ):
            return True
    return False


def _deleted_oracle_changes_from_name_status(
    repo_root: Path,
    output: str,
) -> list[str]:
    """`git name-status` から oracle 削除相当の変更を取り出す。"""
    # oracle から非 oracle への rename は、oracle 集合から見れば削除である。
    deleted: list[str] = []
    for status, paths in git_name_status_entries(output):
        if status == "D":
            deleted.extend(filter_oracle_file_paths(repo_root, paths[:1]))
            continue
        if not status.startswith("R") or len(paths) < 2:
            continue
        source_oracles = filter_oracle_file_paths(repo_root, [paths[0]])
        destination_oracles = filter_oracle_file_paths(repo_root, [paths[1]])
        if source_oracles and not destination_oracles:
            deleted.extend(source_oracles)
    return deleted


def _deleted_implementation_changes_from_name_status(
    repo_root: Path,
    output: str,
) -> list[str]:
    """`git name-status` から実装ファイル削除相当の変更を取り出す。"""
    # 実装ファイルから非実装ファイルへの rename は、実装ファイル集合から
    # 見れば削除である。削除済み path は存在確認できないため、path 規則と
    # gitignore だけで判定する。
    deleted: list[str] = []
    for status, paths in git_name_status_entries(output):
        if status == "D":
            deleted.extend(
                path
                for path in paths[:1]
                if is_implementation_path(repo_root, path)
            )
            continue
        if not status.startswith("R") or len(paths) < 2:
            continue
        source_is_implementation = is_implementation_path(repo_root, paths[0])
        destination_is_implementation = is_implementation_path(
            repo_root,
            paths[1],
        )
        if source_is_implementation and not destination_is_implementation:
            deleted.append(paths[0])
    return deleted


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


def _is_forbidden_apply_investigation_path(relative_path: str) -> bool:
    """Codex read-only 調査の起点にしてはいけない path か判定する。"""
    return relative_path == "memo" or relative_path.startswith("memo/")


def read_session_start_commit(repo_root: Path, branch_name: str) -> str:
    """cmoc session state から session start commit を読む。"""
    session_id = session_id_from_branch(branch_name)
    payload = read_session_state(session_state_root(repo_root), session_id)
    session = payload.get("session")
    if not isinstance(session, dict):
        raise CmocError(
            "session state ファイルに session セクションがありません。",
            [
                "state JSON の内容を確認し、session セクションを復旧してください。",
                "復旧できない場合は、現在の session を使わず新しい session を開始してください。",
            ],
            f"branch: {branch_name}",
        )
    start_commit = session.get("session_start_commit")
    if not isinstance(start_commit, str) or not start_commit:
        raise CmocError(
            "session start commit が session state に記録されていません。",
            [
                "差分評価の前に `cmoc session fork` を実行してください。",
                "全 oracle ファイルを評価する場合は `cmoc review oracles --full` を実行してください。",
            ],
            f"branch: {branch_name}",
        )
    return start_commit


def changed_paths(repo_root: Path) -> list[str]:
    """未コミット差分のパスを porcelain から取り出す。"""
    # rename 行は新しい path だけを返す。
    result = run_git(repo_root, ["status", "--porcelain=v1", "-z"])
    return [path for _status, path in git_status_paths(result.stdout)]


def git_name_only_paths(output: str) -> list[str]:
    """`git ... --name-only -z` の path token を返す。"""
    return [token for token in output.split("\0") if token]


def git_name_status_entries(output: str) -> list[tuple[str, list[str]]]:
    """`git ... --name-status -z` の status と path token を返す。"""
    tokens = git_name_only_paths(output)
    entries: list[tuple[str, list[str]]] = []
    index = 0
    while index < len(tokens):
        status = tokens[index]
        index += 1
        path_count = 2 if status[:1] in {"R", "C"} else 1
        paths = tokens[index:index + path_count]
        index += path_count
        if len(paths) == path_count:
            entries.append((status, paths))
    return entries


def git_status_paths(output: str) -> list[tuple[str, str]]:
    """`git status --porcelain=v1 -z` の status と変更後 path を返す。"""
    tokens = git_name_only_paths(output)
    entries: list[tuple[str, str]] = []
    index = 0
    while index < len(tokens):
        entry = tokens[index]
        index += 1
        if len(entry) < 4:
            continue
        status = entry[:2]
        path = entry[3:]
        entries.append((status, path))
        if status[:1] in {"R", "C"} or status[1:2] in {"R", "C"}:
            index += 1
    return entries


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


def _restore_index_after_internal_commit(
    repo_root: Path,
    staged_diff: str,
    *,
    remove_cmoc: bool,
) -> None:
    """内部 commit 後の index を一時 index で復元し、成功後だけ本体へ反映する。"""
    with tempfile.TemporaryDirectory(prefix="cmoc-restore-index-") as temp_name:
        temp_index = Path(temp_name) / "index"
        _write_restored_index_after_internal_commit(
            repo_root,
            temp_index,
            "HEAD",
            staged_diff,
            remove_cmoc=remove_cmoc,
        )
        _replace_git_index(repo_root, temp_index)


def _write_restored_index_after_internal_commit(
    repo_root: Path,
    index_path: Path,
    base_ref: str,
    staged_diff: str,
    *,
    remove_cmoc: bool,
) -> None:
    """内部 commit 後に使う index 内容を指定 path へ組み立てる。"""
    env = {"GIT_INDEX_FILE": str(index_path)}
    run_git(repo_root, ["read-tree", "--reset", base_ref], env=env)

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
    if _gitignore_content_has_effective_cmoc_rule(head_text):
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


def _stage_worktree_gitignore(repo_root: Path, env: dict[str, str]) -> None:
    """作業ツリーの `.gitignore` を指定 index に stage する。"""
    # unborn HEAD では親 tree が無いため、既存 ignore rule を初期 commit に載せる。
    run_git(repo_root, ["add", "-f", "--", ".gitignore"], env=env)


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
    # broad rule ではなく、oracle 指定の専用行が有効な場合だけ重複を避ける。
    gitignore = repo_root / ".gitignore"
    existing = _read_gitignore_text(gitignore) if gitignore.exists() else ""
    if _gitignore_content_has_effective_cmoc_rule(existing):
        return False

    # 既存内容の末尾改行を整えてから ignore 行を追加する。
    prefix = existing
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    gitignore.write_text(f"{prefix}/.cmoc/\n", encoding="utf-8")
    return True


def _read_gitignore_text(path: Path) -> str:
    """root `.gitignore` を UTF-8 text として読む。"""
    return _read_utf8_text(
        path,
        ".gitignore ファイルを読めませんでした。",
        [
            ".gitignore のファイル権限と文字コードを確認してください。",
            ".gitignore を UTF-8 で読める内容に復旧してから再実行してください。",
        ],
    )


def _read_utf8_text(path: Path, message: str, actions: list[str]) -> str:
    """repo-local text file を UTF-8 として読み、失敗を CmocError に変換する。"""
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise CmocError(message, actions, f"{path}\n{error}") from error
    except UnicodeDecodeError as error:
        raise CmocError(
            message,
            actions,
            f"{path}\nUTF-8 decode error: {error}",
        ) from error


def _assert_cmoc_ignore_guarantee(
    repo_root: Path,
    env: dict[str, str] | None = None,
) -> None:
    """`.cmoc` 追跡対象外保証の完了条件を検証する。"""
    # tracked path と ignore probe の両方で保証状態を確認する。
    tracked = _tracked_cmoc_paths(repo_root, env=env)
    ignored = _is_cmoc_ignore_probe_ignored(repo_root)
    if tracked or not ignored:
        raise CmocError(
            ".cmoc が git 追跡対象外として初期化されていません。",
            [
                "先に `cmoc init` を実行してください。",
                ".gitignore と git index を確認してください。",
                "追跡済みの .cmoc ファイルは `cmoc init` で index から外してください。",
            ],
            "\n".join(tracked)
            or f"probe が ignore されませんでした: {CMOC_IGNORE_PROBE_PATH}",
        )


def _tracked_cmoc_paths(
    repo_root: Path,
    env: dict[str, str] | None = None,
) -> list[str]:
    """git index に残っている `.cmoc` 配下パスを返す。"""
    # `git ls-files` の空でない行だけを tracked path として返す。
    result = run_git(repo_root, ["ls-files", "--", ".cmoc"], env=env)
    return [line for line in result.stdout.splitlines() if line]


def _is_root_gitignored(repo_root: Path, relative_path: str) -> bool:
    """root `.gitignore` の pattern だけで ignore 対象か判定する。"""
    # 単一 path の判定も集合判定の実装に揃える。
    return relative_path in _root_gitignored_paths(repo_root, [relative_path])


def _gitignore_content_ignores_cmoc_probe(gitignore_content: str) -> bool:
    """root `.gitignore` 内容が `.cmoc` probe を ignore するか返す。"""
    return (
        CMOC_IGNORE_PROBE_PATH
        in _root_gitignored_paths_from_content(
            [CMOC_IGNORE_PROBE_PATH],
            gitignore_content,
        )
    )


def _gitignore_content_has_effective_cmoc_rule(gitignore_content: str) -> bool:
    """root `.gitignore` 内容に有効な `/.cmoc/` 専用行があるか返す。"""
    return (
        _gitignore_content_has_cmoc_rule_line(gitignore_content)
        and _gitignore_content_ignores_cmoc_probe(gitignore_content)
    )


def _gitignore_content_has_cmoc_rule_line(gitignore_content: str) -> bool:
    """root `.gitignore` 内容に oracle 指定の `/.cmoc/` 行があるか返す。"""
    return any(line.strip() == "/.cmoc/" for line in gitignore_content.splitlines())


def _is_cmoc_ignore_probe_ignored(repo_root: Path) -> bool:
    """実リポジトリで `.cmoc` probe が ignore 対象か判定する。"""
    result = run_git(
        repo_root,
        ["check-ignore", "-q", "--", CMOC_IGNORE_PROBE_PATH],
        check=False,
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    raise CmocError(
        ".cmoc ignore probe の評価に失敗しました。",
        [
            ".gitignore の構文を確認してからコマンドを再実行してください。",
            "git check-ignore が実行できる状態にしてから再実行してください。",
        ],
        result.stderr.strip(),
    )


def _root_gitignored_paths(
    repo_root: Path,
    relative_paths: list[str],
) -> set[str]:
    """root `.gitignore` だけを Git の wildmatch semantics で評価する。"""
    # 評価対象または root `.gitignore` が無ければ ignore 対象なしとして返す。
    gitignore = repo_root / ".gitignore"
    if not relative_paths or not gitignore.exists():
        return set()
    return _root_gitignored_paths_from_content(
        relative_paths,
        gitignore.read_text(encoding="utf-8"),
    )


def _root_gitignored_paths_from_content(
    relative_paths: list[str],
    gitignore_content: str,
) -> set[str]:
    """root `.gitignore` 内容で path 集合を Git wildmatch 評価する。"""
    if not relative_paths or not gitignore_content:
        return set()

    # 一時 git repository に root `.gitignore` だけを複製して評価環境を作る。
    env = _root_gitignore_git_env()
    with tempfile.TemporaryDirectory(prefix="cmoc-gitignore-") as temp_name:
        temp_root = Path(temp_name)
        (temp_root / ".gitignore").write_text(
            gitignore_content,
            encoding="utf-8",
        )
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
                "-z",
                "--no-index",
                "--stdin",
            ],
            cwd=temp_root,
            check=False,
            input=b"\0".join(os.fsencode(path) for path in relative_paths)
            + b"\0",
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
            result.stderr.decode(errors="replace").strip(),
        )

    # `git check-ignore` が出力した path だけを ignore 対象集合として返す。
    return {
        os.fsdecode(path)
        for path in result.stdout.split(b"\0")
        if path
    }


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
    result = subprocess.run(
        ["git", "check-ignore", "-z", "--no-index", "--stdin"],
        cwd=repo_root,
        check=False,
        input=b"\0".join(os.fsencode(path) for path in relative_paths)
        + b"\0",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode not in {0, 1}:
        raise CmocError(
            ".gitignore の評価に失敗しました。",
            [
                ".gitignore の構文を確認してからコマンドを再実行してください。",
                "一時的に .gitignore を単純化してから cmoc を再実行してください。",
            ],
            result.stderr.decode(errors="replace").strip(),
        )
    return {
        os.fsdecode(path)
        for path in result.stdout.split(b"\0")
        if path
    }


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
