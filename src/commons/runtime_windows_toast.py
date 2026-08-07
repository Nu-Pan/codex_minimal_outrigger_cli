"""Windows toast と Codex TUI callback の非致命的な transport 境界。

根拠: {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
"""

import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Literal

ToastState = Literal["completed", "failed", "interrupted", "waiting"]

_POWERSHELL_TIMEOUT_SEC = 5.0
_WINDOWS_POWERSHELL = Path(
    "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
)
_STATE_TEXT: dict[ToastState, str] = {
    "completed": "完了",
    "failed": "エラー終了",
    "interrupted": "ユーザー中断完了",
    "waiting": "入力待ち",
}
_POWERSHELL_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$data = [Console]::In.ReadToEnd() | ConvertFrom-Json

[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null

$application = Get-StartApps |
    Where-Object { $_.AppID -match '\\WindowsPowerShell\\v1\.0\\powershell\.exe$' } |
    Select-Object -First 1
if ($null -eq $application) {
    throw 'Windows PowerShell AppUserModelID is unavailable.'
}

$xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent(
    [Windows.UI.Notifications.ToastTemplateType]::ToastText02
)
$textNodes = $xml.GetElementsByTagName('text')
[void]$textNodes.Item(0).AppendChild($xml.CreateTextNode([string]$data.title))
[void]$textNodes.Item(1).AppendChild($xml.CreateTextNode([string]$data.message))

$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
$notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier(
    [string]$application.AppID
)
$notifier.Show($toast)
""".strip()
_ENCODED_POWERSHELL_SCRIPT = base64.b64encode(
    _POWERSHELL_SCRIPT.encode("utf-16-le")
).decode("ascii")


@dataclass
class TuiNotificationCallback:
    """1 回の Codex TUI process に閉じた callback と重複排除領域。"""

    command: list[str]
    _state_directory: TemporaryDirectory[str]

    def close(self) -> None:
        """通知用の一時 state を、本命処理へ失敗を返さず破棄する。"""
        # 通知 state の cleanup failure は TUI の terminal result を変更しない。
        try:
            self._state_directory.cleanup()
        except BaseException:
            pass


def create_tui_notification_callback(
    command_name: str,
    repository_root: Path,
) -> TuiNotificationCallback | None:
    """Codex が turn 完了時に起動する invocation-local callback を作る。"""
    if not sys.executable:
        return None

    # callback ごとの process 間重複排除にだけ使う一時 directory を用意する。
    try:
        state_directory = TemporaryDirectory(prefix="cmoc-toast-")
    except OSError:
        return None
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "codex-tui-callback",
        state_directory.name,
        _short_text(command_name, "command"),
        repository_label(repository_root),
    ]
    return TuiNotificationCallback(command, state_directory)


def repository_label(repository_root: Path) -> str:
    """full path を含まない短い repository 識別子を返す。"""
    return _short_text(repository_root.name, "repository")


def notify_terminal_result(
    command_name: str,
    repository_root: Path,
    state: ToastState,
) -> None:
    """最外側サブコマンドの確定済み terminal result を通知する。"""
    _notify_fields(command_name, repository_label(repository_root), state)


def _notify_fields(command_name: str, repository: str, state: ToastState) -> None:
    """制限済み field だけから toast を作り、失敗を呼び出し元へ返さない。"""
    # prompt や assistant 本文を入力に取らず、履歴へ残せる最小情報だけを組み立てる。
    try:
        title = f"cmoc {_short_text(command_name, 'command')}"
        message = f"{_short_text(repository, 'repository')} — {_STATE_TEXT[state]}"
        _run_windows_toast_transport(title, message)
    except BaseException:
        pass


def _short_text(value: str, fallback: str) -> str:
    """通知履歴向けの一行表示へ正規化し、長さを制限する。"""
    normalized = " ".join(value.split())
    return (normalized or fallback)[:80]


def _powershell_executable() -> Path | None:
    """WSL から利用できる Windows PowerShell executable を解決する。"""
    # Windows PATH が WSL へ反映されている環境を先に使う。
    discovered = shutil.which("powershell.exe")
    if discovered is not None:
        return Path(discovered)
    if _WINDOWS_POWERSHELL.is_file():
        return _WINDOWS_POWERSHELL
    return None


def _run_windows_toast_transport(title: str, message: str) -> bool:
    """JSON stdin と固定 PowerShell script で WinRT toast を有限時間だけ試行する。"""
    executable = _powershell_executable()
    if executable is None:
        return False

    # user-controlled text は command や XML へ連結せず、ASCII JSON data として渡す。
    payload = json.dumps(
        {"title": title, "message": message},
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("ascii")
    result = subprocess.run(
        [
            str(executable),
            "-NoLogo",
            "-NoProfile",
            "-NonInteractive",
            "-EncodedCommand",
            _ENCODED_POWERSHELL_SCRIPT,
        ],
        input=payload,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=_POWERSHELL_TIMEOUT_SEC,
        check=False,
    )
    return result.returncode == 0


def _claim_turn(state_root: Path, thread_id: str, turn_id: str) -> bool:
    """TUI invocation 内で同じ turn を最初に受け取った callback だけを選ぶ。"""
    if not thread_id or not turn_id or len(thread_id) > 512 or len(turn_id) > 512:
        return False
    try:
        resolved_root = state_root.resolve(strict=True)
    except OSError:
        return False
    if not resolved_root.is_dir():
        return False

    # hash 固定名と O_EXCL により、並行 callback 間でも一度だけ所有権を得る。
    digest = hashlib.sha256(
        f"{thread_id}\0{turn_id}".encode("utf-8", errors="strict")
    ).hexdigest()
    marker = resolved_root / f"{digest}.seen"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(marker, flags, 0o600)
    except FileExistsError:
        return False
    except OSError:
        return False
    try:
        os.close(descriptor)
    except OSError:
        return False
    return True


def _run_codex_tui_callback(arguments: Sequence[str]) -> int:
    """Codex の JSON callback から turn identity だけを受理する。"""
    if len(arguments) != 5 or arguments[0] != "codex-tui-callback":
        return 0
    state_root = Path(arguments[1])
    command_name = arguments[2]
    repository = arguments[3]
    try:
        payload = json.loads(arguments[4])
    except (json.JSONDecodeError, TypeError):
        return 0
    if not isinstance(payload, dict) or payload.get("type") != "agent-turn-complete":
        return 0
    thread_id = payload.get("thread-id")
    turn_id = payload.get("turn-id")
    if not isinstance(thread_id, str) or not isinstance(turn_id, str):
        return 0
    if not _claim_turn(state_root, thread_id, turn_id):
        return 0

    # callback payload の prompt/assistant 本文は通知内容へ渡さない。
    _notify_fields(command_name, repository, "waiting")
    return 0


def main(arguments: Sequence[str] | None = None) -> int:
    """Codex external notification callback の常に非致命的な入口。"""
    try:
        return _run_codex_tui_callback(
            list(sys.argv[1:] if arguments is None else arguments)
        )
    except BaseException:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
