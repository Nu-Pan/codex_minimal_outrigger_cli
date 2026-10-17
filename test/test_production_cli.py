"""全末端サブコマンドを利用者向け entrypoint の本番経路で検証する。

独立 process、実 Codex CLI、および実推論を使用し、CLI の終了 code と外部から
観測できる report・state・Git・call log を確認する。LLM の回答品質は判定せず、
応答を受けた後の cmoc の制御だけを検証対象にする。

このファイルは 16,000 文字を超えるが、独立 process の共通環境、call log 検証、
状態遷移、PTY の応答完了と終了操作は、全末端の本番経路という一つの責務を構成する。
分割すると同じ実 executable・隔離境界・実推論条件を複数ファイル間で追う必要が
生じるため、一続きの受け入れ試験として保つ。

根拠: {{work-root}}/oracle/doc/dev_rule/test_rule.md
"""

import errno
import fcntl
import json
import os
import pty
import select
import shutil
import signal
import struct
import subprocess
import sys
import termios
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest
from _cli_support import terminal_primary_report
from _codex_support import (
    codex_arg_value,
    codex_override_config,
)
from _command_support import write_python_executable
from _git_support import current_branch, make_repo, run_git
from _report_support import report_metadata

from commons.runtime_config import load_config, write_config
from commons.runtime_editor_input_handoff import start_editor_input_handoff
from commons.runtime_editor_input_handoff_protocol import (
    EDITOR_INPUT_REPOSITORY_ENV,
    EDITOR_INPUT_SOURCE_ENV,
)
from commons.runtime_feedback_history import history_artifact
from commons.runtime_feedback_protocol import (
    FEEDBACK_CAPABILITY_ENV,
    FEEDBACK_COLLECTOR_PORT_ENV,
    FEEDBACK_PROTOCOL_ENV,
)
from commons.runtime_feedback_state import (
    generation_artifacts,
    issue_id,
    load_active_state,
    new_generation_id,
    new_report_cut_id,
    publish_generation_artifacts,
)
from commons.runtime_feedback_store import (
    rfc3339_now,
    sha256_bytes,
    store_agent_observation,
    write_immutable_bytes,
    write_immutable_json,
)
from commons.runtime_ids import new_id
from commons.runtime_run_lifecycle import set_run_state, start_editing_run
from config.cmoc_config import CmocConfig

_WORK_ROOT = Path(__file__).resolve().parents[1]
_CMOC_CONSOLE = Path(sys.executable).with_name("cmoc")
_REAL_CODEX = shutil.which("codex")
# {{work-root}}/oracle/doc/dev_rule/test_rule.md
# 外部 provider の応答待ちを個別 command と test case の両方で局所化する。
_PRODUCTION_COMMAND_TIMEOUT = 1800
_PRODUCTION_CASE_TIMEOUT = 3600
pytestmark = [
    pytest.mark.real_path_integration,
    pytest.mark.skipif(
        not _CMOC_CONSOLE.is_file() or _REAL_CODEX is None,
        reason="real-path integration requires installed cmoc and real Codex CLI",
    ),
]

NONINTERACTIVE_SCENARIO_COMMANDS = {
    ("doctor",),
    ("feedback", "report"),
    ("feedback", "close"),
    ("oracle", "edit"),
    ("realization", "apply"),
    ("realization", "refactor"),
    ("run", "abandon"),
    ("run", "join"),
    ("session", "abandon"),
    ("session", "fork"),
    ("session", "join"),
}

TUI_SCENARIOS = (
    (("tui",), "tui codex"),
    (("oracle", "investigation"), "oracle investigation"),
)

RESUME_COMMAND = ("resume",)
PRODUCTION_SCENARIO_COMMANDS = (
    NONINTERACTIVE_SCENARIO_COMMANDS
    | {RESUME_COMMAND}
    | {scenario[0] for scenario in TUI_SCENARIOS}
)

EDITOR_PROMPT = """# 目的

短い応答を返す。

# 作業対象

ファイル操作は行わない。

# 制約条件

ツールを使用せず、リポジトリを変更しない。

# 期待する成果物

`CMOC_TUI_RESPONSE` という一行だけを返す。

# 出力形式

plain text

# 完了条件

応答を一回返したら完了。

# 成功基準

ファイルに副作用がないこと。

# 裁量範囲

追加作業は不要。
"""


def _write_close_fixture(root: Path, decision_basis: dict[str, Any]) -> str:
    """推論結果を固定せず、close に必要な確定済み state を決定論的入力として作る。"""
    timestamp = rfc3339_now()
    execution = new_id(root, "exec")
    case = new_id(root, "fbc")
    cut, generation = new_report_cut_id(), new_generation_id(root)
    canonical = f"agent\0{new_id(root, 'fbo')}"
    identity = issue_id(canonical)
    reason = "外部環境の確認が必要である。"
    issue = {
        "schema_version": 1,
        "issue_id": identity,
        "case_id": case,
        "origin": "agent_report",
        "canonical_key": canonical,
        "category": "configuration",
        "summary": "外部設定の確認待ち",
        "impact": "設定確認を完了できない。",
        "occurrence_count": 1,
        "affected_session_count": 0,
        "session_digest": {"values": [], "saturated": False},
        "first_observed_at": timestamp,
        "last_observed_at": timestamp,
        "representative_evidence": [],
        "reference_targets": [
            {"path": "README.md", "kind": "file", "location": "README.md:1"}
        ],
        "latest_fingerprints": [],
        "verification": {
            "report_cut_id": cut,
            "verified_at": timestamp,
            "status": "inconclusive",
            "reason": reason,
            "current_evidence": [],
            "human_action": None,
            "decision_basis": decision_basis,
        },
        "machine_state": None,
    }
    source = {"kind": "report", "id": cut, "execution_id": execution}
    report = root / f".cmoc/gu/report/feedback/incomplete/{execution}.md"
    log = root / f".cmoc/gu/log/sub_command/{execution}.jsonl"
    log.write_text("{}\n")
    history_path, content, reference = history_artifact(
        root,
        {
            "schema_version": 1,
            "generation_id": generation,
            "source": source,
            "created_at": timestamp,
            "report": report.relative_to(root).as_posix(),
            "log": log.relative_to(root).as_posix(),
            "events": [
                {
                    "kind": "created",
                    "case_id": case,
                    "issue_id": identity,
                    "before": None,
                    "after": issue,
                    "human_reason": None,
                    "agent_result": {"status": "inconclusive", "reason": reason},
                }
            ],
            "observations": [],
        },
    )
    write_immutable_bytes(history_path, content)
    manifest, artifacts, generation_reference = generation_artifacts(
        root,
        generation_id=generation,
        report_cut_id=cut,
        created_at=timestamp,
        session_commit=run_git(root, "rev-parse", "HEAD").stdout.strip(),
        issues={identity: issue},
        machine_aggregates={},
        source=source,
        base_current=None,
        input_boundary=0,
        history=[reference],
    )
    publish_generation_artifacts(root, manifest, artifacts)
    write_immutable_bytes(
        report, f"# 確定済み fixture\n\n{case}: inconclusive\n".encode()
    )
    write_immutable_json(
        root / ".cmoc/gu/feedback/active/current.json",
        {
            "schema_version": 1,
            "generation_id": generation,
            "generation_manifest_path": generation_reference["path"],
            "generation_manifest_sha256": generation_reference["sha256"],
            "report_cut_id": cut,
            "report_cut_manifest_sha256": sha256_bytes(b"close fixture"),
            "report_path": report.relative_to(root).as_posix(),
            "report_sha256": sha256_bytes(report.read_bytes()),
            "published_at": timestamp,
            "result": "incomplete",
        },
    )
    load_active_state(root)
    return case


def _real_path_config() -> CmocConfig:
    """全 agent call 種別を直接テスト用設定へ対応付ける。"""
    # {{work-root}}/oracle/doc/dev_rule/test_rule.md
    # 具体的な provider/Model 名を fixture に固定せず、短い推論に使う既定 entry
    # の直接設定を全 agent call 種別へ適用する。
    config = CmocConfig(num_parallel=1)
    quota_saving_call = config.codex.agent_calls[
        "build_quota_availability_probe_parameter"
    ]
    return replace(
        config,
        codex=replace(
            config.codex,
            agent_calls={
                agent_call_kind: quota_saving_call
                for agent_call_kind in config.codex.agent_calls
            },
        ),
    )


def _write_real_path_config(root: Path) -> None:
    """実経路統合 subprocess 専用の直接設定を保存する。"""
    config = _real_path_config()
    write_config(root / ".cmoc" / "gt" / "config.json", config)


def _write_noninteractive_fixture_instructions(root: Path) -> None:
    """LLM の意味判断を試験対象から外す fixture instruction を追加する。"""
    # {{work-root}}/oracle/doc/dev_rule/test_rule.md
    # 本番経路との差として許される決定論的入力で、cmoc の制御だけを検証する。
    (root / "AGENTS.md").write_text(
        """# Production-path test fixture

This is an intentionally minimal and internally consistent test repository.
For a realization-refactor file review, report `findings` as an empty array,
`verification.status` as `not_required`, and do not modify files.
For feedback remediation of an observation about the
existence of `README.md`, inspect the file, return `already_resolved` with no
changes, and do not report another issue. For every other call, follow its
explicit prompt exactly.
"""
    )
    run_git(root, "add", "AGENTS.md")
    run_git(root, "commit", "-m", "add deterministic agent instructions")


def _source_codex_home() -> Path:
    """実経路テスト開始時の Codex 認証情報の配置元を返す。"""
    configured = os.environ.get("CODEX_HOME")
    path = Path(configured) if configured is not None else Path.home() / ".codex"
    return path if path.is_absolute() else (_WORK_ROOT / path).resolve()


@pytest.fixture(scope="module")
def isolated_cmoc_installation(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """実経路の共有資材を他の cmoc installation から隔離する。"""
    existing = os.environ.get("CMOC_REAL_PATH_INSTALLATION")
    if existing is not None:
        installation = Path(existing).resolve()
        if (
            not installation.is_relative_to(Path("/tmp"))
            or not (installation / ".git").is_dir()
        ):
            raise ValueError("real-path installation must be a Git repository in /tmp")
        return installation
    parent = tmp_path_factory.mktemp("cmoc-installation")
    installation = make_repo(parent)
    for directory in ("src", "oracle", "bin"):
        shutil.copytree(
            _WORK_ROOT / directory, installation / directory, dirs_exist_ok=True
        )
    shutil.copy2(_WORK_ROOT / "pyproject.toml", installation / "pyproject.toml")
    (installation / ".venv").symlink_to(Path(sys.executable).parents[1])
    run_git(installation, "add", "src", "oracle", "bin", "pyproject.toml")
    run_git(installation, "commit", "-m", "isolated cmoc installation")
    return installation


def _production_environment(
    tmp_path: Path,
    installation: Path,
) -> tuple[Path, dict[str, str], Path]:
    """実 CLI と隔離済み Codex home を使う subprocess 環境を準備する。"""
    assert _CMOC_CONSOLE.is_file()
    assert _REAL_CODEX is not None
    cmoc = _CMOC_CONSOLE
    real_codex = _REAL_CODEX

    # Codex の利用者 session/config と test session を混ぜない。
    # {{work-root}}/oracle/doc/dev_rule/test_rule.md
    home = tmp_path / "home"
    home.mkdir()
    codex_home = tmp_path / "codex-home"
    codex_home.mkdir()
    # Codex の runtime state と user config は隔離し、実 provider の認証だけを
    # test-root 内へ複製する。環境変数による認証はそのまま継承する。
    source_auth = _source_codex_home() / "auth.json"
    if source_auth.is_file():
        shutil.copy2(source_auth, codex_home / "auth.json")
    editor_dir = tmp_path / "editor-bin"
    editor_dir.mkdir()
    report_open_log = editor_dir / "report-open.log"
    write_python_executable(
        editor_dir / "code",
        [
            "import pathlib, sys",
            "if '--wait' in sys.argv:",
            f"    pathlib.Path(sys.argv[-1]).write_text({EDITOR_PROMPT!r})",
            "else:",
            f"    with pathlib.Path({str(report_open_log)!r}).open('a', encoding='utf-8') as log:",
            "        log.write(sys.argv[-1] + '\\n')",
        ],
    )
    environment = {
        **os.environ,
        "HOME": str(home),
        "CODEX_HOME": str(codex_home),
        "PATH": f"{editor_dir}:{os.environ.get('PATH', '')}",
        # 共有 development venv の console script は、この設定がないと親 session
        # worktree を import するため、現在の realization worktree を指定する。
        # {{work-root}}/oracle/doc/dev_rule/test_rule.md
        "PYTHONPATH": os.pathsep.join(
            [
                str(installation / "src"),
                str(installation / "oracle" / "src"),
                *([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else []),
            ]
        ),
        "TERM": "xterm-256color",
    }
    assert (
        Path(shutil.which("codex", path=environment["PATH"]) or "").resolve()
        == Path(real_codex).resolve()
    )
    return cmoc, environment, codex_home


def _run_cmoc(
    cmoc: Path,
    root: Path,
    environment: dict[str, str],
    *args: str,
) -> subprocess.CompletedProcess[str]:
    """利用者向け console script を独立 process で正常完了まで実行する。"""
    # 個々の command hang は pytest 全体の timeout より早く局所化する。
    if args == ("realization", "refactor"):
        result = _run_refactor_until_confirmed([str(cmoc), *args], root, environment)
    else:
        result = subprocess.run(
            [str(cmoc), *args],
            cwd=root,
            env=environment,
            text=True,
            capture_output=True,
            timeout=_PRODUCTION_COMMAND_TIMEOUT,
            check=False,
        )
    assert result.returncode == 0, (
        f"cmoc {' '.join(args)} failed with {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    return result


def _run_refactor_until_confirmed(
    argv: list[str], root: Path, environment: dict[str, str]
) -> subprocess.CompletedProcess[str]:
    """確定実績を観測して SIGINT を送り、継続 workload の通常終了を検証する。"""
    directory = root / ".cmoc/gu/log/sub_command"
    previous = set(directory.glob("*.jsonl"))
    scanned_versions: dict[Path, tuple[int, int]] = {}
    deadline = time.monotonic() + _PRODUCTION_COMMAND_TIMEOUT
    interrupted = False
    with subprocess.Popen(
        argv,
        cwd=root,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    ) as process:
        try:
            while True:
                if time.monotonic() >= deadline:
                    raise subprocess.TimeoutExpired(argv, _PRODUCTION_COMMAND_TIMEOUT)
                if not interrupted:
                    for log in set(directory.glob("*.jsonl")) - previous:
                        stat = log.stat()
                        version = (stat.st_mtime_ns, stat.st_size)
                        if scanned_versions.get(log) == version:
                            continue
                        for line in log.read_text().splitlines():
                            try:
                                event = json.loads(line)
                            except json.JSONDecodeError:
                                continue
                            if (
                                event.get("event") == "refactor_progress"
                                and event.get("confirmed", 0) > 0
                            ):
                                process.send_signal(signal.SIGINT)
                                interrupted = True
                                break
                        # 変更のない履歴を解析し直さず、partial JSON の追記は再確認する。
                        scanned_versions[log] = version
                        if interrupted:
                            break
                try:
                    stdout, stderr = process.communicate(timeout=0.1)
                    break
                except subprocess.TimeoutExpired:
                    continue
        except BaseException:
            _stop_tui_process_group(process)
            process.communicate()
            raise
    assert interrupted, "refactor ended before a confirmed unit and user interruption"
    return subprocess.CompletedProcess(argv, process.returncode, stdout, stderr)


def _codex_call_logs(root: Path) -> set[Path]:
    """repository に保存された exec/TUI call log の集合を返す。"""
    return set((root / ".cmoc" / "gu" / "log" / "codex").glob("*/*_call.json"))


def _run_with_report_review(
    cmoc: Path,
    root: Path,
    environment: dict[str, str],
    *args: str,
) -> subprocess.CompletedProcess[str]:
    """本命の agent call が不要な経路も、primary report の確認は実行する。"""
    before = _codex_call_logs(root)
    result = _run_cmoc(cmoc, root, environment, *args)
    calls = _codex_call_logs(root) - before
    assert calls
    assert {_assert_real_codex_call(path)["agent_call_kind"] for path in calls} <= {
        "build_primary_report_review_parameter",
        "build_quota_availability_probe_parameter",
    }
    return result


def _assert_real_codex_call(path: Path, *, tui: bool = False) -> dict[str, object]:
    """call log が実 CLI と agent call 固有の直接設定を記録したことを確認する。"""
    payload = json.loads(path.read_text())
    assert isinstance(payload, dict)
    raw_argv = payload.get("argv")
    assert isinstance(raw_argv, list)
    assert all(isinstance(value, str) for value in raw_argv)
    argv: list[str] = raw_argv

    assert argv[0] == "codex"
    assert argv.count("--no-daemon") == 1
    assert ("exec" in argv) is not tui
    agent_call_kind = payload["agent_call_kind"]
    assert isinstance(agent_call_kind, str)
    config = _real_path_config()
    call_config = config.codex.agent_calls[agent_call_kind]
    assert payload["model_provider"] == call_config.model_provider
    assert payload["model"] == call_config.model
    assert payload["reasoning_effort"] == call_config.reasoning_effort
    assert codex_arg_value(argv, "--model") == call_config.model
    override = codex_override_config(argv)
    assert override["sandbox_workspace_write"] == {"exclude_slash_tmp": False}
    assert "features" not in override
    if tui:
        assert "--enable" not in argv
        assert payload["prompt_log_path"] is None
        assert argv[-2:] == ["resume", payload["fixed_session_id"]]
    else:
        assert "--enable" not in argv
    assert override["model_reasoning_effort"] == call_config.reasoning_effort
    search_server = override["mcp_servers"]["cmoc_document_search"]
    if agent_call_kind in {
        "build_primary_report_review_parameter",
        "build_quota_availability_probe_parameter",
    }:
        assert search_server["enabled"] is False
    else:
        assert search_server["enabled"] is True
        search_context = json.loads(search_server["args"][-1])
        caller_log = (
            path.parents[2] / "sub_command" / f"{payload['execution_id']}.jsonl"
        )
        caller = json.loads(caller_log.read_text().splitlines()[0])
        assert search_context["log_context"] == {
            "path": str(caller_log.resolve()),
            "command": caller["command"],
            "execution_id": payload["execution_id"],
            "codex_call_id": payload["codex_call_id"],
        }
        tuning = search_context["config"]
        assert search_server["tool_timeout_sec"] > (
            tuning["search_request_timeout_seconds"] + tuning["shutdown_grace_seconds"]
        )
    provider_id = call_config.model_provider
    assert override["model_provider"] == provider_id
    providers = override.get("model_providers", {})
    assert isinstance(providers, dict)
    if config.codex.model_providers[provider_id].settings:
        assert (
            providers[provider_id] == config.codex.model_providers[provider_id].settings
        )
    feedback_server = override["mcp_servers"]["cmoc_feedback"]
    feedback_reporting_enabled = agent_call_kind not in {
        "build_feedback_normalize_issue_parameter",
        "build_feedback_remediate_issue_parameter",
        "build_primary_report_review_parameter",
        "build_quota_availability_probe_parameter",
    }
    assert feedback_server["enabled"] is feedback_reporting_enabled
    assert feedback_server["enabled_tools"] == (
        ["submit_observation"] if feedback_reporting_enabled else []
    )
    assert feedback_server["disabled_tools"] == (
        [] if feedback_reporting_enabled else ["submit_observation"]
    )
    assert feedback_server["required"] is False
    assert feedback_server["default_tools_approval_mode"] == "approve"
    assert feedback_server["env_vars"] == [
        FEEDBACK_CAPABILITY_ENV,
        FEEDBACK_COLLECTOR_PORT_ENV,
        FEEDBACK_PROTOCOL_ENV,
    ]
    if agent_call_kind in {
        "build_tui_launch_tui_parameter",
        "build_oracle_investigation_launch_tui_parameter",
    }:
        editor_input_server = override["mcp_servers"]["cmoc_editor_input"]
        assert editor_input_server["enabled_tools"] == [
            "get_handoff_guide",
            "overwrite",
        ]
        assert editor_input_server["required"] is False
        assert editor_input_server["env_vars"] == [
            EDITOR_INPUT_REPOSITORY_ENV,
            EDITOR_INPUT_SOURCE_ENV,
        ]
    else:
        assert override["mcp_servers"]["cmoc_editor_input"]["enabled"] is False
    return payload


def _is_tui_call_log(path: Path) -> bool:
    """exec ではない共通 call log を TUI の呼び出しとして判定する。"""
    payload = json.loads(path.read_text())
    argv = payload["argv"]
    return isinstance(argv, list) and "exec" not in argv


def _load_session_state(root: Path, branch: str) -> tuple[Path, dict[str, Any]]:
    """session branch に対応する外部永続 state を読み込む。"""
    session_id = branch.removeprefix("cmoc/session/")
    path = root / ".cmoc" / "gu" / "session" / f"{session_id}.json"
    state = json.loads(path.read_text())
    assert isinstance(state, dict)
    return path, state


def _completed_tui_turn(
    codex_home: Path,
    session_id: str,
    scanned_versions: dict[Path, tuple[int, int]],
    *,
    after_turn_id: str | None = None,
) -> tuple[str, str] | None:
    """指定した会話から、必要なら指定 turn より後の完了 ID と応答を探す。"""
    # exec 由来の会話を TUI resume しても session_meta.originator は変わらない。
    # https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/rollout/src/recorder.rs#L995-L1007
    for path in codex_home.glob("sessions/**/rollout-*.jsonl"):
        stat = path.stat()
        version = (stat.st_mtime_ns, stat.st_size)
        if scanned_versions.get(path) == version:
            continue
        recorded_session_id: str | None = None
        after_previous_turn = after_turn_id is None
        completed_turn: tuple[str, str] | None = None
        # TUI は polling 中にこの file を追記するため、最後の chunk が partial UTF-8
        # sequence で終わっていても、無効な session event とは限らない。
        for line in path.read_bytes().decode("utf-8", errors="ignore").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = event.get("payload")
            if event.get("type") == "session_meta" and isinstance(payload, dict):
                recorded_session_id = payload.get("id")
            if event.get("type") != "event_msg" or not isinstance(payload, dict):
                continue
            if payload.get("type") != "task_complete":
                continue
            # 現行の paginated 履歴では user_message は保存されないが、完了は残る。
            # https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/rollout/src/policy.rs#L127-L154
            turn_id = payload.get("turn_id")
            if turn_id == after_turn_id:
                after_previous_turn = True
                completed_turn = None
                continue
            value = payload.get("last_agent_message")
            if (
                after_previous_turn
                and isinstance(turn_id, str)
                and turn_id
                and isinstance(value, str)
                and value.strip()
            ):
                completed_turn = (turn_id, value)
        if recorded_session_id == session_id and completed_turn is not None:
            return completed_turn
        # 完了待ちの同じ本文を poll ごとに読み直さず、追記後は全文を再確認する。
        scanned_versions[path] = version
    return None


def _started_tui_session_id(root: Path, previous_calls: set[Path]) -> str | None:
    """今回生成された TUI process の call log から指定 UUID を得る。"""
    for path in _codex_call_logs(root) - previous_calls:
        try:
            payload = json.loads(path.read_text())
        except json.JSONDecodeError:
            # process 状態を書き換えている途中の file は次の poll で確認する。
            continue
        if "exec" not in payload["argv"] and payload.get("process_state") == "started":
            return payload["fixed_session_id"]
    return None


def _read_pty(master_fd: int, transcript: bytearray) -> bytes:
    """PTY の利用可能な出力を読み、child process の backpressure を防ぐ。"""
    received = bytearray()
    while select.select([master_fd], [], [], 0)[0]:
        try:
            chunk = os.read(master_fd, 65536)
        except OSError as exc:
            if exc.errno in {errno.EAGAIN, errno.EIO}:
                break
            raise
        if not chunk:
            break
        transcript.extend(chunk)
        received.extend(chunk)
    return bytes(received)


def _answer_terminal_queries(
    master_fd: int,
    probe_buffer: bytes,
    received: bytes,
    answered: set[bytes],
) -> bytes:
    """bare PTY の代わりに Codex TUI の端末 capability query へ応答する。"""
    # crossterm が起動時に確認する cursor position、前景色、背景色、device 属性。
    responses = {
        b"\x1b[6n": b"\x1b[1;1R",
        b"\x1b]10;?\x1b\\": b"\x1b]10;rgb:ffff/ffff/ffff\x1b\\",
        b"\x1b]11;?\x1b\\": b"\x1b]11;rgb:0000/0000/0000\x1b\\",
        b"\x1b[c": b"\x1b[?1;2c",
    }
    probe_buffer = (probe_buffer + received)[-128:]
    for query, response in responses.items():
        if query in probe_buffer and query not in answered:
            os.write(master_fd, response)
            answered.add(query)
    return probe_buffer


def _advance_trust_confirmation(
    master_fd: int,
    transcript: bytearray,
    confirmation_ready: bool,
) -> tuple[bool, bool]:
    """信頼確認 prompt の描画後の poll で Enter を一度だけ送る。"""
    if confirmation_ready:
        os.write(master_fd, b"\r")
        return True, True
    return (
        b"Press enter to continue" in transcript or b"Trust and continue" in transcript
    ), False


def _stop_tui_process_group(process: subprocess.Popen[bytes]) -> None:
    """失敗時に cmoc と、その Codex TUI child を同じ group から停止する。"""
    # start_new_session=True で作った group を leader だけ terminate すると、
    # cmoc が起動した実 Codex CLI が test 後も PTY を保持して残る可能性がある。
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, sig)
        except ProcessLookupError:
            return
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            continue
        try:
            os.killpg(process.pid, 0)
        except ProcessLookupError:
            return


def _run_cmoc_tui(
    cmoc: Path,
    root: Path,
    environment: dict[str, str],
    codex_home: Path,
    *args: str,
    input_message: str | None = None,
) -> tuple[str, str]:
    """指定した cmoc TUI 経路を PTY 上で応答完了まで実行する。"""
    # Codex TUI は terminal を必須とするため、24x100 の実 PTY を渡す。
    master_fd, slave_fd = pty.openpty()
    process: subprocess.Popen[bytes] | None = None
    slave_open = True
    transcript = bytearray()
    message: str | None = None
    scanned_versions: dict[Path, tuple[int, int]] = {}
    previous_calls = _codex_call_logs(root)
    session_id: str | None = None
    input_sent = False
    previous_turn_id: str | None = None
    composer_seen = False
    probe_buffer = b""
    answered_queries: set[bytes] = set()
    trust_confirmation_ready = False
    trust_confirmed = False
    deadline = time.monotonic() + _PRODUCTION_COMMAND_TIMEOUT
    try:
        fcntl.ioctl(slave_fd, termios.TIOCSWINSZ, struct.pack("HHHH", 24, 100, 0, 0))
        os.set_blocking(master_fd, False)
        process = subprocess.Popen(
            [str(cmoc), *args],
            cwd=root,
            env=environment,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            close_fds=True,
            start_new_session=True,
        )
        os.close(slave_fd)
        slave_open = False
        # 初回 exec の完了だけでは停止せず、同じ会話を開く TUI の描画も待つ。
        while time.monotonic() < deadline:
            received = _read_pty(master_fd, transcript)
            probe_buffer = _answer_terminal_queries(
                master_fd,
                probe_buffer,
                received,
                answered_queries,
            )
            if not trust_confirmed:
                # 描画中の入力破棄を避け、次の poll で既定の Yes を選ぶ。
                trust_confirmation_ready, trust_confirmed = _advance_trust_confirmation(
                    master_fd,
                    transcript,
                    trust_confirmation_ready,
                )
            if session_id is None:
                session_id = _started_tui_session_id(root, previous_calls)
            if session_id is not None and composer_seen:
                completed_turn = _completed_tui_turn(
                    codex_home,
                    session_id,
                    scanned_versions,
                    after_turn_id=previous_turn_id,
                )
                if completed_turn is not None:
                    if input_message is None or input_sent:
                        _turn_id, message = completed_turn
                        break
                    previous_turn_id = completed_turn[0]
                    # bracketed paste と Enter を分け、paste burst 判定で送信を落とさない。
                    os.write(
                        master_fd,
                        b"\x1b[200~" + input_message.encode() + b"\x1b[201~",
                    )
                    time.sleep(0.1)
                    os.write(master_fd, b"\r")
                    input_sent = True
            # Codex 0.162.1 の composer footer。描画検出の次の poll から操作する。
            # https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/tui/src/bottom_pane/footer.rs#L345-L351
            composer_seen = b" for shortcuts" in transcript
            if process.poll() is not None:
                break
            time.sleep(0.1)
        assert message is not None, transcript[-12000:].decode(errors="replace")

        # 1 回目で入力欄を clear、2 回目で Codex TUI を returncode 0 で終了する。
        os.write(master_fd, b"\x03")
        time.sleep(0.2)
        os.write(master_fd, b"\x03")
        returncode = process.wait(timeout=30)
        _read_pty(master_fd, transcript)
        assert returncode == 0, transcript[-12000:].decode(errors="replace")
    finally:
        if process is not None:
            _stop_tui_process_group(process)
        if slave_open:
            os.close(slave_fd)
        os.close(master_fd)
    return message, transcript.decode(errors="replace")


# {{work-root}}/oracle/doc/dev_rule/test_rule.md
# 複数の実推論と外部 provider の応答時間を case timeout に含める。
@pytest.mark.timeout(_PRODUCTION_CASE_TIMEOUT)
def test_doctor_prepares_real_search_materials_in_isolated_installation(
    tmp_path: Path, isolated_cmoc_installation: Path
) -> None:
    """起動基盤だけの installation で実モデル検証し、再実行と通常同期で再利用する。"""
    root = make_repo(tmp_path)
    cmoc, environment, _codex_home = _production_environment(
        tmp_path, isolated_cmoc_installation
    )

    first = _run_with_report_review(cmoc, root, environment, "doctor")
    first_report_path = terminal_primary_report(first.stdout)
    first_report = first_report_path.read_text(encoding="utf-8")
    assert "照合と実モデル検証: `成功`" in first_report
    assert "文書 embedding: `成功`" in first_report
    assert "query embedding: `成功`" in first_report
    report_open_log = tmp_path / "editor-bin/report-open.log"
    for _ in range(100):
        if report_open_log.is_file():
            break
        time.sleep(0.01)
    assert report_open_log.read_text(encoding="utf-8").splitlines() == [
        str(first_report_path)
    ]

    repeated = _run_with_report_review(cmoc, root, environment, "doctor")
    repeated_report = terminal_primary_report(repeated.stdout).read_text(
        encoding="utf-8"
    )
    assert "準備・再利用: `reused`" in repeated_report
    assert "実行状態: `unchanged`" in repeated_report


# {{work-root}}/oracle/doc/dev_rule/test_rule.md
# 複数の実推論と外部 provider の応答時間を case timeout に含める。
@pytest.mark.timeout(_PRODUCTION_CASE_TIMEOUT)
def test_all_noninteractive_leaf_commands_use_production_process_paths(
    tmp_path: Path,
    isolated_cmoc_installation: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """非対話の全末端を独立 process の代表正常系で完了させる。"""
    root = make_repo(tmp_path)
    _write_noninteractive_fixture_instructions(root)
    _write_real_path_config(root)
    cmoc, environment, _codex_home = _production_environment(
        tmp_path, isolated_cmoc_installation
    )
    executed_commands: set[tuple[str, ...]] = set()

    def run_production(*args: str) -> subprocess.CompletedProcess[str]:
        """実行した非対話 leaf を記録して production process を起動する。"""
        executed_commands.add(args)
        return _run_cmoc(cmoc, root, environment, *args)

    def run_with_report_review(*args: str) -> subprocess.CompletedProcess[str]:
        """確認用 call だけを実行する leaf も実行済み集合へ記録する。"""
        executed_commands.add(args)
        return _run_with_report_review(cmoc, root, environment, *args)

    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # doctor は本番 preprocess を完了してから report を確認する。
    run_with_report_review("doctor")
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert run_git(root, "ls-files", ".cmoc/gt/config.json").stdout.strip()
    assert run_git(
        root, "ls-files", ".cmoc/gt/realization/refactor/state.json"
    ).stdout.strip()

    # active session 上の各 workload を検証する。
    home_branch = current_branch(root)
    run_with_report_review("session", "fork")
    session_branch = current_branch(root)
    assert session_branch.startswith("cmoc/session/")

    # {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
    # oracle edit は同じ入力の編集を独立した exec agent call で直列実行する。
    _state_path, oracle_edit_state_before = _load_session_state(root, session_branch)
    oracle_edit_calls_before = _codex_call_logs(root)
    oracle_edit_result = run_production("oracle", "edit")
    oracle_edit_calls = _codex_call_logs(root) - oracle_edit_calls_before
    oracle_edit_payloads: dict[str, list[dict[str, object]]] = {}
    for call_path in sorted(oracle_edit_calls):
        payload = _assert_real_codex_call(call_path)
        purpose = str(payload["purpose"])
        oracle_edit_payloads.setdefault(purpose, []).append(payload)
    assert "oracle edit first" in oracle_edit_payloads
    assert "oracle edit second" in oracle_edit_payloads
    first_payload = oracle_edit_payloads["oracle edit first"][0]
    second_payload = oracle_edit_payloads["oracle edit second"][0]
    assert first_payload["agent_call_id"] != second_payload["agent_call_id"]
    assert "resume" not in first_payload["argv"]
    assert "resume" not in second_payload["argv"]

    # 各 agent call の stdin に直接渡した完全 prompt 本文を追跡する。
    first_prompt = Path(str(first_payload["prompt_log_path"])).read_text()
    assert EDITOR_PROMPT.strip() in first_prompt
    assert "{{original-prompt-here}}" not in first_prompt
    second_prompt = Path(str(second_payload["prompt_log_path"])).read_text()
    assert EDITOR_PROMPT.strip() in second_prompt
    assert second_prompt == first_prompt
    for key in (
        "agent_call_kind",
        "model_provider",
        "model",
        "reasoning_effort",
        "cwd",
    ):
        assert first_payload[key] == second_payload[key]
    for key in ("codex_call_id", "prompt_log_path", "stdout_log_path", "output_path"):
        assert first_payload[key] != second_payload[key]
    session_ids = []
    for payload in (first_payload, second_payload):
        events = Path(str(payload["stdout_log_path"])).read_text().splitlines()
        session_ids.append(
            next(
                event["thread_id"]
                for line in events
                if (event := json.loads(line)).get("type") == "thread.started"
            )
        )
    assert session_ids[0] != session_ids[1]
    _state_path, oracle_edit_state_after = _load_session_state(root, session_branch)
    assert oracle_edit_state_after == oracle_edit_state_before
    assert oracle_edit_result.stdout.count("# 完了: cmoc oracle edit") == 1
    assert "- result:" not in oracle_edit_result.stdout
    assert "- completion_reason:" not in oracle_edit_result.stdout

    feedback_report_dir = root / ".cmoc" / "gu" / "report" / "feedback"
    feedback_reports = set(feedback_report_dir.rglob("*.md"))
    # 先行する実推論が受理した pending observation があれば remediation call が
    # 発生するため、feedback report 自身も Codex を許可する production 経路で実行する。
    feedback_report_result = run_production("feedback", "report")
    feedback_report = terminal_primary_report(feedback_report_result.stdout)
    assert feedback_report not in feedback_reports
    feedback_report_text = feedback_report.read_text(encoding="utf-8")
    # 実推論の分類は固定せず、仕様が許す正常 publication または incomplete を確認する。
    assert any(
        line
        in {
            'result: "ok"',
            'result: "attention"',
            'result: "incomplete"',
        }
        for line in feedback_report_text.splitlines()
    )
    # feedback の修復 call も実 Codex で実行し、終端分類後の自動 join を検査する。
    # observation は現在性を再確認する入力であり、モデルの結論そのものは固定しない。
    store_agent_observation(
        root,
        {
            "repo_root": str(root),
            "work_root": str(root),
            "head_commit": run_git(root, "rev-parse", "HEAD").stdout.strip(),
            "cmoc_session_id": session_branch.removeprefix("cmoc/session/"),
            "run_id": None,
            "run_kind": None,
            "subcommand": "production fixture",
            "subcommand_invocation_id": "exec_000001_2026-09-29_15-04",
            "agent_call_id": "ac_000008_2026-09-29_15-04",
            "agent_call_kind": "production_fixture",
            "codex_call_id": "cc_000009_2026-09-29_15-04",
            "codex_session_id": None,
            "log_paths": [],
        },
        {
            "schema_version": 2,
            "category": "tooling",
            "severity": "low",
            "summary": "README.md の存在を再確認する必要がある。",
            "impact": "README が欠落すると repository の案内を参照できない。",
            "workload_limitation": "観測元の workload は存在確認を対象としていなかった。",
            "cause": {
                "certainty": "unknown",
                "description": "現在の tree で確認する。",
            },
            "evidence": [
                {
                    "kind": "file",
                    "path": "README.md",
                    "text": "README.md の存在が確認対象。",
                }
            ],
            "continuation": "continued",
        },
    )
    before_remediation = _codex_call_logs(root)
    run_production("feedback", "report")
    remediation_calls = [
        _assert_real_codex_call(path)
        for path in _codex_call_logs(root) - before_remediation
    ]
    remediation_calls = [
        payload
        for payload in remediation_calls
        if payload.get("agent_call_kind") == "build_feedback_remediate_issue_parameter"
    ]
    assert remediation_calls
    assert len({payload["agent_call_id"] for payload in remediation_calls}) == 1
    for payload in remediation_calls:
        assert Path(str(payload["cwd"])) != root
    _state_path, feedback_state = _load_session_state(root, session_branch)
    assert feedback_state["run"]["state"] == "ready"
    assert run_git(root, "status", "--short").stdout.strip() == ""
    # Close は agent を呼ばない。確定済み入力を別 repository に用意し、
    # 本番 entrypoint の state 更新・report・終了 code を観測する。
    close_parent = tmp_path / "close-scenario"
    close_parent.mkdir()
    close_root = make_repo(close_parent)
    _run_with_report_review(cmoc, close_root, environment, "doctor")
    history = load_active_state(root).history
    basis = next(
        event["agent_result"]["decision_basis"]
        for record in reversed(history)
        for event in record["events"]
        if event["agent_result"] is not None
    )
    case = _write_close_fixture(close_root, basis)
    executed_commands.add(("feedback", "close"))
    closed = _run_with_report_review(
        cmoc,
        close_root,
        environment,
        "feedback",
        "close",
        case,
        "--reason",
        "外部設定を修正し、解決を確認した。",
    )
    state = load_active_state(close_root)
    assert state.issues == {}
    assert state.current is not None and state.current["result"] == "ok"
    assert state.history[-1]["events"][0]["kind"] == "manual_close"
    assert case in terminal_primary_report(closed.stdout).read_text()
    assert "- result: `closed`" in closed.stdout
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # workload の正常終了は、同じ invocation での取り込みと回収まで含む。
    for command, kind in [
        (("realization", "apply"), "realization_apply"),
        (("realization", "refactor"), "realization_refactor"),
    ]:
        before_calls = _codex_call_logs(root)
        completed = run_production(*command)
        assert _codex_call_logs(root) - before_calls
        _state_path, completed_state = _load_session_state(root, session_branch)
        assert completed_state["run"] == {
            "state": "ready",
            "kind": None,
            "branch": None,
            "fork_commit": None,
        }
        report = report_metadata(terminal_primary_report(completed.stdout).read_text())
        assert report["run_kind"] == kind
        assert report["state_after"] == "ready"
        assert report["cleanup"] == "completed"
        assert not Path(report["run_worktree"]).exists()

    # 復旧用の末端には停止済み run を用意し、本番 entrypoint で機械的に終了する。
    for operation in ("join", "abandon"):
        with monkeypatch.context() as setup:
            setup.chdir(root)
            context = start_editing_run("realization_apply")
            set_run_state(context, "joinable")
        finished = run_with_report_review("run", operation)
        _state_path, ready_state = _load_session_state(root, session_branch)
        assert ready_state["run"]["state"] == "ready"
        assert not context.run_worktree.exists()
        assert "cleanup: `completed`" in finished.stdout

    # 同じ home branch で join と abandon の両 session 完了経路を観測する。
    state_path, _state = _load_session_state(root, session_branch)
    run_with_report_review("session", "join")
    assert current_branch(root) == home_branch
    assert json.loads(state_path.read_text())["session"]["state"] == "joined"
    assert run_git(root, "branch", "--list", session_branch).stdout.strip() == ""

    run_with_report_review("session", "fork")
    abandoned_session_branch = current_branch(root)
    abandoned_state_path, _state = _load_session_state(root, abandoned_session_branch)
    run_with_report_review("session", "abandon")
    assert current_branch(root) == home_branch
    assert json.loads(abandoned_state_path.read_text())["session"]["state"] == (
        "abandoned"
    )
    assert (
        run_git(root, "branch", "--list", abandoned_session_branch).stdout.strip() == ""
    )
    for call_path in _codex_call_logs(root):
        _assert_real_codex_call(call_path)
    assert executed_commands == NONINTERACTIVE_SCENARIO_COMMANDS


@pytest.mark.parametrize(("command", "tui_purpose"), TUI_SCENARIOS)
# {{work-root}}/oracle/doc/dev_rule/test_rule.md
# TUI の実推論と外部 provider の応答時間を含める。
@pytest.mark.timeout(_PRODUCTION_CASE_TIMEOUT)
def test_tui_leaf_commands_and_resume_use_real_codex_response_over_production_pty(
    tmp_path: Path,
    isolated_cmoc_installation: Path,
    command: tuple[str, ...],
    tui_purpose: str,
) -> None:
    """両 workload の新規起動と公開 resume を実応答後まで完了する。"""
    root = make_repo(tmp_path)
    _write_real_path_config(root)
    cmoc, environment, codex_home = _production_environment(
        tmp_path, isolated_cmoc_installation
    )
    _run_with_report_review(cmoc, root, environment, "doctor")
    # component 検証と doctor 同期の期限は維持し、MCP 全体期限だけを短くする。
    config = load_config(root)
    assert config.document_search is not None
    write_config(
        root / ".cmoc/gt/config.json",
        replace(
            config,
            document_search=replace(
                config.document_search, search_request_timeout_seconds=0.000001
            ),
        ),
    )
    run_git(root, "add", ".cmoc/gt/config.json")
    run_git(root, "commit", "-m", "exercise MCP deadline over live TUI connection")
    head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()
    status_before = run_git(root, "status", "--short").stdout
    calls_before = _codex_call_logs(root)
    report_root = root / ".cmoc" / "gu" / "report"
    report_snapshot_before = {
        path: path.read_bytes() if path.is_file() else None
        for path in report_root.rglob("*")
    }

    # 初回処理完了と、公開 resume 後の直接 callback を OS 通知だけ隔離して確認する。
    toast_path = tmp_path / "toast.jsonl"
    toast_bin = tmp_path / "toast-recorder"
    toast_bin.mkdir()
    write_python_executable(
        toast_bin / "powershell.exe",
        [
            "import pathlib, sys",
            f"with pathlib.Path({str(toast_path)!r}).open('a') as output:",
            "    output.write(sys.stdin.read() + '\\n')",
        ],
    )
    environment["PATH"] = f"{toast_bin}:{environment['PATH']}"

    # 実際の MCP を介して、起動元が注入する送信元情報まで受信する。
    work = root / ".cmoc/gu/log/editor_input/receiver.md"
    work.parent.mkdir(parents=True, exist_ok=True)
    work.write_text("initial")
    target = start_editor_input_handoff(
        root,
        work,
        "instructions に受信側の識別子 CMOC_GUIDE_CONFIRMED を含める。\n"
        "{{original-prompt-here}}",
    )
    handoff_instruction = (
        "人間からの明示的な依頼です。次の active target に "
        "cmoc_editor_input.get_handoff_guide でガイドを取得してから、"
        "cmoc_editor_input.overwrite を使って一度 handoff してください。\n"
        f"target ID: {target.target_id}\n"
        "goal と instructions は CMOC_HANDOFF_REQUEST、background は受け渡しの動作確認、"
        "decisions と open_questions は該当なし、oracle_references は空配列です。\n"
        "instructions にはガイドが指定する受信側の識別子も含めてください。\n"
        "handoff 後に cmoc_document_search.search を query『期限の動作確認』で一度呼び、"
        "期限超過の結果も短く報告してください。\n"
        "リポジトリのファイルは変更せず、tool の結果を短く報告してください。"
    )
    write_python_executable(
        tmp_path / "editor-bin/code",
        [
            "import pathlib, sys",
            f"pathlib.Path(sys.argv[-1]).write_text({handoff_instruction!r})",
        ],
    )
    try:
        response, transcript = _run_cmoc_tui(
            cmoc,
            root,
            environment,
            codex_home,
            *command,
        )
    finally:
        target.close()
    assert response.strip()
    assert "Shutting down" in transcript
    report_snapshot_after = {
        path: path.read_bytes() if path.is_file() else None
        for path in report_root.rglob("*")
    }
    assert report_snapshot_after == report_snapshot_before
    assert not any(
        f"# {heading}: cmoc {' '.join(command)}" in transcript
        for heading in ("完了", "中断完了", "失敗")
    )
    new_calls = _codex_call_logs(root) - calls_before
    tui_calls = {path for path in new_calls if _is_tui_call_log(path)}
    exec_calls = new_calls - tui_calls
    assert len(tui_calls) == 1
    tui_payload = _assert_real_codex_call(next(iter(tui_calls)), tui=True)
    assert tui_payload["purpose"] == tui_purpose
    assert len(exec_calls) == 1
    initial_payload = _assert_real_codex_call(next(iter(exec_calls)))
    assert initial_payload["agent_call_kind"] == tui_payload["agent_call_kind"]
    assert initial_payload["execution_id"] == tui_payload["execution_id"]
    assert initial_payload["agent_call_id"] != tui_payload["agent_call_id"]
    assert initial_payload["codex_call_id"] != tui_payload["codex_call_id"]
    assert tui_payload["initial_session_id"] == tui_payload["fixed_session_id"]
    body = work.read_text()
    assert "CMOC_GUIDE_CONFIRMED" in body, response
    assert initial_payload["codex_call_id"] in body
    # 終了済み process のログを一度だけ解析し、送信元・検索・期限の検証で共有する。
    subcommand_events = {
        path: [json.loads(line) for line in path.read_text().splitlines()]
        for path in (root / ".cmoc/gu/log/sub_command").glob("*.jsonl")
    }
    source_events = [
        (path, event)
        for path, events in subcommand_events.items()
        for event in events
        if event.get("event") == "editor_input_handoff_source"
    ]
    assert {event["codex_call_id"] for _path, event in source_events} == {
        initial_payload["codex_call_id"],
        tui_payload["codex_call_id"],
    }
    log_path, source = next(
        (path, event)
        for path, event in source_events
        if event["codex_call_id"] == initial_payload["codex_call_id"]
    )
    assert source["subcommand"] == " ".join(command)
    assert source["codex_call_id"] == initial_payload["codex_call_id"]
    assert source["sub_command_log_path"] == str(log_path.resolve())
    assert Path(source["call_log_path"]) == next(iter(exec_calls))
    assert source["execution_id"] in body
    assert str(log_path.resolve()) in body
    assert source["execution_id"] in transcript
    search_events = [
        event
        for event in subcommand_events[log_path]
        if event["event"].startswith("document_search_request_")
    ]
    assert len(search_events) == 3
    assert all(
        event["codex_call_id"] == initial_payload["codex_call_id"]
        and event["execution_id"] == source["execution_id"]
        and event["command"] == " ".join(command)
        for event in search_events
    )
    assert len({event["request_id"] for event in search_events}) == 1
    assert search_events[-1]["failure_code"] == "DEADLINE_EXCEEDED"
    deadline = next(
        event
        for event in subcommand_events[log_path]
        if event["event"] == "document_search_deadline_exceeded"
    )
    assert deadline["request_id"] == search_events[-1]["request_id"]
    assert deadline["deadline_kinds"] == ["search_request"]
    notifications = [json.loads(line) for line in toast_path.read_text().splitlines()]
    assert notifications == [
        {"title": f"cmoc {' '.join(command)}", "message": f"{root.name} — 初回処理完了"}
    ]

    # 同じ会話を公開入口から再開し、過去の完了ではなく追加入力の実応答を待つ。
    calls_before_resume = _codex_call_logs(root)
    editor_opened = tmp_path / "resume-editor-opened"
    write_python_executable(
        tmp_path / "editor-bin/code",
        [
            "import pathlib, sys",
            f"pathlib.Path({str(editor_opened)!r}).touch()",
            "sys.exit(1)",
        ],
    )
    response, transcript = _run_cmoc_tui(
        cmoc,
        root,
        environment,
        codex_home,
        *RESUME_COMMAND,
        str(tui_payload["execution_id"]),
        input_message=(
            "続きの入力です。cmoc_document_search.search を query『再開後の期限確認』で"
            "一度呼び、結果を短く報告してください。ファイルは変更しないでください。"
        ),
    )
    assert response.strip()
    assert "Shutting down" in transcript
    assert not editor_opened.exists()
    resumed_calls = _codex_call_logs(root) - calls_before_resume
    assert len(resumed_calls) == 1
    resumed_payload = _assert_real_codex_call(next(iter(resumed_calls)), tui=True)
    assert resumed_payload["resumed_from_execution_id"] == tui_payload["execution_id"]
    for key in ("execution_id", "agent_call_id", "codex_call_id"):
        assert resumed_payload[key] != tui_payload[key]
        assert resumed_payload[key] != initial_payload[key]
    for key in (
        "fixed_session_id",
        "initial_session_id",
        "agent_call_kind",
        "file_access_mode",
        "cwd",
        "codex_home",
    ):
        assert resumed_payload[key] == tui_payload[key]
    assert resumed_payload["subcommand"] == "resume"
    assert resumed_payload["process_state"] == "exited"
    assert resumed_payload["returncode"] == 0
    resumed_log = (
        root / ".cmoc/gu/log/sub_command" / f"{resumed_payload['execution_id']}.jsonl"
    )
    resumed_events = [json.loads(line) for line in resumed_log.read_text().splitlines()]
    resumed_search_events = [
        event
        for event in resumed_events
        if event["event"].startswith("document_search_request_")
    ]
    assert len(resumed_search_events) == 3
    assert all(
        event["codex_call_id"] == resumed_payload["codex_call_id"]
        and event["execution_id"] == resumed_payload["execution_id"]
        and event["command"] == "resume"
        for event in resumed_search_events
    )
    assert resumed_search_events[-1]["failure_code"] == "DEADLINE_EXCEEDED"
    assert [json.loads(line) for line in toast_path.read_text().splitlines()] == [
        *notifications,
        {"title": "cmoc resume", "message": f"{root.name} — 応答完了"},
    ]
    assert {
        path: path.read_bytes() if path.is_file() else None
        for path in report_root.rglob("*")
    } == report_snapshot_before
    assert not any(
        f"# {heading}: cmoc resume" in transcript
        for heading in ("完了", "中断完了", "失敗")
    )
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == head_before
    assert run_git(root, "status", "--short").stdout == status_before
