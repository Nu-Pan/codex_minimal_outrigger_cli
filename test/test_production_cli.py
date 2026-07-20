"""全末端サブコマンドを利用者向け entrypoint の本番経路で検証する。

独立 process、実 Codex CLI、case-local Ollama を使用し、CLI の終了 code と
外部から観測できる report・state・Git・call log を確認する。LLM の回答品質は
判定せず、応答を受けた後の cmoc の制御だけを検証対象にする。

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
import struct
import subprocess
import sys
import termios
import time
from dataclasses import replace
from pathlib import Path
from typing import Any, Iterator

import click
import pytest
from _codex_support import codex_arg_value, codex_override_config
from _command_support import write_python_executable
from _git_support import current_branch, make_repo, run_git
from _ollama_support import (
    TEST_SLM_MODEL,
    LocalOllama,
    local_ollama,
    use_test_local_ollama,
)
from typer.main import get_command

from basic.acp import ReasoningEffort
from commons.runtime_config import write_config
from config.cmoc_config import CmocConfig
from main import app

_CMOC_CONSOLE = Path(sys.executable).with_name("cmoc")
_REAL_CODEX = shutil.which("codex")
pytestmark = pytest.mark.skipif(
    not _CMOC_CONSOLE.is_file() or _REAL_CODEX is None,
    reason="production process test requires installed cmoc and real Codex CLI",
)

PRODUCTION_SCENARIO_COMMANDS = {
    ("doctor",),
    ("indexing",),
    ("oracle", "edit"),
    ("oracle", "investigation"),
    ("oracle", "review"),
    ("realization", "apply", "fork"),
    ("realization", "refactor", "fork"),
    ("run", "abandon"),
    ("run", "join"),
    ("session", "abandon"),
    ("session", "fork"),
    ("session", "join"),
    ("tui",),
}

TUI_PROMPT = """# 目的

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


@pytest.fixture
def ollama_instance(tmp_path: Path) -> Iterator[LocalOllama]:
    """test case ごとに専用 Ollama process group を起動する。"""
    with local_ollama(tmp_path) as instance:
        yield instance


def _write_local_slm_config(root: Path, ollama: LocalOllama) -> None:
    """全 model class を case-local test provider の SLM へ向ける。"""
    # {{work-root}}/oracle/doc/dev_rule/test_rule.md
    # 回答品質に依存せず短時間で制御経路を検証するため、推論強度も low に固定する。
    config = use_test_local_ollama(CmocConfig(num_parallel=1), ollama)
    config = replace(
        config,
        codex=replace(
            config.codex,
            reasoning_effort={effort: "low" for effort in ReasoningEffort},
        ),
        oracle_review=replace(
            config.oracle_review,
            num_enumerate_findings_loop=1,
            num_merge_findings_loop=1,
            num_validate_findings_loop=1,
        ),
    )
    write_config(root / ".cmoc" / "gt" / "ar" / "config.json", config)


def _write_noninteractive_fixture_instructions(root: Path) -> None:
    """SLM の意味判断を試験対象から外す fixture instruction を追加する。"""
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


def _production_environment(
    tmp_path: Path,
) -> tuple[Path, dict[str, str], Path]:
    """実 CLI と隔離済み Codex home を使う subprocess 環境を準備する。"""
    assert _CMOC_CONSOLE.is_file()
    assert _REAL_CODEX is not None
    cmoc = _CMOC_CONSOLE
    real_codex = _REAL_CODEX

    # Codex の利用者 session/config と test session を混ぜない。
    codex_home = tmp_path / "codex-home"
    codex_home.mkdir()
    editor_dir = tmp_path / "editor-bin"
    editor_dir.mkdir()
    write_python_executable(
        editor_dir / "code",
        [
            "import pathlib, sys",
            f"pathlib.Path(sys.argv[-1]).write_text({TUI_PROMPT!r})",
        ],
    )
    environment = {
        **os.environ,
        "CODEX_HOME": str(codex_home),
        "OPENAI_API_KEY": "cmoc-local-test",
        "NO_PROXY": "127.0.0.1,localhost",
        "no_proxy": "127.0.0.1,localhost",
        "PATH": f"{editor_dir}:{os.environ.get('PATH', '')}",
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
        timeout=180,
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


def _assert_local_codex_call(
    path: Path, ollama: LocalOllama, *, tui: bool = False
) -> dict[str, object]:
    """call log が実 CLI と case-local provider argv を記録したことを確認する。"""
    payload = json.loads(path.read_text())
    assert isinstance(payload, dict)
    raw_argv = payload.get("argv")
    assert isinstance(raw_argv, list)
    assert all(isinstance(value, str) for value in raw_argv)
    argv: list[str] = raw_argv

    assert argv[0] == "codex"
    assert ("exec" in argv) is not tui
    assert codex_arg_value(argv, "--model") == TEST_SLM_MODEL
    override = codex_override_config(argv)
    assert "sandbox_workspace_write" not in override
    assert "features" not in override
    assert override["model_provider"] == ollama.provider_id
    providers = override["model_providers"]
    assert isinstance(providers, dict)
    assert providers[ollama.provider_id] == {
        "name": "test-local Ollama",
        "base_url": f"http://{ollama.host}/v1",
        "wire_api": "responses",
    }
    return payload


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
        for line in path.read_text().splitlines():
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
    transcript = bytearray()
    message: str | None = None
    probe_buffer = b""
    answered_queries: set[bytes] = set()
    trust_confirmed = False
    deadline = time.monotonic() + 180
    try:
        # TUI session の永続 event で、stream 表示ではなく応答完了を判定する。
        while time.monotonic() < deadline:
            received = _read_pty(master_fd, transcript)
            probe_buffer = _answer_terminal_queries(
                master_fd,
                probe_buffer,
                received,
                answered_queries,
            )
            if not trust_confirmed and b"Press enter to continue" in transcript:
                # 隔離した test repository の初回 trust prompt は既定の Yes を選ぶ。
                os.write(master_fd, b"\r")
                trust_confirmed = True
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
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        os.close(master_fd)
    return message, transcript.decode(errors="replace")


@pytest.mark.timeout(3600)
def test_all_noninteractive_leaf_commands_use_production_process_paths(
    tmp_path: Path,
    ollama_instance: LocalOllama,
) -> None:
    """非対話の全末端を独立 process の代表正常系で完了させる。"""
    # CLI 登録と固定シナリオを比較し、新しい末端 command の追加漏れを検出する。
    assert _registered_leaf_commands(get_command(app)) == PRODUCTION_SCENARIO_COMMANDS
    root = make_repo(tmp_path)
    _write_noninteractive_fixture_instructions(root)
    _write_local_slm_config(root, ollama_instance)
    cmoc, environment, _codex_home = _production_environment(tmp_path)

    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # doctor は provider lifecycle に触れず本番 preprocess を完了する。
    _run_without_codex_call(cmoc, root, environment, "doctor")
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert run_git(root, "ls-files", ".cmoc/gt/ar/config.json").stdout.strip()
    assert run_git(
        root, "ls-files", ".cmoc/gt/ar/realization/refactor/state.json"
    ).stdout.strip()

    # indexing は実推論 response を INDEX.md と commit に反映する。
    before_indexing_calls = _codex_call_logs(root)
    _run_cmoc(cmoc, root, environment, "indexing")
    indexing_calls = _codex_call_logs(root) - before_indexing_calls
    assert indexing_calls
    for path in indexing_calls:
        payload = _assert_local_codex_call(path, ollama_instance)
        assert str(payload.get("purpose", "")).startswith("indexing index entry for ")
        output_path = Path(str(payload["output_path"]))
        assert output_path.is_file()
        assert json.loads(output_path.read_text())
    assert (root / "INDEX.md").is_file()
    assert run_git(root, "log", "-1", "--pretty=%s").stdout.strip() == "cmoc indexing"
    assert run_git(root, "status", "--short").stdout.strip() == ""

    # active session 上の no-target review も report を生成する正常系である。
    home_branch = current_branch(root)
    _run_without_codex_call(cmoc, root, environment, "session", "fork")
    session_branch = current_branch(root)
    assert session_branch.startswith("cmoc/session/")
    review_dir = root / ".cmoc" / "gu" / "ar" / "report" / "oracle_review"
    review_reports = set(review_dir.glob("*.md"))
    _run_without_codex_call(cmoc, root, environment, "oracle", "review")
    review_report = next(iter(set(review_dir.glob("*.md")) - review_reports))
    assert "result: no_targets" in review_report.read_text()
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # 2 workload と共通 join/abandon を本番 Codex 経路で観測する。
    for command, kind in [
        (("realization", "apply", "fork"), "realization_apply"),
        (("realization", "refactor", "fork"), "realization_refactor"),
    ]:
        before_calls = _codex_call_logs(root)
        _run_cmoc(cmoc, root, environment, *command)
        assert _codex_call_logs(root) - before_calls
        _state_path, completed_state = _load_session_state(root, session_branch)
        assert completed_state["run"]["state"] == "joinable"
        assert completed_state["run"]["kind"] == kind
        joined_worktree = _run_worktree_from_state(root, completed_state)
        assert joined_worktree.is_dir()
        _run_cmoc(cmoc, root, environment, "run", "join")
        _state_path, joined_state = _load_session_state(root, session_branch)
        assert joined_state["run"] == {
            "state": "ready",
            "kind": None,
            "branch": None,
            "fork_commit": None,
        }
        assert not joined_worktree.exists()

    _run_cmoc(cmoc, root, environment, "realization", "apply", "fork")
    _state_path, abandoned_state = _load_session_state(root, session_branch)
    abandoned_worktree = _run_worktree_from_state(root, abandoned_state)
    abandon_result = _run_without_codex_call(cmoc, root, environment, "run", "abandon")
    _state_path, ready_state = _load_session_state(root, session_branch)
    assert ready_state["run"]["state"] == "ready"
    assert not abandoned_worktree.exists()
    assert "cleanup: `completed`" in abandon_result.stdout

    # 同じ home branch で join と abandon の両 session 完了経路を観測する。
    state_path, _state = _load_session_state(root, session_branch)
    _run_without_codex_call(cmoc, root, environment, "session", "join")
    assert current_branch(root) == home_branch
    assert json.loads(state_path.read_text())["session"]["state"] == "joined"
    assert run_git(root, "branch", "--list", session_branch).stdout.strip() == ""

    _run_without_codex_call(cmoc, root, environment, "session", "fork")
    abandoned_session_branch = current_branch(root)
    abandoned_state_path, _state = _load_session_state(root, abandoned_session_branch)
    _run_without_codex_call(cmoc, root, environment, "session", "abandon")
    assert current_branch(root) == home_branch
    assert json.loads(abandoned_state_path.read_text())["session"]["state"] == (
        "abandoned"
    )
    assert (
        run_git(root, "branch", "--list", abandoned_session_branch).stdout.strip() == ""
    )


@pytest.mark.parametrize(
    ("command", "tui_purpose", "expects_resolver"),
    [
        (("tui",), "tui codex", True),
        (("oracle", "edit"), "oracle edit", False),
        (("oracle", "investigation"), "oracle investigation", False),
    ],
)
@pytest.mark.timeout(3600)
def test_tui_leaf_commands_use_real_codex_response_over_production_pty(
    tmp_path: Path,
    ollama_instance: LocalOllama,
    command: tuple[str, ...],
    tui_purpose: str,
    expects_resolver: bool,
) -> None:
    """全 TUI 末端を実 local SLM response 後まで本番経路で完了する。"""
    root = make_repo(tmp_path)
    _write_local_slm_config(root, ollama_instance)
    cmoc, environment, codex_home = _production_environment(tmp_path)
    _run_without_codex_call(cmoc, root, environment, "doctor")
    _run_cmoc(cmoc, root, environment, "indexing")
    # oracle edit も同じ TUI harness で検証できる active main-worktree session を作る。
    _run_without_codex_call(cmoc, root, environment, "session", "fork")
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
    tui_calls = {path for path in new_calls if path.name.endswith("_tui_call.json")}
    exec_calls = new_calls - tui_calls
    assert len(tui_calls) == 1
    tui_payload = _assert_local_codex_call(
        next(iter(tui_calls)), ollama_instance, tui=True
    )
    assert tui_payload["purpose"] == tui_purpose
    has_tui_resolver = any(
        _assert_local_codex_call(path, ollama_instance).get("purpose")
        == "tui resolve parameter"
        for path in exec_calls
    )
    assert has_tui_resolver is expects_resolver
    assert bool(exec_calls) is expects_resolver
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == head_before
    assert run_git(root, "status", "--short").stdout == status_before
