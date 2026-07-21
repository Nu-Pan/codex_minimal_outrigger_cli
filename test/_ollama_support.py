"""実経路統合テスト専用の case-local Ollama を準備する。

この file は 16,000 文字を超えるが、cache の検証・atomic publish・materialize、
GPU-only model の構築・確認、process teardown は、同じ working set と execution
lock のライフサイクルを共有する一つの責務である。分割すると、失敗時にも cache を
変更せず case の process group だけを停止する不変条件を複数 file で追う必要がある。

根拠: {{work-root}}/oracle/doc/dev_rule/test_rule.md
"""

import fcntl
import hashlib
import json
import os
import shutil
import signal
import socket
import stat
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, replace
from pathlib import Path

import pytest

from basic.acp import ModelClass
from commons.runtime_paths import repo_root
from config.cmoc_config import (
    CmocConfig,
    CodexModelProviderConfig,
    CodexModelSpec,
)

# {{work-root}}/oracle/doc/dev_rule/test_rule.md
TEST_SLM_MODEL = "qwen3:4b-instruct-2507-q4_K_M"
TEST_OLLAMA_CACHE_ENV = "CMOC_TEST_OLLAMA_CACHE"
_CACHE_SCHEMA_VERSION = 1
_ARCHIVE_URL = "https://ollama.com/download/ollama-linux-amd64.tar.zst"
_GPU_LAYER_COUNT = 999
_MAX_OUTPUT_TOKENS = 4096
_GPU_INFERENCE_TIMEOUT = 120
_WORK_ROOT = Path(__file__).resolve().parents[1]
_CMOC_ROOT = repo_root(_WORK_ROOT)


@dataclass(frozen=True)
class LocalOllama:
    """単一 test case が所有する Ollama process の接続情報。"""

    root: Path
    executable: Path
    host: str
    process_id: int

    @property
    def provider_id(self) -> str:
        """通常の CmocConfig で選択する test provider ID を返す。"""
        return "test_local_ollama"

    @property
    def provider_config(self) -> CodexModelProviderConfig:
        """動的 port の Ollama を Codex Responses provider として表す。"""
        return CodexModelProviderConfig(
            {
                "name": "test-local Ollama",
                "base_url": f"http://{self.host}/v1",
                "wire_api": "responses",
            }
        )


def use_test_local_ollama(
    config: CmocConfig,
    ollama: LocalOllama,
    model_classes: tuple[ModelClass, ...] = tuple(ModelClass),
) -> CmocConfig:
    """通常の model provider 設定で指定 model class を case-local Ollama へ向ける。"""
    providers = {
        **config.codex.model_providers,
        ollama.provider_id: ollama.provider_config,
    }
    models = dict(config.codex.model)
    models.update(
        {
            model_class: CodexModelSpec(ollama.provider_id, TEST_SLM_MODEL)
            for model_class in model_classes
        }
    )
    return replace(
        config,
        codex=replace(config.codex, model_providers=providers, model=models),
    )


@contextmanager
def local_ollama(tmp_path: Path) -> Iterator[LocalOllama]:
    """cache を materialize し、専用 process group を case 終了まで保持する。"""
    cache_root = _select_cache_root(tmp_path)
    with _file_lock(cache_root / "execution.lock"):
        install_cache = _ensure_cached_install(cache_root)
        case_root = tmp_path / "test-local-ollama"
        case_root.mkdir(mode=0o700)
        install = case_root / "install"
        models = case_root / "models"
        _materialize(install_cache, install)
        cached_models = cache_root / "models"
        if cached_models.is_dir() and not cached_models.is_symlink():
            _materialize(cached_models, models)
        else:
            models.mkdir()

        # HOME、runtime、model working set、binary、PID、log、port を case 内へ隔離する。
        home = case_root / "home"
        runtime = case_root / "runtime"
        home.mkdir()
        runtime.mkdir()
        host = f"127.0.0.1:{_unused_loopback_port()}"
        executable = install / "bin" / "ollama"
        # Codex の built-in instructions/tool schema が小さい既定 context を超えるため、
        # 実プロンプトも収まる test-local context を明示する。
        environment = {
            **{
                key: value
                for key, value in os.environ.items()
                if not key.startswith("OLLAMA_")
            },
            "HOME": str(home),
            "TMPDIR": str(runtime),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "NO_PROXY": "127.0.0.1,localhost",
            "no_proxy": "127.0.0.1,localhost",
            "OLLAMA_CONTEXT_LENGTH": "32768",
            "OLLAMA_HOST": host,
            "OLLAMA_MODELS": str(models),
        }
        log_path = case_root / "ollama.log"
        with log_path.open("wb", buffering=0) as log_file:
            process = subprocess.Popen(
                [str(executable), "serve"],
                cwd=runtime,
                env=environment,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            try:
                (case_root / "ollama.pid").write_text(
                    f"{process.pid}\n", encoding="utf-8"
                )
                _wait_for_server(process, host, log_path)
                cache_changed = _ensure_model(
                    executable,
                    environment,
                    process,
                    log_path,
                    runtime,
                )
                if cache_changed:
                    _publish_models(cache_root, models)
                _require_gpu_inference(process, host, log_path)
                yield LocalOllama(case_root, executable, host, process.pid)
            finally:
                _stop_process_group(process)


def _select_cache_root(tmp_path: Path) -> Path:
    """system temp cache を検証し、利用不能時だけ pytest session temp へ退避する。"""
    override = os.environ.get(TEST_OLLAMA_CACHE_ENV)
    if override:
        candidate = Path(override)
        _prepare_cache_root(candidate)
        return candidate.resolve()
    user = str(os.getuid()) if hasattr(os, "getuid") else os.environ.get("USER", "user")
    candidate = (
        Path(tempfile.gettempdir())
        / f"cmoc-test-ollama-{user}-v{_CACHE_SCHEMA_VERSION}"
    )
    try:
        _prepare_cache_root(candidate)
        return candidate.resolve()
    except OSError:
        fallback = tmp_path.parent / f"ollama-cache-{user}-v{_CACHE_SCHEMA_VERSION}"
        _prepare_cache_root(fallback)
        return fallback.resolve()


def _prepare_cache_root(path: Path) -> None:
    """cache root の owner、permission、I/O、rename、flock 条件を検証する。"""
    resolved = path.resolve(strict=False)
    if any(
        resolved == root or resolved.is_relative_to(root)
        for root in {_CMOC_ROOT, _WORK_ROOT}
    ):
        raise OSError("Ollama test cache must be outside the repository")
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    metadata = path.lstat()
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISDIR(metadata.st_mode)
        or (hasattr(os, "getuid") and metadata.st_uid != os.getuid())
        or stat.S_IMODE(metadata.st_mode) != 0o700
        or not os.access(path, os.R_OK | os.W_OK | os.X_OK)
    ):
        raise OSError(f"unsafe Ollama test cache: {path}")

    # probe は同一 directory 内の atomic rename と advisory file lock の両方を確認する。
    token = f".probe-{os.getpid()}-{uuid.uuid4().hex}"
    source = path / token
    target = path / f"{token}-renamed"
    try:
        descriptor = os.open(source, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        try:
            os.write(descriptor, b"probe")
        finally:
            os.close(descriptor)
        os.replace(source, target)
        with (path / "cache.lock").open("a+b") as lock_file:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
    finally:
        source.unlink(missing_ok=True)
        target.unlink(missing_ok=True)


@contextmanager
def _file_lock(path: Path) -> Iterator[None]:
    """cache 更新または Ollama 実行の process 間排他を保持する。"""
    with path.open("a+b") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _ensure_cached_install(cache_root: Path) -> Path:
    """archive digest で versioning した Ollama working tree を atomic publish する。"""
    with _file_lock(cache_root / "cache.lock"):
        archive = cache_root / "ollama-linux-amd64.tar.zst"
        for attempt in range(2):
            if not archive.is_file() or archive.is_symlink():
                _download_archive(archive)
            digest = _sha256(archive)
            install = cache_root / "binaries" / digest
            if _ollama_executable_ok(install / "bin" / "ollama"):
                return install
            staging = cache_root / f"install-staging-{uuid.uuid4().hex}"
            staging.mkdir()
            try:
                result = subprocess.run(
                    ["tar", "--zstd", "-xf", str(archive), "-C", str(staging)],
                    text=True,
                    capture_output=True,
                    timeout=300,
                    check=False,
                )
                if result.returncode == 0 and _ollama_executable_ok(
                    staging / "bin" / "ollama"
                ):
                    install.parent.mkdir(exist_ok=True)
                    stale = cache_root / f"install-stale-{uuid.uuid4().hex}"
                    try:
                        if install.exists():
                            os.replace(install, stale)
                        os.replace(staging, install)
                    finally:
                        shutil.rmtree(stale, ignore_errors=True)
                    return install
            finally:
                shutil.rmtree(staging, ignore_errors=True)
            archive.unlink(missing_ok=True)
            if attempt:
                raise RuntimeError(
                    "Ollama archive extraction failed: "
                    f"stdout={result.stdout!r}, stderr={result.stderr!r}"
                )
    raise AssertionError("unreachable")


def _download_archive(path: Path) -> None:
    """archive を staging file へ streaming download してから公開する。"""
    staging = path.with_name(f"{path.name}.staging-{uuid.uuid4().hex}")
    try:
        with urllib.request.urlopen(_ARCHIVE_URL, timeout=60) as response:
            with staging.open("xb") as output:
                shutil.copyfileobj(response, output)
                output.flush()
                os.fsync(output.fileno())
        if staging.stat().st_size == 0:
            raise OSError("downloaded Ollama archive is empty")
        os.replace(staging, path)
    finally:
        staging.unlink(missing_ok=True)


def _sha256(path: Path) -> str:
    """cache binary の version key とする archive digest を返す。"""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _ollama_executable_ok(executable: Path) -> bool:
    """cache hit が実在の起動可能な Ollama binary を含むか確認する。"""
    if not executable.is_file() or executable.is_symlink():
        return False
    try:
        result = subprocess.run(
            [str(executable), "--version"],
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except OSError:
        return False
    return result.returncode == 0


def _materialize(source: Path, target: Path) -> None:
    """reflink/copy により cache から独立した case working set を作る。"""
    if target.exists():
        raise FileExistsError(target)
    target.mkdir()
    result = subprocess.run(
        ["cp", "-a", "--reflink=auto", f"{source}/.", str(target)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return
    shutil.rmtree(target)
    shutil.copytree(source, target)


def _unused_loopback_port() -> int:
    """case-local server 用に loopback の動的空き port を予約して返す。"""
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def _wait_for_server(
    process: subprocess.Popen[bytes], host: str, log_path: Path
) -> None:
    """専用 process が HTTP request を受けられるまで待つ。"""
    deadline = time.monotonic() + 60
    endpoint = f"http://{host}/api/tags"
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    while time.monotonic() < deadline:
        if process.poll() is not None:
            break
        try:
            with opener.open(endpoint, timeout=0.5) as response:
                if 200 <= response.status < 300:
                    return
        except (OSError, urllib.error.URLError):
            time.sleep(0.1)
    detail = log_path.read_text(errors="replace") if log_path.exists() else ""
    raise RuntimeError(f"test-local Ollama did not start: {detail[-4000:]}")


def _ensure_model(
    executable: Path,
    environment: dict[str, str],
    process: subprocess.Popen[bytes],
    log_path: Path,
    runtime: Path,
) -> bool:
    """model cache を修復し、GPU-only と有限な応答量を model に固定する。"""
    show = _run_ollama(executable, ["show", TEST_SLM_MODEL], environment, 120)
    changed = show.returncode != 0
    if changed:
        pull = _run_ollama(executable, ["pull", TEST_SLM_MODEL], environment, 1800)
        show = _run_ollama(executable, ["show", TEST_SLM_MODEL], environment, 120)
        if pull.returncode != 0 or show.returncode != 0 or process.poll() is not None:
            log = log_path.read_text(errors="replace") if log_path.exists() else ""
            raise RuntimeError(
                "test-local Ollama model pull failed\n"
                f"pull stdout:\n{pull.stdout}\npull stderr:\n{pull.stderr}\n"
                f"server log:\n{log[-4000:]}"
            )

    parameters = _run_ollama(
        executable,
        ["show", "--parameters", TEST_SLM_MODEL],
        environment,
        120,
    )
    required_settings = {
        ("num_gpu", str(_GPU_LAYER_COUNT)),
        ("num_predict", str(_MAX_OUTPUT_TOKENS)),
    }
    actual_settings = {tuple(line.split()) for line in parameters.stdout.splitlines()}
    if parameters.returncode == 0 and required_settings <= actual_settings:
        return changed

    # {{work-root}}/oracle/doc/dev_rule/test_rule.md
    # Ollama に CPU fallback 禁止 flag はないため、全 layer より大きい num_gpu を
    # 固定する。LLM 回答品質は non-goal のため、正常時を十分上回る num_predict で
    # 暴走生成も timeout より先に止める。
    modelfile = _run_ollama(
        executable,
        ["show", "--modelfile", TEST_SLM_MODEL],
        environment,
        120,
    )
    if modelfile.returncode != 0:
        raise RuntimeError(
            f"test-local Ollama Modelfile export failed: {modelfile.stderr[-4000:]}"
        )
    modelfile_path = runtime / "gpu-only.Modelfile"
    content = "\n".join(
        line
        for line in modelfile.stdout.splitlines()
        if not line.startswith(("PARAMETER num_gpu ", "PARAMETER num_predict "))
    )
    modelfile_path.write_text(
        f"{content}\n"
        f"PARAMETER num_gpu {_GPU_LAYER_COUNT}\n"
        f"PARAMETER num_predict {_MAX_OUTPUT_TOKENS}\n",
        encoding="utf-8",
    )
    try:
        create = _run_ollama(
            executable,
            ["create", TEST_SLM_MODEL, "-f", str(modelfile_path)],
            environment,
            300,
        )
    finally:
        modelfile_path.unlink(missing_ok=True)
    if create.returncode != 0 or process.poll() is not None:
        log = log_path.read_text(errors="replace") if log_path.exists() else ""
        raise RuntimeError(
            "test-local Ollama GPU-only model creation failed\n"
            f"stdout:\n{create.stdout[-4000:]}\nstderr:\n{create.stderr[-4000:]}\n"
            f"server log:\n{log[-4000:]}"
        )
    return True


def _require_gpu_inference(
    process: subprocess.Popen[bytes], host: str, log_path: Path
) -> None:
    """GPU-only load と短い実推論を確認し、利用不能なら test case を skip する。"""
    log_hint = f"; server log: {log_path}"
    try:
        _request_json(
            host,
            "/api/generate",
            {"model": TEST_SLM_MODEL, "keep_alive": -1, "stream": False},
        )
        if process.poll() is not None or not _model_is_fully_on_gpu(host):
            pytest.skip(
                f"test-local Ollama could not load the test SLM fully on GPU{log_hint}"
            )
        result = _request_json(
            host,
            "/api/generate",
            {
                "model": TEST_SLM_MODEL,
                "prompt": "GPU preflight",
                "keep_alive": -1,
                "stream": False,
                "options": {"num_predict": 1},
            },
        )
        if result.get("done") is not True or not _model_is_fully_on_gpu(host):
            pytest.skip(
                f"test-local Ollama GPU inference could not be confirmed{log_hint}"
            )
    except (OSError, TimeoutError) as exc:
        pytest.skip(f"test-local Ollama GPU inference is unavailable: {exc}{log_hint}")


def _model_is_fully_on_gpu(host: str) -> bool:
    """唯一の loaded model が CPU offload なしで VRAM に常駐するか確認する。"""
    payload = _request_json(host, "/api/ps")
    models = payload.get("models")
    if not isinstance(models, list) or len(models) != 1:
        return False
    model = models[0]
    if not isinstance(model, dict):
        return False
    size = model.get("size")
    size_vram = model.get("size_vram")
    return (
        isinstance(size, int)
        and size > 0
        and isinstance(size_vram, int)
        and size_vram >= size
    )


def _request_json(
    host: str,
    path: str,
    payload: dict[str, object] | None = None,
) -> dict[str, object]:
    """proxy を使わず case-local Ollama API の JSON object を取得する。"""
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"http://{host}{path}",
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
    )
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=_GPU_INFERENCE_TIMEOUT) as response:
        result = json.loads(response.read())
    if not isinstance(result, dict):
        raise RuntimeError(f"test-local Ollama returned non-object JSON for {path}")
    return result


def _run_ollama(
    executable: Path,
    args: list[str],
    environment: dict[str, str],
    timeout: float,
) -> subprocess.CompletedProcess[str]:
    """case-local endpoint と model working set で Ollama CLI を実行する。"""
    return subprocess.run(
        [str(executable), *args],
        env=environment,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def _publish_models(cache_root: Path, models: Path) -> None:
    """完成した model store だけを staging directory から atomic publish する。"""
    try:
        with _file_lock(cache_root / "cache.lock"):
            staging = cache_root / f"models-staging-{uuid.uuid4().hex}"
            stale = cache_root / f"models-stale-{uuid.uuid4().hex}"
            try:
                _materialize(models, staging)
                published = cache_root / "models"
                if published.exists() or published.is_symlink():
                    os.replace(published, stale)
                os.replace(staging, published)
            finally:
                shutil.rmtree(staging, ignore_errors=True)
                shutil.rmtree(stale, ignore_errors=True)
    except OSError:
        # {{work-root}}/oracle/doc/dev_rule/test_rule.md
        # cache の消失や cleanup は正常な cache miss であり、case working set は独立している。
        return


def _stop_process_group(process: subprocess.Popen[bytes]) -> None:
    """case が起動した process group だけを TERM、必要なら KILL する。"""
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        process.wait()
        return
    deadline = time.monotonic() + 10
    while _process_group_exists(process.pid) and time.monotonic() < deadline:
        time.sleep(0.05)
    if not _process_group_exists(process.pid):
        process.wait()
        return
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait(timeout=10)
    deadline = time.monotonic() + 10
    while _process_group_exists(process.pid) and time.monotonic() < deadline:
        time.sleep(0.05)
    if _process_group_exists(process.pid):
        raise RuntimeError(
            f"test-local Ollama process group did not stop: {process.pid}"
        )


def _process_group_exists(process_group_id: int) -> bool:
    """leader 終了後の descendant も含めて process group の残存を調べる。"""
    try:
        os.killpg(process_group_id, 0)
    except ProcessLookupError:
        return False
    return True
