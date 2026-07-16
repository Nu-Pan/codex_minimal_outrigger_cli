"""Codex CLI 起動前後の argv/env/schema/error 判定をまとめる境界。

責務境界は Codex CLI に渡す実行環境と Codex CLI から返る機械的な実行結果の
解釈に閉じている。sandbox/argv/cwd、
CODEX_HOME、child process tracking、schema 配置、JSONL error 判定は同じ
subprocess 境界の不変条件を共有するため、分割すると呼び出し側が同時に読むべき
失敗時文脈が増える。現状は Codex subprocess 境界として一箇所に保つ方が凝集性が高い。
根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import fcntl
import json
import os
import select
import signal
import subprocess
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from basic.acp import AgentCallParameter, FileAccessMode
from commons.runtime_content import write_hashed_file
from commons.runtime_errors import CmocError
from commons.runtime_paths import schema_store_dir
from config.cmoc_config import CmocConfig

APPLY_PROCESS_TRACKING_ENV = "CMOC_APPLY_PROCESS_ID_PATH"
_active_apply_process_tracking_path: Path | None = None
_OLLAMA_PROVIDER_ID = "cmoc_managed_ollama"


@contextmanager
def apply_process_id_file_lock(path: Path) -> Iterator[None]:
    """apply process pid file の読み書きを直列化する。"""
    lock_path = path.with_name(f"{path.name}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        # {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
        # abandon が Codex child 起動直後の未記録状態を読まないよう、
        # parent/child pid file 操作は同じ advisory lock に集約する。
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def open_process_fd(process_id: int, process_name: str = "apply process") -> int | None:
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


def send_process_signal(
    process_fd: int,
    process_id: int,
    sig: signal.Signals,
    process_name: str = "apply process",
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


def wait_process_group_exit(process_group_id: int, timeout_sec: float) -> bool:
    """数値 PGID へ signal を送らず、group が空になるまで待つ。"""
    deadline = time.monotonic() + timeout_sec
    while process_group_has_running_member(process_group_id):
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.05)
    return True


def signal_process_group_members(process_group_id: int, sig: signal.Signals) -> None:
    """group member を個別 pidfd で再検証して signal を送る。"""
    members = process_group_members(process_group_id)
    if members is None:
        raise CmocError(
            "実行中 Codex subprocess の process group を確認できません。",
            ["Codex subprocess を手動で停止してから再実行してください。"],
            f"pgid: {process_group_id}",
        )
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


def stop_process_group(process_group_id: int) -> None:
    """Codex group を個別 pidfd で SIGTERM、必要なら SIGKILL する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
    # PGID は member discovery にだけ使い、signal delivery は pidfd に固定する。
    signal_process_group_members(process_group_id, signal.SIGTERM)
    if wait_process_group_exit(process_group_id, 5.0):
        return
    signal_process_group_members(process_group_id, signal.SIGKILL)
    if wait_process_group_exit(process_group_id, 5.0):
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


def parameter_codex_cwd(parameter: AgentCallParameter, codex_work_root: Path) -> Path:
    """AgentCallParameter.cwd を優先し、対象 work root 外の古い呼び出しを補正する。"""
    parameter_cwd = parameter.cwd.resolve()
    work = codex_work_root.resolve()
    if parameter_cwd.is_relative_to(work):
        return parameter_cwd
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # Older call paths may still pass the repo root while launching against a
    # linked worktree; Codex must run inside the target work root.
    return work


def _toml_string(value: str) -> str:
    """TOML string として安全な JSON 互換 quote へ寄せる。"""
    return json.dumps(value, ensure_ascii=False)


def _config_override(key: str, toml_value: str) -> list[str]:
    """Codex CLI の単一 config override を argv fragment にする。"""
    return ["--config", f"{key}={toml_value}"]


def _ollama_provider_override_args() -> list[str]:
    """cmoc managed ollama provider を argv config override にする。"""
    provider_key = f"model_providers.{_OLLAMA_PROVIDER_ID}"
    return [
        # {{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md
        # Codex enables non-function web-search and multi-agent tool types by
        # default, while Ollama's Responses endpoint accepts function tools.
        # Keep the managed local provider on their common tool subset.
        "--disable",
        "multi_agent",
        *_config_override("web_search", _toml_string("disabled")),
        *_config_override("model_provider", _toml_string(_OLLAMA_PROVIDER_ID)),
        *_config_override(f"{provider_key}.name", _toml_string("cmoc managed ollama")),
        *_config_override(
            f"{provider_key}.base_url",
            _toml_string("http://127.0.0.1:11434/v1"),
        ),
        *_config_override(f"{provider_key}.wire_api", _toml_string("responses")),
    ]


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
    ]
    use_cmoc_managed_ollama = model_spec.model_provider == "cmoc"
    if use_cmoc_managed_ollama:
        args.extend(_ollama_provider_override_args())
    return args


def resolve_codex_home(cwd: Path | None = None) -> Path:
    """CODEX_HOME の相対指定を Codex subprocess の cwd 基準で解決する。"""
    value = os.environ.get("CODEX_HOME")
    if value is not None:
        raw_path = Path(value)
        return raw_path if raw_path.is_absolute() else (cwd or Path.cwd()) / raw_path
    return (Path.home() / ".codex").resolve()


def validate_codex_home(codex_home: Path) -> None:
    """Codex 起動前に通常利用に必要な home と auth.json の存在を検査する。"""
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
    auth_path = codex_home / "auth.json"
    if not auth_path.is_file():
        raise CmocError(
            "Codex CLI 認証情報が存在しません。",
            [
                "Codex CLI の通常利用環境を初期化してください。",
                "既存の Codex home を指すように CODEX_HOME を設定してください。",
            ],
            f"CODEX_HOME: {codex_home}\nfailed condition: {auth_path} is file",
        )


def prepare_codex_override_args(
    parameter: AgentCallParameter,
    config: CmocConfig | None = None,
    root: Path | None = None,
) -> list[str]:
    """必要なら local provider を準備し、path 非依存の Codex argv を返す。

    root は managed local provider の事前準備だけに使い、sandbox や詳細な
    ファイルアクセス設定の組み立てには使わない。
    """
    resolved_config = config or CmocConfig()
    if (
        resolved_config.codex.model[parameter.model_class].model_provider == "cmoc"
        and root is not None
    ):
        from commons.runtime_doctor import run_doctor_preprocess

        run_doctor_preprocess(root, resolved_config)
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
        # {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
        # Tracking is apply-run internal state; an inherited env var alone must
        # not redirect unrelated Codex calls to a stale or foreign pid file.
        if _active_apply_process_tracking_path is not None and argv[:1] == ["codex"]:
            return run_tracked_codex_subprocess(
                argv, _active_apply_process_tracking_path, **kwargs
            )
        return subprocess.run(argv, **kwargs)
    except FileNotFoundError as exc:
        if argv[:1] != ["codex"]:
            raise
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        # Codex CLI missing は想定外の exec 失敗として即時に利用者向け失敗にする。
        raise CmocError(
            "Codex CLI が見つかりません。",
            ["Codex CLI をインストールし、PATH に codex を含めてください。"],
            f"argv: {argv}\nerror: {exc}",
        ) from exc


def set_apply_process_tracking_path(path: Path | None) -> Path | None:
    """apply 実行中だけ有効な process-local tracking path を差し替える。"""
    global _active_apply_process_tracking_path
    old_path = _active_apply_process_tracking_path
    _active_apply_process_tracking_path = path
    return old_path


def run_tracked_codex_subprocess(
    argv: list[str], tracking_path: Path, **kwargs: Any
) -> subprocess.CompletedProcess[Any]:
    """apply abandon が止められるよう Codex subprocess group を pid file に記録する。"""
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
    # {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
    # Popen と child 行の登録だけを遅延させ、exec 後の child は通常の SIGTERM を受ける。
    previous_sigterm_handler = signal.getsignal(signal.SIGTERM)
    sigterm_pending = False

    def defer_sigterm(_signum: int, _frame: Any) -> None:
        nonlocal sigterm_pending
        sigterm_pending = True

    signal.signal(signal.SIGTERM, defer_sigterm)
    try:
        try:
            with apply_process_id_file_lock(tracking_path):
                process = subprocess.Popen(argv, start_new_session=True, **kwargs)
                _record_tracked_child_process(
                    tracking_path, process.pid, process_group_id=process.pid
                )
        except OSError as exc:
            if process is None:
                raise
            try:
                stop_process_group(process.pid)
            except CmocError as cleanup_exc:
                raise CmocError(
                    "apply process tracking を更新できません。",
                    [
                        "apply process pid file の権限と保存先を確認してください。",
                        "Codex subprocess の停止にも失敗しました。",
                    ],
                    f"path: {tracking_path}\nerror: {exc}\ncleanup: {cleanup_exc}",
                ) from exc
            raise CmocError(
                "apply process tracking を更新できません。",
                ["apply process pid file の権限と保存先を確認してください。"],
                f"path: {tracking_path}\nerror: {exc}",
            ) from exc
    finally:
        signal.signal(signal.SIGTERM, previous_sigterm_handler)
    if sigterm_pending and previous_sigterm_handler != signal.SIG_IGN:
        # Popen と pid file 更新の間だけ遅らせ、登録後は通常の中断処理へ戻す。
        os.kill(os.getpid(), signal.SIGTERM)
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
        # {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
        # leader 終了後も descendant が group に残る間は tracking を保持する。
        if process.poll() is not None and not process_group_has_running_member(
            process.pid
        ):
            try:
                remove_tracked_child_process(tracking_path, process.pid)
            except OSError as exc:
                raise CmocError(
                    "apply process tracking を更新できません。",
                    ["apply process pid file の権限と保存先を確認してください。"],
                    f"path: {tracking_path}\nerror: {exc}",
                ) from exc


def record_tracked_child_process(
    path: Path, process_id: int, process_group_id: int | None = None
) -> None:
    """apply process pid file へ Codex child process の同一性情報を追記する。"""
    with apply_process_id_file_lock(path):
        _record_tracked_child_process(path, process_id, process_group_id)


def _record_tracked_child_process(
    path: Path, process_id: int, process_group_id: int | None = None
) -> None:
    start_time = process_start_time(process_id)
    if start_time is None:
        raise OSError(f"process {process_id} start time is unavailable")
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.read_text() if path.exists() else ""
    lines = [line for line in current.splitlines() if line.strip()]
    group_id = process_id if process_group_id is None else process_group_id
    child_line = f"child {process_id} {start_time} {group_id}"
    lines = [line for line in lines if not line.startswith(f"child {process_id} ")]
    lines.append(child_line)
    path.write_text("\n".join(lines) + "\n")


def remove_tracked_child_process(path: Path, process_id: int) -> None:
    """終了した Codex child process を apply process pid file から除く。"""
    with apply_process_id_file_lock(path):
        if not path.exists():
            return
        lines = [
            line
            for line in path.read_text().splitlines()
            if not line.startswith(f"child {process_id} ")
        ]
        path.write_text(("\n".join(lines) + "\n") if lines else "")


def prepare_schema(root: Path, schema_source_path: Path | None) -> Path | None:
    """Structured Output schema を指定 root の内容 hash store へ配置する。"""
    if schema_source_path is None:
        return None
    schema_text = schema_source_path.read_text()
    return write_hashed_file(schema_store_dir(root), "", ".json", schema_text)


def read_output_json(path: Path) -> Any:
    """schema なしの Codex output が空または不正 JSON の場合は None を返す。"""
    if not path.exists() or not path.read_text().strip():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return None


def codex_error_text(stdout_text: str, stderr_text: str) -> str:
    """Codex の stderr と JSONL event 内 message を利用者向け detail に束ねる。"""
    fragments: list[str] = [stderr_text]
    for line in stdout_text.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # Keep the original line visible even when it is blank; malformed
            # stdout is a protocol failure, not an ignorable diagnostic.
            fragments.append(f"malformed JSONL event (invalid JSON): {line}")
            continue
        if not isinstance(item, dict):
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # Known JSONL events are objects; preserve malformed output in
            # error detail so the caller takes the non-retryable failure path.
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
    """quota retry で resume できる thread id を Codex JSONL stdout から拾う。"""
    for line in stdout_text.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(item, dict):
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # A non-object event cannot carry a resume token.
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
            # A JSONL protocol violation is unexpected even when the process
            # returned zero and the output-last-message file is valid.
            messages.append(None)
            continue
        if not isinstance(item, dict):
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # A malformed event is an unexpected error, never a retry signal.
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
    # Only capacity and quota events have recovery paths; malformed or other
    # error events must not be hidden by a zero subprocess return code.
    return any(
        not isinstance(message, str)
        or (
            _CAPACITY_ERROR_MARKER not in message
            and not any(marker in message for marker in _QUOTA_ERROR_MARKERS)
        )
        for message in _codex_jsonl_error_messages(stdout_text)
    )
