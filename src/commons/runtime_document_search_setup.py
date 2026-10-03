"""固定した検索用コンポーネントを cmoc installation の非追跡領域へ準備する。"""

import hashlib
import json
import math
import os
import shutil
import signal
import subprocess
import tempfile
import time
import urllib.request
from dataclasses import asdict
from importlib import resources
from pathlib import Path
from urllib.parse import quote

from oracle.other.document_search import (
    EMBEDDING_QUERY_TEMPLATE,
    INITIAL_SEARCH_MATERIALS,
    DocumentSearchConfig,
    ModelArtifact,
)

from .runtime_document_search import SearchError, _file_lock, _safe_directory
from .runtime_document_search_worker import (
    NodeSearchWorker,
    _runtime_tree_hash,
    _sha256,
    _verify_lock,
    _verify_vector_dependency,
    materials_directory,
    verification_condition,
    verify_search_materials,
)
from .runtime_git import require_cmoc_ignored


def _download_model(base: Path, artifact: ModelArtifact) -> None:
    """固定 revision の GGUF をサイズと SHA-256 で確認して公開する。"""
    destination = base / artifact.filename
    if destination.is_file() and not destination.is_symlink():
        if (
            destination.stat().st_size == artifact.size_bytes
            and _sha256(destination) == artifact.sha256
        ):
            return
    url = (
        f"https://huggingface.co/{artifact.repository}/resolve/"
        f"{artifact.revision}/{quote(artifact.filename)}"
    )
    descriptor, temporary = tempfile.mkstemp(prefix=f".{artifact.filename}.", dir=base)
    temporary_path = Path(temporary)
    digest = hashlib.sha256()
    size = 0
    try:
        with (
            os.fdopen(descriptor, "wb") as output,
            urllib.request.urlopen(url, timeout=60) as source,
        ):
            while block := source.read(1024 * 1024):
                output.write(block)
                digest.update(block)
                size += len(block)
                if size > artifact.size_bytes:
                    raise ValueError("downloaded model exceeds fixed size")
            output.flush()
            os.fsync(output.fileno())
        if size != artifact.size_bytes or digest.hexdigest() != artifact.sha256:
            raise ValueError(f"model checksum mismatch: {artifact.filename}")
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def _copy_worker_source(base: Path, filename: str) -> str:
    """package に固定した worker file を配置し hash を返す。"""
    source = resources.files("commons.document_search_worker").joinpath(filename)
    with resources.as_file(source) as path:
        digest = _sha256(path)
        target = base / filename
        if not target.is_file() or target.is_symlink() or _sha256(target) != digest:
            shutil.copyfile(path, target)
        return digest


def _runtime_versions(base: Path) -> None:
    """Node と sqlite-vec を固定版として確認する。"""
    node = (
        subprocess.run(
            ["node", "--version"], check=True, capture_output=True, text=True, timeout=5
        )
        .stdout.strip()
        .removeprefix("v")
    )
    if node != INITIAL_SEARCH_MATERIALS.node_version:
        raise ValueError("Node version does not match fixed materials")
    _verify_vector_dependency()
    package = json.loads(
        (base / "node_modules/node-llama-cpp/package.json").read_text(encoding="utf-8")
    )
    if package.get("version") != INITIAL_SEARCH_MATERIALS.node_llama_cpp_version:
        raise ValueError("node-llama-cpp version does not match fixed materials")
    _verify_lock(base)


def _install_node_runtime(base: Path, materials_fd: int) -> None:
    """npm とその子 process を収束させてから資材 lock を解放できるようにする。"""
    command = [
        "npm",
        "ci",
        "--ignore-scripts",
        "--include=optional",
        "--no-audit",
        "--no-fund",
    ]
    process = subprocess.Popen(
        command,
        cwd=base,
        env={**os.environ, "npm_config_cache": str(base.parent / "npm-cache")},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
        pass_fds=(materials_fd,),
    )
    try:
        stdout, stderr = process.communicate(timeout=7200)
    except BaseException:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.communicate()
        raise
    if process.returncode != 0:
        raise subprocess.CalledProcessError(
            process.returncode, command, output=stdout, stderr=stderr
        )


def _valid_vector(value: object) -> bool:
    """実モデルが返した固定次元の有限・非ゼロ embedding を確認する。"""
    return (
        isinstance(value, list)
        and len(value) == INITIAL_SEARCH_MATERIALS.embedding_dimensions
        and all(type(item) in (int, float) and math.isfinite(item) for item in value)
        and any(value)
    )


def _compatibility_probe(base: Path, root: Path, config: DocumentSearchConfig) -> None:
    """通常検索と同じ worker・設定で文書と query の embedding を検証する。"""
    worker = NodeSearchWorker(root, config, material_base=base)
    query = "日本語の検索"
    document = "関連する日本語の文書です。"
    settings = asdict(config)
    residency = base.parent / "residency/model.lock"
    with _file_lock(residency, time.monotonic() + config.startup_timeout_seconds) as fd:
        cases: tuple[tuple[str, dict[str, object]], ...] = (
            ("chunk_embed", {"documents": {"probe.md": document}, "config": settings}),
            (
                "embed_query",
                {
                    "text": EMBEDDING_QUERY_TEMPLATE.format(query=query),
                    "config": settings,
                },
            ),
        )
        for operation, payload in cases:
            try:
                value = worker.run(
                    operation,
                    payload,
                    deadline=time.monotonic() + config.request_timeout_seconds,
                    residency_fd=fd,
                )
            except SearchError as exc:
                raise SearchError(
                    exc.code, f"{operation} real-model validation failed: {exc}"
                ) from exc
            if operation == "chunk_embed":
                chunks = value.get("probe.md") if isinstance(value, dict) else None
                valid = (
                    isinstance(chunks, list)
                    and bool(chunks)
                    and all(
                        isinstance(chunk, dict)
                        and type(chunk.get("start")) is int
                        and type(chunk.get("end")) is int
                        and 0 <= chunk["start"] < chunk["end"] <= len(document)
                        and _valid_vector(chunk.get("embedding"))
                        for chunk in chunks
                    )
                )
            else:
                valid = _valid_vector(value)
            if not valid:
                raise ValueError(f"real-model validation returned invalid {operation}")


def _material_lock(root: Path) -> Path:
    """検索と doctor が共有する資材切替 lock。"""
    return materials_directory(root).parent / "materials.lock"


def require_document_search_materials(root: Path, config: DocumentSearchConfig) -> Path:
    """通常起動では資材を変えず、現在の条件に対応する検証記録だけを受理する。"""
    require_cmoc_ignored(root)
    with _file_lock(
        _material_lock(root),
        time.monotonic() + config.startup_timeout_seconds,
        shared=True,
    ):
        return verify_search_materials(root, config)


def _write_manifest(base: Path, manifest: dict[str, object]) -> None:
    """検証完了の記録だけを原子的に公開する。"""
    descriptor, temporary = tempfile.mkstemp(prefix=".manifest-", dir=base)
    path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            json.dump(manifest, output, sort_keys=True)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(path, base / "manifest.json")
    finally:
        path.unlink(missing_ok=True)


def _manifest(
    base: Path, hashes: dict[str, str], config: DocumentSearchConfig
) -> dict[str, object]:
    """固定 identity と実モデル検証条件を記録する。"""
    return {
        "worker_sha256": hashes["worker.mjs"],
        "package_sha256": hashes["package.json"],
        "lock_sha256": hashes["package-lock.json"],
        "runtime_tree_sha256": _runtime_tree_hash(base),
        "materials": {
            "node_version": INITIAL_SEARCH_MATERIALS.node_version,
            "node_llama_cpp_version": INITIAL_SEARCH_MATERIALS.node_llama_cpp_version,
            "llama_cpp_revision": INITIAL_SEARCH_MATERIALS.llama_cpp_revision,
            "sqlite_vec_version": INITIAL_SEARCH_MATERIALS.sqlite_vec_version,
            "embedding_sha256": INITIAL_SEARCH_MATERIALS.embedding.sha256,
            "embedding_tokenizer_sha256": INITIAL_SEARCH_MATERIALS.embedding.tokenizer_metadata_sha256,
            "embedding_pooling": INITIAL_SEARCH_MATERIALS.embedding.pooling,
            "embedding_dimensions": INITIAL_SEARCH_MATERIALS.embedding_dimensions,
        },
        "verified_conditions": {
            verification_condition(config): "document-query-embedding"
        },
    }


def _reuse_or_download(base: Path, staging: Path, artifact: ModelArtifact) -> str:
    """既存モデルが正しければ再利用し、不一致だけ固定 revision から取得する。"""
    source = base / artifact.filename
    if (
        source.is_file()
        and not source.is_symlink()
        and source.stat().st_size == artifact.size_bytes
        and _sha256(source) == artifact.sha256
    ):
        try:
            os.link(source, staging / artifact.filename)
        except OSError:
            shutil.copyfile(source, staging / artifact.filename)
        return "reused"
    _download_model(staging, artifact)
    return "downloaded"


def _recover_previous_materials(base: Path) -> bool:
    """切替途中の異常終了で退避した資材を次回 doctor で再照合する。"""
    if base.exists():
        return False
    previous = sorted(
        (
            path
            for path in base.parent.glob(".previous-*")
            if path.is_dir() and not path.is_symlink()
        ),
        key=lambda path: path.stat().st_mtime_ns,
        reverse=True,
    )
    if not previous:
        return False
    os.replace(previous[0], base)
    return True


def _discard_incomplete_staging(base: Path) -> None:
    """前回の準備で公開されなかった中間 directory だけを回収する。"""
    for staging in base.parent.glob(".building-*"):
        if staging.is_symlink():
            raise ValueError(f"staging path is a symlink: {staging}")
        if staging.is_dir():
            shutil.rmtree(staging)


def prepare_document_search_materials(
    root: Path, config: DocumentSearchConfig
) -> dict[str, str]:
    """正常資材を再利用し、不一致時だけ隔離領域で再構築して切り替える。"""
    require_cmoc_ignored(root)
    base = materials_directory(root)
    _safe_directory(base.parent)
    with _file_lock(_material_lock(root), time.monotonic() + 7200) as materials_fd:
        if base.is_symlink():
            raise ValueError(f"material directory is a symlink: {base}")
        _discard_incomplete_staging(base)
        recovered = _recover_previous_materials(base)
        try:
            verify_search_materials(root)
        except SearchError:
            reusable = False
        else:
            reusable = True
        if reusable:
            manifest = json.loads((base / "manifest.json").read_text(encoding="utf-8"))
            verified = manifest.get("verified_conditions")
            condition = verification_condition(config)
            if (
                not isinstance(verified, dict)
                or verified.get(condition) != "document-query-embedding"
            ):
                _compatibility_probe(base, root, config)
                manifest["verified_conditions"] = {
                    **(verified if isinstance(verified, dict) else {}),
                    condition: "document-query-embedding",
                }
                _write_manifest(base, manifest)
                status = "validated"
            else:
                status = "recovered" if recovered else "reused"
            verify_search_materials(root, config)
            return {"status": status, "path": str(base), "models": "reused"}

        staging = Path(tempfile.mkdtemp(prefix=".building-", dir=base.parent))
        backup: Path | None = None
        published = False
        phase = "worker and lock placement"
        try:
            hashes = {
                name: _copy_worker_source(staging, name)
                for name in ("worker.mjs", "package.json", "package-lock.json")
            }
            phase = "npm runtime build"
            _install_node_runtime(staging, materials_fd)
            phase = "runtime and vector dependency check"
            _runtime_versions(staging)
            phase = "model download and checksum check"
            model_action = _reuse_or_download(
                base, staging, INITIAL_SEARCH_MATERIALS.embedding
            )
            phase = "real-model embedding validation"
            _compatibility_probe(staging, root, config)
            phase = "verified material publication"
            _write_manifest(staging, _manifest(staging, hashes, config))
            if base.exists():
                backup = Path(tempfile.mkdtemp(prefix=".previous-", dir=base.parent))
                backup.rmdir()
                os.replace(base, backup)
            os.replace(staging, base)
            published = True
            verify_search_materials(root, config)
            return {
                "status": "repaired" if backup else "built",
                "path": str(base),
                "models": model_action,
            }
        except BaseException as exc:
            if published:
                if base.is_dir():
                    shutil.rmtree(base)
                else:
                    base.unlink()
            if backup is not None and backup.exists():
                os.replace(backup, base)
                backup = None
            if isinstance(
                exc, (SearchError, OSError, ValueError, subprocess.SubprocessError)
            ):
                raise ValueError(f"{phase}: {exc}") from exc
            raise
        finally:
            if staging.exists():
                shutil.rmtree(staging)
            if backup is not None and backup.exists():
                if backup.is_dir():
                    shutil.rmtree(backup)
                else:
                    backup.unlink()
