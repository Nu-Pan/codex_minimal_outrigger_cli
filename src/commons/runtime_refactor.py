"""realization refactor の調査 state を検証・同期・永続化する。"""

import json
import re
import stat
from pathlib import Path
from typing import TypedDict

from .runtime_errors import CmocError
from .runtime_git import (
    enumerate_oracle_and_realization_files,
    literal_pathspec,
    run_git,
)
from .runtime_paths import refactor_state_path


class RefactorEntry(TypedDict):
    """run をまたぐ選択順序に使う、起点ごとの最終調査日時。"""

    last_investigated_at: str | None


RefactorState = dict[str, RefactorEntry]


def load_refactor_state(root: Path) -> RefactorState:
    """refactor state を読み、永続情報を破棄せず schema を検証する。

    根拠: {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    """
    path = refactor_state_path(root)
    if not _validate_refactor_state_path(path):
        return {}
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise _invalid_refactor_state(path, "JSON を読み込めません。") from exc
    return _parse_state(path, content)


def write_refactor_state(root: Path, state: RefactorState) -> None:
    """refactor state を path 順の安定した JSON 表現で保存する。"""
    path = refactor_state_path(root)
    _validate_refactor_state_path(path)
    validated = _validated_state(path, state)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        # {{work-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md
        # の「回帰検証」
        # JSON の ASCII escape で surrogateescape された filesystem path も UTF-8
        # の state file へ保存し、列挙結果の entry を失わないようにする。
        json.dumps(dict(sorted(validated.items())), ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )


def sync_refactor_state(root: Path, *, sync_entries: bool = True) -> RefactorState:
    """schema を検証し、必要なら oracle/realization file 集合と同期する。"""
    path = refactor_state_path(root)
    original = load_refactor_state(root)
    state = _synchronized_entries(root, original) if sync_entries else original
    if not path.exists() or original != state:
        write_refactor_state(root, state)
    return state


def merge_refactor_states(
    root: Path, refs: tuple[str, ...], *, sync_entries: bool = True
) -> RefactorState:
    """両 branch の確定日時を統合し、必要なら統合後の tree と同期する。"""
    # Git の自動 merge が古い日時を採用した場合も、確定済みの両側から決め直す。
    path = refactor_state_path(root)
    relative = path.relative_to(root).as_posix()
    merged: RefactorState = {}
    # no-op join で両 HEAD が同じ場合、同じ確定済み state を再取得しない。
    for ref in dict.fromkeys(refs):
        tracked = run_git(
            ["ls-tree", "-z", ref, "--", literal_pathspec(relative)], root
        ).stdout
        if not tracked:
            continue
        if not tracked.startswith(("100644 blob ", "100755 blob ")):
            raise _invalid_refactor_state(path, f"通常 file ではありません: {ref}")
        content = run_git(["show", f"{ref}:{relative}"], root).stdout
        for target, entry in _parse_state(path, content).items():
            previous = merged.get(target)
            if previous is None or (entry["last_investigated_at"] or "") > (
                previous["last_investigated_at"] or ""
            ):
                merged[target] = entry
    if sync_entries:
        merged = _synchronized_entries(root, merged)
    write_refactor_state(root, merged)
    return merged


def _synchronized_entries(root: Path, state: RefactorState) -> RefactorState:
    # 内容は読まず、同じ path の日時をそのまま保持する。
    return {
        relative: state.get(relative, new_refactor_entry())
        for relative in enumerate_refactor_targets(root)
    }


def _parse_state(path: Path, content: str) -> RefactorState:
    # worktree と確定済み branch に同じ schema 検証を適用する。
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise _invalid_refactor_state(path, "JSON を読み込めません。") from exc
    return _validated_state(path, data)


def enumerate_refactor_targets(root: Path) -> list[str]:
    """現在存在する全 oracle file と realization file を列挙する。"""
    # {{work-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md
    # の「分類結果」
    # doctor preprocess と refactor workload は、共通の full-tree 分類結果で
    # state entry を同期する。
    oracle_files, realization_files = enumerate_oracle_and_realization_files(root)
    return sorted(
        path.relative_to(root.absolute()).as_posix()
        for path in [*oracle_files, *realization_files]
    )


def new_refactor_entry() -> RefactorEntry:
    """未調査 file の初期 entry を返す。"""
    return {
        "last_investigated_at": None,
    }


def refactor_cycle_targets(state: RefactorState) -> list[str]:
    """未調査、保存日時の古い順、path の順で全対象の巡回順を固定する。"""
    return sorted(
        state,
        key=lambda path: (
            state[path]["last_investigated_at"] or "",
            path,
        ),
    )


def _validate_refactor_state_path(path: Path) -> bool:
    """state と親の種類を一度ずつ検証し、state file の存在を返す。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    # 祖先から検証し、symlink の参照先へ降りずに file/directory の種類を確認する。
    absolute = path.absolute()
    for current in (*reversed(absolute.parents), absolute):
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            return False
        except OSError as exc:
            raise _invalid_refactor_state(
                path, "state path を検証できません。"
            ) from exc
        if stat.S_ISLNK(mode):
            raise _invalid_refactor_state(
                path, "state path は symlink 経由で扱えません。"
            )
        if current == absolute:
            if not stat.S_ISREG(mode):
                raise _invalid_refactor_state(
                    path, "state path は通常ファイルではありません。"
                )
        elif not stat.S_ISDIR(mode):
            raise _invalid_refactor_state(
                path, "state path の親が通常の directory ではありません。"
            )
    return True


def _validated_state(path: Path, value: object) -> RefactorState:
    """refactor state 全体を schema 検証し、型付けされた state として返す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    """
    if not isinstance(value, dict):
        raise _invalid_refactor_state(
            path, "top-level は object である必要があります。"
        )
    state: RefactorState = {}
    for raw_path, raw_entry in value.items():
        if not isinstance(raw_path, str) or not is_normalized_relative_path(raw_path):
            raise _invalid_refactor_state(path, f"不正な path key: {raw_path!r}")
        state[raw_path] = _validated_entry(path, raw_path, raw_entry)
    return state


def is_normalized_relative_path(value: str) -> bool:
    """refactor 契約で許可される正規化済み work-root 相対 path か判定する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    """
    path = Path(value)
    return (
        bool(path.parts)
        and "\x00" not in value
        and not path.is_absolute()
        and not path.drive
        and not path.root
        and ".." not in path.parts
        and path.as_posix() == value
    )


def _validated_entry(path: Path, key: str, value: object) -> RefactorEntry:
    """JSON の entry を検証し、型付けされた refactor entry として返す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    """
    if not isinstance(value, dict):
        raise _invalid_refactor_state(path, f"entry は object ではありません: {key}")
    if set(value) != {"last_investigated_at"}:
        raise _invalid_refactor_state(path, f"entry field が不正です: {key}")
    investigated_at = value["last_investigated_at"]
    # {{work-root}}/oracle/doc/app_spec/timestamp.md
    # state の履歴時刻はミリ秒精度の {{time-stamp}} として保存する。
    if investigated_at is not None and (
        not isinstance(investigated_at, str)
        or re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}_[0-9]{3}",
            investigated_at,
        )
        is None
    ):
        raise _invalid_refactor_state(path, f"調査日時が不正です: {key}")
    return {
        "last_investigated_at": investigated_at,
    }


def _invalid_refactor_state(path: Path, reason: str) -> CmocError:
    """不正な refactor state を利用者向け例外へ変換する。"""
    return CmocError(
        "realization refactor state が不正です。",
        ["既存の永続情報を保持したまま state file を修復してください。"],
        f"{path}\n{reason}",
    )
