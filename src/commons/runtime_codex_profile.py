"""Codex CLI 起動前後の argv/env/schema/error 判定をまとめる境界。

責務境界は Codex CLI に渡す実行環境と Codex CLI から返る機械的な実行結果の
解釈に閉じている。sandbox/argv/cwd、
CODEX_HOME、child process tracking、schema 配置、JSONL error 判定は同じ
subprocess 境界の不変条件を共有するため、分割すると呼び出し側が同時に読むべき
失敗時文脈が増える。現状は Codex subprocess 境界として一箇所に保つ方が凝集性が高い。
根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import errno
import fcntl
import json
import os
import re
import select
import signal
import subprocess
import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from types import FrameType
from typing import Any

from basic.acp import AgentCallParameter, FileAccessMode
from config.cmoc_config import CmocConfig, JsonTomlValue

from .runtime_config import validate_json_toml_value
from .runtime_content import write_hashed_file
from .runtime_errors import CmocError
from .runtime_feedback import (
    FEEDBACK_CAPABILITY_ENV,
    FEEDBACK_COLLECTOR_ENV,
    FEEDBACK_PROTOCOL_ENV,
)
from .runtime_paths import schema_store_dir

RUN_PROCESS_TRACKING_ENV = "CMOC_RUN_PROCESS_ID_PATH"
_active_run_process_tracking_path: Path | None = None


def _first_symlink_component(path: Path) -> Path | None:
    """path を順にたどり、最初に見つかった symlink component を返す。"""
    absolute = path.absolute()
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


def _validate_process_tracking_path(path: Path) -> None:
    """tracking file と lock を管理領域内の通常 file として扱えるか検証する。"""
    lock_path = path.with_name(f"{path.name}.lock")
    # {{work-root}}/oracle/doc/app_spec/run_isolation.md
    # process tracking は repo-root 側に置く cmoc 管理データなので、symlink 経由の
    # 外部 read/write と lock の外部化を許可しない。
    for candidate in (path, lock_path):
        if symlink := _first_symlink_component(candidate):
            raise CmocError(
                "run process tracking path は symlink 経由で扱えません。",
                [
                    "tracking file と親 directory を通常の file/directory に戻してから再実行してください。"
                ],
                f"path: {candidate}\nsymlink: {symlink}",
            )
    for candidate in (path, lock_path):
        if candidate.exists() and not candidate.is_file():
            raise CmocError(
                "run process tracking path は通常 file ではありません。",
                [
                    "tracking file と lock file を通常の file に戻してから再実行してください。"
                ],
                str(candidate),
            )


def _is_valid_process_id(process_id: int) -> bool:
    """OS の process API へ安全に渡せる pid_t 範囲か判定する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    return 0 < process_id <= 2**31 - 1


@contextmanager
def run_process_id_file_lock(path: Path) -> Iterator[None]:
    """editing run の process tracking file を直列化する。"""
    _validate_process_tracking_path(path)
    lock_path = path.with_name(f"{path.name}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # abandon が Codex child 起動直後の未記録状態を読まないよう、
        # parent/child pid file 操作は同じ advisory lock に集約する。
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _validate_tracked_process_file(path: Path) -> None:
    """Codex child を起動する前に tracking file の形式を検証する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # abandon は壊れた tracking file を停止対象なしとして扱うため、壊れた既存 state に
    # child 行だけを追記すると、実行中 process を cleanup できないまま worktree を破棄する。
    lines = [
        line.split()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not lines or len(lines[0]) not in {1, 2}:
        raise OSError(f"invalid run process tracking file: {path}")
    try:
        parent_id = int(lines[0][0])
        parent_start_time = int(lines[0][1]) if len(lines[0]) == 2 else None
        if not _is_valid_process_id(parent_id) or (
            parent_start_time is not None and parent_start_time < 0
        ):
            raise ValueError
        for parts in lines[1:]:
            if len(parts) not in {3, 4} or parts[0] != "child":
                raise ValueError
            child_id = int(parts[1])
            child_start_time = int(parts[2])
            group_id = int(parts[3]) if len(parts) == 4 else None
            if (
                not _is_valid_process_id(child_id)
                or child_start_time < 0
                or (
                    group_id is not None
                    and (not _is_valid_process_id(group_id) or group_id != child_id)
                )
            ):
                raise ValueError
    except (IndexError, ValueError) as exc:
        raise OSError(f"invalid run process tracking file: {path}") from exc


def open_process_fd(process_id: int, process_name: str = "run process") -> int | None:
    """pidfd 対応環境でだけ race を避けた process 参照を開く。"""
    if not (hasattr(os, "pidfd_open") and hasattr(signal, "pidfd_send_signal")):
        raise CmocError(
            f"{process_name} の同一性を安全に確認できません。",
            [f"{process_name} を手動で停止してから再実行してください。"],
            f"pid: {process_id}",
        )
    try:
        return os.pidfd_open(process_id)
    except ProcessLookupError:
        return None
    except PermissionError as exc:
        raise CmocError(
            f"実行中 {process_name} の確認権限がありません。",
            [f"{process_name} を手動で確認してから再実行してください。"],
            f"pid: {process_id}",
        ) from exc
    except OSError as exc:
        if exc.errno == errno.EINVAL:
            # {{work-root}}/oracle/doc/app_spec/run_isolation.md
            # pidfd を開けない場合は呼び出し側の start time/group 検証へ渡し、
            # leader が消えた group を数値 PGID だけで停止しない。
            return None
        raise


def send_process_signal(
    process_fd: int,
    process_id: int,
    sig: signal.Signals,
    process_name: str = "run process",
) -> None:
    """pidfd 経由で process へ signal を送り、PID reuse を避ける。"""
    try:
        signal.pidfd_send_signal(process_fd, sig)
    except ProcessLookupError:
        return
    except PermissionError as exc:
        raise CmocError(
            f"実行中 {process_name} を停止する権限がありません。",
            [f"{process_name} を手動で停止してから再実行してください。"],
            f"pid: {process_id}",
        ) from exc


def wait_process_fd_exit(process_fd: int, timeout_sec: float) -> bool:
    """pidfd の readable 化を process 終了として待つ。"""
    readable, _, _ = select.select([process_fd], [], [], timeout_sec)
    return bool(readable)


def _process_stat(process_id: int) -> list[str] | None:
    """Linux proc statを読み、検証可能なfield列だけを返す。"""
    try:
        stat = Path(f"/proc/{process_id}/stat").read_text()
    except OSError:
        return None
    try:
        fields = stat.rsplit(") ", 1)[1].split()
    except IndexError:
        return None
    return fields if len(fields) > 19 else None


def process_start_time(process_id: int) -> int | None:
    """pid 再利用を検出するため Linux proc stat の starttime を読む。"""
    fields = _process_stat(process_id)
    if fields is None:
        return None
    try:
        return int(fields[19])
    except ValueError:
        return None


def process_group_members(
    process_group_id: int,
) -> tuple[tuple[int, int], ...] | None:
    """group 内の非 zombie process を PID と starttime の組で列挙する。"""
    proc = Path("/proc")
    if not proc.is_dir():
        return None
    members: list[tuple[int, int]] = []
    try:
        entries = tuple(proc.iterdir())
    except OSError:
        return None
    for path in entries:
        if not path.name.isdigit():
            continue
        fields = _process_stat(int(path.name))
        if fields is None:
            continue
        try:
            state = fields[0]
            member_group_id = int(fields[2])
            start_time = int(fields[19])
        except ValueError:
            continue
        if member_group_id == process_group_id and state != "Z":
            members.append((int(path.name), start_time))
    return tuple(members)


def process_group_has_running_member(process_group_id: int) -> bool:
    """group 内に停止対象となる process が残っているか確認する。"""
    members = process_group_members(process_group_id)
    return members is None or bool(members)


def _signal_process_members(
    members: tuple[tuple[int, int], ...], sig: signal.Signals
) -> None:
    """snapshot の member を個別 pidfd で再検証して signal を送る。"""
    for process_id, expected_start_time in members:
        process_fd = open_process_fd(process_id, "Codex subprocess")
        if process_fd is None:
            continue
        try:
            # stat 読み取りと pidfd_open の間の PID reuse も signal 前に捨てる。
            if process_start_time(process_id) != expected_start_time:
                continue
            send_process_signal(
                process_fd,
                process_id,
                sig,
                "Codex subprocess",
            )
        finally:
            os.close(process_fd)


def signal_process_group_members(process_group_id: int, sig: signal.Signals) -> None:
    """group member を個別 pidfd で再検証して signal を送る。"""
    members = process_group_members(process_group_id)
    if members is None:
        raise CmocError(
            "実行中 Codex subprocess の process group を確認できません。",
            ["Codex subprocess を手動で停止してから再実行してください。"],
            f"pgid: {process_group_id}",
        )
    _signal_process_members(members, sig)


def _wait_tracked_process_group_exit(
    process_group_id: int,
    known_members: set[tuple[int, int]],
    timeout_sec: float,
) -> bool:
    """初回 snapshot と同じ group が終了するまで待つ。"""
    deadline = time.monotonic() + timeout_sec
    while True:
        members = process_group_members(process_group_id)
        if members is None:
            return False
        if not any(member in known_members for member in members):
            if members:
                raise _unverified_process_group_error(process_group_id)
            return True
        # group が存続している間に増えた descendant も、同じ group の identity として
        # 次の signal 対象へ加える。元の全 member が消えた後の PGID 再利用は追加しない。
        known_members.update(members)
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.05)


def _unverified_process_group_error(process_group_id: int) -> CmocError:
    """既知の member が消えた後に残る未検証 group の error を作る。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    return CmocError(
        "実行中 Codex subprocess の同一性を確認できません。",
        ["Codex subprocess を手動で停止してから再実行してください。"],
        f"pgid: {process_group_id}",
    )


def _current_tracked_process_group_members(
    process_group_id: int, known_members: set[tuple[int, int]]
) -> tuple[tuple[int, int], ...] | None:
    """既知の group identity が残る場合だけ現在の member snapshot を返す。"""
    members = process_group_members(process_group_id)
    if members is None:
        return None
    if not any(member in known_members for member in members):
        if members:
            raise _unverified_process_group_error(process_group_id)
        return ()
    known_members.update(members)
    return members


def stop_process_group(
    process_group_id: int,
    expected_leader: tuple[int, int] | None = None,
    expected_members: tuple[tuple[int, int], ...] | None = None,
) -> None:
    """Codex group を個別 pidfd で SIGTERM、必要なら SIGKILL する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # PGID は member discovery にだけ使い、signal delivery は pidfd に固定する。
    # 初回 snapshot と同じ group identity が消えた後の PGID 再利用へ signal を送らない。
    # leader が検証直後に終了しても、停止前 snapshot と現在の member に重なりが
    # あれば同じ group とみなす。ただし leader が現在の snapshot にいない場合は、
    # 保存済み snapshot にも leader が含まれることを確認し、別 group の member overlap
    # だけで停止を許可しない。
    initial_members = process_group_members(process_group_id)
    if initial_members is None:
        raise CmocError(
            "実行中 Codex subprocess の process group を確認できません。",
            ["Codex subprocess を手動で停止してから再実行してください。"],
            f"pgid: {process_group_id}",
        )
    if expected_leader is not None and (
        # 空 snapshot は leader の終了と観測欠落を区別できないため、停止済み扱いにしない。
        expected_members is None
        or expected_leader not in expected_members
        or not initial_members
    ):
        raise CmocError(
            "実行中 Codex subprocess の同一性を確認できません。",
            ["Codex subprocess を手動で停止してから再実行してください。"],
            f"pid: {expected_leader[0]}\npgid: {process_group_id}",
        )
    if (
        expected_members is not None
        and initial_members
        and not any(member in expected_members for member in initial_members)
    ):
        raise CmocError(
            "実行中 Codex subprocess の同一性を確認できません。",
            ["Codex subprocess を手動で停止してから再実行してください。"],
            f"pgid: {process_group_id}",
        )
    if (
        expected_leader is not None
        and initial_members
        and expected_leader not in initial_members
        and (
            expected_members is None
            or expected_leader not in expected_members
            or not any(member in expected_members for member in initial_members)
        )
    ):
        raise CmocError(
            "実行中 Codex subprocess の同一性を確認できません。",
            ["Codex subprocess を手動で停止してから再実行してください。"],
            f"pid: {expected_leader[0]}\npgid: {process_group_id}",
        )
    known_members = set(initial_members)
    _signal_process_members(initial_members, signal.SIGTERM)
    if _wait_tracked_process_group_exit(process_group_id, known_members, 5.0):
        return
    current_members = _current_tracked_process_group_members(
        process_group_id, known_members
    )
    if current_members is None:
        raise CmocError(
            "実行中 Codex subprocess の process group を確認できません。",
            ["Codex subprocess を手動で停止してから再実行してください。"],
            f"pgid: {process_group_id}",
        )
    if not current_members:
        return
    _signal_process_members(current_members, signal.SIGKILL)
    if _wait_tracked_process_group_exit(process_group_id, known_members, 5.0):
        return
    raise CmocError(
        "実行中 Codex subprocess を停止できません。",
        ["Codex subprocess を確認して停止後に再実行してください。"],
        f"pgid: {process_group_id}",
    )


def file_access_to_sandbox_mode(mode: FileAccessMode) -> str:
    """cmoc の file access policy を Codex CLI が理解する sandbox 名へ落とす。"""
    match mode:
        case FileAccessMode.READONLY | FileAccessMode.PURE_ORACLE_READ:
            return "read-only"
        case (
            FileAccessMode.REALIZATION_WRITE
            | FileAccessMode.PURE_ORACLE_WRITE
            | FileAccessMode.REPO_WRITE
            | FileAccessMode.NO_RULE
        ):
            return "workspace-write"
        case _:
            raise CmocError("不明な FileAccessMode です。", [], str(mode))


def _toml_string(value: str) -> str:
    """TOML string として安全な JSON 互換 quote へ寄せる。"""
    validate_json_toml_value(value)
    # JSON が raw のまま残す DEL は TOML basic string では escape が必要になる。
    return json.dumps(value, ensure_ascii=False).replace("\x7f", "\\u007F")


def _is_bare_toml_key_segment(value: str) -> bool:
    """Codex CLI の dotted override path で bare に渡せる key か判定する。"""
    return re.fullmatch(r"[A-Za-z0-9_-]+", value) is not None


def _toml_key_segment(value: str) -> str:
    """provider ID/key を意味を保つ単一の TOML key segment にする。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # Codex CLI の dotted override path は bare key を引用せず渡す必要がある。
    if _is_bare_toml_key_segment(value):
        return value
    return _toml_string(value)


def _toml_value(value: JsonTomlValue) -> str:
    """null 以外の JSON value を一意な TOML value へ変換する。"""
    value = validate_json_toml_value(value)
    if isinstance(value, str):
        return _toml_string(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, list):
        return "[" + ", ".join(_toml_value(item) for item in value) + "]"
    return (
        "{"
        + ", ".join(
            f"{_toml_key_segment(key)} = {_toml_value(item)}"
            for key, item in value.items()
        )
        + "}"
    )


def _config_override(key: str, toml_value: str) -> list[str]:
    """Codex CLI の単一 config override を argv fragment にする。"""
    return ["--config", f"{key}={toml_value}"]


def _model_provider_override_args(
    provider_id: str,
    config: CmocConfig,
) -> list[str]:
    """選択した provider と provider-local 設定だけを argv にする。"""
    try:
        provider = config.codex.model_providers[provider_id]
    except KeyError as exc:
        raise CmocError(
            "Codex model provider が未定義です。",
            [
                "{{work-root}}/.cmoc/gt/ar/config.json の codex.model_providers を確認してください。"
            ],
            f"model provider ID: {provider_id!r}",
        ) from exc
    try:
        provider_key = f"model_providers.{_toml_key_segment(provider_id)}"
        provider_value = _toml_string(provider_id)
    except TypeError as exc:
        raise CmocError(
            "Codex model provider ID が不正です。",
            [
                "model provider ID を Codex CLI が解釈できる TOML key/value に修正してください。"
            ],
            f"model provider ID: {provider_id!r}",
        ) from exc
    args = _config_override("model_provider", provider_value)
    normalized_settings: dict[str, JsonTomlValue] = {}
    has_non_bare_segment = not _is_bare_toml_key_segment(provider_id)
    encoded_settings: list[tuple[str, str]] = []
    for key, value in provider.settings.items():
        if not isinstance(key, str):
            raise CmocError(
                "Codex model provider 設定が不正です。",
                [
                    "{{work-root}}/.cmoc/gt/ar/config.json の provider-local key を確認してください。"
                ],
                f"model provider ID: {provider_id!r}\nkey: {key!r}",
            )
        try:
            key_segment = _toml_key_segment(key)
            normalized_value = validate_json_toml_value(value)
            toml_value = _toml_value(normalized_value)
        except TypeError as exc:
            raise CmocError(
                "Codex model provider 設定が不正です。",
                [
                    "provider-local setting を null 以外の JSON/TOML 共通値へ修正してください。"
                ],
                f"model provider ID: {provider_id!r}\nkey: {key!r}",
            ) from exc
        normalized_settings[key] = normalized_value
        encoded_settings.append((key_segment, toml_value))
        has_non_bare_segment |= not _is_bare_toml_key_segment(key)
    if has_non_bare_segment and encoded_settings:
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        # Codex CLI の dotted override parser は quoted key segment を path として解釈せず、
        # provider ID/key に dot を含む設定を壊す。inline TOML table なら同じ
        # provider-local key を一つの config override として意味を保てる。
        args.extend(
            _config_override(
                "model_providers",
                _toml_value({provider_id: normalized_settings}),
            )
        )
        return args
    for key_segment, toml_value in encoded_settings:
        args.extend(_config_override(f"{provider_key}.{key_segment}", toml_value))
    return args


def _feedback_mcp_override_args() -> list[str]:
    """cmoc_feedback server の effective configuration 全体を支配する。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # capability value は argv に載せず、Codex process の local environment から
    # reporter process だけが whitelist 名で継承する。
    server: dict[str, JsonTomlValue] = {
        "command": sys.executable,
        "args": ["-m", "commons.runtime_feedback_reporter"],
        "env_vars": [
            FEEDBACK_CAPABILITY_ENV,
            FEEDBACK_COLLECTOR_ENV,
            FEEDBACK_PROTOCOL_ENV,
        ],
        "enabled": True,
        "required": False,
        "enabled_tools": ["submit_observation"],
        "disabled_tools": [],
        "startup_timeout_sec": 5,
        "tool_timeout_sec": 15,
        "default_tools_approval_mode": "approve",
        "tools": {"submit_observation": {"approval_mode": "approve"}},
    }
    args = _config_override("mcp_servers.cmoc_feedback", _toml_value(server))
    # MCP process への env_vars 転送には Codex process の環境が必要だが、同じ値を
    # agent が起動する shell command へ継承させてはならない。
    for name in (
        FEEDBACK_CAPABILITY_ENV,
        FEEDBACK_COLLECTOR_ENV,
        FEEDBACK_PROTOCOL_ENV,
    ):
        args.extend(
            _config_override(
                f"shell_environment_policy.filters.{name}",
                _toml_string("exclude"),
            )
        )
    return args


def build_codex_override_args(
    parameter: AgentCallParameter,
    config: CmocConfig,
) -> list[str]:
    """論理設定を専用 sandbox 引数と必要最小限の config argv にする。"""
    sandbox_mode = file_access_to_sandbox_mode(parameter.file_access_mode)
    model_spec = config.codex.model[parameter.model_class]
    reasoning_effort = config.codex.reasoning_effort[parameter.reasoning_effort]
    args = [
        "--ask-for-approval",
        "on-request",
        "--model",
        model_spec.model,
        "--sandbox",
        sandbox_mode,
        *_config_override("approvals_reviewer", _toml_string("auto_review")),
        *_config_override("model_reasoning_effort", _toml_string(reasoning_effort)),
        *_feedback_mcp_override_args(),
    ]
    if model_spec.model_provider is not None:
        args.extend(_model_provider_override_args(model_spec.model_provider, config))
    return args


def resolve_codex_home(agent_call_cwd: Path) -> Path:
    """CODEX_HOME の相対指定を Codex subprocess の cwd 基準で解決する。"""
    value = os.environ.get("CODEX_HOME")
    if value is not None:
        raw_path = Path(value)
        return raw_path if raw_path.is_absolute() else agent_call_cwd / raw_path
    return (Path.home() / ".codex").resolve()


def validate_codex_home(codex_home: Path) -> None:
    """Codex 起動前に CODEX_HOME が directory であることだけを検査する。"""
    if not codex_home.exists():
        raise CmocError(
            "Codex home が存在しません。",
            [
                "Codex CLI の通常利用環境を初期化してください。",
                "既存の Codex home を指すように CODEX_HOME を設定してください。",
            ],
            f"CODEX_HOME: {codex_home}\nfailed condition: CODEX_HOME exists",
        )
    if not codex_home.is_dir():
        raise CmocError(
            "Codex home がディレクトリではありません。",
            [
                "CODEX_HOME が既存ディレクトリを指すように修正してください。",
                "CODEX_HOME のファイル種別を確認してください。",
            ],
            f"CODEX_HOME: {codex_home}\nfailed condition: CODEX_HOME is directory",
        )


def prepare_codex_override_args(
    parameter: AgentCallParameter,
    config: CmocConfig | None = None,
) -> list[str]:
    """CmocConfig だけから path 非依存の Codex argv を返す。"""
    resolved_config = config or CmocConfig()
    return build_codex_override_args(parameter, resolved_config)


def codex_subprocess_env(codex_home: Path) -> dict[str, str]:
    """Codex subprocess に渡す CODEX_HOME を、利用者指定があればそのまま保つ。"""
    value = os.environ.get("CODEX_HOME")
    if value is None:
        value = str(codex_home)
    return {**os.environ, "CODEX_HOME": value}


def run_codex_subprocess(
    argv: list[str], **kwargs: Any
) -> subprocess.CompletedProcess[Any]:
    """Codex CLI 不在を Python の生例外ではなく cmoc の実行時エラーにそろえる。"""
    try:
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # tracking は editing run の内部 state なので、継承した env var だけで無関係な Codex
        # call を stale または別 process の pid file へ向けてはならない。
        if _active_run_process_tracking_path is not None and argv[:1] == ["codex"]:
            return run_tracked_codex_subprocess(
                argv, _active_run_process_tracking_path, **kwargs
            )
        return subprocess.run(argv, **kwargs)
    except FileNotFoundError as exc:
        if not _is_missing_codex_executable(exc, argv, kwargs):
            raise
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        # Codex CLI missing は想定外の exec 失敗として即時に利用者向け失敗にする。
        raise CmocError(
            "Codex CLI が見つかりません。",
            ["Codex CLI をインストールし、PATH に codex を含めてください。"],
            f"argv: {argv}\nerror: {exc}",
        ) from exc


def _is_missing_codex_executable(
    exc: FileNotFoundError, argv: list[str], kwargs: dict[str, Any]
) -> bool:
    """FileNotFoundError が Codex executable の不在を示すか判定する。"""
    if argv[:1] != ["codex"]:
        return False
    if exc.filename is None:
        # テスト double などが filename を設定しない FileNotFoundError を許容する。
        return True
    # {{work-root}}/oracle/doc/dev_rule/coding_rule.md
    # subprocess の cwd key は API 名として維持し、内部値には process の役割を付ける。
    codex_process_cwd = kwargs.get("cwd")
    if codex_process_cwd is not None and not isinstance(codex_process_cwd, int):
        try:
            if not Path(codex_process_cwd).is_dir():
                return False
        except (OSError, TypeError):
            return False
    return os.fsdecode(exc.filename) == argv[0]


def set_run_process_tracking_path(path: Path | None) -> Path | None:
    """editing run 実行中だけ有効な process-local tracking path を差し替える。"""
    global _active_run_process_tracking_path
    old_path = _active_run_process_tracking_path
    _active_run_process_tracking_path = path
    return old_path


def run_process_tracking_active() -> bool:
    """editing run の Codex subprocess tracking が有効か返す。"""
    return _active_run_process_tracking_path is not None


def run_tracked_codex_subprocess(
    argv: list[str], tracking_path: Path, **kwargs: Any
) -> subprocess.CompletedProcess[Any]:
    """run abandon が止められるよう Codex subprocess group を記録する。"""
    input_data = kwargs.pop("input", None)
    capture_output = kwargs.pop("capture_output", False)
    check = kwargs.pop("check", False)
    if input_data is not None:
        if kwargs.get("stdin") is not None:
            raise ValueError("stdin and input arguments may not both be used.")
        kwargs["stdin"] = subprocess.PIPE
    if capture_output:
        kwargs.setdefault("stdout", subprocess.PIPE)
        kwargs.setdefault("stderr", subprocess.PIPE)
    process: subprocess.Popen[Any] | None = None
    cleanup_expected_leader: tuple[int, int] | None = None
    cleanup_expected_members: tuple[tuple[int, int], ...] | None = None
    tracked_start_time: int | None = None
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # Popen と child 行の登録だけを遅延させ、exec 後の child は通常の SIGTERM を受ける。
    previous_sigterm_handler = signal.getsignal(signal.SIGTERM)
    sigterm_pending = False

    def _defer_sigterm(_signum: int, _frame: FrameType | None) -> None:
        """tracking情報の登録が終わるまでSIGTERMを保留する。"""
        nonlocal sigterm_pending
        sigterm_pending = True

    def _restore_sigterm_handler() -> None:
        """保留した SIGTERM を setup 成否にかかわらず復元する。"""
        signal.signal(signal.SIGTERM, previous_sigterm_handler)
        if sigterm_pending and previous_sigterm_handler != signal.SIG_IGN:
            # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
            # Popen/child 行登録の途中だけ signal を遅延し、setup 失敗時も元の
            # handler へ再配送して run の中断を握りつぶさない。
            os.kill(os.getpid(), signal.SIGTERM)

    signal.signal(signal.SIGTERM, _defer_sigterm)
    try:
        try:
            with run_process_id_file_lock(tracking_path):
                _validate_tracked_process_file(tracking_path)
                process = subprocess.Popen(argv, start_new_session=True, **kwargs)
                # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
                # tracking 更新に失敗しても、後から PGID を再探索して別 group を停止しない
                # よう、Popen 直後の identity snapshot を cleanup に引き継ぐ。
                cleanup_start_time = process_start_time(process.pid)
                if cleanup_start_time is not None:
                    cleanup_expected_leader = (process.pid, cleanup_start_time)
                cleanup_expected_members = process_group_members(process.pid)
                tracked_start_time = _record_tracked_child_process(
                    tracking_path, process.pid, process_group_id=process.pid
                )
        except BaseException as exc:
            if process is None:
                raise
            try:
                if cleanup_expected_members is None or cleanup_expected_leader is None:
                    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
                    # leader の identity を取得できない snapshot を停止済みと
                    # 扱うと、live child の process.wait() だけを無期限に待つ。
                    # group 停止を証明できない場合は outer fallback の Popen child
                    # kill/reap へ渡し、未確認の group cleanup を成功扱いしない。
                    raise CmocError(
                        "実行中 Codex subprocess の process group を確認できません。",
                        ["Codex subprocess を手動で停止してから再実行してください。"],
                        f"pid: {process.pid}",
                    )
                stop_process_group(
                    process.pid,
                    expected_leader=cleanup_expected_leader,
                    expected_members=cleanup_expected_members,
                )
                process.wait()
            except BaseException as cleanup_exc:
                try:
                    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
                    # process group cleanup が完了しない場合は PGID を推測して signal せず、
                    # Popen が直接保持する child だけを停止してから reap する。
                    if process.poll() is None:
                        process.kill()
                    process.wait()
                except BaseException as reap_exc:
                    raise CmocError(
                        "run process tracking を更新できません。",
                        [
                            "run process tracking file の権限と保存先を確認してください。",
                            "Codex subprocess の停止にも失敗しました。",
                        ],
                        f"path: {tracking_path}\nerror: {exc}\n"
                        f"cleanup: {cleanup_exc}\nreap: {reap_exc}",
                    ) from reap_exc
                raise CmocError(
                    "run process tracking を更新できません。",
                    [
                        "run process tracking file の権限と保存先を確認してください。",
                        "Codex subprocess の停止にも失敗しました。",
                    ],
                    f"path: {tracking_path}\nerror: {exc}\ncleanup: {cleanup_exc}",
                ) from cleanup_exc
            if isinstance(exc, OSError):
                raise CmocError(
                    "run process tracking を更新できません。",
                    ["run process tracking file の権限と保存先を確認してください。"],
                    f"path: {tracking_path}\nerror: {exc}",
                ) from exc
            raise
    finally:
        _restore_sigterm_handler()
    try:
        stdout, stderr = process.communicate(input_data)
        result = subprocess.CompletedProcess(argv, process.returncode, stdout, stderr)
        if check and result.returncode:
            raise subprocess.CalledProcessError(
                result.returncode,
                argv,
                output=stdout,
                stderr=stderr,
            )
        return result
    finally:
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # leader 終了後も descendant が group に残る間は tracking を保持する。
        if (
            process.poll() is not None
            and not process_group_has_running_member(process.pid)
            and tracked_start_time is not None
        ):
            try:
                _remove_tracked_child_process(
                    tracking_path,
                    process.pid,
                    tracked_start_time,
                    process.pid,
                )
            except OSError as exc:
                raise CmocError(
                    "run process tracking を更新できません。",
                    ["run process tracking file の権限と保存先を確認してください。"],
                    f"path: {tracking_path}\nerror: {exc}",
                ) from exc


def _record_tracked_child_process(
    path: Path, process_id: int, process_group_id: int | None = None
) -> int:
    """Codex child の identity を tracking file へ保存し、start time を返す。"""
    _validate_tracked_process_file(path)
    start_time = process_start_time(process_id)
    if start_time is None:
        raise OSError(f"process {process_id} start time is unavailable")
    current = path.read_text(encoding="utf-8")
    lines = [line for line in current.splitlines() if line.strip()]
    group_id = process_id if process_group_id is None else process_group_id
    child_line = f"child {process_id} {start_time} {group_id}"
    lines = [line for line in lines if not line.startswith(f"child {process_id} ")]
    lines.append(child_line)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return start_time


def _remove_tracked_child_process(
    path: Path,
    process_id: int,
    expected_start_time: int,
    expected_group_id: int | None = None,
) -> None:
    """同じ identity の終了済み Codex child を tracking file から除く。"""
    with run_process_id_file_lock(path):
        if not path.exists():
            return

        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # PID は再利用されるため、古い child の cleanup で新しい tracking 行を消さない。
        def is_same_child(line: str) -> bool:
            """PID 再利用後に登録された新しい child 行を保持する。"""
            parts = line.split()
            if len(parts) not in {3, 4} or parts[0] != "child":
                return False
            try:
                if int(parts[1]) != process_id or int(parts[2]) != expected_start_time:
                    return False
                return (
                    expected_group_id is None
                    or len(parts) == 3
                    or int(parts[3]) == expected_group_id
                )
            except ValueError:
                return False

        lines = [
            line
            for line in path.read_text(encoding="utf-8").splitlines()
            if not is_same_child(line)
        ]
        path.write_text(("\n".join(lines) + "\n") if lines else "", encoding="utf-8")


def prepare_schema(root: Path, schema_source_path: Path | None) -> Path | None:
    """Structured Output schema を指定 root の内容 hash store へ配置する。"""
    if schema_source_path is None:
        return None
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # hash path と保存本文を schema source の UTF-8 bytes に一致させるため、
    # Path.read_text() の改行変換を通さない。
    schema_text = schema_source_path.read_bytes().decode("utf-8")
    return write_hashed_file(schema_store_dir(root), "", ".json", schema_text)


def read_output_json(path: Path) -> Any:
    """schema なしの Codex output が空または不正 JSON の場合は None を返す。"""
    try:
        output_text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeError):
        return None
    if not output_text.strip():
        return None
    try:
        return json.loads(output_text)
    except (json.JSONDecodeError, UnicodeError):
        return None


def codex_error_text(stdout_text: str, stderr_text: str) -> str:
    """Codex の stderr と JSONL event 内 message を利用者向け detail に束ねる。"""
    fragments: list[str] = [stderr_text]
    for line in stdout_text.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # blank でも元の line を表示できるようにする。malformed stdout は無視できる
            # diagnostic ではなく protocol failure である。
            fragments.append(f"malformed JSONL event (invalid JSON): {line}")
            continue
        if not isinstance(item, dict):
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # 既知の JSONL event は object なので、malformed output を error detail に残して
            # caller が non-retryable failure path を選ぶようにする。
            fragments.append(f"malformed JSONL event (expected object): {line}")
            continue
        message = item.get("message")
        if isinstance(message, str):
            fragments.append(message)
        error = item.get("error")
        if isinstance(error, dict) and isinstance(error.get("message"), str):
            fragments.append(error["message"])
    return "\n".join(fragments)


def extract_resume_token(stdout_text: str) -> str | None:
    """`codex exec resume` に渡す session ID を Codex JSONL stdout から拾う。"""
    for line in stdout_text.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(item, dict):
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # non-object event は session ID を持てない。
            continue
        if item.get("type") != "thread.started":
            continue
        value = item.get("thread_id")
        if isinstance(value, str) and value:
            return value
    return None


def _codex_jsonl_error_messages(stdout_text: str) -> list[str | None]:
    """Codex JSONL の error event message を retry 判定用に抽出する。"""
    messages: list[str | None] = []
    for line in stdout_text.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # process が zero を返し output-last-message file が有効でも、JSONL protocol
            # violation は unexpected error である。
            messages.append(None)
            continue
        if not isinstance(item, dict):
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # malformed event は unexpected error であり、retry signal にはならない。
            messages.append(None)
            continue
        if item.get("type") == "error":
            message = item.get("message")
            messages.append(message if isinstance(message, str) else None)
        elif item.get("type") == "turn.failed":
            error = item.get("error")
            message = error.get("message") if isinstance(error, dict) else None
            messages.append(message if isinstance(message, str) else None)
    return messages


_CAPACITY_ERROR_MARKER = "Selected model is at capacity"
_QUOTA_ERROR_MARKERS = (
    "Quota exceeded",
    "You've hit your usage limit",
    "out of credits",
    "You hit your spend cap",
)


def is_capacity_error(stdout_text: str) -> bool:
    """Codex JSONL 上の model capacity error だけを retry 対象として判定する。"""
    return any(
        isinstance(message, str) and _CAPACITY_ERROR_MARKER in message
        for message in _codex_jsonl_error_messages(stdout_text)
    )


def is_quota_error(stdout_text: str) -> bool:
    """usage limit 系の Codex JSONL error を quota 待機対象として判定する。"""
    return any(
        isinstance(message, str) and marker in message
        for message in _codex_jsonl_error_messages(stdout_text)
        for marker in _QUOTA_ERROR_MARKERS
    )


def is_unexpected_error(stdout_text: str) -> bool:
    """既知の capacity/quota 以外の Codex JSONL error を検出する。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # recovery path があるのは capacity と quota event だけである。malformed またはその他の
    # error event を subprocess の zero return code で隠してはならない。
    return any(
        not isinstance(message, str)
        or (
            _CAPACITY_ERROR_MARKER not in message
            and not any(marker in message for marker in _QUOTA_ERROR_MARKERS)
        )
        for message in _codex_jsonl_error_messages(stdout_text)
    )
