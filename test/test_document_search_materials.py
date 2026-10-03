"""共有検索用コンポーネントの準備と通常起動での検証記録を小さな固定資材で検査する。

正本仕様: {{work-root}}/oracle/doc/app_spec/document_search.md の「検索用コンポーネントの検証契約」。
"""

import hashlib
import json
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from oracle.other.document_search import (
    EMBEDDING_QUERY_TEMPLATE,
    DocumentSearchConfig,
)

import commons.runtime_document_search_setup as setup
import commons.runtime_document_search_worker as worker
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
    return contents


def _installed_runtime(base: Path) -> None:
    """lock が要求する CPU native と本体の最小配置を作る。"""
    native = base / "node_modules/@node-llama-cpp/linux-x64"
    native.mkdir(parents=True)
    (native / "binding.node").write_bytes(b"fixed native")
    package = base / "node_modules/node-llama-cpp/package.json"
    package.parent.mkdir(parents=True)
    package.write_text(json.dumps({"version": "3.20.0"}))


def test_doctor_reuses_valid_materials_and_requires_current_validation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    small_materials: dict[str, bytes],
) -> None:
    """初回構築、同条件での再利用、変更後の未検証拒否を確認する。"""
    config = DocumentSearchConfig()
    npm_calls: list[Path] = []

    def fake_version(_args: list[str], **_kwargs: Any) -> SimpleNamespace:
        return SimpleNamespace(stdout="v22.23.2")

    def fake_install(base: Path, _fd: int) -> None:
        npm_calls.append(base)
        _installed_runtime(base)

    def fake_download(base: Path, artifact: object) -> None:
        name = getattr(artifact, "filename")
        assert name == setup.SEARCH_MATERIALS.embedding.filename
        (base / name).write_bytes(small_materials["embedding"])

    probes: list[DocumentSearchConfig] = []
    monkeypatch.setattr(setup, "_install_node_runtime", fake_install)
    monkeypatch.setattr(worker.subprocess, "run", fake_version)
    monkeypatch.setattr(setup, "_runtime_versions", lambda _base: None)
    monkeypatch.setattr(setup, "_download_model", fake_download)
    monkeypatch.setattr(
        setup,
        "_compatibility_probe",
        lambda _base, _root, tuning: probes.append(tuning),
    )
    first = setup.prepare_document_search_materials(tmp_path, config)
    assert first["status"] == "built"
    assert len(npm_calls) == 1
    assert probes == [config]
    assert setup.require_document_search_materials(tmp_path, config).is_dir()

    second = setup.prepare_document_search_materials(tmp_path, config)
    assert second["status"] == "reused"
    assert len(npm_calls) == 1
    assert probes == [config]

    base = setup.materials_directory(tmp_path)
    previous = base.parent / ".previous-interrupted"
    base.rename(previous)
    recovered = setup.prepare_document_search_materials(tmp_path, config)
    assert recovered["status"] == "recovered"
    assert len(npm_calls) == 1
    assert not previous.exists()

    changed = replace(config, threads=config.threads + 1)
    with pytest.raises(SearchError, match="real-model validation is missing"):
        setup.require_document_search_materials(tmp_path, changed)
    validated = setup.prepare_document_search_materials(tmp_path, changed)
    assert validated["status"] == "validated"
    assert probes == [config, changed]
    assert len(npm_calls) == 1

    with monkeypatch.context() as changed_input:
        changed_input.setattr(
            worker, "EMBEDDING_QUERY_TEMPLATE", "Changed query format: {query}"
        )
        with pytest.raises(SearchError, match="real-model validation is missing"):
            setup.require_document_search_materials(tmp_path, config)

    model = (
        setup.materials_directory(tmp_path) / setup.SEARCH_MATERIALS.embedding.filename
    )
    model.write_bytes(b"corrupted")
    with pytest.raises(SearchError, match="model checksum mismatch"):
        setup.require_document_search_materials(tmp_path, config)
    repaired = setup.prepare_document_search_materials(tmp_path, config)
    assert repaired["status"] == "repaired"
    assert len(npm_calls) == 2
    assert setup.require_document_search_materials(tmp_path, config).is_dir()


def test_failed_real_model_probe_never_publishes_materials(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    small_materials: dict[str, bytes],
) -> None:
    """推論検証に失敗した隔離 build を次回起動で準備済みと扱わない。"""

    def fake_version(_args: list[str], **_kwargs: Any) -> SimpleNamespace:
        return SimpleNamespace(stdout="v22.23.2")

    def fake_download(base: Path, artifact: object) -> None:
        name = getattr(artifact, "filename")
        assert name == setup.SEARCH_MATERIALS.embedding.filename
        (base / name).write_bytes(small_materials["embedding"])

    monkeypatch.setattr(
        setup, "_install_node_runtime", lambda base, _fd: _installed_runtime(base)
    )
    monkeypatch.setattr(worker.subprocess, "run", fake_version)
    monkeypatch.setattr(setup, "_runtime_versions", lambda _base: None)
    monkeypatch.setattr(setup, "_download_model", fake_download)
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


@pytest.mark.parametrize("operation", ["chunk_embed", "embed_query"])
@pytest.mark.parametrize(
    "bad_vector",
    [
        [],
        [0.0] * SEARCH_MATERIALS.embedding_dimensions,
        [float("nan")] * SEARCH_MATERIALS.embedding_dimensions,
    ],
)
def test_probe_uses_search_inputs_and_rejects_invalid_embedding(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    operation: str,
    bad_vector: list[float],
) -> None:
    """doctor 検証が通常検索と同じ文書/query 入力を通し、不正 embedding を拒否する。"""
    config = DocumentSearchConfig()
    calls: list[tuple[str, dict[str, object]]] = []
    vector = [1.0] + [0.0] * (SEARCH_MATERIALS.embedding_dimensions - 1)

    def fake_run(
        _worker: worker.NodeSearchWorker,
        operation: str,
        payload: dict[str, object],
        **_kwargs: object,
    ) -> object:
        calls.append((operation, payload))
        if operation == "chunk_embed":
            document = payload["documents"]["probe.md"]
            return {
                "probe.md": [{"start": 0, "end": len(document), "embedding": vector}]
            }
        assert operation == "embed_query"
        return vector

    monkeypatch.setattr(worker.NodeSearchWorker, "run", fake_run)
    setup._compatibility_probe(tmp_path / "staging", tmp_path, config)
    assert [operation for operation, _payload in calls] == [
        "chunk_embed",
        "embed_query",
    ]
    assert calls[1][1]["text"] == EMBEDDING_QUERY_TEMPLATE.format(query="日本語の検索")

    def invalid_embedding(
        _worker: worker.NodeSearchWorker,
        current_operation: str,
        payload: dict[str, object],
        **kwargs: object,
    ) -> object:
        result = fake_run(_worker, current_operation, payload, **kwargs)
        if current_operation == operation:
            if operation == "chunk_embed":
                result["probe.md"][0]["embedding"] = bad_vector
            else:
                result = bad_vector
        return result

    monkeypatch.setattr(worker.NodeSearchWorker, "run", invalid_embedding)
    with pytest.raises(ValueError, match=f"invalid {operation}"):
        setup._compatibility_probe(tmp_path / "staging", tmp_path, config)
