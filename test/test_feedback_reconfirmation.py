"""feedback の根拠変更・再確認・封印と publication artifact の整合性を検証する。

Git・Codex・共通 ID 発行・ディスク同期・pending store 列挙の境界を置き換え、
wave、checkpoint、固定入力と判定根拠の検査には実装を使う。
"""

import copy
import json
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from _acp_builder_support import oracle_schema_path
from _git_support import RUN_BRANCH, SESSION_BRANCH, SESSION_ID
from test_feedback import (
    _assert_hash_verified_state_snapshot,
    _context,
    _fake_result,
    _payload,
    _remediation_output,
)

from cmoc_runtime import CmocError
from commons import runtime_feedback_run_state as run_state
from commons import runtime_feedback_state as feedback_state
from commons import runtime_feedback_store as feedback_store
from commons.runtime_feedback_run_state import (
    selected_remediation_checkpoints,
    validate_decision_basis,
    validate_remediation_checkpoint,
    validate_run_artifacts,
)
from commons.runtime_feedback_state import (
    _validate_report_cut_checkpoint,
    _validate_report_cut_manifest,
    artifact_reference,
    cleanup_published_report,
    load_active_state,
    load_report_cut,
    normalization_checkpoint_path,
    recover_report_cut_checkpoint_references,
    validate_feedback_state,
    write_report_cut_manifest,
)
from commons.runtime_feedback_store import (
    canonical_json_bytes,
    feedback_root,
    observation_path,
    read_json_object,
    rfc3339_now,
    sha256_bytes,
    store_agent_observation,
    write_immutable_json,
)
from commons.runtime_run_join_state import JoinRecord
from commons.runtime_run_lifecycle import EditingRunContext
from sub_commands.feedback import decision, remediation, report


@pytest.fixture
def feedback_run(tmp_path, monkeypatch, feedback_remediation_request_stub):
    # 同期順序・同期失敗時の保存状態は test_feedback_store.py、CLI・collector との結合は
    # test_feedback.py に残す。write・rename・読込と破損検査はここでも実行する。
    monkeypatch.setattr("os.fsync", lambda _fd: None)
    repo, worktree, session = (tmp_path / name for name in ("repo", "run", "session"))
    for directory in (repo, worktree, session):
        directory.mkdir()
    (worktree / "README.md").write_text("subject\n")
    (worktree / "dependency.conf").write_text("old\n")
    context = EditingRunContext(
        repo,
        session,
        SESSION_ID,
        repo / "state.json",
        SESSION_BRANCH,
        "a" * 40,
        "feedback_report",
        RUN_BRANCH,
        "a" * 40,
        worktree,
    )
    # 採番の永続性は test_runtime_ids.py、並行発行は test_codex_runtime_paths.py、
    # feedback との結合は test_feedback.py に残し、ID の対応と artifact の実検査を保つ。
    # 追加 evidence の観測 ID も同じ採番を使う。os.fsync の置換では SQLite の同期は省けない。
    sequences = Counter()

    def allocate_id(root, prefix):
        assert root == repo
        assert prefix in {"fbr", "fbg", "fbc", "fbo", "exec"}
        sequence = sequences[prefix]
        sequences[prefix] += 1
        return f"{prefix}_{sequence:06d}_2026-09-29_15-04"

    for module in (run_state, feedback_state, feedback_store, remediation):
        monkeypatch.setattr(module, "new_id", allocate_id)
    monkeypatch.setattr(
        remediation, "current_execution_id", lambda root: allocate_id(root, "exec")
    )
    state = load_active_state(repo)
    manifest = remediation._new_manifest(context, state)
    manifest["run"]["invocation_log"] = (
        ".cmoc/gu/log/sub_command/exec_000000_2026-09-29_15-04.jsonl"
    )
    invocation_log = repo / manifest["run"]["invocation_log"]
    invocation_log.parent.mkdir(parents=True)
    invocation_log.write_text("")
    path, _ = write_report_cut_manifest(repo, manifest)
    harness = SimpleNamespace(
        context=context,
        state=state,
        manifest=manifest,
        path=path,
        candidates={},
        calls=[],
        head="a" * 40,
        committed={},
        commits=[],
        commit_attempts=[],
        handler=lambda issue: _remediation_output(issue["issue_id"], "not_actionable"),
    )

    def input_paths():
        return [path for path in worktree.iterdir() if path.is_file()]

    def contents():
        return {path.name: path.read_bytes() for path in input_paths()}

    harness.committed = contents()
    # path を返す境界では本文を読まず、根拠収集と差分検査に必要な読み込みだけ残す。
    monkeypatch.setattr(
        decision,
        "enumerate_oracle_and_realization_files",
        lambda root: ([], [root / path.name for path in input_paths()]),
    )

    def changed(*_args, **_kwargs):
        current = contents()
        return sorted(
            name
            for name in current.keys() | harness.committed.keys()
            if current.get(name) != harness.committed.get(name)
        )

    def commit(*_args):
        paths = changed()
        harness.commit_attempts.append(paths)
        if not paths:
            return None
        harness.head = f"{len(harness.commits) + 1:040x}"
        harness.committed = contents()
        harness.commits.append(harness.head)
        return harness.head

    def call(parameter, **_kwargs):
        issue = json.loads(parameter.prompt)
        harness.calls.append(issue)
        return _fake_result(repo, harness.handler(issue))

    monkeypatch.setattr(
        decision,
        "run_git",
        lambda *_args, **_kwargs: SimpleNamespace(
            stdout="\0".join(sorted(path.name for path in input_paths())) + "\0",
            returncode=0,
        ),
    )
    monkeypatch.setattr(
        remediation,
        "run_git",
        lambda *_args, **_kwargs: SimpleNamespace(stdout="", returncode=0),
    )
    monkeypatch.setattr(remediation, "head_commit", lambda _root: harness.head)
    monkeypatch.setattr(remediation, "require_clean_worktree", lambda *_args: None)
    monkeypatch.setattr(remediation, "worktree_change_paths", changed)
    monkeypatch.setattr(remediation, "unexpected_agent_paths", lambda *_args: [])
    monkeypatch.setattr(remediation, "unexpected_run_paths", lambda *_args: [])
    monkeypatch.setattr(remediation, "commit_work_unit", commit)
    monkeypatch.setattr(remediation, "sync_refactor_state", lambda *_args: None)
    monkeypatch.setattr(remediation, "stop_tracked_codex_children", lambda *_args: None)
    monkeypatch.setattr(remediation, "_update_progress", lambda *_args: None)
    monkeypatch.setattr(
        remediation, "doctor_preprocess_for_join", lambda **_kwargs: None
    )
    monkeypatch.setattr(
        remediation, "validate_run_join", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(remediation, "capture_high_watermark", lambda *_args: (0, []))
    # intake は境界値と候補を直接渡すため、wave ごとの store 列挙を重ねない。
    # raw の破損拒否・publication 阻止は test_feedback.py の pending reader と
    # invalid_raw_observation_blocks_publication、実 intake との結合は wave test に残す。
    # 固定した observation の読込・hash・schema 検査と manifest の検証は実行する。
    monkeypatch.setattr(report, "_pending_observations", lambda _root: ([], {}))
    monkeypatch.setattr(
        report, "_build_candidates", lambda *_args, **_kwargs: (harness.candidates, {})
    )
    monkeypatch.setattr(report, "run_codex_exec", call)
    # 共通 join と実 Git の照合は CLI test に任せ、封印時の準備済み境界を渡す。
    record = JoinRecord(context, harness.head)
    harness.join = record
    monkeypatch.setattr(record, "save", lambda: None)
    original_seal = remediation._seal

    def seal(*args):
        original_seal(*args)
        record.original_run_head = record.prepared_run_head = harness.head
        record.session_head = record.session_commit = harness.head
        record.session_tree = "a" * 40
        record.imported = True
        record.resolution = {
            "agent_status": "not_needed",
            "prepared_feedback_inputs_sha256": decision.state_hash(
                decision.worktree_inputs(worktree)
            ),
            "feedback_cut": harness.manifest["run"]["sealed"],
        }

    monkeypatch.setattr(remediation, "_seal", seal)
    monkeypatch.setattr(remediation, "join_record", lambda *_args: record)
    monkeypatch.setattr(remediation, "load_join_record", lambda *_args: record)
    monkeypatch.setattr(remediation, "confirm_import", lambda item: item.imported)
    return harness


def _add_candidate(harness, letter):
    observation = {
        "source": "agent_report",
        "payload": _payload(),
        "observed_at": rfc3339_now(),
    }
    # a、b の observation ID は issue ID の辞書順も a、b の順になる。
    suffix = str("abcdef".index(letter))
    candidate = report._new_candidate(
        observation, "agent\0fbo_00000" + suffix + "_2026-08-01_00-00"
    )
    identity = candidate["candidate_id"]
    candidate["occurrence_count"] = 1
    harness.candidates[identity] = candidate
    return identity


def _run(harness):
    return remediation._wave_loop(harness.context, harness.manifest, harness.state)


@pytest.mark.parametrize("late_issue", [False, True], ids=["empty", "late-issue"])
def test_empty_wave_collects_basis_only_after_an_issue_arrives(
    feedback_run, monkeypatch, late_issue
):
    h = feedback_run
    collect_inputs = decision.worktree_inputs

    def collect_for_issue(worktree):
        assert h.candidates, "an empty wave has no issue basis to collect"
        return collect_inputs(worktree)

    def prepare_join(**_kwargs):
        if late_issue and not h.candidates:
            _add_candidate(h, "a")

    prepare = Mock(side_effect=prepare_join)
    monkeypatch.setattr(decision, "worktree_inputs", collect_for_issue)
    monkeypatch.setattr(remediation, "doctor_preprocess_for_join", prepare)

    candidates, aggregates = _run(h)

    assert candidates == h.candidates
    assert aggregates == {}
    assert len(h.calls) == int(late_issue)
    assert prepare.call_count == (2 if late_issue else 1)
    manifest, _ = load_report_cut(h.context.repo)
    assert len(manifest["run"]["waves"]) == (2 if late_issue else 1)
    first_wave = run_state.read_run_artifact(
        h.context.repo, manifest["run"]["waves"][0]
    )
    assert first_wave["candidates"] == {}


def test_run_artifact_reader_uses_one_snapshot(tmp_path, monkeypatch):
    """hash を確認した byte 列を返し、次の呼出しでは変更を再検査する。"""
    path = tmp_path / ".cmoc/gu/feedback/work/cut/record.json"
    value = {"report_cut_id": "cut"}
    write_immutable_json(path, value)
    reference = artifact_reference(tmp_path, path)
    reads = []
    original_read = Path.read_bytes

    def changing_read(target):
        content = original_read(target)
        if target == path:
            reads.append(target)
            if len(reads) == 1:
                target.write_bytes(canonical_json_bytes({"changed": True}))
        return content

    monkeypatch.setattr(Path, "read_bytes", changing_read)

    assert run_state.read_run_artifact(tmp_path, reference) == value
    assert reads == [path]
    with pytest.raises(CmocError, match="SHA256"):
        run_state.read_run_artifact(tmp_path, reference)
    assert reads == [path, path]


def test_run_artifact_validation_reads_once_and_checks_cleanup(
    feedback_run, monkeypatch
):
    """wave と join 記録を一度ずつ読み、cleanup の欠落後も現存 hash を検査する。"""
    h = feedback_run
    for sequence in (1, 2):
        wave_path = h.path.parent / "wave" / str(sequence) / "input.json"
        write_immutable_json(
            wave_path,
            {
                "sequence": sequence,
                "after": sequence - 1,
                "high_watermark": sequence,
                "inputs": {},
                "candidates": {},
            },
        )
        h.manifest["run"]["waves"].append(artifact_reference(h.context.repo, wave_path))
    h.manifest["run"]["high_watermark"] = 2
    remediation._seal(h.context, h.manifest, {}, {})
    for source in h.context.run_worktree.iterdir():
        (h.context.session_worktree / source.name).write_bytes(source.read_bytes())
    monkeypatch.setattr(remediation, "_is_ancestor", lambda *_args: True)
    monkeypatch.setattr(remediation, "tree_changes", lambda *_args: [])
    remediation._record_merge(h.context, h.manifest, None)
    remediation._complete_join(h.context, h.manifest)
    paths = {
        h.context.repo / item["path"]
        for item in run_state.run_artifact_references(h.manifest)
    }
    reads = Counter()
    original_read = Path.read_bytes

    def counted_read(path):
        if path in paths:
            reads[path] += 1
        return original_read(path)

    monkeypatch.setattr(Path, "read_bytes", counted_read)

    def validate(allow_missing):
        validate_run_artifacts(
            h.context.repo, h.manifest, h.path, allow_missing=allow_missing
        )

    for allow_missing in (False, True):
        reads.clear()
        validate(allow_missing)
        assert reads == {path: 1 for path in paths}
    first, second = (
        h.context.repo / item["path"] for item in h.manifest["run"]["waves"]
    )
    second_content = original_read(second)
    second.write_bytes(canonical_json_bytes({"changed": True}))
    with pytest.raises(CmocError, match="SHA256"):
        validate(False)
    second.write_bytes(second_content)
    first.unlink()
    with pytest.raises(CmocError, match="通常 file"):
        validate(False)
    validate(True)
    second.write_bytes(canonical_json_bytes({"changed": True}))
    with pytest.raises(CmocError, match="SHA256"):
        validate(True)
    second.unlink()
    validate(True)
    sealed = h.context.repo / h.manifest["run"]["sealed"]["path"]
    sealed.write_bytes(canonical_json_bytes({"changed": True}))
    with pytest.raises(CmocError, match="SHA256"):
        validate(True)
    sealed.unlink()
    validate(True)


def test_run_artifacts_reject_noncontiguous_wave_boundaries(feedback_run):
    """wave は直前の durable high-watermark から連続していなければならない。"""
    harness = feedback_run
    for sequence, (after, high_watermark) in enumerate(((0, 1), (2, 3)), 1):
        wave_path = harness.path.parent / "wave" / str(sequence) / "input.json"
        write_immutable_json(
            wave_path,
            {
                "sequence": sequence,
                "after": after,
                "high_watermark": high_watermark,
                "inputs": {},
                "candidates": {},
            },
        )
        harness.manifest["run"]["waves"].append(
            artifact_reference(harness.context.repo, wave_path)
        )
    harness.manifest["run"]["high_watermark"] = 3

    with pytest.raises(CmocError, match="high-watermark"):
        validate_run_artifacts(
            harness.context.repo,
            harness.manifest,
            harness.path,
            allow_missing=False,
        )


def test_report_cut_rejects_duplicate_observation_entries(feedback_run):
    """同じ raw observation を report cut の処理対象へ二重計上しない。"""
    harness = feedback_run
    observed_at = rfc3339_now()
    observation_id = "fbo_000001_2026-08-01_00-00"
    raw_path = observation_path(harness.context.repo, observation_id, observed_at)
    write_immutable_json(
        raw_path, {"observation_id": observation_id, "observed_at": observed_at}
    )
    entry = {
        "observation_id": observation_id,
        **artifact_reference(harness.context.repo, raw_path),
    }
    harness.manifest["inputs"]["observations"] = [entry, entry.copy()]

    with pytest.raises(CmocError, match="重複"):
        _validate_report_cut_manifest(
            harness.context.repo, harness.manifest, harness.path
        )


@pytest.fixture
def report_cut_inputs(feedback_run):
    # Git や CLI を起動せず、正式な remediation checkpoint の保存経路を使う。
    h = feedback_run
    _add_candidate(h, "a")
    _run(h)
    repo = h.context.repo
    observation_id = "fbo_000001_2026-08-01_00-00"
    observed_at = "2026-08-01T00:00:00Z"
    raw = observation_path(repo, observation_id, observed_at)
    write_immutable_json(
        raw, {"observation_id": observation_id, "observed_at": observed_at}
    )
    h.manifest["inputs"]["observations"] = [
        {"observation_id": observation_id, **artifact_reference(repo, raw)}
    ]
    normalization = normalization_checkpoint_path(
        repo, h.manifest["report_cut_id"], observation_id
    )
    output = {"result": {"decision": "new", "existing_issue_id": None}}
    write_immutable_json(
        normalization,
        {
            "schema_version": 1,
            "kind": "normalization",
            "report_cut_id": h.manifest["report_cut_id"],
            "candidate_id": observation_id,
            "input_sha256": "0" * 64,
            "builder_sha256": "1" * 64,
            "schema_sha256": "2" * 64,
            "structured_output": output,
            "output_sha256": sha256_bytes(canonical_json_bytes(output)),
        },
    )
    h.manifest["processing"]["normalization_checkpoints"] = [
        {"observation_id": observation_id, **artifact_reference(repo, normalization)}
    ]
    [remediation_reference] = h.manifest["processing"]["remediation_checkpoints"]
    return h, {
        "observation": raw,
        "normalization": normalization,
        "remediation": repo / remediation_reference["path"],
    }


@pytest.mark.parametrize("read_state", [load_active_state, validate_feedback_state])
def test_unpublished_active_state_uses_one_work_snapshot(
    report_cut_inputs, monkeypatch, read_state
):
    """current がなくても work を一度検証し、次の呼出しでは改変を拒否する。"""
    h, _ = report_cut_inputs
    root = h.context.repo
    write_report_cut_manifest(root, h.manifest)
    original_read = Path.read_bytes
    original_content = original_read(h.path)
    manifest_reads = 0

    def replace_after_read(path):
        nonlocal manifest_reads
        content = original_read(path)
        if path == h.path:
            manifest_reads += 1
            if manifest_reads == 1:
                path.write_bytes(b"{}\n")
        return content

    try:
        with monkeypatch.context() as snapshot_patch:
            snapshot_patch.setattr(Path, "read_bytes", replace_after_read)
            state = read_state(root)
            assert state.current is None
            assert state.issues == state.machine_aggregates == {}
            assert manifest_reads == 1
            with pytest.raises(CmocError):
                read_state(root)
    finally:
        h.path.write_bytes(original_content)

    # current 未作成でも、work の検証だけで未列挙 active artifact を許容しない。
    unknown = feedback_root(root) / "active" / "unknown.json"
    unknown.parent.mkdir(parents=True)
    unknown.write_bytes(b"{}\n")
    with pytest.raises(CmocError, match="未定義 artifact"):
        read_state(root)


def test_report_cut_update_skips_unchanged_write_but_rechecks_inputs(
    report_cut_inputs, monkeypatch
):
    """同一内容では保存を省き、実際の更新と参照の破損検出は維持する。"""
    h, paths = report_cut_inputs
    reference = write_report_cut_manifest(h.context.repo, h.manifest)
    original_content = h.path.read_bytes()
    write = Mock(wraps=feedback_state._atomic_write_json)
    monkeypatch.setattr(feedback_state, "_atomic_write_json", write)

    assert write_report_cut_manifest(h.context.repo, h.manifest) == reference
    write.assert_not_called()
    assert h.path.read_bytes() == original_content

    h.manifest["processing"].update(status="failed", failure="test interruption")
    path, digest = write_report_cut_manifest(h.context.repo, h.manifest)
    changed_content = path.read_bytes()
    assert changed_content != original_content
    assert digest == sha256_bytes(changed_content)
    assert read_json_object(path) == h.manifest
    assert write.call_count == 1

    # 呼び出し間で検証結果を cache しない。manifest が同一でも raw の破損を拒否する。
    paths["observation"].write_bytes(canonical_json_bytes({"changed": True}))
    write.reset_mock()
    with pytest.raises(CmocError, match="SHA256"):
        write_report_cut_manifest(h.context.repo, h.manifest)
    write.assert_not_called()
    assert h.path.read_bytes() == changed_content


def test_report_cut_manifest_reads_hash_verified_inputs_once(
    report_cut_inputs, monkeypatch
):
    h, paths = report_cut_inputs
    original_read = Path.read_bytes
    reads = Counter()

    def replace_after_read(path):
        content = original_read(path)
        if path in paths.values():
            reads[path] += 1
            if path == replaced and reads[path] == 1:
                path.write_bytes(canonical_json_bytes({"changed": True}))
        return content

    monkeypatch.setattr(Path, "read_bytes", replace_after_read)
    # 同じ wave・checkpoint の準備を共有し、各入力は検査後に元へ戻す。
    for target, replaced in paths.items():
        original_content = original_read(replaced)
        for allow_missing in (False, True):
            reads.clear()
            # hash を確認した同じ byte 列を検証し、後からの置換を混ぜない。
            _validate_report_cut_manifest(
                h.context.repo,
                h.manifest,
                h.path,
                allow_missing_cleanup_targets=allow_missing,
            )
            assert reads == {path: 1 for path in paths.values()}, (
                target,
                allow_missing,
            )
            # 呼出し間の cache は持たず、次の検証では置換による破損を検出する。
            with pytest.raises(CmocError, match="SHA256"):
                _validate_report_cut_manifest(
                    h.context.repo,
                    h.manifest,
                    h.path,
                    allow_missing_cleanup_targets=allow_missing,
                )
            replaced.write_bytes(original_content)


def test_report_cut_manifest_cleanup_relaxes_only_input_existence(report_cut_inputs):
    h, paths = report_cut_inputs

    def validate(allow_missing):
        _validate_report_cut_manifest(
            h.context.repo,
            h.manifest,
            h.path,
            allow_missing_cleanup_targets=allow_missing,
        )

    # 入力の種類で許容条件は変わらないため、正式な保存処理の準備を共有する。
    for path in paths.values():
        original_content = path.read_bytes()
        path.unlink()
        with pytest.raises(CmocError, match="通常 file"):
            validate(False)
        validate(True)

        # 削除済み file の許容を、dangling symlink や directory に広げない。
        path.symlink_to(h.context.repo / "missing-input.json")
        for allow_missing in (False, True):
            with pytest.raises(CmocError, match="symlink"):
                validate(allow_missing)
        path.unlink()
        path.mkdir()
        for allow_missing in (False, True):
            with pytest.raises(CmocError, match="通常 file"):
                validate(allow_missing)
        path.rmdir()

        path.write_bytes(canonical_json_bytes({"changed": True}))
        for allow_missing in (False, True):
            with pytest.raises(CmocError, match="SHA256"):
                validate(allow_missing)

        # 次の入力の検査へ破損を持ち越さず、正常な組へ復旧できたことも確かめる。
        path.write_bytes(original_content)
        validate(False)


def test_normalization_checkpoint_rejects_schema_invalid_output(tmp_path):
    """normalization checkpoint は output hash だけで正式結果にならない。"""
    output = {
        "result": {"decision": "new", "existing_issue_id": None},
        "unexpected": True,
    }
    checkpoint = {
        "schema_version": 1,
        "kind": "normalization",
        "report_cut_id": "fbc_00000000-0000-7000-8000-000000000001",
        "candidate_id": "fbo_000001_2026-08-01_00-00",
        "input_sha256": "0" * 64,
        "builder_sha256": "1" * 64,
        "schema_sha256": "2" * 64,
        "structured_output": output,
        "output_sha256": sha256_bytes(canonical_json_bytes(output)),
    }

    with pytest.raises(CmocError, match="schema"):
        _validate_report_cut_checkpoint(
            checkpoint,
            tmp_path / "normalization.json",
            expected_kind="normalization",
            expected_report_cut_id=checkpoint["report_cut_id"],
            expected_candidate_id=checkpoint["candidate_id"],
        )


def test_remediation_checkpoint_rejects_malformed_fields(feedback_run):
    """report cut の検査は専用 validator へ委譲した hash・audit・開始時状態も拒否する。"""
    harness = feedback_run
    _add_candidate(harness, "a")
    _run(harness)
    loaded, _ = load_report_cut(harness.context.repo)
    [reference] = loaded["processing"]["remediation_checkpoints"]
    checkpoint = read_json_object(harness.context.repo / reference["path"])
    path = harness.context.repo / reference["path"]

    def validate(value):
        _validate_report_cut_checkpoint(
            value,
            path,
            expected_kind="remediation",
            expected_report_cut_id=checkpoint["report_cut_id"],
            expected_candidate_id=checkpoint["candidate_id"],
        )

    validate(checkpoint)
    # 同じ正式 checkpoint の準備を共有し、各破損は独立した copy へ加える。
    missing_hash = copy.deepcopy(checkpoint)
    missing_hash.pop("input_sha256")
    invalid_wave = copy.deepcopy(checkpoint)
    invalid_wave["audit"]["wave"] = None
    invalid_output_hash = copy.deepcopy(checkpoint)
    invalid_output_hash["output_sha256"] = "0" * 64
    invalid_input_state = copy.deepcopy(checkpoint)
    input_value = invalid_input_state["input"]
    input_value["decision_state"]["files"] = {"../outside": "0" * 64}
    input_value["issue"]["decision_state_sha256"] = sha256_bytes(
        canonical_json_bytes(input_value["decision_state"])
    )
    invalid_input_state["input_sha256"] = sha256_bytes(
        canonical_json_bytes(input_value)
    )
    invalid_result_state = copy.deepcopy(checkpoint)
    invalid_result_state["audit"]["decision_basis"]["state"]["evidence_sha256"] = None
    for invalid, reason in (
        (missing_hash, "field set"),
        (invalid_wave, "wave"),
        (invalid_output_hash, "output hash"),
        (invalid_input_state, "path"),
        (invalid_result_state, "hash"),
    ):
        with pytest.raises(CmocError, match=reason):
            validate(invalid)


def test_remediation_state_validation_rechecks_schema_and_value(
    feedback_run, tmp_path, monkeypatch, request
):
    """同じ内容の再検証後も、入力・schema の変化と artifact の破損を拒否する。"""
    h = feedback_run
    identity = _add_candidate(h, "a")
    h.handler = lambda _issue: _remediation_output(identity, "human_required")
    _run(h)
    manifest, _ = load_report_cut(h.context.repo)
    [reference] = manifest["processing"]["remediation_checkpoints"]
    path = h.context.repo / reference["path"]
    checkpoint = read_json_object(path)
    schema_directory = tmp_path / "schema"
    schema_directory.mkdir()
    schema_path = schema_directory / "remediate_issue.json"
    schema_text = oracle_schema_path("feedback", "remediate_issue.json").read_text(
        encoding="utf-8"
    )
    original_files = run_state.resources.files
    monkeypatch.setattr(
        run_state.resources,
        "files",
        lambda package: (
            schema_directory
            if package == "oracle.acp_builder.feedback.remediate_issue"
            else original_files(package)
        ),
    )
    run_state._remediation_schema_resource.cache_clear()
    request.addfinalizer(run_state._remediation_schema_resource.cache_clear)

    # wave の生成は一度だけ行い、schema と検査対象を各ケースで初期化する。
    for target in ("checkpoint", "verification", "current_evidence"):
        schema_path.write_text(schema_text, encoding="utf-8")
        if target == "checkpoint":
            value = copy.deepcopy(checkpoint)

            def validate(value):
                validate_remediation_checkpoint(value, path)

        else:
            value = copy.deepcopy(checkpoint["audit"]["decision_basis"])
            value["state_sha256"] = sha256_bytes(
                canonical_json_bytes(value.pop("state"))
            )

            def validate(value):
                validate_decision_basis(value, path, compact=True)

        validate(value)
        validate(value)
        if target == "checkpoint":
            bad_hash = copy.deepcopy(value)
            bad_hash["output_sha256"] = "0" * 64
            with pytest.raises(CmocError, match="output hash"):
                validate(bad_hash)
        for invalid_entries in ([{}], [{"summary": float("nan")}]):
            invalid = copy.deepcopy(value)
            if target == "checkpoint":
                invalid["structured_output"]["result"]["verification"] = invalid_entries
                if invalid_entries == [{}]:
                    invalid["output_sha256"] = sha256_bytes(
                        canonical_json_bytes(invalid["structured_output"])
                    )
            else:
                invalid[target] = invalid_entries
            with pytest.raises(CmocError, match="schema"):
                validate(invalid)
        validate(value)

        schema = json.loads(schema_text)
        if target == "checkpoint":
            schema["properties"]["extra"] = {"type": "null"}
            schema["required"].append("extra")
        elif target == "verification":
            schema["$defs"]["verifications"]["minItems"] = 2
        else:
            schema["$defs"]["current_evidence_optional"]["maxItems"] = 0
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
        with pytest.raises(CmocError, match="schema"):
            validate(value)
        schema_path.write_text(schema_text, encoding="utf-8")
        validate(value)

        schema_path.write_text("{", encoding="utf-8")
        with pytest.raises(json.JSONDecodeError):
            validate(value)
        schema_path.unlink()
        with pytest.raises(FileNotFoundError):
            validate(value)


def _join_and_publish(harness, monkeypatch):
    h = harness
    remediation._seal(h.context, h.manifest, h.candidates, {})
    for source in h.context.run_worktree.iterdir():
        (h.context.session_worktree / source.name).write_bytes(source.read_bytes())
    monkeypatch.setattr(remediation, "_is_ancestor", Mock(return_value=True))
    monkeypatch.setattr(
        report, "current_branch", lambda *_args: h.context.session_branch
    )
    remediation._record_merge(h.context, h.manifest, None)
    remediation._complete_join(h.context, h.manifest)
    return remediation._publish(h.context, h.manifest, h.path, h.state)


@pytest.fixture
def publication_feedback(feedback_run, monkeypatch):
    """正式な checkpoint と publication を、cleanup 前まで一度だけ準備する。"""
    h = feedback_run
    identity = _add_candidate(h, "a")
    h.handler = lambda _issue: _remediation_output(identity, "human_required")
    _run(h)
    result = _join_and_publish(h, monkeypatch)
    assert result.result == "attention"
    return h


def test_later_dependency_change_rechecks_every_result(feedback_run, monkeypatch):
    """全結果分類の再確認を同じ run で検査し、wave と publication の準備を共有する。"""
    h = feedback_run
    git = Mock(wraps=remediation.run_git)
    monkeypatch.setattr(remediation, "run_git", git)
    *prior_issues, repairing_issue = sorted(
        _add_candidate(h, letter) for letter in "abcdef"
    )
    # fixed の修正を最初、依存設定の変更を最後にし、全先行判定を同じ根拠で再確認する。
    statuses = dict(
        zip(
            prior_issues,
            (
                "fixed",
                "already_resolved",
                "not_actionable",
                "human_required",
                "inconclusive",
            ),
            strict=True,
        )
    )

    def call(issue):
        identity = issue["issue_id"]
        if identity == repairing_issue:
            assert issue["reconfirmation"] is None
            (h.context.run_worktree / "dependency.conf").write_text("new\n")
            output = _remediation_output(identity, "fixed")
            output["result"]["changed_paths"] = ["dependency.conf"]
        elif issue["reconfirmation"] is None:
            status = statuses[identity]
            output = _remediation_output(identity, status)
            if status == "fixed":
                (h.context.run_worktree / "README.md").write_text("fixed\n")
                output["result"]["changed_paths"] = ["README.md"]
        else:
            assert (
                issue["reconfirmation"]["previous_result"]["status"]
                == statuses[identity]
            )
            assert issue["reconfirmation"]["changes"]["paths"] == ["dependency.conf"]
            output = _remediation_output(identity, "already_resolved")
        return output

    h.handler = call
    _run(h)
    assert h.commit_attempts == [["README.md"], ["dependency.conf"]]
    assert [item["issue_id"] for item in h.calls] == [
        *prior_issues,
        repairing_issue,
        *prior_issues,
    ]
    assert len(h.manifest["run"]["waves"]) == 2
    assert h.manifest["run"]["high_watermark"] == 0
    loaded, _ = load_report_cut(h.context.repo)
    assert len(loaded["processing"]["remediation_checkpoints"]) == 11
    selected = selected_remediation_checkpoints(loaded)
    assert len(selected) == report._remediation_candidate_count(loaded) == 6
    for reference in selected[:-1]:
        assert reference["path"].endswith(".00000002.json")
        checkpoint = run_state.read_run_artifact(
            h.context.repo, {key: reference[key] for key in ("path", "sha256")}
        )
        audit = checkpoint["audit"]
        assert audit["commit"] is None
        assert audit["before_commit"] == audit["after_commit"] == h.head
        assert audit["changed_paths"] == []
        assert audit["diff_sha256"] == sha256_bytes(b"")
    read_checkpoint = Mock(wraps=remediation.read_run_artifact)
    validate_checkpoint = Mock(wraps=remediation.validate_remediation_checkpoint)
    confirm_import = Mock(wraps=remediation.confirm_import)
    redundant_tree_diff = Mock(side_effect=AssertionError("trees already confirmed"))
    with monkeypatch.context() as audit_patch:
        audit_patch.setattr(remediation, "read_run_artifact", read_checkpoint)
        audit_patch.setattr(
            remediation, "validate_remediation_checkpoint", validate_checkpoint
        )
        audit_patch.setattr(remediation, "confirm_import", confirm_import)
        audit_patch.setattr(remediation, "tree_changes", redundant_tree_diff)
        result = _join_and_publish(h, monkeypatch)
        confirm_import.assert_called_once_with(h.join)
        redundant_tree_diff.assert_not_called()
        # 共通照合が不一致を返す場合は、保存済み結果だけで publication を進めない。
        # 実 tree・親・到達可能性の拒否条件は test_runtime_run_join_state.py で検査する。
        confirm_import.return_value = False
        with pytest.raises(CmocError, match="準備・取り込み記録"):
            remediation._complete_join(h.context, h.manifest)
    # 採用結果は seal・join・publication で各一回読み、join 内では再読しない。
    # 旧判定も含め、全 checkpoint の schema・audit 検査を join に残す。
    selected = selected_remediation_checkpoints(h.manifest)
    selected_paths = {reference["path"] for reference in selected}
    references = h.manifest["processing"]["remediation_checkpoints"]
    reads = Counter(call.args[1]["path"] for call in read_checkpoint.call_args_list)
    validations = Counter(call.args[1] for call in validate_checkpoint.call_args_list)
    for reference in references:
        path = reference["path"]
        assert reads[path] == (3 if path in selected_paths else 1)
        assert validations[h.context.repo / path] == (
            2 if path in selected_paths else 1
        )
    assert result.result == "ok"
    assert load_active_state(h.context.repo).issues == {}
    assert "remediation_issue_count: 6" in result.primary_report.read_text()
    # checkpoint 保存と join 後の監査で、空差分の Git 起動を増やさない。
    audit_diffs = [
        call.args[0] for call in git.call_args_list if "--binary" in call.args[0]
    ]
    assert audit_diffs
    assert all(args[-2] != args[-1] for args in audit_diffs)
    # 同じ commit を使う再確認 checkpoint でも、到達可能性の Git 起動は共有する。
    ancestor = remediation._is_ancestor
    assert Counter(call.args[1] for call in ancestor.call_args_list) == {
        commit: 1 for commit in h.commits
    }
    # 次の検証へ結果を持ち越さず、run HEAD 以外の到達不能な commit も拒否する。
    ancestor.reset_mock()
    ancestor.side_effect = lambda _context, commit: commit != h.commits[0]
    with pytest.raises(CmocError, match="issue commit または net 差分 hash"):
        remediation._complete_join(h.context, h.manifest)
    assert [call.args[1] for call in ancestor.call_args_list] == [
        h.head,
        h.commits[0],
    ]
    ancestor.side_effect = None
    # 次の join 検証では、採用済み結果も旧判定も artifact の改変を再検査する。
    for reference in (selected[0], references[0]):
        path = h.context.repo / reference["path"]
        content = path.read_bytes()
        path.write_bytes(b"{}\n")
        try:
            with pytest.raises(CmocError, match="SHA256"):
                remediation._complete_join(h.context, h.manifest)
        finally:
            path.write_bytes(content)
    # path が同じでも参照 hash が違う場合、検証済み snapshot を流用しない。
    original_hash = selected[0]["sha256"]
    selected[0]["sha256"] = "f" * 64
    try:
        with pytest.raises(CmocError, match="SHA256"):
            remediation._complete_join(h.context, h.manifest)
    finally:
        selected[0]["sha256"] = original_hash


@pytest.mark.parametrize("fault", ["head", "forbidden_path"])
def test_unchanged_issue_still_checks_the_whole_work_unit(
    feedback_run, monkeypatch, fault
):
    """agent 差分が空でも、確定前の HEAD と全差分の検査を省略しない。"""
    h = feedback_run
    _add_candidate(h, "a")
    inspections = 0

    def changed(*_args, **_kwargs):
        nonlocal inspections
        inspections += 1
        if inspections == 1:
            return []
        if fault == "head":
            h.head = "b" * 40
            return []
        return ["AGENTS.md"]

    monkeypatch.setattr(remediation, "worktree_change_paths", changed)
    monkeypatch.setattr(
        remediation,
        "unexpected_run_paths",
        lambda _context, changes: [path for change in changes for path in change.paths],
    )

    with pytest.raises(CmocError, match="想定外差分"):
        _run(h)

    assert inspections == 2
    assert h.commit_attempts == []
    assert h.manifest["processing"]["remediation_checkpoints"] == []


@pytest.mark.parametrize("additional_evidence", [False, True])
def test_intake_rechecks_evidence_but_not_duplicate_counts(
    feedback_run, monkeypatch, additional_evidence
):
    h = feedback_run
    identity = _add_candidate(h, "a")
    candidate = h.candidates[identity]
    candidate["occurrence_count"] = 0
    monkeypatch.setattr(
        "test_feedback.run_git", lambda *_args: SimpleNamespace(stdout=h.head)
    )
    context = _context(h.context.repo)
    _, raw = store_agent_observation(h.context.repo, context, _payload())
    observation = read_json_object(raw)
    first_reference = {
        "observation_id": observation["observation_id"],
        **artifact_reference(h.context.repo, raw),
    }
    report._merge_observation(h.context.repo, candidate, observation)

    captures = 0

    def intake(*_args):
        nonlocal captures
        captures += 1
        if captures == 1:
            return 1, [first_reference]
        if captures == 2:
            payload = copy.deepcopy(observation["payload"])
            if additional_evidence:
                payload["cause"]["description"] = "new diagnostic evidence"
            _, path = store_agent_observation(h.context.repo, context, payload)
            incoming = read_json_object(path)
            report._merge_observation(h.context.repo, candidate, incoming)
            return 2, [
                {
                    "observation_id": incoming["observation_id"],
                    **artifact_reference(h.context.repo, path),
                }
            ]
        return 2, []

    monkeypatch.setattr(remediation, "capture_high_watermark", intake)
    h.handler = lambda _issue: _remediation_output(identity, "human_required")
    _run(h)
    assert len(h.calls) == (2 if additional_evidence else 1)
    assert candidate["occurrence_count"] == 2
    if additional_evidence:
        assert h.calls[-1]["reconfirmation"]["changes"]["evidence_changed"]
        [reference] = h.calls[-1]["evidence_observations"]
        assert reference != first_reference
        assert (
            read_json_object(h.context.repo / reference["path"])["payload"]["cause"][
                "description"
            ]
            == "new diagnostic evidence"
        )


@pytest.mark.parametrize("resolution", ["inconclusive", "new_repair"])
def test_repeated_repair_cycle_stops_or_accepts_a_new_repair(
    feedback_run, monkeypatch, resolution
):
    h = feedback_run
    first, second = (_add_candidate(h, letter) for letter in ("a", "b"))
    history_reads = []
    read_artifact = decision.read_run_artifact

    def read_history(repo, reference):
        history_reads.append((len(h.calls), reference["path"]))
        return read_artifact(repo, reference)

    monkeypatch.setattr(decision, "read_run_artifact", read_history)

    def call(issue):
        recheck = issue["reconfirmation"]
        if (h.context.run_worktree / "dependency.conf").read_text() == "stable\n":
            return _remediation_output(issue["issue_id"], "already_resolved")
        if recheck and recheck["cycle_states"]:
            if resolution == "inconclusive":
                output = _remediation_output(issue["issue_id"], "inconclusive")
                output["result"]["reason"] = recheck["cycle_reason"]
            else:
                (h.context.run_worktree / "dependency.conf").write_text("stable\n")
                output = _remediation_output(issue["issue_id"], "fixed")
                output["result"]["changed_paths"] = ["dependency.conf"]
            return output
        (h.context.run_worktree / "dependency.conf").write_text(
            "new\n" if issue["issue_id"] == first else "old\n"
        )
        output = _remediation_output(issue["issue_id"], "fixed")
        output["result"]["changed_paths"] = ["dependency.conf"]
        return output

    h.handler = call
    _run(h)
    # 収束後の照合では、準備前後とも最新だけを読む。再確認には全履歴が必要。
    final_reads = Counter(
        path for call_count, path in history_reads if call_count == len(h.calls)
    )
    assert final_reads == Counter(
        {
            reference["path"]: 2
            for reference in selected_remediation_checkpoints(h.manifest)
        }
    )
    history = decision.issue_history(h.context.repo, h.manifest, first)
    checkpoint = history[-1][1]
    diagnostic = resolution == "inconclusive"
    assert checkpoint["structured_output"]["result"]["status"] == (
        "inconclusive" if diagnostic else "fixed"
    )
    assert [item["issue_id"] for item in h.calls] == [
        first,
        second,
        first,
        second,
        first,
    ] + ([] if diagnostic else [second])
    result = _join_and_publish(h, monkeypatch)
    assert result.result == ("incomplete" if diagnostic else "ok")
    state = load_active_state(h.context.repo)
    assert state.current is not None
    assert (first in state.issues) == diagnostic
    if diagnostic:
        assert "non-converging cycle" in result.primary_report.read_text()
        assert "fixed_issue_count: 1" in result.primary_report.read_text()
    basis = checkpoint["audit"]["decision_basis"]
    for content in ("old\n", "new\n"):
        (h.context.run_worktree / "dependency.conf").write_text(content)
        current = decision.decision_state(
            decision.worktree_inputs(h.context.run_worktree), h.candidates[first]
        )
        assert decision.basis_is_valid(basis, current) == diagnostic
    assert second in {
        item["candidate_id"] for item in selected_remediation_checkpoints(h.manifest)
    }


def test_checkpoint_reference_recovery_keeps_rechecks(feedback_run, monkeypatch):
    h = feedback_run
    identity = _add_candidate(h, "a")
    _run(h)
    (h.context.run_worktree / "dependency.conf").write_text("new\n")
    remediation.commit_work_unit(h.context.run_worktree, "later change")
    original = report._record_checkpoint

    def failed_reference(*_args):
        raise OSError("reference update failed")

    monkeypatch.setattr(report, "_record_checkpoint", failed_reference)
    with pytest.raises(OSError, match="reference update failed"):
        _run(h)
    monkeypatch.setattr(report, "_record_checkpoint", original)
    assert recover_report_cut_checkpoint_references(h.context.repo, h.manifest, h.path)
    loaded, _ = load_report_cut(h.context.repo)
    assert len(loaded["processing"]["remediation_checkpoints"]) == 2
    assert len(decision.issue_history(h.context.repo, loaded, identity)) == 2


@pytest.mark.parametrize(
    "status", ["already_resolved", "not_actionable", "human_required", "inconclusive"]
)
def test_sealed_result_cannot_publish_or_recover_with_changed_basis(
    feedback_run, monkeypatch, status
):
    h = feedback_run
    identity = _add_candidate(h, "a")
    h.handler = lambda _issue: _remediation_output(identity, status)
    candidates, aggregates = _run(h)
    # 封印時の分類には根拠検証で読んだ checkpoint を使い、再読しない。
    read_checkpoint = Mock(wraps=remediation.read_run_artifact)
    with monkeypatch.context() as seal_patch:
        seal_patch.setattr(remediation, "read_run_artifact", read_checkpoint)
        remediation._seal(h.context, h.manifest, candidates, aggregates)
    assert read_checkpoint.call_count == 1
    case_id = h.manifest["run"]["targets"]["case_ids"][identity]
    assert (case_id is not None) == (status in {"human_required", "inconclusive"})

    # 再利用は一回の封印内に限り、次の呼出しでは改変を拒否する。
    [reference] = selected_remediation_checkpoints(h.manifest)
    checkpoint_path = h.context.repo / reference["path"]
    checkpoint_bytes = checkpoint_path.read_bytes()
    checkpoint_path.write_bytes(b"{}\n")
    try:
        with pytest.raises(CmocError, match="SHA256"):
            remediation._seal(h.context, h.manifest, candidates, aggregates)
    finally:
        checkpoint_path.write_bytes(checkpoint_bytes)
    seal_path = h.context.repo / h.manifest["run"]["sealed"]["path"]
    sealed_bytes = seal_path.read_bytes()
    for source in h.context.run_worktree.iterdir():
        (h.context.session_worktree / source.name).write_bytes(source.read_bytes())
    (h.context.session_worktree / "dependency.conf").write_text("post-join change\n")
    monkeypatch.setattr(remediation, "_is_ancestor", lambda *_args: True)
    with pytest.raises(CmocError, match="最終状態"):
        remediation._complete_join(h.context, h.manifest)
    monkeypatch.setattr(
        remediation,
        "sync_refactor_state",
        lambda *_args: pytest.fail(
            "invalid sealed results must not be repaired during recovery"
        ),
    )
    with pytest.raises(CmocError, match="最終状態"):
        remediation._recover_join(h.context, h.manifest)
    assert h.manifest["run"]["completion"] is None
    assert h.manifest["publication"] is None
    assert seal_path.read_bytes() == sealed_bytes
    assert len(h.calls) == 1
    assert artifact_reference(h.context.repo, seal_path) == h.manifest["run"]["sealed"]


def test_verified_merge_adjustment_keeps_sealed_result_without_run_tree_equality(
    feedback_run, monkeypatch
):
    """agent 検証済み調整なら封印結果と最終 tree の対応を別に記録する。"""
    h = feedback_run
    identity = _add_candidate(h, "a")
    h.handler = lambda _issue: _remediation_output(identity, "already_resolved")
    candidates, aggregates = _run(h)
    remediation._seal(h.context, h.manifest, candidates, aggregates)
    seal = read_json_object(h.context.repo / h.manifest["run"]["sealed"]["path"])
    for source in h.context.run_worktree.iterdir():
        (h.context.session_worktree / source.name).write_bytes(source.read_bytes())
    (h.context.session_worktree / "dependency.conf").write_text("joined adjustment\n")
    log_path = h.context.repo / h.manifest["run"]["invocation_log"]
    log_path.write_text(json.dumps({"event": "agent_verification"}) + "\n")
    (h.context.run_worktree / "dependency.conf").write_text("joined adjustment\n")
    h.join.resolution = {
        "agent_status": "resolved",
        "agent_report": "merge_resolution: resolved\n検証: 採用結果を維持。",
        "call_log": str(log_path),
        "verified_run_commit": h.head,
        "initial_conflicts": ["dependency.conf"],
    }
    monkeypatch.setattr(remediation, "tree_changes", lambda *_args: [])
    remediation._verify_prepared_feedback(h.context, h.manifest, h.join)
    remediation._record_merge(h.context, h.manifest, "merge-commit", h.join.resolution)
    monkeypatch.setattr(remediation, "_is_ancestor", lambda *_args: True)
    remediation._complete_join(h.context, h.manifest)
    completion = read_json_object(
        h.context.repo / h.manifest["run"]["completion"]["path"]
    )

    assert completion["merge_adjustment"]["agent_status"] == "resolved"
    assert completion["final_decision_inputs_sha256"] != seal["decision_inputs_sha256"]
    assert completion["merged"] == h.manifest["run"]["merged"]
    assert completion["checks"]["decision_basis"] is True
    log_path.write_text(json.dumps({"event": "tampered"}) + "\n")
    with pytest.raises(CmocError, match="判定根拠"):
        remediation._complete_join(h.context, h.manifest)


def test_recovery_uses_prepared_join_record_without_new_calls(
    feedback_run, monkeypatch
):
    """取り込み直後の停止では、封印時 HEAD と準備完了 HEAD を区別して回復する。"""
    h = feedback_run
    _run(h)
    remediation._seal(h.context, h.manifest, h.candidates, {})
    for source in h.context.run_worktree.iterdir():
        (h.context.session_worktree / source.name).write_bytes(source.read_bytes())
    h.join.prepared_run_head = "b" * 40
    h.join.session_commit = h.join.join_commit = "c" * 40
    monkeypatch.setattr(remediation, "_is_ancestor", lambda *_args: True)
    monkeypatch.setattr(remediation, "head_commit", lambda _root: "b" * 40)
    monkeypatch.setattr(remediation, "tree_changes", lambda *_args: [])
    calls_before = len(h.calls)
    remediation._recover_join(h.context, h.manifest)
    merged = read_json_object(h.context.repo / h.manifest["run"]["merged"]["path"])
    assert merged["run_join_commit"] == "c" * 40
    assert merged["prepared_run_head"] == "b" * 40
    assert h.join.original_run_head == "a" * 40
    assert len(h.calls) == calls_before


def test_current_pointer_rejects_non_markdown_report_path(feedback_run, monkeypatch):
    """current pointer が Markdown 以外の report artifact を選べない。"""
    h = feedback_run
    _run(h)
    result = _join_and_publish(h, monkeypatch)
    assert result.result == "ok"
    root = h.context.repo
    assert cleanup_published_report(root, load_active_state(root))
    assert load_report_cut(root) is None
    assert validate_feedback_state(root).issues == {}

    pointer_path = feedback_root(root) / "active" / "current.json"
    pointer = read_json_object(pointer_path)
    current_report = root / str(pointer["report_path"])
    invalid_report = current_report.with_suffix(".json")
    invalid_report.write_bytes(current_report.read_bytes())
    pointer["report_path"] = invalid_report.relative_to(root).as_posix()
    pointer["report_sha256"] = sha256_bytes(invalid_report.read_bytes())
    pointer_path.write_bytes(canonical_json_bytes(pointer))

    with pytest.raises(CmocError, match="Markdown report path"):
        load_active_state(root)


def test_publication_and_active_generation_use_hash_verified_bytes(
    publication_feedback, monkeypatch
):
    """公開から cleanup 後の active まで、hash・判定根拠・inventory を検証する。"""
    h = publication_feedback
    root = h.context.repo
    publication = h.manifest["publication"]
    paths = [
        root / reference["path"]
        for reference in (
            *publication["generation_artifacts"],
            *publication["history_artifacts"],
            publication["report"],
        )
    ]
    original_read = Path.read_bytes
    # 同じ publication を使い、artifact ごとの置換を独立に検査する。
    for replaced in paths:
        original_content = original_read(replaced)
        reads = Counter()

        def replace_after_read(path):
            if path == h.path:
                pytest.fail("validated manifest must not be reread")
            content = original_read(path)
            if path in paths:
                reads[path] += 1
                if path == replaced and reads[path] == 1:
                    path.write_bytes(b"{}\n")
            return content

        try:
            with monkeypatch.context() as snapshot_patch:
                snapshot_patch.setattr(Path, "read_bytes", replace_after_read)
                _validate_report_cut_manifest(root, h.manifest, h.path)
                assert reads == {path: 1 for path in paths}
                with pytest.raises(CmocError, match="SHA256"):
                    _validate_report_cut_manifest(root, h.manifest, h.path)
        finally:
            replaced.write_bytes(original_content)

    assert cleanup_published_report(root, load_active_state(root))
    assert load_report_cut(root) is None
    state = validate_feedback_state(root)
    assert state.current is not None
    assert state.generation_manifest is not None
    assert set(state.issues) == set(h.candidates)
    # checkpoint の cleanup 後も、active だけで次回の再確認入力を構築できる。
    [identity] = state.issues
    active = state.issues[identity]
    basis = active["verification"]["decision_basis"]
    assert basis["scope"] == "repository-inputs-v1"
    assert len(basis["state_sha256"]) == 64
    assert (
        basis["verification"]
        == _remediation_output(identity, "human_required")["result"]["verification"]
    )
    assert "state" not in basis
    candidate = report._candidate_from_active(active)
    assert (
        report._remediation_candidate_payload(candidate)["previous_verification"]
        == active["verification"]
    )

    [reference] = state.generation_manifest["issues"]
    # helper が改変と patch を毎回戻すため、同じ publication で独立に検査できる。
    for path in (
        root / state.current["generation_manifest_path"],
        root / reference["path"],
    ):
        _assert_hash_verified_state_snapshot(root, state, path, monkeypatch)

    # 次の cut は検証した generation と同じ参照だけを受理する。publication を再準備しない。
    current = report._active_state_input(root, state)
    reference = current["issues"][0]
    for name, references in (
        ("issues", None),
        ("issues", []),
        ("issues", [reference, reference]),
        ("issues", [{**reference, "issue_id": "invalid"}]),
        ("issues", [{**reference, "sha256": "0" * 64}]),
        ("issues", [{**reference, "path": "../outside.json"}]),
        ("issues", [{**reference, "extra": True}]),
        ("machine_aggregates", None),
        ("machine_aggregates", [{}]),
    ):
        with pytest.raises(CmocError, match="generation manifest"):
            feedback_state._validate_report_cut_current_input(
                root,
                {**current, name: references},
                root / "cut.json",
                allow_missing=False,
            )

    # 同じ cleanup 済み generation で、未列挙 artifact を拒否する境界も検査する。
    manifest_path = root / str(state.current["generation_manifest_path"])
    unexpected = manifest_path.parent / "unexpected.json"
    unexpected.write_text("{}\n")
    with pytest.raises(CmocError, match="未定義 artifact"):
        validate_feedback_state(root)


def test_published_active_state_reuses_one_cleanup_snapshot(
    publication_feedback, monkeypatch
):
    """cleanup 待ちでも検証済み artifact を再読せず、次回は改変を拒否する。"""
    h = publication_feedback
    root = h.context.repo
    expected = load_active_state(root)
    original_read = Path.read_bytes
    publication = h.manifest["publication"]
    paths = [h.path] + [
        root / reference["path"]
        for reference in (
            *publication["generation_artifacts"],
            *publication["history_artifacts"],
            publication["report"],
        )
    ]
    # 準備を共有し、cleanup manifest・generation・履歴・report の置換を個別に検査する。
    for replaced in paths:
        original_content = original_read(replaced)
        reads = Counter()

        def replace_after_read(path):
            content = original_read(path)
            if path in paths:
                reads[path] += 1
                if path == replaced and reads[path] == 1:
                    path.write_bytes(b"{}\n")
            return content

        try:
            with monkeypatch.context() as snapshot_patch:
                snapshot_patch.setattr(Path, "read_bytes", replace_after_read)
                assert validate_feedback_state(root) == expected
                assert reads == {path: 1 for path in paths}
                with pytest.raises(CmocError, match="SHA256"):
                    validate_feedback_state(root)
                assert reads[replaced] == 2
        finally:
            replaced.write_bytes(original_content)


def test_cleanup_publication_must_match_current_references(publication_feedback):
    """cleanup の参照が current と異なる場合は検証済み snapshot を流用しない。"""
    h = publication_feedback
    root = h.context.repo
    pointer_path = feedback_state.current_pointer_path(root)
    pointer_content = pointer_path.read_bytes()
    manifest_content = h.path.read_bytes()
    publication = h.manifest["publication"]
    mismatches = {
        "generation_id": "fbg_999999_2026-09-29_15-04",
        "generation_manifest": {
            **publication["generation_manifest"],
            "sha256": "0" * 64,
        },
        "report": {**publication["report"], "sha256": "0" * 64},
        "result": "incomplete",
    }
    for name, value in mismatches.items():
        manifest = copy.deepcopy(h.manifest)
        manifest["publication"][name] = value
        content = canonical_json_bytes(manifest)
        pointer = json.loads(pointer_content)
        pointer["report_cut_manifest_sha256"] = sha256_bytes(content)
        try:
            h.path.write_bytes(content)
            pointer_path.write_bytes(canonical_json_bytes(pointer))
            with pytest.raises(CmocError, match="publication artifact の参照"):
                validate_feedback_state(root)
        finally:
            h.path.write_bytes(manifest_content)
            pointer_path.write_bytes(pointer_content)
    assert validate_feedback_state(root) == load_active_state(root)


def test_published_cleanup_still_checks_work_inventory(publication_feedback):
    """内容の再検証を省いても、余分な cut・file・symlink を許容しない。"""
    h = publication_feedback
    root = h.context.repo
    work_root = h.path.parent.parent
    expected = load_active_state(root)

    # 同じ publication を保ち、work root と cut 内部の未定義 file を独立に検査する。
    for path in (work_root / "unknown.json", h.path.parent / "unknown.json"):
        path.write_bytes(b"{}\n")
        try:
            with pytest.raises(CmocError, match="未定義 artifact"):
                validate_feedback_state(root)
        finally:
            path.unlink()

    extra_cut = work_root / "fbc_00000000-0000-7000-8000-000000000002"
    extra_cut.mkdir()
    try:
        with pytest.raises(CmocError, match="複数"):
            validate_feedback_state(root)
    finally:
        extra_cut.rmdir()

    alias = work_root / "alias"
    alias.symlink_to(h.path.parent, target_is_directory=True)
    try:
        with pytest.raises(CmocError, match="未定義 artifact"):
            validate_feedback_state(root)
    finally:
        alias.unlink()
    assert validate_feedback_state(root) == expected


def test_publication_staging_relaxes_only_artifact_existence(publication_feedback):
    """保存途中の欠落だけを許し、現存する破損と不正な file を拒否する。"""
    h = publication_feedback
    root = h.context.repo
    staged = copy.deepcopy(h.manifest)
    staged["processing"]["status"] = "staging"
    publication = h.manifest["publication"]
    paths = [
        root / reference["path"]
        for reference in (
            *publication["generation_artifacts"],
            *publication["history_artifacts"],
            publication["report"],
        )
    ]
    for path in paths:
        original_content = path.read_bytes()
        path.unlink()
        with pytest.raises(CmocError, match="通常 file"):
            _validate_report_cut_manifest(root, h.manifest, h.path)
        _validate_report_cut_manifest(root, staged, h.path)

        path.symlink_to(root / "missing-artifact.json")
        for manifest in (h.manifest, staged):
            with pytest.raises(CmocError, match="symlink"):
                _validate_report_cut_manifest(root, manifest, h.path)
        path.unlink()
        path.mkdir()
        for manifest in (h.manifest, staged):
            with pytest.raises(CmocError, match="通常 file"):
                _validate_report_cut_manifest(root, manifest, h.path)
        path.rmdir()

        path.write_bytes(b"{}\n")
        for manifest in (h.manifest, staged):
            with pytest.raises(CmocError, match="SHA256"):
                _validate_report_cut_manifest(root, manifest, h.path)
        path.write_bytes(original_content)
        _validate_report_cut_manifest(root, h.manifest, h.path)


def test_publication_cleanup_matches_input_references_without_repeated_scans(
    publication_feedback,
):
    """消費対象を固定入力の部分集合に限定し、照合の二乗走査を検出する。"""
    h = publication_feedback
    staged = copy.deepcopy(h.manifest)
    staged["processing"]["status"] = "staging"
    comparisons = 0

    class ComparedReference(dict):
        def __eq__(self, other):
            nonlocal comparisons
            comparisons += 1
            return super().__eq__(other)

    # raw の hash・schema 検証は manifest の入力検査に残し、ここでは対象の照合を検査する。
    entries = [
        {
            "observation_id": f"fbo_{index:06d}_2026-10-08_00-00",
            "path": f".cmoc/gu/feedback/observation/v1/2026/10/08/fbo_{index:06d}_2026-10-08_00-00.json",
            "sha256": f"{index:064x}",
        }
        for index in range(128)
    ]
    staged["inputs"]["observations"] = entries
    cleanup = staged["publication"]["cleanup"]
    selected = [
        ComparedReference({key: entry[key] for key in ("path", "sha256")})
        for entry in reversed(entries[::2])
    ]
    cleanup["observations"] = selected

    def validate():
        feedback_state._validate_publication_section(h.context.repo, staged, h.path)

    # cleanup は入力順の prefix や全件でなくてもよく、未消費の入力を残せる。
    validate()
    assert comparisons <= 12 * len(entries)
    for invalid in (
        {**selected[0], "sha256": "f" * 64},
        {**selected[0], "path": ".cmoc/gu/feedback/observation/v1/unlisted.json"},
    ):
        cleanup["observations"] = [invalid, *selected[1:]]
        with pytest.raises(CmocError, match="固定した observation に含まれません"):
            validate()
    cleanup["observations"] = []
    validate()
    cleanup["observations"] = [selected[0], selected[0]]
    with pytest.raises(CmocError, match="一意な path"):
        validate()
