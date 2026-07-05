import fcntl
import os
import subprocess
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from config.cmoc_config import CmocConfig

from commons.runtime_config import load_config, sync_config
from commons.runtime_errors import CmocError
from commons.runtime_git import ensure_cmoc_ignored, run_git

_OLLAMA_ARCHIVE_URL = "https://ollama.com/download/ollama-linux-amd64.tar.zst"
_OLLAMA_HOST = "127.0.0.1:11434"
_OLLAMA_CONNECT_TIMEOUT_SEC = 0.5
_OLLAMA_START_TIMEOUT_SEC = 30.0
_OLLAMA_SERVICE_NAME = "cmoc-ollama"


def run_doctor_preprocess(root: Path, config: CmocConfig | None = None) -> None:
    """共通実行前修復を行い、修復差分だけを commit する。"""
    root = root.resolve()
    ensure_cmoc_ignored(root)
    _ensure_agents_tracked(root)
    sync_config(root)
    _ensure_ollama_serves_local_slm(root, config)
    _commit_doctor_repairs(root)


def _ensure_agents_tracked(root: Path) -> None:
    # <work-root>/oracle/doc/app_spec/doctor_preprocess.md
    # .agents は agent 操作禁止領域なので、tracked file がない場合だけ
    # placeholder を追加して差分が出る余地を小さくする。
    agents = root / ".agents"
    agents.mkdir(exist_ok=True)
    if run_git(["ls-files", "--", ".agents"], root).stdout.strip():
        return
    gitkeep = agents / ".gitkeep"
    gitkeep.touch(exist_ok=True)
    run_git(["add", "-f", ".agents/.gitkeep"], root)
    if not run_git(["ls-files", "--", ".agents"], root).stdout.strip():
        raise CmocError(
            ".agents を git 追跡対象にできませんでした。",
            [".agents/.gitkeep と git index の状態を確認してください。"],
            str(agents),
        )


def _commit_doctor_repairs(root: Path) -> None:
    repair_paths = [".gitignore", ".agents/.gitkeep", ".cmoc/config.json"]
    # <work-root>/oracle/doc/app_spec/doctor_preprocess.md
    # `.cmoc/` 全体が ignored でも、修復した config は commit 対象に保つ。
    run_git(["add", "-f", "--", *repair_paths], root)
    diff = run_git(
        ["diff", "--cached", "--quiet", "--", *repair_paths],
        root,
        check=False,
    )
    if diff.returncode == 1:
        run_git(["commit", "-m", "cmoc doctor preprocess", "--", *repair_paths], root)


def _ensure_ollama_serves_local_slm(
    root: Path, config: CmocConfig | None = None
) -> None:
    # <work-root>/oracle/doc/app_spec/cmoc_managed_ollama.md
    # cmoc provider を要求する model がある場合だけ、user service として 11434 固定で扱う。
    models = _cmoc_managed_model_names(root, config)
    if not models:
        return
    with _ollama_lock():
        executable = _ensure_ollama_installed()
        _ensure_ollama_service(executable)
        _verify_ollama_service(executable)
        for model in models:
            _ensure_ollama_model(executable, model)


def _cmoc_managed_model_names(
    root: Path, config: CmocConfig | None = None
) -> list[str]:
    if config is None:
        try:
            config = load_config(root)
        except CmocError:
            config = CmocConfig()
    models: list[str] = []
    seen: set[str] = set()
    for spec in config.codex.model.values():
        if spec.model_provider == "cmoc":
            if spec.model not in seen:
                models.append(spec.model)
                seen.add(spec.model)
    return models


def _ollama_root() -> Path:
    return Path.home() / ".cmoc" / "ollama"


def _ollama_executable() -> Path:
    return _ollama_root() / "bin" / "ollama"


def _ollama_service_file() -> Path:
    return (
        Path.home()
        / ".config"
        / "systemd"
        / "user"
        / f"{_OLLAMA_SERVICE_NAME}.service"
    )


@contextmanager
def _ollama_lock() -> Iterator[None]:
    lock_path = _ollama_root() / "lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _ensure_ollama_installed() -> Path:
    executable = _ollama_executable()
    if _ollama_version_ok(executable):
        return executable
    archive_path = _ollama_root() / "ollama-linux-amd64.tar.zst"
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    if not archive_path.exists():
        _download_ollama_archive(archive_path)
    target = _ollama_root()
    target.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["tar", "--zstd", "-xf", str(archive_path), "-C", str(target)],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0 or not _ollama_version_ok(executable):
        raise CmocError(
            "ollama をインストールできませんでした。",
            [
                "archive の取得状態と tar/zstd の利用可否を確認してください。",
                "~/.cmoc/ollama を削除してから再実行してください。",
            ],
            f"archive: {archive_path}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
    return executable


def _ollama_version_ok(executable: Path) -> bool:
    if not executable.exists():
        return False
    result = subprocess.run(
        [str(executable), "--version"],
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def _download_ollama_archive(path: Path) -> None:
    try:
        with urllib.request.urlopen(_OLLAMA_ARCHIVE_URL) as response:
            path.write_bytes(response.read())
    except (OSError, urllib.error.URLError) as exc:
        raise CmocError(
            "ollama archive を取得できませんでした。",
            [
                "ネットワーク接続を確認してから再実行してください。",
                "既に取得済みの archive がある場合は ~/.cmoc/ollama に配置してください。",
            ],
            f"url: {_OLLAMA_ARCHIVE_URL}\npath: {path}",
        ) from exc


def _ensure_ollama_service(executable: Path) -> None:
    _write_ollama_service_file(executable)
    reload_result = _run_systemctl(["daemon-reload"])
    if reload_result.returncode != 0:
        _raise_systemctl_error(
            "ollama service 設定を再読み込みできませんでした。", reload_result
        )
    start_result = _run_systemctl(["enable", "--now", _OLLAMA_SERVICE_NAME])
    if start_result.returncode != 0:
        _raise_systemctl_error("ollama service を起動できませんでした。", start_result)


def _write_ollama_service_file(executable: Path) -> None:
    models_dir = executable.parents[1] / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    service_path = _ollama_service_file()
    service_path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(
        [
            "[Unit]",
            "Description=cmoc managed ollama",
            "",
            "[Service]",
            f"ExecStart={executable} serve",
            f"Environment=OLLAMA_HOST={_OLLAMA_HOST}",
            "Environment=OLLAMA_MODELS=%h/.cmoc/ollama/models",
            "",
            "[Install]",
            "WantedBy=default.target",
            "",
        ]
    )
    if not service_path.exists() or service_path.read_text() != text:
        service_path.write_text(text)


def _verify_ollama_service(executable: Path) -> None:
    if not _service_active():
        raise CmocError(
            "cmoc managed ollama service が起動していません。",
            [f"systemctl --user status {_OLLAMA_SERVICE_NAME} を確認してください。"],
            f"service: {_OLLAMA_SERVICE_NAME}",
        )
    if not _service_process_matches(executable):
        raise CmocError(
            "127.0.0.1:11434 の ollama service が cmoc managed ollama と一致しません。",
            [
                f"systemctl --user restart {_OLLAMA_SERVICE_NAME} を実行してから再試行してください。"
            ],
            f"expected executable: {executable}",
        )
    deadline = time.monotonic() + _OLLAMA_START_TIMEOUT_SEC
    while time.monotonic() < deadline:
        if _ollama_http_ok():
            return
        time.sleep(0.2)
    raise CmocError(
        "cmoc managed ollama へ接続できませんでした。",
        [
            f"systemctl --user status {_OLLAMA_SERVICE_NAME} を確認してください。",
            "127.0.0.1:11434 の利用状況を確認してください。",
        ],
        f"host: {_OLLAMA_HOST}",
    )


def _service_active() -> bool:
    return (
        _run_systemctl(["is-active", "--quiet", _OLLAMA_SERVICE_NAME]).returncode == 0
    )


def _service_process_matches(executable: Path) -> bool:
    pid_result = _run_systemctl(
        ["show", _OLLAMA_SERVICE_NAME, "--property=MainPID", "--value"]
    )
    if pid_result.returncode != 0:
        return _service_file_matches(executable)
    try:
        process_id = int(pid_result.stdout.strip())
    except ValueError:
        return _service_file_matches(executable)
    if process_id <= 0:
        return _service_file_matches(executable)
    return _process_argv_uses_executable(process_id, executable) or _service_file_matches(
        executable
    )


def _service_file_matches(executable: Path) -> bool:
    try:
        lines = _ollama_service_file().read_text().splitlines()
    except OSError:
        return False
    return f"ExecStart={executable} serve" in lines


def _process_argv_uses_executable(process_id: int, executable: Path) -> bool:
    try:
        raw = Path(f"/proc/{process_id}/cmdline").read_bytes()
    except OSError:
        return False
    argv = [item.decode(errors="replace") for item in raw.split(b"\0") if item]
    return str(executable) in argv[:2]


def _ollama_http_ok() -> bool:
    try:
        with urllib.request.urlopen(
            f"http://{_OLLAMA_HOST}/api/tags",
            timeout=_OLLAMA_CONNECT_TIMEOUT_SEC,
        ) as response:
            return 200 <= response.status < 500
    except (OSError, urllib.error.URLError):
        return False


def _ensure_ollama_model(executable: Path, model: str) -> None:
    if _run_ollama(executable, ["show", model]).returncode == 0:
        return
    pull = _run_ollama(executable, ["pull", model])
    if pull.returncode != 0:
        raise CmocError(
            "ollama SLM model を取得できませんでした。",
            ["モデル名と ollama の接続状態を確認してください。"],
            f"model: {model}\nstdout:\n{pull.stdout}\nstderr:\n{pull.stderr}",
        )
    show = _run_ollama(executable, ["show", model])
    if show.returncode != 0:
        raise CmocError(
            "ollama SLM model を serve 可能な状態にできませんでした。",
            ["モデル名と ollama の model store を確認してください。"],
            f"model: {model}\nstdout:\n{show.stdout}\nstderr:\n{show.stderr}",
        )


def _run_ollama(executable: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(_ollama_env())
    return subprocess.run(
        [str(executable), *args],
        text=True,
        capture_output=True,
        env=env,
    )


def _ollama_env() -> dict[str, str]:
    root = Path.home() / ".cmoc" / "ollama"
    return {
        "OLLAMA_HOST": _OLLAMA_HOST,
        "OLLAMA_MODELS": str(root / "models"),
    }


def _run_systemctl(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["systemctl", "--user", *args],
        text=True,
        capture_output=True,
    )


def _raise_systemctl_error(
    message: str, result: subprocess.CompletedProcess[str]
) -> None:
    raise CmocError(
        message,
        ["systemd user service と systemctl --user の利用可否を確認してください。"],
        f"argv: {' '.join(result.args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
    )
