"""Codex quota exceeded 後の probe/resume/retry 制御を検証する。

このファイルは 16,000 文字を超えるが、責務境界は quota 待機から復帰する
Codex exec の外部挙動に閉じている。probe 共有、resume token、再実行、call log、
subcommand log、CODEX_HOME/cwd は同じ retry 状態機械の観測点であり、分割すると
同じ fake Codex 呼び出し列を追う文脈が分散する。現状は quota retry 回帰として
一箇所に保つ方が凝集性が高い。
根拠: {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
および {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import TextIO, cast

import pytest
from _codex_support import (
    codex_arg_value,
    codex_override_config,
    setup_codex_home,
    stub_codex_overrides,
)
from _command_support import write_python_executable
from _git_support import make_repo

import cmoc_runtime
import commons.runtime_codex_exec as runtime_codex_exec
from acp.builder.quota_probe import build_quota_availability_probe_parameter
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import SubcommandLogger
from commons.runtime_codex import run_codex_exec
from commons.runtime_errors import CmocError
from config.cmoc_config import CmocConfig


def quota_probe_prompt(cwd: Path) -> str:
    """実在する quota probe adapter が生成する prompt を返す。"""
    return build_quota_availability_probe_parameter(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.READONLY,
            "base",
            None,
            cwd=cwd,
        )
    ).prompt


def test_resume_token_is_read_from_persisted_jsonl_log(tmp_path: Path) -> None:
    """保存済み JSONL から resume token を復元し、欠落時は None にする。"""
    log_path = tmp_path / "failed_call.jsonl"
    log_path.write_text('{"type":"thread.started","thread_id":"sess-from-log"}\n')

    assert (
        runtime_codex_exec._extract_resume_token_from_jsonl_log(log_path)
        == "sess-from-log"
    )
    assert (
        runtime_codex_exec._extract_resume_token_from_jsonl_log(
            tmp_path / "missing.jsonl"
        )
        is None
    )


def test_run_codex_exec_polls_and_resumes_after_quota(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """quota 枯渇後に代表 probe を実行し、元 session を resume する。"""
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    timestamps = iter(
        [
            "2099-01-01_00-00_30_000000000",
            "2099-01-01_00-00_20_000000000",
            "2099-01-01_00-00_10_000000000",
        ]
    )
    monkeypatch.setattr(runtime_codex_exec, "timestamp", lambda: next(timestamps))
    probe_prompt = quota_probe_prompt(root)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "calls.jsonl"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, os, pathlib, sys",
            f"calls = pathlib.Path({str(calls)!r})",
            "args = sys.argv[1:]",
            "stdin = sys.stdin.read()",
            "with calls.open('a') as f: f.write(json.dumps({'args': args, 'stdin': stdin, 'codex_home': os.environ.get('CODEX_HOME')}) + '\\n')",
            "if 'resume' in args:",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'ok': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            f"if stdin == {probe_prompt!r}:",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'probe': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            "print(json.dumps({'type':'thread.started','thread_id':'sess-1'}))",
            "print(json.dumps({'type':'error','message':'Quota exceeded'}))",
            "sys.exit(1)",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.FLAGSHIP,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )
    logger = SubcommandLogger(root, "test")

    result = run_codex_exec(
        parameter,
        root=root,
        quota_poll_interval_sec=0,
        max_quota_polls=1,
        config=CmocConfig(),
        subcommand_logger=logger,
    )

    call_records = [json.loads(line) for line in calls.read_text().splitlines()]
    argv_calls = [record["args"] for record in call_records]
    assert argv_calls[0][-1] == "-"
    assert all(record["codex_home"] == str(codex_home) for record in call_records)
    assert call_records[1]["stdin"] == probe_prompt
    assert argv_calls[1][:2] == ["exec", "--skip-git-repo-check"]
    assert codex_arg_value(argv_calls[1], "--model") == "gpt-5.4-mini"
    assert codex_arg_value(argv_calls[1], "--sandbox") == "read-only"
    assert codex_override_config(argv_calls[1])["model_reasoning_effort"] == "low"
    assert "--profile" not in argv_calls[1]
    assert "--json" in argv_calls[1]
    assert "--output-last-message" in argv_calls[1]
    assert argv_calls[1][-1] == "-"
    assert "resume" in argv_calls[2]
    assert "sess-1" in argv_calls[2]
    assert result.output_json == {"ok": True}
    call_entries = [
        (path, json.loads(path.read_text()))
        for path in sorted(
            (root / ".cmoc" / "gu" / "ar" / "log" / "codex").glob("*_call.json")
        )
    ]
    call_logs = [log for _path, log in call_entries]
    assert [log["purpose"] for log in call_logs] == [
        "codex exec",
        "quota availability probe",
        "codex exec",
    ]
    probe_logs = [
        log for log in call_logs if log["purpose"] == "quota availability probe"
    ]
    probe_call_path = next(
        path
        for path, log in call_entries
        if log["purpose"] == "quota availability probe"
    )
    assert len(probe_logs) == 1
    assert probe_logs[0]["argv"][1:] == argv_calls[1]
    assert "profile_name" not in probe_logs[0]
    assert "profile_path" not in probe_logs[0]
    assert probe_logs[0]["model_class"] == "minimum"
    assert probe_logs[0]["reasoning_effort"] == "low"
    assert probe_logs[0]["file_access_mode"] == "readonly"
    assert Path(probe_logs[0]["stdout_log_path"]).read_text().strip() == (
        '{"type": "turn.completed"}'
    )
    assert Path(probe_logs[0]["prompt_log_path"]).read_text() == probe_prompt
    assert Path(probe_logs[0]["stderr_log_path"]).read_text() == ""
    assert Path(probe_logs[0]["output_path"]).read_text() == '{"probe": true}'
    main_entries = [
        (path, log) for path, log in call_entries if log["purpose"] == "codex exec"
    ]
    main_logs = [log for _path, log in main_entries]
    assert len(main_logs) == 2
    assert [log["argv"][1:] for log in main_logs] == [argv_calls[0], argv_calls[2]]
    initial_log = next(log for log in main_logs if "resume" not in log["argv"])
    resume_log = next(log for log in main_logs if "resume" in log["argv"])
    resume_entry = next((path, log) for path, log in main_entries if log is resume_log)
    assert initial_log["argv"][1:] == argv_calls[0]
    assert resume_log["argv"][1:] == argv_calls[2]
    assert codex_arg_value(probe_logs[0]["argv"], "--model") == "gpt-5.4-mini"
    assert codex_arg_value(initial_log["argv"], "--model") == "gpt-5.6-sol"
    assert codex_arg_value(initial_log["argv"], "--sandbox") == "read-only"
    assert codex_arg_value(resume_log["argv"], "--sandbox") == "read-only"
    assert "--profile" not in initial_log["argv"]
    assert "profile_name" not in initial_log
    assert "profile_path" not in initial_log
    assert len({log["stdout_log_path"] for log in main_logs}) == 2
    assert [Path(log["prompt_log_path"]).read_text() for log in main_logs] == [
        "prompt",
        "prompt",
    ]
    assert len({log["prompt_log_path"] for log in main_logs}) == 2
    assert Path(initial_log["stdout_log_path"]).read_text().strip() == (
        '{"type": "thread.started", "thread_id": "sess-1"}\n'
        '{"type": "error", "message": "Quota exceeded"}'
    )
    assert Path(initial_log["output_jsonl_log_path"]).name.endswith("_output.jsonl")
    assert (
        Path(initial_log["output_jsonl_log_path"]).read_text()
        == Path(initial_log["stdout_log_path"]).read_text()
    )
    assert Path(resume_log["stdout_log_path"]).read_text().strip() == (
        '{"type": "turn.completed"}'
    )
    assert result.call_log_path == resume_entry[0]
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["purpose"] for event in codex_events] == [
        "codex exec",
        "quota availability probe",
        "codex exec",
    ]
    assert [event["status"] for event in codex_events] == [
        "quota_waiting",
        "succeeded",
        "succeeded",
    ]
    assert codex_events[0]["returncode"] == 1
    assert codex_events[0]["stdout_log_path"] == main_logs[0]["stdout_log_path"]
    assert codex_events[0]["prompt_log_path"] == main_logs[0]["prompt_log_path"]
    assert codex_events[0]["output_path"] == main_logs[0]["output_path"]
    assert codex_events[1]["returncode"] == 0
    assert codex_events[1]["stdout_log_path"] == probe_logs[0]["stdout_log_path"]
    assert codex_events[1]["prompt_log_path"] == probe_logs[0]["prompt_log_path"]
    assert codex_events[1]["output_path"] == probe_logs[0]["output_path"]
    console = capsys.readouterr().out
    assert "- Purpose: `codex exec`" in console
    assert "- Purpose: `quota availability probe`" in console
    assert f"- Call log: `{probe_call_path}`" in console
    assert "- Elapsed time: `" in console
    assert "- Exit code: `0`" in console


def test_capacity_probe_retry_skips_quota_poll_interval(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """probe の capacity retry は quota polling 間隔を重ねて待たない。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    probe_prompt = quota_probe_prompt(root)
    sleeps: list[float] = []
    monkeypatch.setattr(runtime_codex_exec.time, "sleep", sleeps.append)
    calls: list[str] = []
    probe_count = 0

    def fake_run(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        """quota failure, capacity probe, recovery probe, resume の列を返す。"""
        nonlocal probe_count
        stdin = cast(TextIO, kwargs["stdin"]).read()
        if "resume" in argv:
            kind = "resume"
        elif stdin == probe_prompt:
            kind = "probe"
        else:
            kind = "initial"
        calls.append(kind)
        output = Path(argv[argv.index("--output-last-message") + 1])
        if kind == "initial":
            return subprocess.CompletedProcess(
                argv,
                1,
                '{"type":"thread.started","thread_id":"sess-1"}\n'
                '{"type":"error","message":"Quota exceeded"}\n',
                "",
            )
        if kind == "probe":
            probe_count += 1
            if probe_count == 1:
                return subprocess.CompletedProcess(
                    argv,
                    1,
                    '{"type":"error","message":"Selected model is at capacity"}\n',
                    "",
                )
        output.write_text('{"ok":true}')
        return subprocess.CompletedProcess(argv, 0, '{"type":"turn.completed"}\n', "")

    monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", fake_run)
    result = run_codex_exec(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.READONLY,
            "prompt",
            None,
        ),
        root=root,
        quota_poll_interval_sec=1800,
        capacity_initial_sleep_sec=5,
        max_quota_polls=1,
        config=CmocConfig(),
    )

    assert calls == ["initial", "probe", "probe", "resume"]
    assert sleeps == [1800, 5]
    assert result.quota_wait_sec == 1800
    assert result.output_json == {"ok": True}


def test_run_codex_exec_logs_keyboard_interrupt_from_quota_probe(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """代表 probe の KeyboardInterrupt をログへ記録して伝播する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    probe_prompt = quota_probe_prompt(root)
    calls: list[str] = []

    def fake_run(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        """初回 quota 失敗後の代表 probe を KeyboardInterrupt にする。"""
        prompt = cast(TextIO, kwargs["stdin"]).read()
        calls.append(prompt)
        if prompt == "prompt":
            return subprocess.CompletedProcess(
                argv,
                1,
                '{"type":"thread.started","thread_id":"sess-1"}\n'
                '{"type":"error","message":"Quota exceeded"}\n',
                "",
            )
        raise KeyboardInterrupt

    monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", fake_run)
    logger = SubcommandLogger(root, "test")

    with pytest.raises(KeyboardInterrupt):
        run_codex_exec(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                FileAccessMode.READONLY,
                "prompt",
                None,
            ),
            root=root,
            quota_poll_interval_sec=0,
            max_quota_polls=1,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    assert calls == ["prompt", probe_prompt]
    console = capsys.readouterr().out
    assert "- Purpose: `quota availability probe`" in console
    assert "- Error: `KeyboardInterrupt()`" in console
    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert [event["purpose"] for event in codex_events] == [
        "codex exec",
        "quota availability probe",
    ]
    assert codex_events[0]["status"] == "quota_waiting"
    assert codex_events[1]["status"] == "failed"
    assert codex_events[1]["error"] == "KeyboardInterrupt()"


def test_quota_probe_adapter_builds_minimal_probe() -> None:
    """配布 tree に正本 builder がなくても最小 probe を構築する。"""
    base = AgentCallParameter(
        ModelClass.FLAGSHIP,
        ReasoningEffort.HIGH,
        FileAccessMode.REPO_WRITE,
        "base",
        None,
        run_indexing_preflight=True,
        cwd=Path("/tmp/base-cwd"),
    )
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    probe = build_quota_availability_probe_parameter(base)

    assert probe.model_class == ModelClass.MINIMUM
    assert probe.reasoning_effort == ReasoningEffort.LOW
    assert probe.file_access_mode == FileAccessMode.READONLY
    assert probe.prompt == ""
    assert probe.structured_output_schema_path is None
    assert probe.run_indexing_preflight is False
    assert probe.cwd == base.cwd


def test_quota_probe_uses_codex_cwd_for_relative_codex_home(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """probe も Codex cwd 基準で相対 CODEX_HOME を解決する。"""
    root = make_repo(tmp_path)
    initial_codex_home = root / "relative_codex_home"
    probe_codex_home = root / "relative_codex_home"
    for codex_home in {initial_codex_home, probe_codex_home}:
        codex_home.mkdir()
        (codex_home / "auth.json").write_text("{}\n")
    monkeypatch.setenv("CODEX_HOME", "relative_codex_home")
    stub_codex_overrides(monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    probe_prompt = quota_probe_prompt(root)
    records: list[tuple[str, Path, Path, Path, Path]] = []

    def fake_run(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        """初回、probe、resume の cwd と CODEX_HOME を記録する。"""
        stdin = cast(TextIO, kwargs["stdin"]).read()
        cwd = Path(cast(str, kwargs["cwd"]))
        kind = (
            "resume"
            if "resume" in argv
            else "probe"
            if stdin == probe_prompt
            else "initial"
        )
        home = Path(cast(dict[str, str], kwargs["env"])["CODEX_HOME"])
        records.append(
            (kind, cwd, home, cwd / home, Path(argv[argv.index("--cd") + 1]))
        )
        if kind == "initial":
            return subprocess.CompletedProcess(
                argv,
                1,
                '{"type":"thread.started","thread_id":"sess-1"}\n'
                '{"type":"error","message":"Quota exceeded"}\n',
                "",
            )
        output = Path(argv[argv.index("--output-last-message") + 1])
        output.write_text(json.dumps({"ok": kind}))
        return subprocess.CompletedProcess(argv, 0, '{"type": "turn.completed"}\n', "")

    monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", fake_run)
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.PURE_ORACLE_READ,
        "prompt",
        None,
    )

    run_codex_exec(
        parameter,
        root=root,
        quota_poll_interval_sec=0,
        max_quota_polls=1,
        config=CmocConfig(),
    )

    expected = [
        (
            "initial",
            root,
            Path("relative_codex_home"),
            initial_codex_home,
            root,
        ),
        ("probe", root, Path("relative_codex_home"), probe_codex_home, root),
        (
            "resume",
            root,
            Path("relative_codex_home"),
            initial_codex_home,
            root,
        ),
    ]
    assert records == [
        (kind, cwd, home, resolved_home, codex_cd)
        for kind, cwd, home, resolved_home, codex_cd in expected
    ]


def test_run_codex_exec_reruns_after_quota_without_resume_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """resume token がない quota 復帰で同じ prompt を再実行する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    probe_prompt = quota_probe_prompt(root)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "calls.jsonl"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys",
            f"calls = pathlib.Path({str(calls)!r})",
            "args = sys.argv[1:]",
            "stdin = sys.stdin.read()",
            "records = calls.read_text().splitlines() if calls.exists() else []",
            "with calls.open('a') as f: f.write(json.dumps({'args': args, 'stdin': stdin}) + '\\n')",
            f"if stdin == {probe_prompt!r}:",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'probe': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            "if records:",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'ok': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            "print(json.dumps({'type':'error','message':'Quota exceeded'}))",
            "sys.exit(1)",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    result = run_codex_exec(
        parameter,
        root=root,
        quota_poll_interval_sec=0,
        max_quota_polls=1,
        config=CmocConfig(),
    )

    call_records = [json.loads(line) for line in calls.read_text().splitlines()]
    assert [record["stdin"] for record in call_records] == [
        "prompt",
        probe_prompt,
        "prompt",
    ]
    assert all("resume" not in record["args"] for record in call_records)
    assert result.output_json == {"ok": True}


@pytest.mark.parametrize("probe_returncode", [0, 2])
def test_quota_probe_non_quota_failure_fails_immediately(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, probe_returncode: int
) -> None:
    """代表 probe の quota 以外の失敗を即時に伝播する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    probe_prompt = quota_probe_prompt(root)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "failed_probe_calls.jsonl"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys",
            f"calls = pathlib.Path({str(calls)!r})",
            "args = sys.argv[1:]",
            "stdin = sys.stdin.read()",
            "with calls.open('a') as f: f.write(json.dumps({'args': args, 'stdin': stdin}) + '\\n')",
            f"if stdin == {probe_prompt!r}:",
            "    print(json.dumps({'type':'error','message':'override is broken'}))",
            f"    sys.exit({probe_returncode})",
            "print(json.dumps({'type':'thread.started','thread_id':'sess-1'}))",
            "print(json.dumps({'type':'error','message':'Quota exceeded'}))",
            "sys.exit(1)",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )
    logger = SubcommandLogger(root, "test")

    with pytest.raises(CmocError, match="quota availability probe"):
        run_codex_exec(
            parameter,
            root=root,
            quota_poll_interval_sec=0,
            max_quota_polls=3,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    call_records = [json.loads(line) for line in calls.read_text().splitlines()]
    assert [record["stdin"] for record in call_records] == [
        "prompt",
        probe_prompt,
    ]
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == ["quota_waiting", "failed"]
    assert codex_events[1]["purpose"] == "quota availability probe"
    assert codex_events[1]["returncode"] == probe_returncode
    assert "override is broken" in codex_events[1]["error"]


def test_quota_probe_rejects_invalid_jsonl_with_zero_returncode_and_valid_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """probe も valid output だけでは不正 stdout を成功扱いしない。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    probe_prompt = quota_probe_prompt(root)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            "args = sys.argv[1:]",
            "stdin = sys.stdin.read()",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "if stdin == 'prompt':",
            "    print(json.dumps({'type':'error','message':'Quota exceeded'}))",
            "    sys.exit(1)",
            f"if stdin == {probe_prompt!r}:",
            "    output.write_text(json.dumps({'probe': True}))",
            "    print('not-json')",
            "    sys.exit(0)",
            "raise AssertionError('unexpected extra call')",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    with pytest.raises(CmocError) as exc_info:
        run_codex_exec(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                FileAccessMode.READONLY,
                "prompt",
                None,
            ),
            root=root,
            quota_poll_interval_sec=0,
            max_quota_polls=1,
            config=CmocConfig(),
        )

    assert "quota availability probe" in str(exc_info.value)
    assert "malformed JSONL event (invalid JSON): not-json" not in exc_info.value.detail


def test_quota_poll_limit_stops_before_probe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """quota poll 上限到達時は代表 probe を起動せず失敗する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "quota_limit_calls.jsonl"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            f"calls = pathlib.Path({str(calls)!r})",
            "args = sys.argv[1:]",
            "stdin = sys.stdin.read()",
            "with calls.open('a') as f: f.write(json.dumps({'stdin': stdin}) + '\\n')",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "if stdin == 'prompt':",
            "    pathlib.Path('src').mkdir(exist_ok=True)",
            "    pathlib.Path('src/blocked.py').write_text('blocked\\n')",
            "    print(json.dumps({'type':'thread.started','thread_id':'sess-1'}))",
            "    print(json.dumps({'type':'error','message':'Quota exceeded'}))",
            "    sys.exit(1)",
            "raise AssertionError('unexpected extra call')",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    with pytest.raises(CmocError, match="quota"):
        run_codex_exec(
            parameter,
            root=root,
            quota_poll_interval_sec=0,
            max_quota_polls=0,
            config=CmocConfig(),
        )

    call_records = [json.loads(line) for line in calls.read_text().splitlines()]
    assert len(call_records) == 1
    assert call_records[0]["stdin"] == "prompt"
    assert (root / "src" / "blocked.py").read_text() == "blocked\n"


def test_quota_probe_failure_reports_probe_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """代表 probe の失敗を quota 復帰失敗として報告する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    probe_prompt = quota_probe_prompt(root)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "probe_failure_calls.jsonl"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            f"calls = pathlib.Path({str(calls)!r})",
            "args = sys.argv[1:]",
            "stdin = sys.stdin.read()",
            "with calls.open('a') as f: f.write(json.dumps({'stdin': stdin}) + '\\n')",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "if stdin == 'prompt':",
            "    print(json.dumps({'type':'thread.started','thread_id':'sess-1'}))",
            "    print(json.dumps({'type':'error','message':'Quota exceeded'}))",
            "    sys.exit(1)",
            f"if stdin == {probe_prompt!r}:",
            "    pathlib.Path('src').mkdir(exist_ok=True)",
            "    pathlib.Path('src/probe.py').write_text('blocked\\n')",
            "    print(json.dumps({'type':'error','message':'override is broken'}))",
            "    sys.exit(2)",
            "raise AssertionError('unexpected extra call')",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    with pytest.raises(CmocError, match="quota availability probe"):
        run_codex_exec(
            parameter,
            root=root,
            quota_poll_interval_sec=0,
            max_quota_polls=1,
            config=CmocConfig(),
        )

    call_records = [json.loads(line) for line in calls.read_text().splitlines()]
    assert [record["stdin"] for record in call_records] == ["prompt", probe_prompt]
    assert (root / "src" / "probe.py").read_text() == "blocked\n"


def test_run_codex_exec_uses_single_representative_quota_probe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """並行 quota 待機を一つの代表 probe に集約する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    probe_prompt = quota_probe_prompt(root)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "parallel_calls.jsonl"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys, time",
            f"calls = pathlib.Path({str(calls)!r})",
            "args = sys.argv[1:]",
            "stdin = sys.stdin.read()",
            f"kind = 'resume' if 'resume' in args else 'probe' if stdin == {probe_prompt!r} else 'initial'",
            "with calls.open('a') as f: f.write(json.dumps({'kind': kind, 'args': args}) + '\\n')",
            "if kind == 'resume':",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'ok': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            "if kind == 'probe':",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'probe': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            "deadline = time.time() + 5",
            "while time.time() < deadline:",
            "    lines = calls.read_text().splitlines() if calls.exists() else []",
            "    if sum(1 for line in lines if json.loads(line)['kind'] == 'initial') >= 2:",
            "        break",
            "    time.sleep(0.01)",
            "print(json.dumps({'type':'thread.started','thread_id':'sess-parallel'}))",
            "print(json.dumps({'type':'error','message':'Quota exceeded'}))",
            "sys.exit(1)",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    def call_codex() -> object:
        """並行呼び出し一件分の quota 復帰処理を実行する。"""
        return run_codex_exec(
            parameter,
            root=root,
            quota_poll_interval_sec=0.05,
            max_quota_polls=1,
            config=CmocConfig(),
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _index: call_codex(), range(2)))

    events = [json.loads(line) for line in calls.read_text().splitlines()]
    assert [event["kind"] for event in events].count("initial") == 2
    assert [event["kind"] for event in events].count("probe") == 1
    assert [event["kind"] for event in events].count("resume") == 2
    assert [result.output_json for result in results] == [{"ok": True}, {"ok": True}]


def test_waiting_quota_calls_fail_when_representative_probe_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """代表 probe の失敗を待機中の全呼び出しへ伝播する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    probe_prompt = quota_probe_prompt(root)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "parallel_failed_probe_calls.jsonl"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys, time",
            f"calls = pathlib.Path({str(calls)!r})",
            "args = sys.argv[1:]",
            "stdin = sys.stdin.read()",
            f"kind = 'resume' if 'resume' in args else 'probe' if stdin == {probe_prompt!r} else 'initial'",
            "with calls.open('a') as f: f.write(json.dumps({'kind': kind, 'args': args}) + '\\n')",
            "if kind == 'resume':",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'unexpected': 'resume'}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            "if kind == 'probe':",
            "    print(json.dumps({'type':'error','message':'Quota exceeded'}))",
            "    sys.exit(1)",
            "deadline = time.time() + 5",
            "while time.time() < deadline:",
            "    lines = calls.read_text().splitlines() if calls.exists() else []",
            "    if sum(1 for line in lines if json.loads(line)['kind'] == 'initial') >= 2:",
            "        break",
            "    time.sleep(0.01)",
            "print(json.dumps({'type':'thread.started','thread_id':'sess-parallel'}))",
            "print(json.dumps({'type':'error','message':'Quota exceeded'}))",
            "sys.exit(1)",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    def call_codex() -> object:
        """代表 probe 失敗を受ける並行呼び出し一件を実行する。"""
        return run_codex_exec(
            parameter,
            root=root,
            quota_poll_interval_sec=0.05,
            max_quota_polls=1,
            config=CmocConfig(),
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(call_codex) for _index in range(2)]
        errors = [future.exception() for future in futures]

    events = [json.loads(line) for line in calls.read_text().splitlines()]
    assert [event["kind"] for event in events].count("initial") == 2
    assert [event["kind"] for event in events].count("probe") == 1
    assert [event["kind"] for event in events].count("resume") == 0
    assert all(isinstance(error, CmocError) for error in errors)


def test_resume_token_returns_none_for_invalid_encoding(tmp_path: Path) -> None:
    """不正な UTF-8 の保存ログでは resume せず再実行する。"""
    log_path = tmp_path / "invalid_encoding.jsonl"
    log_path.write_bytes(b"\xff\n")

    assert runtime_codex_exec._extract_resume_token_from_jsonl_log(log_path) is None


def test_quota_polling_state_is_cleared_when_progress_output_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """quota 待機開始時の出力失敗でも待機中フラグを解除する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)

    def fake_run(
        argv: list[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """quota 待機へ入る初回呼び出しだけを返す。"""
        return subprocess.CompletedProcess(
            argv,
            1,
            '{"type":"error","message":"Quota exceeded"}\n',
            "",
        )

    def fail_print(*_args: object, **_kwargs: object) -> None:
        raise BrokenPipeError("closed output")

    monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", fake_run)
    monkeypatch.setattr(runtime_codex_exec, "print", fail_print, raising=False)
    try:
        with pytest.raises(BrokenPipeError, match="closed output"):
            run_codex_exec(
                AgentCallParameter(
                    ModelClass.EFFICIENCY,
                    ReasoningEffort.LOW,
                    FileAccessMode.READONLY,
                    "prompt",
                    None,
                ),
                root=root,
                quota_poll_interval_sec=0,
                max_quota_polls=1,
                config=CmocConfig(),
            )

        with runtime_codex_exec._QUOTA_CONDITION:
            assert not runtime_codex_exec._QUOTA_POLLING
    finally:
        with runtime_codex_exec._QUOTA_CONDITION:
            runtime_codex_exec._QUOTA_POLLING = False
            runtime_codex_exec._QUOTA_PROBE_AVAILABLE = False
            runtime_codex_exec._QUOTA_PROBE_ERROR = None
            runtime_codex_exec._QUOTA_CONDITION.notify_all()
