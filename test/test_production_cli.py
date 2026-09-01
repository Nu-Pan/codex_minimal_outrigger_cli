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

import click
import pytest
from _codex_support import (
    codex_arg_value,
    codex_override_config,
)
from _command_support import write_python_executable
from _git_support import current_branch, make_repo, run_git
from typer.main import get_command

from commons.indexing import commit_index_updates, render_index_entry
from commons.runtime_config import write_config
from commons.runtime_editor_input_handoff_protocol import EDITOR_INPUT_REPOSITORY_ENV
from commons.runtime_feedback import (
    FEEDBACK_CAPABILITY_ENV,
    FEEDBACK_COLLECTOR_PORT_ENV,
    FEEDBACK_PROTOCOL_ENV,
)
from config.cmoc_config import CmocConfig
from main import app

_WORK_ROOT = Path(__file__).resolve().parents[1]
_CMOC_CONSOLE = Path(sys.executable).with_name("cmoc")
_REAL_CODEX = shutil.which("codex")
# {{work-root}}/oracle/doc/dev_rule/test_rule.md
# 外部 provider の応答待ちを個別 command と test case の両方で局所化する。
_PRODUCTION_COMMAND_TIMEOUT = 300
_PRODUCTION_CASE_TIMEOUT = 600
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
    ("indexing",),
    ("oracle", "edit"),
    ("realization", "apply", "fork"),
    ("realization", "refactor", "fork"),
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

PRODUCTION_SCENARIO_COMMANDS = NONINTERACTIVE_SCENARIO_COMMANDS | {
    scenario[0] for scenario in TUI_SCENARIOS
}

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


def _registered_leaf_commands(
    command: click.Command, prefix: tuple[str, ...] = ()
) -> set[tuple[str, ...]]:
    """Click command tree から実行可能な末端 command path を列挙する。"""
    # 新しい公開末端の追加時に、本番経路試験の追加漏れを同じ変更で検出する。
    commands = getattr(command, "commands", None)
    if commands is not None:
        leaves: set[tuple[str, ...]] = set()
        for name, child in commands.items():
            leaves.update(_registered_leaf_commands(child, (*prefix, name)))
        return leaves
    return {prefix}


def _real_path_config() -> CmocConfig:
    """全 agent call 種別を直接テスト用設定へ対応付ける。"""
    # {{work-root}}/oracle/doc/dev_rule/test_rule.md
    # 具体的な provider/Model 名を fixture に固定せず、quota 消費を抑える既定 entry
    # の直接設定を全 agent call 種別へ適用する。
    config = CmocConfig(num_parallel=1)
    quota_saving_call = config.codex.agent_calls["build_indexing_index_entry_parameter"]
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
    write_config(root / ".cmoc" / "gt" / "ar" / "config.json", config)


def _write_noninteractive_fixture_instructions(root: Path) -> None:
    """LLM の意味判断を試験対象から外す fixture instruction を追加する。"""
    # {{work-root}}/oracle/doc/dev_rule/test_rule.md
    # 本番経路との差として許される決定論的入力で、cmoc の制御だけを検証する。
    (root / "AGENTS.md").write_text(
        """# Production-path test fixture

This is an intentionally minimal and internally consistent test repository.
For a realization-refactor file review, report `findings` as an empty array and
do not modify files. For every other call, follow its explicit prompt exactly.
"""
    )
    run_git(root, "add", "AGENTS.md")
    run_git(root, "commit", "-m", "add deterministic agent instructions")


def _write_fresh_index_fixture(root: Path) -> None:
    """TUI 本体と無関係な INDEX.md を、実推論なしで最新状態へ準備する。"""

    # {{work-root}}/oracle/doc/dev_rule/test_rule.md
    # {{work-root}}/oracle/doc/app_spec/indexing.md
    # indexing 末端の実推論は非対話 scenario で検証する。TUI case は valid な
    # INDEX.md を直接用意し、TUI 自身の実推論を Codex callback で置き換えない。
    entry = {
        "summary": ["Minimal production-path test fixture."],
        "read_this_when": ["Testing the isolated production path."],
        "do_not_read_this_when": ["Working outside this fixture."],
    }
    oracle_index = root / "oracle" / "INDEX.md"
    oracle_index.write_text(
        render_index_entry(root, root / "oracle" / "spec.md", entry)
    )
    root_index = root / "INDEX.md"
    root_index.write_text(
        "\n\n".join(
            [
                render_index_entry(root, root / "README.md", entry).rstrip(),
                render_index_entry(root, root / "oracle", entry).rstrip(),
            ]
        )
        + "\n"
    )
    commit_index_updates(root, [oracle_index, root_index])


def _source_codex_home() -> Path:
    """実経路テスト開始時の Codex 認証情報の配置元を返す。"""
    configured = os.environ.get("CODEX_HOME")
    path = Path(configured) if configured is not None else Path.home() / ".codex"
    return path if path.is_absolute() else (_WORK_ROOT / path).resolve()


def _production_environment(
    tmp_path: Path,
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
    write_python_executable(
        editor_dir / "code",
        [
            "import pathlib, sys",
            f"pathlib.Path(sys.argv[-1]).write_text({EDITOR_PROMPT!r})",
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
                str(_WORK_ROOT / "src"),
                str(_WORK_ROOT / "oracle" / "src"),
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


def _codex_call_logs(root: Path) -> set[Path]:
    """repository に保存された exec/TUI call log の集合を返す。"""
    return set((root / ".cmoc" / "gu" / "ar" / "log" / "codex").glob("*_call.json"))


def _run_without_codex_call(
    cmoc: Path,
    root: Path,
    environment: dict[str, str],
    *args: str,
) -> subprocess.CompletedProcess[str]:
    """Codex 不要の代表正常系が予期せず agent call しないことも確認する。"""
    before = _codex_call_logs(root)
    result = _run_cmoc(cmoc, root, environment, *args)
    assert _codex_call_logs(root) == before
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
    assert "sandbox_workspace_write" not in override
    assert "features" not in override
    assert override["model_reasoning_effort"] == call_config.reasoning_effort
    provider_id = call_config.model_provider
    assert override["model_provider"] == provider_id
    providers = override.get("model_providers", {})
    assert isinstance(providers, dict)
    if config.codex.model_providers[provider_id].settings:
        assert (
            providers[provider_id] == config.codex.model_providers[provider_id].settings
        )
    feedback_server = override["mcp_servers"]["cmoc_feedback"]
    assert feedback_server["enabled_tools"] == ["submit_observation"]
    assert feedback_server["required"] is False
    assert feedback_server["default_tools_approval_mode"] == "approve"
    assert feedback_server["env_vars"] == [
        FEEDBACK_CAPABILITY_ENV,
        FEEDBACK_COLLECTOR_PORT_ENV,
        FEEDBACK_PROTOCOL_ENV,
    ]
    if tui:
        editor_input_server = override["mcp_servers"]["cmoc_editor_input"]
        assert editor_input_server["enabled_tools"] == ["overwrite"]
        assert editor_input_server["required"] is False
        assert editor_input_server["env_vars"] == [EDITOR_INPUT_REPOSITORY_ENV]
    else:
        assert "cmoc_editor_input" not in override["mcp_servers"]
    return payload


def _is_tui_call_log(path: Path) -> bool:
    """exec ではない共通 call log を TUI の呼び出しとして判定する。"""
    payload = json.loads(path.read_text())
    argv = payload["argv"]
    return isinstance(argv, list) and "exec" not in argv


def _load_session_state(root: Path, branch: str) -> tuple[Path, dict[str, Any]]:
    """session branch に対応する外部永続 state を読み込む。"""
    session_id = branch.removeprefix("cmoc/session/")
    path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    state = json.loads(path.read_text())
    assert isinstance(state, dict)
    return path, state


def _run_worktree_from_state(root: Path, state: dict[str, Any]) -> Path:
    """共通 run branch 名から仕様上の managed worktree path を復元する。"""
    branch = state["run"]["branch"]
    assert isinstance(branch, str)
    parts = branch.split("/")
    assert len(parts) == 4 and parts[:2] == ["cmoc", "run"]
    return root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]


def _completed_tui_message(codex_home: Path) -> str | None:
    """Codex TUI session が保存した完了済み assistant response を探す。"""
    # session file の originator で resolver の `codex exec` と TUI を区別する。
    for path in codex_home.glob("sessions/**/rollout-*.jsonl"):
        originator: str | None = None
        completed_message: str | None = None
        # TUI は polling 中にこの file を追記するため、最後の chunk が partial UTF-8
        # sequence で終わっていても、無効な session event とは限らない。
        for line in path.read_bytes().decode("utf-8", errors="ignore").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = event.get("payload")
            if event.get("type") == "session_meta" and isinstance(payload, dict):
                value = payload.get("originator")
                originator = value if isinstance(value, str) else None
            if event.get("type") != "event_msg" or not isinstance(payload, dict):
                continue
            if payload.get("type") != "task_complete":
                continue
            value = payload.get("last_agent_message")
            if isinstance(value, str) and value.strip():
                completed_message = value
        if originator == "codex-tui" and completed_message is not None:
            return completed_message
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
    return b"Press enter to continue" in transcript, False


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
) -> tuple[str, str]:
    """指定した cmoc TUI 経路を PTY 上で応答完了まで実行する。"""
    # Codex TUI は terminal を必須とするため、24x100 の実 PTY を渡す。
    master_fd, slave_fd = pty.openpty()
    process: subprocess.Popen[bytes] | None = None
    slave_open = True
    transcript = bytearray()
    message: str | None = None
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
        # TUI session の永続 event で、stream 表示ではなく応答完了を判定する。
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
            message = _completed_tui_message(codex_home)
            if message is not None:
                break
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
def test_all_noninteractive_leaf_commands_use_production_process_paths(
    tmp_path: Path,
) -> None:
    """非対話の全末端を独立 process の代表正常系で完了させる。"""
    # CLI 登録と固定シナリオを比較し、新しい末端 command の追加漏れを検出する。
    assert _registered_leaf_commands(get_command(app)) == PRODUCTION_SCENARIO_COMMANDS
    root = make_repo(tmp_path)
    _write_noninteractive_fixture_instructions(root)
    _write_real_path_config(root)
    cmoc, environment, _codex_home = _production_environment(tmp_path)
    executed_commands: set[tuple[str, ...]] = set()

    def run_production(*args: str) -> subprocess.CompletedProcess[str]:
        """実行した非対話 leaf を記録して production process を起動する。"""
        executed_commands.add(args)
        return _run_cmoc(cmoc, root, environment, *args)

    def run_without_codex(*args: str) -> subprocess.CompletedProcess[str]:
        """Codex 不要の leaf も実行済み集合へ記録する。"""
        executed_commands.add(args)
        return _run_without_codex_call(cmoc, root, environment, *args)

    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # doctor は provider lifecycle に触れず本番 preprocess を完了する。
    run_without_codex("doctor")
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert run_git(root, "ls-files", ".cmoc/gt/ar/config.json").stdout.strip()
    assert run_git(
        root, "ls-files", ".cmoc/gt/ar/realization/refactor/state.json"
    ).stdout.strip()

    # indexing は実推論 response を INDEX.md と commit に反映する。
    before_indexing_calls = _codex_call_logs(root)
    run_production("indexing")
    indexing_calls = _codex_call_logs(root) - before_indexing_calls
    assert indexing_calls
    latest_output_by_purpose: dict[str, Path] = {}
    for path in sorted(indexing_calls):
        payload = _assert_real_codex_call(path)
        purpose = str(payload.get("purpose", ""))
        assert purpose.startswith("indexing index entry for ")
        latest_output_by_purpose[purpose] = Path(str(payload["output_path"]))
    # LLM 品質は non-goal。失敗 attempt の log も残るため、retry 後の最終応答を検証する。
    for output_path in latest_output_by_purpose.values():
        assert output_path.is_file()
        assert json.loads(output_path.read_text())
    assert (root / "INDEX.md").is_file()
    assert run_git(root, "log", "-1", "--pretty=%s").stdout.strip() == "cmoc indexing"
    assert run_git(root, "status", "--short").stdout.strip() == ""

    # active session 上の各 workload を検証する。
    home_branch = current_branch(root)
    run_without_codex("session", "fork")
    session_branch = current_branch(root)
    assert session_branch.startswith("cmoc/session/")

    # {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
    # oracle edit は本命と仕様削減を別の exec agent call として直列実行する。
    _state_path, oracle_edit_state_before = _load_session_state(root, session_branch)
    oracle_edit_calls_before = _codex_call_logs(root)
    oracle_edit_result = run_production("oracle", "edit")
    oracle_edit_calls = _codex_call_logs(root) - oracle_edit_calls_before
    oracle_edit_payloads: dict[str, list[dict[str, object]]] = {}
    for call_path in sorted(oracle_edit_calls):
        payload = _assert_real_codex_call(call_path)
        purpose = str(payload["purpose"])
        oracle_edit_payloads.setdefault(purpose, []).append(payload)
    assert "oracle edit main" in oracle_edit_payloads
    assert "oracle edit reduction" in oracle_edit_payloads
    main_payload = oracle_edit_payloads["oracle edit main"][0]
    reduction_payload = oracle_edit_payloads["oracle edit reduction"][0]
    assert main_payload["agent_call_id"] != reduction_payload["agent_call_id"]
    assert "resume" not in main_payload["argv"]
    assert "resume" not in reduction_payload["argv"]

    # 各 agent call の stdin に直接渡した完全 prompt 本文を追跡する。
    main_prompt = Path(str(main_payload["prompt_log_path"])).read_text()
    assert EDITOR_PROMPT.strip() in main_prompt
    assert "{{original-prompt-here}}" not in main_prompt
    reduction_prompt = Path(str(reduction_payload["prompt_log_path"])).read_text()
    assert EDITOR_PROMPT.strip() in reduction_prompt
    assert "# 仕様削減の判断条件" in reduction_prompt
    _state_path, oracle_edit_state_after = _load_session_state(root, session_branch)
    assert oracle_edit_state_after == oracle_edit_state_before
    assert oracle_edit_result.stdout.count("# 完了: cmoc oracle edit") == 1
    assert "- result:" not in oracle_edit_result.stdout
    assert "- completion_reason:" not in oracle_edit_result.stdout

    feedback_report_dir = root / ".cmoc" / "gu" / "ar" / "report" / "feedback"
    feedback_reports = set(feedback_report_dir.glob("*.md"))
    run_without_codex("feedback", "report")
    feedback_report = next(
        iter(set(feedback_report_dir.glob("*.md")) - feedback_reports)
    )
    assert 'result: "ok"' in feedback_report.read_text()
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # 2 workload と共通 join/abandon を本番 Codex 経路で観測する。
    for command, kind in [
        (("realization", "apply", "fork"), "realization_apply"),
        (("realization", "refactor", "fork"), "realization_refactor"),
    ]:
        before_calls = _codex_call_logs(root)
        run_production(*command)
        assert _codex_call_logs(root) - before_calls
        _state_path, completed_state = _load_session_state(root, session_branch)
        assert completed_state["run"]["state"] == "joinable"
        assert completed_state["run"]["kind"] == kind
        joined_worktree = _run_worktree_from_state(root, completed_state)
        assert joined_worktree.is_dir()
        run_without_codex("run", "join")
        _state_path, joined_state = _load_session_state(root, session_branch)
        assert joined_state["run"] == {
            "state": "ready",
            "kind": None,
            "branch": None,
            "fork_commit": None,
        }
        assert not joined_worktree.exists()

    run_production("realization", "apply", "fork")
    _state_path, abandoned_state = _load_session_state(root, session_branch)
    abandoned_worktree = _run_worktree_from_state(root, abandoned_state)
    abandon_result = run_without_codex("run", "abandon")
    _state_path, ready_state = _load_session_state(root, session_branch)
    assert ready_state["run"]["state"] == "ready"
    assert not abandoned_worktree.exists()
    assert "cleanup: `completed`" in abandon_result.stdout

    # 同じ home branch で join と abandon の両 session 完了経路を観測する。
    state_path, _state = _load_session_state(root, session_branch)
    run_without_codex("session", "join")
    assert current_branch(root) == home_branch
    assert json.loads(state_path.read_text())["session"]["state"] == "joined"
    assert run_git(root, "branch", "--list", session_branch).stdout.strip() == ""

    run_without_codex("session", "fork")
    abandoned_session_branch = current_branch(root)
    abandoned_state_path, _state = _load_session_state(root, abandoned_session_branch)
    run_without_codex("session", "abandon")
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
def test_tui_leaf_commands_use_real_codex_response_over_production_pty(
    tmp_path: Path,
    command: tuple[str, ...],
    tui_purpose: str,
) -> None:
    """全 TUI 末端を実 Codex response 後まで本番経路で完了する。"""
    root = make_repo(tmp_path)
    _write_real_path_config(root)
    cmoc, environment, codex_home = _production_environment(tmp_path)
    _run_without_codex_call(cmoc, root, environment, "doctor")
    _write_fresh_index_fixture(root)
    head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()
    status_before = run_git(root, "status", "--short").stdout
    calls_before = _codex_call_logs(root)

    # editor 自動化以外は、本番と同じ TUI、Codex executable、provider を使う。
    response, transcript = _run_cmoc_tui(
        cmoc,
        root,
        environment,
        codex_home,
        *command,
    )
    assert response.strip()
    assert "Shutting down" in transcript
    new_calls = _codex_call_logs(root) - calls_before
    tui_calls = {path for path in new_calls if _is_tui_call_log(path)}
    exec_calls = new_calls - tui_calls
    assert len(tui_calls) == 1
    tui_payload = _assert_real_codex_call(next(iter(tui_calls)), tui=True)
    assert tui_payload["purpose"] == tui_purpose
    assert not exec_calls
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == head_before
    assert run_git(root, "status", "--short").stdout == status_before
