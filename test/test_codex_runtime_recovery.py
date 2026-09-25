"""回復の分類、理由変更、設定継承、再発と中断を観測する。"""

import json
import signal
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context
from dataclasses import replace
from pathlib import Path

import pytest
from _codex_support import (
    codex_arg_value,
    codex_override_config,
    codex_parameter,
    setup_codex_home,
)
from _git_support import make_repo

from commons import runtime_codex_exec as runtime
from commons import runtime_codex_recovery as recovery
from commons.runtime_codex_profile import classify_codex_call
from commons.runtime_errors import CmocError
from commons.runtime_logging import SubcommandLogger
from config.cmoc_config import CmocConfig, CodexCallConfig, CodexModelProviderConfig

CAPACITY = {"type": "error", "message": "Selected model is at capacity"}
QUOTA = {"type": "error", "message": "Quota exceeded"}
COMPLETED = {"type": "turn.completed"}
SESSION = {"type": "thread.started", "thread_id": "original-session"}


def jsonl(*events):
    return "".join(json.dumps(event) + "\n" for event in events)


@pytest.mark.parametrize(
    ("events", "returncode", "expected"),
    [
        ([CAPACITY, COMPLETED], 0, "succeeded"),
        ([QUOTA, COMPLETED], 0, "succeeded"),
        (
            [{"type": "error", "message": "temporary transport error"}, COMPLETED],
            0,
            "succeeded",
        ),
        ([QUOTA, COMPLETED], 1, "failed"),
        (
            [
                {"type": "turn.failed", "error": {"message": "Quota exceeded"}},
                COMPLETED,
            ],
            0,
            "failed",
        ),
        ([COMPLETED, CAPACITY], 0, "failed"),
        ([], 0, "failed"),
        ([SESSION], 1, "failed"),
        ([{"type": []}], 0, "failed"),
        (
            [CAPACITY, {"type": "turn.failed", "error": {"message": "invalid model"}}],
            1,
            "failed",
        ),
        (
            [
                QUOTA,
                {
                    "type": "turn.failed",
                    "error": {"message": "Selected model is at capacity"},
                },
            ],
            1,
            "transient",
        ),
        ([{"type": "error", "message": "HTTP 503 response timeout"}], 1, "failed"),
        (
            [
                {
                    "type": "item.completed",
                    "item": {"output": "Selected model is at capacity"},
                },
                COMPLETED,
            ],
            0,
            "succeeded",
        ),
        ([{"type": "turn.failed", "error": {"message": "out of credits"}}], 1, "quota"),
    ],
)
def test_final_cli_outcome(events, returncode, expected):
    assert classify_codex_call(jsonl(*events), returncode) == expected


@pytest.fixture
def recovery_case(tmp_path, monkeypatch):
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    return (
        root,
        codex_parameter(agent_call_cwd=root),
        CmocConfig(),
        SubcommandLogger(root, "test"),
    )


def script_calls(monkeypatch, responses, *, on_call=None):
    calls = []
    replies = iter(responses)

    def run(argv, **kwargs):
        prompt = kwargs["stdin"].read()
        calls.append(
            {
                "argv": argv,
                "prompt": prompt,
                "env": kwargs["env"],
                "timeout": kwargs["timeout"],
            }
        )
        if on_call is not None:
            on_call(len(calls), calls[-1])
        response = next(replies)
        if isinstance(response, BaseException):
            raise response
        returncode, stdout, output = response
        if output is not None:
            Path(codex_arg_value(argv, "--output-last-message")).write_text(output)
        return subprocess.CompletedProcess(argv, returncode, stdout, "")

    monkeypatch.setattr(runtime, "run_codex_subprocess", run)
    return calls


def execute(case, **kwargs):
    root, parameter, config, logger = case
    return runtime.run_codex_exec(
        parameter,
        root=root,
        config=config,
        subcommand_logger=logger,
        quota_poll_interval_sec=0,
        transient_poll_interval_sec=0,
        **kwargs,
    )


def test_reason_changes_preserve_settings_session_and_work(recovery_case, monkeypatch):
    root, parameter, config, logger = recovery_case
    config.codex.agent_calls[parameter.agent_call_kind] = CodexCallConfig(
        "custom", "work-model", "high"
    )
    config.codex.model_providers["custom"] = CodexModelProviderConfig(
        {"base_url": "https://provider.invalid/v1", "env_key": "TEST_CREDENTIAL"}
    )
    config.codex.agent_calls["build_quota_availability_probe_parameter"] = (
        CodexCallConfig("openai", "probe-model", "low")
    )
    artifact = root / "result.txt"

    def during_call(index, call):
        if index == 1:
            artifact.write_text("partial work")
            config.codex.agent_calls[parameter.agent_call_kind] = CodexCallConfig(
                "openai", "changed-model", "low"
            )
            config.codex.model_providers["custom"].settings["base_url"] = (
                "https://changed.invalid"
            )

    calls = script_calls(
        monkeypatch,
        [
            (1, jsonl(SESSION, CAPACITY), None),
            (1, jsonl(QUOTA), None),
            (1, jsonl(CAPACITY), None),
            (0, jsonl(COMPLETED), "ready"),
            (1, jsonl(CAPACITY), None),
            (0, jsonl(COMPLETED), "ready"),
            (0, jsonl(COMPLETED), "done"),
        ],
        on_call=during_call,
    )
    result = execute(recovery_case)
    assert result.output_text == "done"
    assert artifact.read_text() == "partial work"
    assert len(calls) == 7
    for call in calls:
        assert codex_arg_value(call["argv"], "--model") == "work-model"
        overrides = codex_override_config(call["argv"])
        assert overrides["model_provider"] == "custom"
        assert overrides["model_reasoning_effort"] == "high"
        assert overrides["model_providers"]["custom"] == {
            "base_url": "https://provider.invalid/v1",
            "env_key": "TEST_CREDENTIAL",
        }
    for index in (4, 6):
        assert codex_arg_value(calls[index]["argv"], "resume") == "original-session"
        assert calls[index]["prompt"] == calls[0]["prompt"]
    for index in (1, 2, 3, 5):
        assert "resume" not in calls[index]["argv"]
        assert codex_arg_value(calls[index]["argv"], "--sandbox") == "workspace-write"
        assert calls[index]["timeout"] > 0
    logs = [
        json.loads(p.read_text())
        for p in sorted((root / ".cmoc/gu/log/codex").glob("*_call.json"))
    ]
    assert (
        len({log["agent_call_id"] for log in logs if log["purpose"] == "codex exec"})
        == 1
    )
    assert (
        len({log["agent_call_id"] for log in logs if log["purpose"] != "codex exec"})
        == 4
    )
    assert len({log["codex_call_id"] for log in logs}) == 7
    assert logs[4]["resumed_from_codex_call_id"] == logs[0]["codex_call_id"]
    assert logs[6]["resumed_from_codex_call_id"] == logs[4]["codex_call_id"]
    assert logger.quota_wait_sec > 0
    assert logger.transient_wait_sec > 0
    assert result.quota_wait_sec == logger.quota_wait_sec
    assert result.transient_wait_sec == logger.transient_wait_sec
    assert any(
        e["status"] == "reason_changed"
        for e in logger.event_records()
        if e["event"] == "codex_recovery"
    )


def test_quota_to_capacity_inherits_before_accepting_recovery(
    recovery_case, monkeypatch
):
    _, parameter, config, _ = recovery_case
    config.codex.agent_calls[parameter.agent_call_kind] = CodexCallConfig(
        "openai", "work", "high"
    )
    config.codex.agent_calls["build_quota_availability_probe_parameter"] = (
        CodexCallConfig("openai", "probe", "low")
    )
    calls = script_calls(
        monkeypatch,
        [
            (1, jsonl(SESSION, QUOTA), None),
            (1, jsonl(CAPACITY), None),
            (1, jsonl(QUOTA), None),
            (0, jsonl(COMPLETED), "ready"),
            (0, jsonl(COMPLETED), "done"),
        ],
    )
    sleeps = []
    monkeypatch.setattr(recovery.time, "sleep", sleeps.append)
    root, parameter, config, logger = recovery_case
    runtime.run_codex_exec(
        parameter,
        root=root,
        config=config,
        subcommand_logger=logger,
        transient_poll_interval_sec=17,
    )
    assert sleeps == [1800, 17, 1800]
    assert [codex_arg_value(c["argv"], "--model") for c in calls] == [
        "work",
        "probe",
        "work",
        "work",
        "work",
    ]


@pytest.mark.parametrize("reason", [QUOTA, CAPACITY])
def test_recovery_does_not_stop_at_old_retry_limits(recovery_case, monkeypatch, reason):
    calls = script_calls(
        monkeypatch,
        [
            (1, jsonl(SESSION, reason), None),
            *[(1, jsonl(reason), None)] * 10,
            (0, jsonl(COMPLETED), "ready"),
            (0, jsonl(COMPLETED), "done"),
        ],
    )
    assert execute(recovery_case).output_text == "done"
    assert len(calls) == 13
    assert sum(c["prompt"] == "prompt" for c in calls) == 2


@pytest.mark.parametrize(
    "probe_reply",
    [
        (0, jsonl(COMPLETED), ""),
        (0, jsonl(COMPLETED), None),
        (0, jsonl(COMPLETED), "x" * 4097),
        (0, "", "ready"),
        (1, jsonl({"type": "error", "message": "authentication failed"}), None),
        subprocess.TimeoutExpired(
            "codex", 0.1, output=b'{"type":"error","message":"Quota exceeded"}\n'
        ),
    ],
)
def test_unconfirmed_or_unrecoverable_probe_stops(
    recovery_case, monkeypatch, probe_reply
):
    calls = script_calls(monkeypatch, [(1, jsonl(CAPACITY), None), probe_reply])
    with pytest.raises(CmocError, match="回復確認 probe"):
        execute(recovery_case)
    assert len(calls) == 2


def test_resume_failure_never_starts_fresh_session(recovery_case, monkeypatch):
    calls = script_calls(
        monkeypatch,
        [
            (1, jsonl(SESSION, CAPACITY), None),
            (0, jsonl(COMPLETED), "ready"),
            (1, jsonl({"type": "error", "message": "session does not exist"}), None),
        ],
    )
    with pytest.raises(CmocError, match="呼び出しが失敗"):
        execute(recovery_case)
    assert len(calls) == 3
    assert codex_arg_value(calls[-1]["argv"], "resume") == "original-session"


@pytest.fixture
def structured_recovery_case(recovery_case):
    root, parameter, config, logger = recovery_case
    schema = root / "schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "required": ["ok"],
                "properties": {"ok": {"type": "boolean"}},
                "additionalProperties": False,
            }
        )
    )
    return (
        root,
        replace(parameter, structured_output_schema_path=schema),
        config,
        logger,
    )


def test_recovery_during_correction_preserves_turn_budget(
    structured_recovery_case, monkeypatch
):
    root, parameter, config, logger = structured_recovery_case
    calls = script_calls(
        monkeypatch,
        [
            (0, jsonl(SESSION, COMPLETED), "{}"),
            (1, jsonl(CAPACITY), None),
            (1, jsonl(QUOTA), None),
            (0, jsonl(COMPLETED), "ready"),
            (0, jsonl(COMPLETED), "{}"),
            (1, jsonl(CAPACITY), None),
            (0, jsonl(COMPLETED), "ready"),
            (0, jsonl(COMPLETED), "{}"),
        ],
    )
    with pytest.raises(CmocError, match="Structured Output 検証"):
        execute((root, parameter, config, logger))
    assert len(calls) == 8
    for index in (1, 4, 5, 7):
        assert codex_arg_value(calls[index]["argv"], "resume") == "original-session"
    assert calls[1]["prompt"] == calls[4]["prompt"]
    assert calls[5]["prompt"] == calls[7]["prompt"]
    assert (
        sum(
            e["status"] == "output_correction_requested"
            for e in logger.codex_call_records()
        )
        == 2
    )


def test_probe_failure_during_correction_records_original_call(
    structured_recovery_case, monkeypatch
):
    _, parameter, _, logger = structured_recovery_case
    calls = script_calls(
        monkeypatch,
        [
            (0, jsonl(SESSION, COMPLETED), "{}"),
            (1, jsonl(CAPACITY), None),
            (1, jsonl({"type": "error", "message": "authentication failed"}), None),
        ],
    )
    with pytest.raises(CmocError, match="回復確認 probe"):
        execute(structured_recovery_case)
    assert len(calls) == 3
    [diagnostic] = [
        e
        for e in logger.event_records()
        if e["event"] == "codex.structured_output_validation_exhausted"
    ]
    original_call = logger.codex_call_records()[1]
    assert diagnostic["agent_call_id"] == original_call["agent_call_id"]
    assert diagnostic["codex_call_id"] == original_call["codex_call_id"]
    assert diagnostic["agent_call_kind"] == parameter.agent_call_kind
    assert diagnostic["codex_session_id"] == "original-session"


@pytest.mark.parametrize("point", ["wait", "probe_success"])
def test_interruption_wins_over_probe_success(recovery_case, monkeypatch, point):
    restore = recovery.install_recovery_interruption()
    try:
        cancellation = recovery.current_recovery_cancellation()

        def on_call(index, call):
            if index == 2 and point == "probe_success":
                cancellation.set()

        if point == "wait":

            def cancel_wait(timeout):
                cancellation.set()
                return True

            monkeypatch.setattr(cancellation, "wait", cancel_wait)
        calls = script_calls(
            monkeypatch,
            [
                (1, jsonl(CAPACITY), None),
                (0, jsonl(COMPLETED), "ready"),
            ],
            on_call=on_call,
        )
        with pytest.raises(KeyboardInterrupt):
            execute(recovery_case)
        assert len(calls) == (1 if point == "wait" else 2)
    finally:
        restore()


def test_signal_cancellation_is_shared_with_workers():
    previous = signal.getsignal(signal.SIGINT)
    restore = recovery.install_recovery_interruption()
    try:
        with pytest.raises(KeyboardInterrupt):
            signal.raise_signal(signal.SIGINT)
        assert recovery.current_recovery_cancellation().is_set()
    finally:
        restore()
    assert signal.getsignal(signal.SIGINT) is previous
    assert recovery.current_recovery_cancellation() is None


@pytest.mark.parametrize("different_model", [False, True])
def test_parallel_capacity_checks_share_only_matching_conditions(
    recovery_case, monkeypatch, different_model
):
    root, parameter, config, logger = recovery_case
    other = CmocConfig()
    if different_model:
        original = other.codex.agent_calls[parameter.agent_call_kind]
        other.codex.agent_calls[parameter.agent_call_kind] = replace(
            original, model="other-model"
        )
    barrier = threading.Barrier(2)
    probes = []

    def run(argv, **kwargs):
        prompt = kwargs["stdin"].read()
        if prompt == "prompt" and "resume" not in argv:
            barrier.wait(timeout=5)
            return subprocess.CompletedProcess(argv, 1, jsonl(SESSION, CAPACITY), "")
        if prompt != "prompt":
            probes.append(codex_arg_value(argv, "--model"))
        Path(codex_arg_value(argv, "--output-last-message")).write_text("ready")
        return subprocess.CompletedProcess(argv, 0, jsonl(COMPLETED), "")

    monkeypatch.setattr(runtime, "run_codex_subprocess", run)

    def invoke(call_config):
        return runtime.run_codex_exec(
            parameter,
            root=root,
            config=call_config,
            subcommand_logger=logger,
            transient_poll_interval_sec=0.1,
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(invoke, (config, other)))
    assert len(probes) == (2 if different_model else 1)
    assert all(result.output_text == "ready" for result in results)


def test_interruption_stops_representative_and_waiting_workers(
    recovery_case, monkeypatch
):
    root, parameter, config, logger = recovery_case
    restore = recovery.install_recovery_interruption()
    cancellation = recovery.current_recovery_cancellation()
    probe_started = threading.Event()
    barrier = threading.Barrier(2)
    prompts = []

    def run(argv, **kwargs):
        prompt = kwargs["stdin"].read()
        prompts.append(prompt)
        if prompt == "prompt":
            barrier.wait(timeout=5)
            return subprocess.CompletedProcess(argv, 1, jsonl(SESSION, CAPACITY), "")
        probe_started.set()
        assert cancellation.wait(5)
        raise KeyboardInterrupt

    monkeypatch.setattr(runtime, "run_codex_subprocess", run)
    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(
                    copy_context().run,
                    runtime.run_codex_exec,
                    parameter,
                    root=root,
                    config=config,
                    subcommand_logger=logger,
                    transient_poll_interval_sec=0.1,
                )
                for _ in range(2)
            ]
            assert probe_started.wait(5)
            cancellation.set()
            for future in futures:
                with pytest.raises(KeyboardInterrupt):
                    future.result(timeout=5)
    finally:
        cancellation.set()
        restore()
    assert len(prompts) == 3
    assert sum(prompt == "prompt" for prompt in prompts) == 2
