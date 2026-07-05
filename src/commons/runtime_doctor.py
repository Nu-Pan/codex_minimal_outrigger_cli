import fcntl
import os
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from config.cmoc_config import CmocConfig

from commons.runtime_config import load_config
from commons.runtime_errors import CmocError
from commons.runtime_git import ensure_cmoc_ignored, run_git, with_cmoc_ignore_pattern

_OLLAMA_ARCHIVE_URL = "https://ollama.com/download/ollama-linux-amd64.tar.zst"
_OLLAMA_HOST = "127.0.0.1:11434"
_OLLAMA_CONNECT_TIMEOUT_SEC = 0.5
_OLLAMA_START_TIMEOUT_SEC = 30.0
_OLLAMA_SERVICE_NAME = "cmoc-ollama"


def run_doctor_preprocess(root: Path, config: CmocConfig | None = None) -> None:
    """共通実行前修復を行い、修復差分だけを commit する。"""
    root = root.resolve()
    restored_index_tree = _restored_index_tree(root)
    ensure_cmoc_ignored(root)
    _ensure_agents_tracked(root)
    _ensure_ollama_serves_local_slm(root, config)
    _commit_doctor_repairs(root, restored_index_tree)


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


def _commit_doctor_repairs(root: Path, restored_index_tree: str) -> None:
    _commit_doctor_repairs_from_head(root)
    try:
        run_git(["reset", "-q", "HEAD"], root)
    finally:
        run_git(["read-tree", restored_index_tree], root)


def _commit_doctor_repairs_from_head(root: Path) -> None:
    # <work-root>/oracle/doc/app_spec/doctor_preprocess.md
    # repair commit は doctor の作業差分だけなので、通常 index ではなく
    # HEAD 起点の一時 index で user staged hunks と同一 path 上でも分離する。
    fd, index_name = tempfile.mkstemp(prefix="cmoc-doctor-index-")
    os.close(fd)
    index_path = Path(index_name)
    try:
        _run_git_with_index(["read-tree", "HEAD"], root, index_path)
        _stage_gitignore_repair(root, index_path)
        _stage_agents_gitkeep_repair(root, index_path)
        _run_git_with_index(
            ["rm", "--cached", "-r", "--ignore-unmatch", ".cmoc/local"],
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
    head = run_git(["show", "HEAD:.gitignore"], root, check=False)
    head_content = head.stdout if head.returncode == 0 else ""
    repaired = with_cmoc_ignore_pattern(head_content)
    if repaired != head_content:
        _stage_text(root, index_path, ".gitignore", repaired)


def _stage_agents_gitkeep_repair(root: Path, index_path: Path) -> None:
    head_agents = run_git(
        ["ls-tree", "-r", "--name-only", "HEAD", "--", ".agents"], root
    ).stdout.strip()
    if not head_agents and (root / ".agents" / ".gitkeep").exists():
        _stage_text(root, index_path, ".agents/.gitkeep", "")


def _restored_index_tree(root: Path) -> str:
    # <work-root>/oracle/doc/app_spec/doctor_preprocess.md
    # 復元対象は path 列挙ではなく index 全体で扱う。rename や同一 path の
    # unstaged hunk を壊さず、doctor 優先の修復だけを合成した tree を戻す。
    index_path = _copy_current_index(root)
    try:
        _stage_gitignore_repair_from_index(root, index_path)
        _stage_agents_gitkeep_repair_from_index(root, index_path)
        _run_git_with_index(
            ["rm", "--cached", "-r", "--ignore-unmatch", ".cmoc/local"],
            root,
            index_path,
        )
        return _run_git_with_index(["write-tree"], root, index_path).stdout.strip()
    finally:
        index_path.unlink(missing_ok=True)


def _copy_current_index(root: Path) -> Path:
    fd, index_name = tempfile.mkstemp(prefix="cmoc-doctor-restore-index-")
    os.close(fd)
    index_path = Path(index_name)
    current_index = root / run_git(
        ["rev-parse", "--git-path", "index"], root
    ).stdout.strip()
    if current_index.exists():
        shutil.copy2(current_index, index_path)
    else:
        _run_git_with_index(["read-tree", "HEAD"], root, index_path)
    return index_path


def _stage_gitignore_repair_from_index(root: Path, index_path: Path) -> None:
    current = _index_text(root, index_path, ".gitignore")
    repaired = with_cmoc_ignore_pattern(current or "")
    if repaired != (current or ""):
        _stage_text(root, index_path, ".gitignore", repaired)


def _stage_agents_gitkeep_repair_from_index(root: Path, index_path: Path) -> None:
    agents = _run_git_with_index(
        ["ls-files", "--", ".agents"], root, index_path
    ).stdout.strip()
    if not agents:
        _stage_text(root, index_path, ".agents/.gitkeep", "")


def _index_text(root: Path, index_path: Path, path: str) -> str | None:
    result = _run_git_with_index(["show", f":{path}"], root, index_path, check=False)
    if result.returncode != 0:
        return None
    return result.stdout


def _stage_text(root: Path, index_path: Path, path: str, content: str) -> None:
    blob = _run_git_with_index(
        ["hash-object", "-w", "--stdin"], root, index_path, input_text=content
    ).stdout.strip()
    _run_git_with_index(
        ["update-index", "--add", "--cacheinfo", "100644", blob, path],
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
    main_pid = _service_main_pid()
    if main_pid is None or not _process_argv_uses_executable(main_pid, executable):
        raise CmocError(
            "127.0.0.1:11434 の ollama service が cmoc managed ollama と一致しません。",
            [
                f"systemctl --user restart {_OLLAMA_SERVICE_NAME} を実行してから再試行してください。"
            ],
            f"expected executable: {executable}",
        )
    deadline = time.monotonic() + _OLLAMA_START_TIMEOUT_SEC
    listener_matched = False
    while time.monotonic() < deadline:
        listener_matched = _listener_matches_service(main_pid, executable)
        if listener_matched and _ollama_http_ok():
            return
        time.sleep(0.2)
    if not listener_matched:
        raise CmocError(
            "127.0.0.1:11434 の ollama service が cmoc managed ollama と一致しません。",
            [
                f"systemctl --user restart {_OLLAMA_SERVICE_NAME} を実行してから再試行してください。"
            ],
            f"expected executable: {executable}",
        )
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


def _service_main_pid() -> int | None:
    pid_result = _run_systemctl(
        ["show", _OLLAMA_SERVICE_NAME, "--property=MainPID", "--value"]
    )
    if pid_result.returncode != 0:
        return None
    try:
        process_id = int(pid_result.stdout.strip())
    except ValueError:
        return None
    return process_id if process_id > 0 else None


def _listener_matches_service(main_pid: int, executable: Path) -> bool:
    # <work-root>/oracle/doc/app_spec/cmoc_managed_ollama.md
    # service file は設定の正しさだけを示すため、11434 の現 listener を
    # /proc で MainPID 系列の cmoc managed ollama process と直接対応付ける。
    for process_id in _ollama_listener_process_ids():
        if _process_is_descendant(process_id, main_pid) and _process_argv_uses_executable(
            process_id, executable
        ):
            return True
    return False


def _process_argv_uses_executable(process_id: int, executable: Path) -> bool:
    try:
        raw = Path(f"/proc/{process_id}/cmdline").read_bytes()
    except OSError:
        return False
    argv = [item.decode(errors="replace") for item in raw.split(b"\0") if item]
    return str(executable) in argv[:2]


def _ollama_listener_process_ids() -> set[int]:
    inodes = _listening_socket_inodes()
    if not inodes:
        return set()
    process_ids: set[int] = set()
    for process_dir in Path("/proc").iterdir():
        if not process_dir.name.isdigit():
            continue
        fd_dir = process_dir / "fd"
        try:
            fds = list(fd_dir.iterdir())
        except OSError:
            continue
        for fd in fds:
            try:
                target = os.readlink(fd)
            except OSError:
                continue
            if target.startswith("socket:[") and target[8:-1] in inodes:
                process_ids.add(int(process_dir.name))
                break
    return process_ids


def _listening_socket_inodes() -> set[str]:
    inodes: set[str] = set()
    for table in (Path("/proc/net/tcp"), Path("/proc/net/tcp6")):
        try:
            lines = table.read_text().splitlines()[1:]
        except OSError:
            continue
        for line in lines:
            fields = line.split()
            if len(fields) > 9 and _is_ollama_listen_socket(fields[1], fields[3]):
                inodes.add(fields[9])
    return inodes


def _is_ollama_listen_socket(local_address: str, state: str) -> bool:
    if state != "0A":
        return False
    host_hex, port_hex = local_address.rsplit(":", 1)
    return host_hex == "0100007F" and int(port_hex, 16) == 11434


def _process_is_descendant(process_id: int, ancestor_id: int) -> bool:
    seen: set[int] = set()
    while process_id > 0 and process_id not in seen:
        if process_id == ancestor_id:
            return True
        seen.add(process_id)
        process_id = _process_parent_id(process_id)
    return False


def _process_parent_id(process_id: int) -> int:
    try:
        stat = Path(f"/proc/{process_id}/stat").read_text()
    except OSError:
        return 0
    tail = stat.rsplit(") ", 1)[-1].split()
    if len(tail) < 2:
        return 0
    try:
        return int(tail[1])
    except ValueError:
        return 0


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
