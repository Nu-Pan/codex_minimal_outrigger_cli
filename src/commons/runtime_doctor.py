import fcntl
import os
import random
import socket
import subprocess
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from basic.acp import ModelClass
from config.cmoc_config import CmocConfig

from commons.runtime_config import load_config, sync_config
from commons.runtime_errors import CmocError
from commons.runtime_git import ensure_cmoc_ignored, run_git

_OLLAMA_ARCHIVE_URL = "https://ollama.com/download/ollama-linux-amd64.tar.zst"
_OLLAMA_PORT_MIN = 49152
_OLLAMA_PORT_MAX = 65535
_OLLAMA_CONNECT_TIMEOUT_SEC = 0.5
_OLLAMA_START_TIMEOUT_SEC = 30.0


def run_doctor_preprocess(root: Path) -> None:
    """共通実行前修復を行い、修復差分だけを commit する。"""
    root = root.resolve()
    ensure_cmoc_ignored(root)
    _ensure_agents_tracked(root)
    sync_config(root)
    _ensure_ollama_serves_local_slm(root)
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
    run_git(["add", "--", *repair_paths], root)
    diff = run_git(
        ["diff", "--cached", "--quiet", "--", *repair_paths],
        root,
        check=False,
    )
    if diff.returncode == 1:
        run_git(["commit", "-m", "cmoc doctor preprocess", "--", *repair_paths], root)


def _ensure_ollama_serves_local_slm(root: Path) -> None:
    # <work-root>/oracle/doc/app_spec/ollama_slm_server.md
    # repo-local な ollama instance と port file を Codex profile 境界で共有する。
    with _ollama_lock(root):
        executable = _ensure_ollama_installed(root)
        port = _ensure_ollama_running(root, executable)
        model = _local_slm_model(root)
        _ensure_ollama_model(executable, port, model)


def _local_slm_model(root: Path) -> str:
    try:
        config = load_config(root)
    except CmocError:
        config = CmocConfig()
    return config.codex.model[ModelClass.LOCAL_SLM]


def _ollama_root(root: Path) -> Path:
    return root / ".cmoc" / "local" / "ollama"


def _ollama_executable(root: Path) -> Path:
    return _ollama_root(root) / "bin" / "ollama"


def _ollama_port_file(root: Path) -> Path:
    return _ollama_root(root) / "port"


@contextmanager
def _ollama_lock(root: Path) -> Iterator[None]:
    lock_path = _ollama_root(root) / "lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _ensure_ollama_installed(root: Path) -> Path:
    executable = _ollama_executable(root)
    if _ollama_version_ok(executable):
        return executable
    archive_path = root / ".cmoc" / "local" / "ollama-linux-amd64.tar.zst"
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    if not archive_path.exists():
        _download_ollama_archive(archive_path)
    target = _ollama_root(root)
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
                "<repo-root>/.cmoc/local/ollama を削除してから再実行してください。",
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
                "既に取得済みの archive がある場合は <repo-root>/.cmoc/local に配置してください。",
            ],
            f"url: {_OLLAMA_ARCHIVE_URL}\npath: {path}",
        ) from exc


def _ensure_ollama_running(root: Path, executable: Path) -> int:
    port_path = _ollama_port_file(root)
    existing_port = _read_port(port_path)
    if existing_port is not None and _ollama_http_ok(existing_port):
        return existing_port
    port = _choose_port()
    env = os.environ.copy()
    env["OLLAMA_HOST"] = f"127.0.0.1:{port}"
    log_path = _ollama_root(root) / "serve.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_file = log_path.open("ab")
    try:
        subprocess.Popen(
            [str(executable), "serve"],
            cwd=root,
            env=env,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    finally:
        log_file.close()
    deadline = time.monotonic() + _OLLAMA_START_TIMEOUT_SEC
    while time.monotonic() < deadline:
        if _ollama_http_ok(port):
            port_path.write_text(f"{port}\n")
            return port
        time.sleep(0.2)
    raise CmocError(
        "ollama serve を起動できませんでした。",
        [
            "<repo-root>/.cmoc/local/ollama/serve.log を確認してください。",
            "使用可能な local port と ollama 実行ファイルを確認してください。",
        ],
        f"port: {port}\nlog: {log_path}",
    )


def _read_port(path: Path) -> int | None:
    try:
        port = int(path.read_text().strip())
    except (OSError, ValueError):
        return None
    if _OLLAMA_PORT_MIN <= port <= _OLLAMA_PORT_MAX:
        return port
    return None


def _choose_port() -> int:
    for _ in range(100):
        port = random.randint(_OLLAMA_PORT_MIN, _OLLAMA_PORT_MAX)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise CmocError(
        "ollama 用 local port を選択できませんでした。",
        ["49152-65535 の local port 使用状況を確認してください。"],
        "available port was not found",
    )


def _ollama_http_ok(port: int) -> bool:
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/api/tags",
            timeout=_OLLAMA_CONNECT_TIMEOUT_SEC,
        ) as response:
            return 200 <= response.status < 500
    except (OSError, urllib.error.URLError):
        return False


def _ensure_ollama_model(executable: Path, port: int, model: str) -> None:
    if _run_ollama(executable, port, ["show", model]).returncode == 0:
        return
    pull = _run_ollama(executable, port, ["pull", model])
    if pull.returncode != 0:
        raise CmocError(
            "ollama SLM model を取得できませんでした。",
            ["モデル名と ollama の接続状態を確認してください。"],
            f"model: {model}\nstdout:\n{pull.stdout}\nstderr:\n{pull.stderr}",
        )
    show = _run_ollama(executable, port, ["show", model])
    if show.returncode != 0:
        raise CmocError(
            "ollama SLM model を serve 可能な状態にできませんでした。",
            ["モデル名と ollama の model store を確認してください。"],
            f"model: {model}\nstdout:\n{show.stdout}\nstderr:\n{show.stderr}",
        )


def _run_ollama(
    executable: Path, port: int, args: list[str]
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["OLLAMA_HOST"] = f"127.0.0.1:{port}"
    return subprocess.run(
        [str(executable), *args],
        text=True,
        capture_output=True,
        env=env,
    )
