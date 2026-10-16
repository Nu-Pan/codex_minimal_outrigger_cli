"""共有検索用コンポーネントの準備と通常起動での検証記録を小さな固定資材で検査する。

正本仕様: {{work-root}}/oracle/doc/app_spec/document_search.md の「検索用コンポーネントの検証契約」。
"""

import hashlib
import io
import json
import shutil
import urllib.request
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from oracle.other.cmoc_config import DocumentSearchConfig
from oracle.other.document_search import EMBEDDING_QUERY_TEMPLATE

import commons.runtime_document_search_setup as setup
import commons.runtime_document_search_worker as worker
import commons.runtime_download_asset_cache as cache_module
from commons.runtime_document_search import SearchError
from commons.runtime_document_search_types import SEARCH_MATERIALS


@pytest.fixture
def small_materials(monkeypatch: pytest.MonkeyPatch) -> dict[str, bytes]:
    """実モデルを取得せず checksum と固定 identity の境界を保つ。"""
    contents = {"embedding": b"embedding model"}
    materials = replace(
        SEARCH_MATERIALS,
        embedding=replace(
            SEARCH_MATERIALS.embedding,
            size_bytes=len(contents["embedding"]),
            sha256=hashlib.sha256(contents["embedding"]).hexdigest(),
        ),
    )
    monkeypatch.setattr(setup, "SEARCH_MATERIALS", materials)
    monkeypatch.setattr(worker, "SEARCH_MATERIALS", materials)
    monkeypatch.setattr(setup, "require_cmoc_ignored", lambda _root: None)
    monkeypatch.setattr(setup, "prepare_node_runtime", lambda *_args: None)

    # 通信経路は test_download_asset_cache.py で検査し、ここでは TLS 初期化も省く。
    def fake_opener(*_handlers: object) -> SimpleNamespace:
        return SimpleNamespace(
            open=lambda *_args, **_kwargs: io.BytesIO(contents["embedding"])
        )

    monkeypatch.setattr(urllib.request, "build_opener", fake_opener)
    return contents


def _installed_native_metadata(base: Path) -> Path:
    """revision 照合に必要な native directory と採用情報だけを配置する。"""
    metadata = (
        base
        / "node_modules/@node-llama-cpp/linux-x64/bins/linux-x64/_nlcBuildMetadata.json"
    )
    metadata.parent.mkdir(parents=True)
    metadata.write_text(
        json.dumps(
            {
                "buildOptions": {
                    "llamaCpp": {
                        "repo": "ggml-org/llama.cpp",
                        "release": SEARCH_MATERIALS.llama_cpp_release,
                    }
                }
            }
        )
    )
    return metadata


def _installed_runtime(base: Path) -> None:
    """資材の lifecycle 検査には CPU native と Node 本体も配置する。"""
    _installed_native_metadata(base)
    (base / "node_modules/@node-llama-cpp/linux-x64/binding.node").write_bytes(
        b"fixed native"
    )
    node = base / "node/bin/node"
    node.parent.mkdir(parents=True)
    node.write_bytes(b"fixed node")
    package = base / "node_modules/node-llama-cpp/package.json"
    package.parent.mkdir(parents=True)
    package.write_text(json.dumps({"version": SEARCH_MATERIALS.node_llama_cpp_version}))


@pytest.mark.parametrize("field", ["repo", "release"])
def test_native_llama_revision_must_match_adoption(tmp_path: Path, field: str) -> None:
    """同じ npm 版でも、付属 native が採用した llama.cpp を使うことを確認する。"""
    setup._copy_worker_source(tmp_path, "package-lock.json")
    path = _installed_native_metadata(tmp_path)
    worker._verify_lock(tmp_path)
    metadata = json.loads(path.read_text())
    metadata["buildOptions"]["llamaCpp"][field] = "different"
    path.write_text(json.dumps(metadata))
    with pytest.raises(ValueError, match="llama.cpp revision mismatch"):
        worker._verify_lock(tmp_path)


def test_doctor_reuses_valid_materials_and_requires_current_validation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    small_materials: dict[str, bytes],
) -> None:
    """初回構築、同条件での再利用、変更後の未検証拒否を確認する。"""
    config = DocumentSearchConfig()
    npm_calls: list[Path] = []
    base = setup.materials_directory(tmp_path)
    model = base / setup.SEARCH_MATERIALS.embedding.filename
    model_reads: list[Path] = []
    sha256 = worker._sha256

    def checksum(path: Path) -> str:
        if path == model:
            model_reads.append(path)
        return sha256(path)

    def fake_version(_args: list[str], **_kwargs: Any) -> SimpleNamespace:
        return SimpleNamespace(stdout="v" + SEARCH_MATERIALS.node_version)

    def fake_install(_root: Path, base: Path, _fd: int) -> None:
        npm_calls.append(base)
        _installed_runtime(base)

    probes: list[DocumentSearchConfig] = []
    monkeypatch.setattr(setup, "_install_node_runtime", fake_install)
    monkeypatch.setattr(worker.subprocess, "run", fake_version)
    monkeypatch.setattr(setup, "_runtime_versions", lambda _base: None)
    monkeypatch.setattr(
        setup,
        "_compatibility_probe",
        lambda _base, _root, tuning: probes.append(tuning),
    )
    monkeypatch.setattr(worker, "_sha256", checksum)
    first = setup.prepare_document_search_materials(tmp_path, config)
    assert first["status"] == "built"
    assert len(npm_calls) == 1
    assert probes == [config]
    assert setup.require_document_search_materials(tmp_path, config).is_dir()

    model_reads.clear()
    second = setup.prepare_document_search_materials(tmp_path, config)
    assert second["status"] == "reused"
    assert len(npm_calls) == 1
    assert probes == [config]
    # 変更のない再利用では、大容量モデルの checksum を一度だけ読む。
    assert len(model_reads) == 1

    # 導入前の component と、cache 回収後の通常起動・doctor を共に維持する。
    shutil.rmtree(cache_module.asset_cache_directory())
    assert setup.require_document_search_materials(tmp_path, config).is_dir()
    assert (
        setup.prepare_document_search_materials(tmp_path, config)["status"] == "reused"
    )
    assert not cache_module.asset_cache_directory().exists()

    previous = base.parent / ".previous-interrupted"
    base.rename(previous)
    recovered = setup.prepare_document_search_materials(tmp_path, config)
    assert recovered["status"] == "recovered"
    assert len(npm_calls) == 1
    assert not previous.exists()

    changed = replace(config, threads=config.threads + 1)
    with pytest.raises(SearchError, match="real-model validation is missing"):
        setup.require_document_search_materials(tmp_path, changed)
    model_reads.clear()
    validated = setup.prepare_document_search_materials(tmp_path, changed)
    assert validated["status"] == "validated"
    assert probes == [config, changed]
    assert len(npm_calls) == 1
    # 実モデルを動かした後の再検査は保ち、probe による資材変更も検出する。
    assert len(model_reads) == 2

    with monkeypatch.context() as changed_input:
        changed_input.setattr(
            worker, "EMBEDDING_QUERY_TEMPLATE", "Changed query format: {query}"
        )
        with pytest.raises(SearchError, match="real-model validation is missing"):
            setup.require_document_search_materials(tmp_path, config)

    model.write_bytes(b"corrupted")
    with pytest.raises(SearchError, match="model checksum mismatch"):
        setup.require_document_search_materials(tmp_path, config)
    repaired = setup.prepare_document_search_materials(tmp_path, config)
    assert repaired["status"] == "repaired"
    assert len(npm_calls) == 1
    assert setup.require_document_search_materials(tmp_path, config).is_dir()

    # runtime 自体の破損時は再構築し、正常モデルの取得を省く。
    (base / "node_modules/@node-llama-cpp/linux-x64/binding.node").write_bytes(
        b"bad runtime"
    )
    repaired = setup.prepare_document_search_materials(tmp_path, config)
    assert repaired["models"] == "reused"
    assert len(npm_calls) == 2

    # 現在の条件への検証失敗は、別条件で正常な既存 component を壊さない。
    monkeypatch.setattr(
        setup,
        "_compatibility_probe",
        lambda *_args: (_ for _ in ()).throw(ValueError("probe failed")),
    )
    with pytest.raises(ValueError, match="probe failed"):
        setup.prepare_document_search_materials(tmp_path, changed)
    assert setup.require_document_search_materials(tmp_path, config).is_dir()


def test_failed_real_model_probe_never_publishes_materials(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    small_materials: dict[str, bytes],
) -> None:
    """推論検証に失敗した隔離 build を次回起動で準備済みと扱わない。"""
    # probe 失敗後は資材内容の検査に進まないため、runtime/model を作らない。
    # 正常構築と資材検査は上の lifecycle test に残し、ここでは隔離 build の失敗を通す。
    monkeypatch.setattr(
        setup,
        "_install_node_runtime",
        lambda _root, _base, _fd: None,
    )
    monkeypatch.setattr(
        setup,
        "prepare_model",
        lambda _root, _base, _staging, _artifact: "downloaded",
    )
    monkeypatch.setattr(setup, "_runtime_versions", lambda _base: None)
    monkeypatch.setattr(
        setup,
        "_compatibility_probe",
        lambda *_args: (_ for _ in ()).throw(ValueError("embedding probe failed")),
    )

    with pytest.raises(ValueError, match="embedding probe failed"):
        setup.prepare_document_search_materials(tmp_path, DocumentSearchConfig())
    assert not setup.materials_directory(tmp_path).exists()
    with pytest.raises(SearchError) as exc_info:
        setup.require_document_search_materials(tmp_path, DocumentSearchConfig())
    assert exc_info.value.code == "NOT_READY"


@pytest.mark.parametrize(
    ("operation", "bad_vector"),
    [(None, None)]
    + [
        (operation, vector)
        for operation in ("chunk_embed", "embed_query")
        for vector in (
            [],
            [0.0] * SEARCH_MATERIALS.embedding_dimensions,
            [float("nan")] * SEARCH_MATERIALS.embedding_dimensions,
        )
    ],
    ids=(
        "valid",
        "document-empty",
        "document-zero",
        "document-nan",
        "query-empty",
        "query-zero",
        "query-nan",
    ),
)
def test_probe_uses_search_inputs_and_rejects_invalid_embedding(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    operation: str | None,
    bad_vector: list[float] | None,
) -> None:
    """doctor 検証が通常検索と同じ文書/query 入力を通し、不正 embedding を拒否する。"""
    config = DocumentSearchConfig()
    calls: list[tuple[str, dict[str, object]]] = []
    vector = [1.0] + [0.0] * (SEARCH_MATERIALS.embedding_dimensions - 1)

    def fake_run(
        _worker: worker.NodeSearchWorker,
        current_operation: str,
        payload: dict[str, object],
        **_kwargs: object,
    ) -> object:
        calls.append((current_operation, payload))
        embedding = bad_vector if current_operation == operation else vector
        if current_operation == "chunk_embed":
            document = payload["documents"]["probe.md"]
            return {
                "probe.md": [{"start": 0, "end": len(document), "embedding": embedding}]
            }
        assert current_operation == "embed_query"
        return embedding

    monkeypatch.setattr(worker.NodeSearchWorker, "run", fake_run)
    if operation is None:
        setup._compatibility_probe(tmp_path / "staging", tmp_path, config)
        assert [name for name, _payload in calls] == ["chunk_embed", "embed_query"]
        assert calls[0][1]["documents"] == {"probe.md": "関連する日本語の文書です。"}
        assert calls[1][1]["text"] == EMBEDDING_QUERY_TEMPLATE.format(
            query="日本語の検索"
        )
    else:
        with pytest.raises(ValueError, match=f"invalid {operation}"):
            setup._compatibility_probe(tmp_path / "staging", tmp_path, config)
