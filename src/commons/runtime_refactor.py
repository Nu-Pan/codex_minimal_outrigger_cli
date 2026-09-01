"""realization refactor の調査 state を検証・同期・永続化する。"""

import json
import re
import string
from collections.abc import Collection
from pathlib import Path
from typing import Literal, TypedDict, cast

from .runtime_content import file_sha256
from .runtime_errors import CmocError
from .runtime_git import enumerate_oracle_and_realization_files
from .runtime_paths import refactor_state_path

_InvestigationResult = Literal["not_investigated", "no_findings", "findings"]


class RefactorEntry(TypedDict):
    """単一の oracle または realization file の調査履歴。"""

    investigation_required: bool
    last_investigation_result: _InvestigationResult
    last_investigated_sha256: str | None
    last_investigated_at: str | None


RefactorState = dict[str, RefactorEntry]


def load_refactor_state(root: Path) -> RefactorState:
    """refactor state を読み、履歴を破棄せず schema を検証する。

    根拠: {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    """
    path = refactor_state_path(root)
    _reject_symlinked_state_path(path)
    _reject_non_file_state_path(path)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise _invalid_refactor_state(path, "JSON を読み込めません。") from exc
    return _validated_state(path, data)


def write_refactor_state(root: Path, state: RefactorState) -> None:
    """refactor state を path 順の安定した JSON 表現で保存する。"""
    path = refactor_state_path(root)
    _reject_symlinked_state_path(path)
    _reject_non_file_state_path(path)
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
    state = original
    if sync_entries:
        synchronized: RefactorState = {}
        for relative in enumerate_refactor_targets(root):
            digest = file_sha256(root / relative)
            entry = state.get(relative)
            if entry is None:
                entry = new_refactor_entry()
            else:
                entry = {
                    "investigation_required": entry["investigation_required"],
                    "last_investigation_result": entry["last_investigation_result"],
                    "last_investigated_sha256": entry["last_investigated_sha256"],
                    "last_investigated_at": entry["last_investigated_at"],
                }
                if entry["last_investigated_sha256"] != digest:
                    entry["investigation_required"] = True
            synchronized[relative] = entry
        state = synchronized
    if not path.exists() or original != state:
        write_refactor_state(root, state)
    return state


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
        "investigation_required": True,
        "last_investigation_result": "not_investigated",
        "last_investigated_sha256": None,
        "last_investigated_at": None,
    }


def select_refactor_target(
    state: RefactorState,
    excluded_paths: Collection[str] = (),
) -> str | None:
    """正本の優先順位で次の investigation target を選ぶ。"""
    candidates = [
        (path, entry)
        for path, entry in state.items()
        if entry["investigation_required"] and path not in excluded_paths
    ]
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda item: (
            item[1]["last_investigation_result"] != "not_investigated",
            item[1]["last_investigated_at"] or "",
            item[0],
        ),
    )[0]


def mark_all_refactor_targets_required(state: RefactorState) -> None:
    """完了済み state から新しい full refactor cycle を開始する。"""
    for entry in state.values():
        entry["investigation_required"] = True


def _reject_symlinked_state_path(path: Path) -> None:
    """state path の symlink 経由アクセスを拒否する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    # state は cmoc が更新する管理 file なので、親 directory を含めて symlink を
    # 追跡すると work-root 外の file を読み書きしてしまう。
    absolute = path.absolute()
    current = absolute
    while current != current.parent:
        if current.is_symlink():
            raise _invalid_refactor_state(
                path, "state path は symlink 経由で扱えません。"
            )
        current = current.parent


def _reject_non_file_state_path(path: Path) -> None:
    """state path が通常 file でない場合の block と raw exception を防ぐ。"""
    if path.exists() and not path.is_file():
        raise _invalid_refactor_state(path, "state path は通常ファイルではありません。")


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
    expected = {
        "investigation_required",
        "last_investigation_result",
        "last_investigated_sha256",
        "last_investigated_at",
    }
    if set(value) != expected:
        raise _invalid_refactor_state(path, f"entry field が不正です: {key}")
    required = value["investigation_required"]
    result = value["last_investigation_result"]
    digest = value["last_investigated_sha256"]
    investigated_at = value["last_investigated_at"]
    if (
        type(required) is not bool
        or not isinstance(result, str)
        or result
        not in {
            "not_investigated",
            "no_findings",
            "findings",
        }
    ):
        raise _invalid_refactor_state(path, f"entry value が不正です: {key}")
    validated_result = cast(_InvestigationResult, result)
    if digest is not None and (
        not isinstance(digest, str)
        or len(digest) != 64
        or any(character not in string.hexdigits for character in digest)
    ):
        raise _invalid_refactor_state(path, f"SHA256 が不正です: {key}")
    # {{work-root}}/oracle/doc/app_spec/timestamp.md
    # state の履歴時刻は、file name と同じ固定幅の {{time-stamp}} にそろえる。
    if investigated_at is not None and (
        not isinstance(investigated_at, str)
        or re.fullmatch(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}_\d{2}_\d{9}", investigated_at)
        is None
    ):
        raise _invalid_refactor_state(path, f"調査日時が不正です: {key}")
    if result == "not_investigated" and (
        digest is not None or investigated_at is not None
    ):
        raise _invalid_refactor_state(path, f"未調査 entry に履歴があります: {key}")
    return {
        "investigation_required": required,
        "last_investigation_result": validated_result,
        "last_investigated_sha256": digest,
        "last_investigated_at": investigated_at,
    }


def _invalid_refactor_state(path: Path, reason: str) -> CmocError:
    """不正な refactor state を利用者向け例外へ変換する。"""
    return CmocError(
        "realization refactor state が不正です。",
        ["既存の調査履歴を保持したまま state file を修復してください。"],
        f"{path}\n{reason}",
    )
