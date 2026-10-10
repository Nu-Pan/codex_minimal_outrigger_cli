"""feedback の根拠変更・再確認・封印と publication artifact の整合性を検証する。

Git と Codex の境界だけを置き換え、wave、checkpoint、根拠検査には実装を使う。
"""

import copy
import json
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import pytest
from _acp_builder_support import oracle_schema_path
from _git_support import RUN_BRANCH, SESSION_BRANCH, SESSION_ID
from test_feedback import _context, _fake_result, _payload, _remediation_output

from cmoc_runtime import CmocError
from commons import runtime_feedback_run_state as run_state
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
from commons.runtime_run_lifecycle import EditingRunContext, GitChange
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
        SESSION_ID,
        repo / "state.json",
        SESSION_BRANCH,
        "a" * 40,
        "feedback_report",
        RUN_BRANCH,
        "a" * 40,
        worktree,
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
        lambda text, root, **_kwargs: SimpleNamespace(
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
    # 二つの observation ID は issue ID の辞書順も a、b の順になる。
    suffix = {"a": "0", "b": "1"}[letter]
    candidate = report._new_candidate(
        observation, "agent\0fbo_00000" + suffix + "_2026-08-01_00-00"
    )
    identity = candidate["candidate_id"]
    candidate["occurrence_count"] = 1
    harness.candidates[identity] = candidate
    return identity


def _run(harness):
    return remediation._wave_loop(harness.context, harness.manifest, harness.state)


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


@pytest.mark.parametrize("target", ["checkpoint", "verification", "current_evidence"])
def test_remediation_state_validation_rechecks_schema_and_value(
    feedback_run, tmp_path, monkeypatch, target
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
    if target == "checkpoint":
        value = checkpoint

        def validate(value):
            validate_remediation_checkpoint(value, path)

    else:
        value = copy.deepcopy(checkpoint["audit"]["decision_basis"])
        value["state_sha256"] = sha256_bytes(canonical_json_bytes(value.pop("state")))

        def validate(value):
            validate_decision_basis(value, path, compact=True)

    schema_directory = tmp_path / "schema"
    schema_directory.mkdir()
    schema_path = schema_directory / "remediate_issue.json"
    schema_text = oracle_schema_path("feedback", "remediate_issue.json").read_text(
        encoding="utf-8"
    )
    schema_path.write_text(schema_text, encoding="utf-8")
    original_files = run_state.resources.files
    monkeypatch.setattr(
        run_state.resources,
        "files",
        lambda package: (
            schema_directory
            if package == "oracle.acp_builder.feedback"
            else original_files(package)
        ),
    )

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
    monkeypatch.setattr(remediation, "_is_ancestor", lambda *_args: True)
    monkeypatch.setattr(remediation, "tree_changes", lambda *_args: [])
    monkeypatch.setattr(
        report, "current_branch", lambda *_args: h.context.session_branch
    )
    remediation._record_merge(h.context, h.manifest, None)
    remediation._complete_join(h.context, h.manifest)
    return remediation._publish(h.context, h.manifest, h.path, h.state)


@pytest.fixture
def published_feedback(feedback_run, monkeypatch):
    """実際の checkpoint・publication・cleanup から一件の active state を作る。"""
    h = feedback_run
    identity = _add_candidate(h, "a")
    h.handler = lambda _issue: _remediation_output(identity, "human_required")
    _run(h)
    result = _join_and_publish(h, monkeypatch)
    assert result.result == "attention"
    root = h.context.repo
    assert cleanup_published_report(root)
    assert load_report_cut(root) is None
    state = validate_feedback_state(root)
    assert set(state.issues) == {identity}
    return root, state


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
    remediation._record_merge(
        h.context,
        h.manifest,
        "merge-commit",
        {
            "agent_status": "resolved",
            "agent_report": "merge_resolution: resolved\n検証: 採用結果を維持。",
            "call_log": str(log_path),
            "initial_conflicts": ["dependency.conf"],
        },
    )
    monkeypatch.setattr(remediation, "_is_ancestor", lambda *_args: True)

    def changes(_root, base, *_args):
        return [] if base == "merge-commit" else [GitChange("M", ("dependency.conf",))]

    monkeypatch.setattr(remediation, "tree_changes", changes)
    remediation._complete_join(h.context, h.manifest)
    completion = read_json_object(
        h.context.repo / h.manifest["run"]["completion"]["path"]
    )

    assert completion["merge_adjustment"]["agent_status"] == "resolved"
    assert completion["final_decision_inputs_sha256"] != seal["decision_inputs_sha256"]
    assert completion["merged"] == h.manifest["run"]["merged"]
    assert completion["checks"]["decision_basis"] is True
    log_path.write_text(json.dumps({"event": "tampered"}) + "\n")
    with pytest.raises(CmocError, match="最終状態"):
        remediation._complete_join(h.context, h.manifest)


@pytest.mark.parametrize("log_layout", ["current", "flat", "other_execution"])
def test_recovery_uses_saved_merge_verification_after_commit(
    feedback_run, monkeypatch, log_layout
):
    """merge commit 後は封印済み実行の directory 内の call log だけを再利用する。"""
    h = feedback_run
    identity = _add_candidate(h, "a")
    h.handler = lambda _issue: _remediation_output(identity, "already_resolved")
    candidates, aggregates = _run(h)
    remediation._seal(h.context, h.manifest, candidates, aggregates)
    seal = read_json_object(h.context.repo / h.manifest["run"]["sealed"]["path"])
    parameter = SimpleNamespace(
        agent_call_kind="build_run_join_conflict_resolution_parameter",
        file_access_mode=SimpleNamespace(value="realization_write"),
        prompt=f"sealed: {h.manifest['run']['sealed']['path']}",
    )
    monkeypatch.setattr(
        remediation,
        "build_run_join_conflict_resolution_parameter",
        lambda *_args, **_kwargs: parameter,
    )
    log_dir = h.context.repo / ".cmoc/gu/log/codex"
    if log_layout == "current":
        log_dir /= h.manifest["run"]["targets"]["execution_id"]
    elif log_layout == "other_execution":
        log_dir /= "exec_zzzzzz_2026-09-29_15-04"
    log_dir.mkdir(parents=True)
    call_id = "cc_000000_2026-09-29_15-04"
    call_path = log_dir / f"{call_id}_call.json"
    prompt_path = log_dir / f"{call_id}_prompt.md"
    output_path = log_dir / f"{call_id}_output.json"
    prompt_path.write_text(parameter.prompt)
    output_path.write_text(
        "merge_resolution: resolved\n採用結果を維持する調整と検証を実施。\n"
    )
    call_path.write_text(
        json.dumps(
            {
                "purpose": "run join conflict resolution",
                "agent_call_kind": parameter.agent_call_kind,
                "file_access_mode": parameter.file_access_mode.value,
                "cwd": str(h.context.session_worktree.resolve()),
                "prompt_log_path": str(prompt_path),
                "output_path": str(output_path),
            }
        )
    )
    invocation_log = h.context.repo / h.manifest["run"]["invocation_log"]
    invocation_log.write_text(
        json.dumps(
            {
                "event": "codex_call",
                "purpose": "run join conflict resolution",
                "status": "succeeded",
                "returncode": 0,
                "call_log_path": str(call_path),
                "prompt_log_path": str(prompt_path),
                "output_path": str(output_path),
            }
        )
        + "\n"
    )
    merge_head = "b" * 40
    monkeypatch.setattr(
        remediation,
        "head_commit",
        lambda root: (
            merge_head if root == h.context.session_worktree else seal["run_head"]
        ),
    )
    monkeypatch.setattr(
        remediation,
        "run_git",
        lambda *_args, **_kwargs: SimpleNamespace(
            stdout=f"{seal['session_head_before']} {seal['run_head']}\n",
            returncode=0,
        ),
    )
    monkeypatch.setattr(remediation, "_is_ancestor", lambda *_args: True)
    monkeypatch.setattr(remediation.decision, "state_hash", lambda _files: "changed")
    monkeypatch.setattr(remediation, "tree_changes", lambda *_args: [])
    monkeypatch.setattr(remediation, "_complete_join", lambda *_args: None)

    if log_layout != "current":
        with pytest.raises(CmocError, match="検証を一意に確認"):
            remediation._recover_join(h.context, h.manifest)
        assert h.manifest["run"]["merged"] is None
        return

    remediation._recover_join(h.context, h.manifest)
    merged = read_json_object(h.context.repo / h.manifest["run"]["merged"]["path"])
    assert merged["run_join_commit"] == merge_head
    assert merged["resolution"]["agent_status"] == "resolved"
    assert merged["resolution"]["recovered_from_call_log"] is True
    assert merged["resolution"]["call_log"] == artifact_reference(
        h.context.repo, call_path
    )

    output_path.write_text("merge_resolution: unresolved\n")
    with pytest.raises(CmocError, match="検証を一意に確認"):
        remediation._recover_merge_resolution(
            h.context, h.manifest, seal, required=True
        )


def test_active_issue_materializes_basis_without_checkpoint_dependency(
    published_feedback,
):
    _, state = published_feedback
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


def test_current_pointer_rejects_non_markdown_report_path(feedback_run, monkeypatch):
    """current pointer が Markdown 以外の report artifact を選べない。"""
    h = feedback_run
    _run(h)
    result = _join_and_publish(h, monkeypatch)
    assert result.result == "ok"
    root = h.context.repo
    assert cleanup_published_report(root)
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


def test_active_generation_hash_mismatch_is_corruption(published_feedback):
    """current pointer が列挙する active record の改変を無視して続行しない。"""
    root, state = published_feedback
    assert state.generation_manifest is not None
    [reference] = state.generation_manifest["issues"]
    issue_path = root / reference["path"]
    issue = read_json_object(issue_path)
    issue["summary"] = "改変済み"
    issue_path.write_bytes(canonical_json_bytes(issue))

    with pytest.raises(CmocError, match="SHA256"):
        load_active_state(root)


def test_unlisted_active_generation_artifact_is_corruption(published_feedback):
    """manifest が列挙しない active generation file を無視しない。"""
    root, state = published_feedback
    assert state.current is not None
    manifest_path = root / str(state.current["generation_manifest_path"])
    unexpected = manifest_path.parent / "unexpected.json"
    unexpected.write_text("{}\n")

    with pytest.raises(CmocError, match="未定義 artifact"):
        validate_feedback_state(root)
