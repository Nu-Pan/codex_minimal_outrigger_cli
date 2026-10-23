"""回復の分類、理由変更、設定継承、再発と中断を観測する。"""

import json
import os
import select
import signal
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context
from dataclasses import replace
from itertools import count
from pathlib import Path
from types import SimpleNamespace

import pytest
from _codex_support import (
    codex_arg_value,
    codex_override_config,
    codex_parameter,
    script_codex_calls,
    setup_codex_home,
    stub_codex_overrides,
)

from commons import runtime_codex_exec as runtime
from commons import runtime_codex_recovery as recovery
from commons import runtime_logging
from commons.runtime_codex_profile import classify_codex_call, codex_error_text
from commons.runtime_errors import CmocError
from commons.runtime_git import WorktreeSnapshot
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


@pytest.mark.parametrize("event_type", ["error", "turn.failed"])
@pytest.mark.parametrize(
    ("message", "returncode", "expected"),
    [
        pytest.param("Selected model is at capacity", 0, "transient", id="capacity-0"),
        pytest.param("Selected model is at capacity", 1, "transient", id="capacity-1"),
        pytest.param("unexpected failure", 0, "failed", id="unknown-0"),
    ],
)
def test_failure_diagnostic_classification(message, returncode, expected, event_type):
    """診断形式と終了 code の分類・本文抽出を、回復や log の準備なしで検査する。"""
    # 回復・即時失敗・終了 code の保存との結合は test_codex_runtime_retry.py に残す。
    event = (
        {"type": event_type, "message": message}
        if event_type == "error"
        else {"type": event_type, "error": {"message": message}}
    )
    stdout = jsonl(event)

    assert classify_codex_call(stdout, returncode) == expected
    assert message in codex_error_text(stdout, "")


@pytest.fixture
def recovery_case(tmp_path, monkeypatch):
    # 設定継承・回復制御は解決済みの path context で検証する。
    # 実 Git の cwd・linked worktree 境界は test_codex_runtime_paths.py に残す。
    root = tmp_path / "repo"
    root.mkdir()
    setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.setattr(
        runtime,
        "AgentCallPathContext",
        lambda agent_call_cwd: SimpleNamespace(
            agent_call_cwd=agent_call_cwd, work_root=root, repo_root=root
        ),
    )
    # 完全 prompt と probe の起動契約は test_codex_runtime_quota_retry.py に残す。
    # ここでは各 probe の生成時に cwd と固有の設定 key を持つ parameter を返す。
    monkeypatch.setattr(
        runtime,
        "_quota_availability_probe_parameter",
        lambda base: replace(
            codex_parameter(agent_call_cwd=base.agent_call_cwd),
            agent_call_kind="build_quota_availability_probe_request",
            prompt="recovery probe",
        ),
    )
    # ID の区別・引継ぎとログ保存は観測し、永続採番は test_runtime_ids.py、
    # logger の実採番との結合は test_runtime_cli.py の
    # test_subcommand_logger_keeps_one_file_per_execution と quota_retry に残す。
    ids = count()
    for id_consumer in (runtime, runtime_logging):
        monkeypatch.setattr(
            id_consumer,
            "new_id",
            lambda _root, prefix: f"{prefix}_{next(ids):06d}_2000-01-01_00-00",
        )
    return (
        root,
        codex_parameter(agent_call_cwd=root),
        CmocConfig(),
        SubcommandLogger(root, "test"),
    )


@pytest.fixture
def recovery_control_case(recovery_case, monkeypatch):
    """回復制御の検査では、設定 argv の反復生成を省く。"""
    # 設定継承・理由変更と並列の条件照合は recovery_case の実 argv で検証する。
    # probe・resume の制御と出力・ログ保存はここでも実処理を通す。
    stub_codex_overrides(monkeypatch)
    return recovery_case


@pytest.fixture
def parallel_recovery_case(recovery_case, monkeypatch):
    """両 worker の回復開始を通知し、Fake probe 側で完了を待てるようにする。"""
    _, _, _, logger = recovery_case
    registered = threading.Event()
    original_event = logger.event

    def observe_registration(event, **fields):
        original_event(event, **fields)
        if event == "codex_recovery" and fields["status"] in {"started", "joined"}:
            registrations = [
                record
                for record in logger.event_records()
                if record["event"] == "codex_recovery"
                and record["status"] in {"started", "joined"}
            ]
            if len(registrations) == 2:
                registered.set()

    monkeypatch.setattr(logger, "event", observe_registration)
    return (*recovery_case, registered)


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


@pytest.mark.parametrize(
    "call_kind", ["realization_edit", "build_feedback_issue_normalization_request"]
)
def test_reason_changes_preserve_settings_session_and_work(
    recovery_case, monkeypatch, call_kind
):
    root, parameter, config, logger = recovery_case
    parameter = replace(parameter, agent_call_kind=call_kind)
    recovery_case = (root, parameter, config, logger)
    headers = {"X-Test": "original"}
    config.codex.agent_calls[parameter.agent_call_kind] = CodexCallConfig(
        "custom", "work-model", "high"
    )
    config.codex.model_providers["custom"] = CodexModelProviderConfig(
        {
            "base_url": "https://provider.invalid/v1",
            "env_key": "TEST_CREDENTIAL",
            "http_headers": headers,
        }
    )
    config.codex.agent_calls["build_quota_availability_probe_request"] = (
        CodexCallConfig("openai", "probe-model", "low")
    )
    artifact = root / "result.txt"

    def during_call(index, call):
        if index == 1:
            artifact.write_text("partial work")
            config.codex.agent_calls[parameter.agent_call_kind] = CodexCallConfig(
                "openai", "changed-model", "low"
            )
            config.codex.model_providers["custom"].settings[
                "base_url"
            ] = "https://changed.invalid"
            headers["X-Test"] = "changed"

    calls = script_codex_calls(
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
            "http_headers": {"X-Test": "original"},
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
        for p in sorted((root / ".cmoc/gu/log/codex").glob("*/*_call.json"))
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


@pytest.mark.parametrize(
    "call_kind", ["realization_edit", "build_feedback_issue_normalization_request"]
)
def test_quota_to_capacity_inherits_only_until_resume(
    recovery_case, monkeypatch, call_kind
):
    root, parameter, config, logger = recovery_case
    parameter = replace(parameter, agent_call_kind=call_kind)
    recovery_case = (root, parameter, config, logger)
    config.codex.agent_calls[parameter.agent_call_kind] = CodexCallConfig(
        "openai", "work", "high"
    )
    config.codex.agent_calls["build_quota_availability_probe_request"] = (
        CodexCallConfig("openai", "probe", "low")
    )
    calls = script_codex_calls(
        monkeypatch,
        [
            (1, jsonl(SESSION, QUOTA), None),
            (1, jsonl(CAPACITY), None),
            (1, jsonl(QUOTA), None),
            (0, jsonl(COMPLETED), "ready"),
            # 再開後の新しい quota 待機には、probe 自身の設定を再び使う。
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
    assert sleeps == [1800, 17, 1800, 1800]
    assert [codex_arg_value(c["argv"], "--model") for c in calls] == [
        "work",
        "probe",
        "work",
        "work",
        "work",
        "probe",
        "work",
    ]


@pytest.mark.parametrize("reason", ["quota", "transient"])
def test_recovery_does_not_stop_at_old_retry_limits(monkeypatch, reason):
    """回数・総待機時間による打切りを、実待機や call ごとの I/O なしで検査する。"""
    # 分類・probe・再開・ログとの結合は reason_changes と quota_retry に残す。
    # 同じ理由での継続だけを直接検査し、11 probe 分の出力・ログ生成を省く。
    elapsed = 0.0
    intervals = []
    probes = []

    def sleep(seconds):
        nonlocal elapsed
        intervals.append(seconds)
        elapsed += seconds

    monkeypatch.setattr(
        recovery, "time", SimpleNamespace(perf_counter=lambda: elapsed, sleep=sleep)
    )

    def probe(probe_reason, inherited, _recovery_id):
        probes.append((probe_reason, inherited))
        return reason if len(probes) <= 10 else "succeeded"

    waited = recovery.wait_for_recovery(
        key=(object(),),
        reason=reason,
        probe=probe,
        quota_interval=1800,
        transient_interval=17,
        logger=None,
        agent_call_id="agent",
        stopped_codex_call_id="call",
        call_log_path="call.json",
    )

    interval = 1800 if reason == "quota" else 17
    assert intervals == [interval] * 11
    assert probes == [(reason, reason == "transient")] * 11
    assert waited == {"quota": 0.0, "transient": 0.0} | {reason: interval * 11}


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
    recovery_control_case, monkeypatch, probe_reply
):
    calls = script_codex_calls(monkeypatch, [(1, jsonl(CAPACITY), None), probe_reply])
    with pytest.raises(CmocError, match="回復確認 probe"):
        execute(recovery_control_case)
    assert len(calls) == 2


def test_resume_failure_never_starts_fresh_session(recovery_control_case, monkeypatch):
    calls = script_codex_calls(
        monkeypatch,
        [
            (1, jsonl(SESSION, CAPACITY), None),
            (0, jsonl(COMPLETED), "ready"),
            (1, jsonl({"type": "error", "message": "session does not exist"}), None),
        ],
    )
    with pytest.raises(CmocError, match="呼び出しが失敗"):
        execute(recovery_control_case)
    assert len(calls) == 3
    assert codex_arg_value(calls[-1]["argv"], "resume") == "original-session"


@pytest.fixture
def structured_recovery_case(recovery_control_case, monkeypatch):
    root, parameter, config, logger = recovery_control_case
    # 成果物の列挙・補正中の変動検出・復元は test_codex_runtime_retry.py に残す。
    # ここでは成果物が変わらない前提で、回復と補正予算・診断の結合を検証する。
    monkeypatch.setattr(
        runtime,
        "capture_worktree_snapshot",
        lambda work_root: WorktreeSnapshot(work_root, ()),
    )
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
    calls = script_codex_calls(
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
    calls = script_codex_calls(
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
def test_interruption_wins_over_probe_success(
    recovery_control_case, monkeypatch, point
):
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
        calls = script_codex_calls(
            monkeypatch,
            [
                (1, jsonl(CAPACITY), None),
                (0, jsonl(COMPLETED), "ready"),
            ],
            on_call=on_call,
        )
        with pytest.raises(KeyboardInterrupt):
            execute(recovery_control_case)
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


def test_deferred_commit_finishes_when_foreground_group_receives_sigint(tmp_path):
    """Ctrl+C が親と commit 子 process に届いても、確定記録を終えてから中断する。"""
    script = """
import pathlib, subprocess, sys
from commons.runtime_codex_recovery import defer_recovery_interruption
try:
    with defer_recovery_interruption():
        subprocess.run([sys.executable, '-S', '-c',
            "import pathlib, sys; print('ready', flush=True); "
            "sys.stdin.read(); pathlib.Path('artifact').write_text('committed')"],
            check=True)
        pathlib.Path('record').write_text('confirmed')
except KeyboardInterrupt:
    print('stopped after commit')
"""
    repository = Path(__file__).resolve().parents[1]
    environment = {
        **os.environ,
        "PYTHONPATH": os.pathsep.join(
            str(repository / path) for path in ("src", "referenece/src")
        ),
    }
    # 明示した PYTHONPATH と標準ライブラリだけを使い、site の初期化を省く。
    with subprocess.Popen(
        [sys.executable, "-S", "-c", script],
        cwd=tmp_path,
        env=environment,
        start_new_session=True,
        text=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as process:
        try:
            assert select.select([process.stdout], [], [], 5)[0], "child did not start"
            assert process.stdout.readline() == "ready\n"
            os.killpg(process.pid, signal.SIGINT)
            # SIGINT を送ってから子を解放し、固定待機なしで確定中の中断を保証する。
            stdout, stderr = process.communicate(input="commit\n", timeout=5)
        finally:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGKILL)
                process.communicate(timeout=5)
    assert process.returncode == 0, stderr
    assert stdout == "stopped after commit\n"
    assert (tmp_path / "artifact").read_text() == "committed"
    assert (tmp_path / "record").read_text() == "confirmed"


@pytest.mark.parametrize("different_model", [False, True])
def test_parallel_capacity_checks_share_only_matching_conditions(
    parallel_recovery_case, monkeypatch, different_model
):
    root, parameter, config, logger, registered = parallel_recovery_case
    other = CmocConfig()
    if different_model:
        original = other.codex.agent_calls[parameter.agent_call_kind]
        other.codex.agent_calls[parameter.agent_call_kind] = replace(
            original, model="other-model"
        )
    probes = []

    def run(argv, **kwargs):
        prompt = kwargs["stdin"].read()
        if prompt == "prompt" and "resume" not in argv:
            return subprocess.CompletedProcess(argv, 1, jsonl(SESSION, CAPACITY), "")
        if prompt != "prompt":
            assert registered.wait(5)
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
            transient_poll_interval_sec=0,
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(invoke, (config, other)))
    assert len(probes) == (2 if different_model else 1)
    assert all(result.output_text == "ready" for result in results)


def test_interruption_stops_representative_and_waiting_workers(
    parallel_recovery_case, monkeypatch
):
    root, parameter, config, logger, registered = parallel_recovery_case
    restore = recovery.install_recovery_interruption()
    cancellation = recovery.current_recovery_cancellation()
    probe_started = threading.Event()
    prompts = []

    def run(argv, **kwargs):
        prompt = kwargs["stdin"].read()
        prompts.append(prompt)
        if prompt == "prompt":
            return subprocess.CompletedProcess(argv, 1, jsonl(SESSION, CAPACITY), "")
        assert registered.wait(5)
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
                    transient_poll_interval_sec=0,
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
