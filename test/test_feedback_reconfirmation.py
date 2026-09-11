"""feedback.md と feedback_state.md の根拠変更・再確認・封印の制御を検証する。

Git と Codex の境界だけを置き換え、wave、checkpoint、根拠検査には実装を使う。
"""

import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_feedback import _context, _fake_result, _payload, _remediation_output

from cmoc_runtime import CmocError
from commons.runtime_feedback_run_state import (
    selected_remediation_checkpoints,
    validate_remediation_checkpoint,
    validate_run_artifacts,
)
from commons.runtime_feedback_state import (
    _validate_report_cut_checkpoint,
    _validate_report_cut_manifest,
    artifact_reference,
    load_active_state,
    load_report_cut,
    recover_report_cut_checkpoint_references,
    write_report_cut_manifest,
)
from commons.runtime_feedback_store import (
    canonical_json_bytes,
    observation_path,
    read_json_object,
    rfc3339_now,
    sha256_bytes,
    store_agent_observation,
    write_immutable_json,
)
from commons.runtime_run_lifecycle import EditingRunContext
from sub_commands.feedback import decision, remediation, report


@pytest.fixture
def feedback_run(tmp_path, monkeypatch):
    repo, worktree, session = (tmp_path / name for name in ("repo", "run", "session"))
    for directory in (repo, worktree, session):
        directory.mkdir()
    (worktree / "README.md").write_text("subject\n")
    (worktree / "dependency.conf").write_text("old\n")
    context = EditingRunContext(
        repo,
        session,
        "session",
        repo / "state.json",
        "cmoc/session/session",
        "a" * 40,
        "feedback_report",
        "cmoc/run/session/run",
        "a" * 40,
        worktree,
    )
    state = load_active_state(repo)
    manifest = remediation._new_manifest(context, state)
    manifest["run"]["invocation_log"] = ".cmoc/gu/log/sub_command/invocation.jsonl"
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
        handler=lambda issue: _remediation_output(issue["issue_id"], "not_actionable"),
    )

    def contents():
        return {p.name: p.read_bytes() for p in worktree.iterdir() if p.is_file()}

    harness.committed = contents()
    monkeypatch.setattr(
        decision,
        "enumerate_oracle_and_realization_files",
        lambda root: ([], [root / name for name in contents()]),
    )

    def changed(*_args, **_kwargs):
        current = contents()
        return sorted(
            name
            for name in current.keys() | harness.committed.keys()
            if current.get(name) != harness.committed.get(name)
        )

    def commit(*_args):
        if not changed():
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
            stdout="\0".join(sorted(contents())) + "\0", returncode=0
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
    monkeypatch.setattr(remediation, "refresh_indexes", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(remediation, "stop_tracked_codex_children", lambda *_args: None)
    monkeypatch.setattr(remediation, "_update_progress", lambda *_args: None)
    monkeypatch.setattr(remediation, "doctor_preprocess_for_join", lambda: set())
    monkeypatch.setattr(
        remediation, "validate_run_join", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(remediation, "capture_high_watermark", lambda *_args: (0, []))
    monkeypatch.setattr(
        report, "_build_candidates", lambda *_args, **_kwargs: (harness.candidates, {})
    )
    monkeypatch.setattr(report, "run_codex_exec", call)
    schema = Path(
        report.build_feedback_remediate_issue_parameter.__code__.co_filename
    ).with_suffix(".json")
    monkeypatch.setattr(
        remediation,
        "build_feedback_remediate_issue_parameter",
        lambda text, root: SimpleNamespace(
            prompt=text, agent_call_cwd=root, structured_output_schema_path=schema
        ),
    )
    return harness


def _add_candidate(harness, letter):
    observation = {
        "source": "agent_report",
        "payload": _payload(),
        "observed_at": rfc3339_now(),
    }
    # この二つの UUID は issue ID の辞書順も a、b の順になる。
    suffix = {"a": "1", "b": "2"}[letter]
    candidate = report._new_candidate(
        observation, "agent\0fbo_00000000-0000-7000-8000-00000000000" + suffix
    )
    identity = candidate["candidate_id"]
    candidate["occurrence_count"] = 1
    harness.candidates[identity] = candidate
    return identity


def _run(harness):
    return remediation._wave_loop(harness.context, harness.manifest, harness.state)


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
    observation_id = "fbo_00000000-0000-7000-8000-000000000001"
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
        "candidate_id": "fbo_00000000-0000-7000-8000-000000000001",
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


def test_remediation_checkpoint_rejects_missing_top_level_hash(feedback_run):
    """欠落した checkpoint hash を KeyError ではなく corruption として扱う。"""
    harness = feedback_run
    _add_candidate(harness, "a")
    _run(harness)
    loaded, _ = load_report_cut(harness.context.repo)
    [reference] = loaded["processing"]["remediation_checkpoints"]
    checkpoint = read_json_object(harness.context.repo / reference["path"])
    checkpoint.pop("input_sha256")

    with pytest.raises(CmocError, match="field set"):
        validate_remediation_checkpoint(
            checkpoint, harness.context.repo / reference["path"]
        )


def test_remediation_checkpoint_rejects_malformed_audit_reference(feedback_run):
    """不正な audit reference を Path の例外ではなく corruption として扱う。"""
    harness = feedback_run
    _add_candidate(harness, "a")
    _run(harness)
    loaded, _ = load_report_cut(harness.context.repo)
    [reference] = loaded["processing"]["remediation_checkpoints"]
    checkpoint = read_json_object(harness.context.repo / reference["path"])
    checkpoint["audit"]["wave"] = None

    with pytest.raises(CmocError, match="wave"):
        validate_remediation_checkpoint(
            checkpoint, harness.context.repo / reference["path"]
        )


def _join_and_publish(harness, monkeypatch):
    h = harness
    remediation._seal(h.context, h.manifest, h.candidates, {})
    for source in h.context.run_worktree.iterdir():
        (h.context.session_worktree / source.name).write_bytes(source.read_bytes())
    monkeypatch.setattr(remediation, "_is_ancestor", lambda *_args: True)
    monkeypatch.setattr(remediation, "tree_changes", lambda *_args: [])
    monkeypatch.setattr(
        report, "current_branch", lambda *_args: h.context.session_branch
    )
    remediation._record_merge(h.context, h.manifest, None)
    remediation._complete_join(h.context, h.manifest)
    return remediation._publish(h.context, h.manifest, h.path, h.state)


@pytest.mark.parametrize(
    "status",
    ["fixed", "already_resolved", "not_actionable", "human_required", "inconclusive"],
)
def test_later_dependency_change_rechecks_every_result(
    feedback_run, monkeypatch, status
):
    h = feedback_run
    first, second = (_add_candidate(h, letter) for letter in ("a", "b"))

    def call(issue):
        identity = issue["issue_id"]
        if identity == second:
            (h.context.run_worktree / "dependency.conf").write_text("new\n")
            output = _remediation_output(identity, "fixed")
            output["result"]["changed_paths"] = ["dependency.conf"]
        elif issue["reconfirmation"] is None:
            output = _remediation_output(identity, status)
            if status == "fixed":
                (h.context.run_worktree / "README.md").write_text("fixed\n")
                output["result"]["changed_paths"] = ["README.md"]
        else:
            assert issue["reconfirmation"]["previous_result"]["status"] == status
            assert issue["reconfirmation"]["changes"]["paths"] == ["dependency.conf"]
            output = _remediation_output(identity, "already_resolved")
        return output

    h.handler = call
    _run(h)
    assert [item["issue_id"] for item in h.calls] == [first, second, first]
    assert len(h.manifest["run"]["waves"]) == 2
    assert h.manifest["run"]["high_watermark"] == 0
    loaded, _ = load_report_cut(h.context.repo)
    assert len(loaded["processing"]["remediation_checkpoints"]) == 3
    selected = selected_remediation_checkpoints(loaded)
    assert len(selected) == report._remediation_candidate_count(loaded) == 2
    assert selected[0]["path"].endswith(".00000002.json")
    result = _join_and_publish(h, monkeypatch)
    assert result.result == "ok"
    assert load_active_state(h.context.repo).issues == {}
    assert "remediation_issue_count: 2" in result.primary_report.read_text()


def test_mechanical_sync_is_rechecked_before_seal(feedback_run, monkeypatch):
    h = feedback_run
    identity = _add_candidate(h, "a")

    def call(issue):
        status = "already_resolved" if issue["reconfirmation"] else "fixed"
        result = _remediation_output(identity, status)
        if status == "fixed":
            (h.context.run_worktree / "README.md").write_text("fixed\n")
            result["result"]["changed_paths"] = ["README.md"]
        return result

    h.handler = call
    monkeypatch.setattr(
        remediation,
        "refresh_indexes",
        lambda *_args, **_kwargs: (
            h.context.run_worktree / "generated.json"
        ).write_text("synchronized\n"),
    )
    _run(h)
    assert len(h.calls) == 2
    assert h.calls[-1]["reconfirmation"]["changes"]["paths"] == ["generated.json"]


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
    assert (load_active_state(h.context.repo).current is None) == diagnostic
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
    candidates, aggregates, _ = _run(h)
    remediation._seal(h.context, h.manifest, candidates, aggregates)
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
    with pytest.raises(CmocError, match="recovery の対象外"):
        remediation._recover_join(h.context, h.manifest)
    assert h.manifest["run"]["completion"] is None
    assert h.manifest["publication"] is None
    assert seal_path.read_bytes() == sealed_bytes
    assert len(h.calls) == 1
    assert artifact_reference(h.context.repo, seal_path) == h.manifest["run"]["sealed"]


def test_active_issue_materializes_basis_without_checkpoint_dependency(
    feedback_run, monkeypatch
):
    h = feedback_run
    identity = _add_candidate(h, "a")
    h.handler = lambda _issue: _remediation_output(identity, "human_required")
    _run(h)
    result = _join_and_publish(h, monkeypatch)
    assert result.result == "attention"
    active = load_active_state(h.context.repo).issues[identity]
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
