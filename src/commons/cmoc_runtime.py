import hashlib
import json
import os
import shutil
import subprocess
import threading
import time
import traceback
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import validate

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from basic.path_model import resolve_repo_root, resolve_work_root
from config.cmoc_config import (
    CmocConfig,
    CmocConfigApplyFork,
    CmocConfigCodex,
    CmocConfigReviewOracle,
)

MANAGED_BRANCH_PREFIXES = ("cmoc/session/", "cmoc/apply/", "cmoc/run/")
_CURRENT_SUBCOMMAND_LOGGER: ContextVar["SubcommandLogger | None"] = ContextVar(
    "CURRENT_SUBCOMMAND_LOGGER",
    default=None,
)
_QUOTA_CONDITION = threading.Condition()
_QUOTA_POLLING = False


class CmocError(RuntimeError):
    def __init__(self, summary: str, next_actions: list[str], detail: str):
        super().__init__(summary)
        self.summary = summary
        self.next_actions = next_actions
        self.detail = detail


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class CodexExecResult:
    returncode: int
    output_text: str
    output_json: Any
    call_log_path: Path
    stdout_log_path: Path
    stderr_log_path: Path
    output_path: Path
    codex_home: Path
    profile_name: str
    profile_path: Path
    schema_path: Path | None
    elapsed_sec: float = 0.0
    quota_wait_sec: float = 0.0
    quota_polls: int = 0


class SubcommandLogger:
    def __init__(self, root: Path, command: str):
        self.root = root
        self.command = command
        self.started_at = time.perf_counter()
        self.quota_wait_sec = 0.0
        self.path = logs_dir(root) / f"{timestamp()}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def event(self, kind: str, **payload: Any) -> None:
        record = {
            "event": kind,
            "command": self.command,
            "timestamp": datetime.now().isoformat(),
            **payload,
        }
        with self.path.open("a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()

    def elapsed(self) -> float:
        return time.perf_counter() - self.started_at

    def add_quota_wait(self, seconds: float) -> None:
        self.quota_wait_sec += seconds


def set_current_subcommand_logger(logger: SubcommandLogger | None):
    return _CURRENT_SUBCOMMAND_LOGGER.set(logger)


def reset_current_subcommand_logger(token) -> None:
    _CURRENT_SUBCOMMAND_LOGGER.reset(token)


def current_subcommand_logger() -> SubcommandLogger | None:
    return _CURRENT_SUBCOMMAND_LOGGER.get()


@dataclass
class SessionPart:
    state: str = "active"
    session_home_branch: str | None = None
    session_start_commit: str | None = None
    last_joined_apply_oracle_snapshot_commit: str | None = None
    joined_at: str | None = None


@dataclass
class ApplyPart:
    state: str = "ready"
    apply_branch: str | None = None
    oracle_snapshot_commit: str | None = None


@dataclass
class SessionState:
    session: SessionPart = field(default_factory=SessionPart)
    apply: ApplyPart = field(default_factory=ApplyPart)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SessionState":
        session_data = {
            key: value
            for key, value in data.get("session", {}).items()
            if key in SessionPart.__dataclass_fields__
        }
        apply_data = {
            key: value
            for key, value in data.get("apply", {}).items()
            if key in ApplyPart.__dataclass_fields__
        }
        return cls(
            session=SessionPart(**session_data),
            apply=ApplyPart(**apply_data),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_git(args: list[str], cwd: Path, check: bool = True) -> CommandResult:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
    )
    command_result = CommandResult(result.returncode, result.stdout, result.stderr)
    if check and result.returncode != 0:
        raise CmocError(
            "git コマンドが失敗しました。",
            ["git の状態を確認してから、同じ cmoc コマンドを再実行してください。"],
            f"command: git {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
    return command_result


def repo_root(cwd: Path | None = None) -> Path:
    try:
        return resolve_repo_root(cwd)
    except ValueError as exc:
        raise CmocError(
            "<repo-root> を特定できません。",
            ["git repository 内から cmoc を再実行してください。"],
            str(cwd or Path.cwd()),
        ) from exc


def work_root(cwd: Path | None = None) -> Path:
    try:
        return resolve_work_root(cwd)
    except ValueError as exc:
        raise CmocError(
            "<work-root> を特定できません。",
            ["git worktree 内から cmoc を再実行してください。"],
            str(cwd or Path.cwd()),
        ) from exc


def current_branch(root: Path) -> str:
    result = run_git(["branch", "--show-current"], root)
    branch = result.stdout.strip()
    if not branch:
        raise CmocError(
            "detached HEAD 上では実行できません。",
            ["通常の local branch に checkout してから再実行してください。"],
            "git branch --show-current が空文字を返しました。",
        )
    return branch


def head_commit(root: Path) -> str:
    return run_git(["rev-parse", "HEAD"], root).stdout.strip()


def require_clean_worktree(root: Path) -> None:
    status = run_git(["status", "--short"], root).stdout.strip()
    if status:
        raise CmocError(
            "git 未コミット差分が存在します。",
            ["差分を commit または退避してから再実行してください。"],
            status,
        )


def is_managed_branch(branch: str) -> bool:
    return branch.startswith(MANAGED_BRANCH_PREFIXES)


def branch_exists(root: Path, branch: str) -> bool:
    return run_git(["rev-parse", "--verify", branch], root, check=False).returncode == 0


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M_%S_%f000")


def console_timestamp() -> str:
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]


def format_duration(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = seconds - hours * 3600 - minutes * 60
    return f"{hours:2d}h {minutes:2d}m {sec:04.1f}s"


def sessions_dir(root: Path) -> Path:
    return root / ".cmoc" / "sessions"


def reports_dir(root: Path, command: str) -> Path:
    return root / ".cmoc" / "reports" / command


def logs_dir(root: Path) -> Path:
    return root / ".cmoc" / "log" / "sub_command"


def worktrees_dir(root: Path) -> Path:
    return root / ".cmoc" / "worktrees"


def codex_log_dir(root: Path) -> Path:
    return root / ".cmoc" / "log" / "codex"


def schema_store_dir(root: Path) -> Path:
    return root / ".cmoc" / "state" / "schema"


def config_path(root: Path) -> Path:
    return root / ".cmoc" / "config.json"


def config_to_dict(config: CmocConfig) -> dict[str, Any]:
    return {
        "num_parallel": config.num_parallel,
        "codex": {
            "model": {
                key.value: value
                for key, value in sorted(
                    config.codex.model.items(), key=lambda item: item[0].value
                )
            },
            "reasoning_effort": {
                key.value: value
                for key, value in sorted(
                    config.codex.reasoning_effort.items(),
                    key=lambda item: item[0].value,
                )
            },
        },
        "apply_fork": {
            "num_apply_loop": config.apply_fork.num_apply_loop,
            "num_improve_findings_loop": config.apply_fork.num_improve_findings_loop,
        },
        "review_oracle": {
            "num_enumerate_findings_loop": config.review_oracle.num_enumerate_findings_loop,
            "num_merge_findings_loop": config.review_oracle.num_merge_findings_loop,
            "num_validate_findings_loop": config.review_oracle.num_validate_findings_loop,
        },
    }


def config_from_dict(data: dict[str, Any]) -> CmocConfig:
    default = CmocConfig()
    try:
        codex_data = data.get("codex", {})
        if not isinstance(codex_data, dict):
            codex_data = {}
        model = dict(default.codex.model)
        model_data = codex_data.get("model", {})
        if isinstance(model_data, dict):
            for key, value in model_data.items():
                model[ModelClass(key)] = str(value)
        reasoning_effort = dict(default.codex.reasoning_effort)
        reasoning_data = codex_data.get("reasoning_effort", {})
        if isinstance(reasoning_data, dict):
            for key, value in reasoning_data.items():
                reasoning_effort[ReasoningEffort(key)] = str(value)

        apply_fork_data = data.get("apply_fork", {})
        if not isinstance(apply_fork_data, dict):
            apply_fork_data = {}
        review_oracle_data = data.get("review_oracle", {})
        if not isinstance(review_oracle_data, dict):
            review_oracle_data = {}

        return CmocConfig(
            num_parallel=int(data.get("num_parallel", default.num_parallel)),
            codex=CmocConfigCodex(model=model, reasoning_effort=reasoning_effort),
            apply_fork=CmocConfigApplyFork(
                num_apply_loop=int(
                    apply_fork_data.get(
                        "num_apply_loop",
                        default.apply_fork.num_apply_loop,
                    )
                ),
                num_improve_findings_loop=int(
                    apply_fork_data.get(
                        "num_improve_findings_loop",
                        default.apply_fork.num_improve_findings_loop,
                    )
                ),
            ),
            review_oracle=CmocConfigReviewOracle(
                num_enumerate_findings_loop=int(
                    review_oracle_data.get(
                        "num_enumerate_findings_loop",
                        default.review_oracle.num_enumerate_findings_loop,
                    )
                ),
                num_merge_findings_loop=int(
                    review_oracle_data.get(
                        "num_merge_findings_loop",
                        default.review_oracle.num_merge_findings_loop,
                    )
                ),
                num_validate_findings_loop=int(
                    review_oracle_data.get(
                        "num_validate_findings_loop",
                        default.review_oracle.num_validate_findings_loop,
                    )
                ),
            ),
        )
    except (TypeError, ValueError) as exc:
        raise CmocError(
            "cmoc config が不正です。",
            ["<repo-root>/.cmoc/config.json を確認してから再実行してください。"],
            json.dumps(data, ensure_ascii=False, indent=2),
        ) from exc


def write_config(path: Path, config: CmocConfig) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(config_to_dict(config), ensure_ascii=False, indent=2) + "\n"
    )


def load_config(root: Path) -> CmocConfig:
    path = config_path(root)
    if not path.exists():
        return sync_config(root)
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise CmocError(
            "cmoc config JSON を読み込めません。",
            ["<repo-root>/.cmoc/config.json の JSON 構文を確認してください。"],
            str(path),
        ) from exc
    if not isinstance(data, dict):
        raise CmocError(
            "cmoc config の top-level は object である必要があります。",
            ["<repo-root>/.cmoc/config.json を object に修正してください。"],
            str(path),
        )
    return config_from_dict(data)


def sync_config(root: Path) -> CmocConfig:
    path = config_path(root)
    if path.exists():
        config = load_config(root)
    else:
        config = CmocConfig()
    write_config(path, config)
    return config


def state_path(root: Path, session_id: str) -> Path:
    return sessions_dir(root) / f"{session_id}.json"


def branch_session_id(branch: str, kind: str = "session") -> str:
    prefix = f"cmoc/{kind}/"
    if not branch.startswith(prefix):
        raise CmocError(
            f"現在の branch は cmoc {kind} branch ではありません。",
            [f"`cmoc {kind}` 系コマンドを cmoc {kind} branch 上で実行してください。"],
            f"current branch: {branch}",
        )
    return branch.removeprefix(prefix).split("/", 1)[0]


def load_state_for_branch(root: Path, branch: str) -> tuple[str, Path, SessionState]:
    if branch.startswith("cmoc/session/"):
        session_id = branch_session_id(branch, "session")
    elif branch.startswith("cmoc/apply/"):
        parts = branch.split("/")
        if len(parts) < 4:
            raise CmocError(
                "apply branch 名から session-id を特定できません。",
                ["branch 名と session state file を確認してください。"],
                f"branch: {branch}",
            )
        session_id = parts[2]
    else:
        raise CmocError(
            "現在の branch は cmoc 管理 branch ではありません。",
            ["cmoc session branch または cmoc apply branch 上で再実行してください。"],
            f"current branch: {branch}",
        )
    path = state_path(root, session_id)
    if not path.is_file():
        raise CmocError(
            "session state file が存在しません。",
            ["対象 session が正しく作成されているか確認してください。"],
            str(path),
        )
    return session_id, path, SessionState.from_dict(json.loads(path.read_text()))


def write_state(path: Path, state: SessionState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state.to_dict(), ensure_ascii=False, indent=2) + "\n")


def create_run_worktree(
    root: Path, branch: str, worktree: Path, start_point: str = "HEAD"
) -> Path:
    worktree.parent.mkdir(parents=True, exist_ok=True)
    if worktree.exists():
        shutil.rmtree(worktree)
    run_git(["worktree", "add", "-b", branch, str(worktree), start_point], root)
    return worktree


def remove_worktree(root: Path, worktree: Path) -> CommandResult:
    result = run_git(
        ["worktree", "remove", "--force", str(worktree)], root, check=False
    )
    if result.returncode != 0 and worktree.exists():
        shutil.rmtree(worktree)
    run_git(["worktree", "prune"], root, check=False)
    return result


def delete_branch(root: Path, branch: str, force: bool = False) -> CommandResult:
    return run_git(["branch", "-D" if force else "-d", branch], root, check=False)


@contextmanager
def pushd(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def ensure_cmoc_ignored(root: Path) -> None:
    gitignore = root / ".gitignore"
    existing = gitignore.read_text().splitlines() if gitignore.exists() else []
    if "/.cmoc/" not in existing:
        with gitignore.open("a") as f:
            if existing and existing[-1] != "":
                f.write("\n")
            f.write("/.cmoc/\n")
    run_git(["rm", "--cached", "-r", "--ignore-unmatch", ".cmoc"], root)
    tracked = run_git(["ls-files", "--", ".cmoc"], root).stdout.strip()
    ignored = run_git(
        ["check-ignore", "-q", ".cmoc/.__cmoc_ignore_probe__"],
        root,
        check=False,
    )
    if tracked or ignored.returncode != 0:
        raise CmocError(
            ".cmoc を git 追跡対象外にできませんでした。",
            [".gitignore と git index の状態を確認してください。"],
            f"tracked:\n{tracked}\ncheck-ignore returncode: {ignored.returncode}",
        )


def active_session_for_home(root: Path, home_branch: str) -> Path | None:
    for path in sessions_dir(root).glob("*.json"):
        state = SessionState.from_dict(json.loads(path.read_text()))
        if (
            state.session.state == "active"
            and state.session.session_home_branch == home_branch
        ):
            return path
    return None


def render_error(exc: BaseException) -> str:
    if isinstance(exc, CmocError):
        summary = exc.summary
        actions = exc.next_actions
        detail = exc.detail
    else:
        summary = str(exc) or exc.__class__.__name__
        actions = [
            "エラー内容を確認し、必要なら手動で状態を修復してから再実行してください。"
        ]
        detail = repr(exc)
    return "\n".join(
        [
            "# ERROR",
            "## Summary",
            summary,
            "## Next actions",
            *[f"- {action}" for action in actions],
            "## Detail",
            detail,
            "## Call stack",
            traceback.format_exc(),
        ]
    )


def cmoc_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "bin" / "cmoc").is_file() or (candidate / ".git").is_dir():
            return candidate
    raise CmocError(
        "<cmoc-root> を特定できません。",
        ["cmoc repository 内から実行しているか確認してください。"],
        str(Path(__file__).resolve()),
    )


def file_access_to_sandbox_mode(mode: FileAccessMode) -> str:
    match mode:
        case FileAccessMode.READONLY | FileAccessMode.PURE_ORACLE_READ:
            return "read-only"
        case (
            FileAccessMode.REALIZATION_WRITE
            | FileAccessMode.ORACLE_WRITE
            | FileAccessMode.REPO_WRITE
        ):
            return "workspace-write"
        case _:
            raise CmocError("不明な FileAccessMode です。", [], str(mode))


def build_codex_profile(parameter: AgentCallParameter, config: CmocConfig) -> str:
    model = config.codex.model[parameter.model_class]
    reasoning_effort = config.codex.reasoning_effort[parameter.reasoning_effort]
    sandbox_mode = file_access_to_sandbox_mode(parameter.file_access_mode)
    return "\n".join(
        [
            f'model = "{model}"',
            f'reasoning_effort = "{reasoning_effort}"',
            f'sandbox_mode = "{sandbox_mode}"',
            "",
        ]
    )


def write_hashed_file(directory: Path, prefix: str, suffix: str, content: str) -> Path:
    digest = text_sha256(content)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{prefix}{digest}{suffix}"
    if not path.exists() or path.read_text() != content:
        path.write_text(content)
    return path


def write_hashed_file_in_existing_dir(
    directory: Path, prefix: str, suffix: str, content: str
) -> Path:
    digest = text_sha256(content)
    path = directory / f"{prefix}{digest}{suffix}"
    if not path.exists() or path.read_text() != content:
        path.write_text(content)
    return path


def resolve_codex_home() -> Path:
    value = os.environ.get("CODEX_HOME")
    if value:
        return Path(value).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def validate_codex_home(codex_home: Path) -> None:
    if not codex_home.exists():
        raise CmocError(
            "Codex home が存在しません。",
            [
                "Codex CLI の通常利用環境を初期化してください。",
                "既存の Codex home を指すように CODEX_HOME を設定してください。",
            ],
            f"CODEX_HOME: {codex_home}\nfailed condition: CODEX_HOME exists",
        )
    if not codex_home.is_dir():
        raise CmocError(
            "Codex home がディレクトリではありません。",
            [
                "CODEX_HOME が既存ディレクトリを指すように修正してください。",
                "CODEX_HOME のファイル種別を確認してください。",
            ],
            f"CODEX_HOME: {codex_home}\nfailed condition: CODEX_HOME is directory",
        )
    auth_path = codex_home / "auth.json"
    if not auth_path.is_file():
        raise CmocError(
            "Codex CLI 認証情報が存在しません。",
            [
                "Codex CLI の通常利用環境を初期化してください。",
                "既存の Codex home を指すように CODEX_HOME を設定してください。",
            ],
            f"CODEX_HOME: {codex_home}\nfailed condition: {auth_path} is file",
        )


def codex_profile_name(profile_path: Path) -> str:
    suffix = ".config.toml"
    if profile_path.name.endswith(suffix):
        return profile_path.name[: -len(suffix)]
    return profile_path.stem


def prepare_codex_profile(
    parameter: AgentCallParameter,
    config: CmocConfig | None = None,
    codex_home: Path | None = None,
) -> Path:
    profile = build_codex_profile(parameter, config or CmocConfig())
    target_home = codex_home or resolve_codex_home()
    try:
        return write_hashed_file_in_existing_dir(
            target_home, "cmoc_", ".config.toml", profile
        )
    except OSError as exc:
        raise CmocError(
            "Codex profile を生成できません。",
            [
                "CODEX_HOME の権限を確認してください。",
                "Codex CLI の通常利用環境を初期化してから再実行してください。",
            ],
            f"CODEX_HOME: {target_home}\nerror: {exc}",
        ) from exc


def codex_subprocess_env(codex_home: Path) -> dict[str, str]:
    return {**os.environ, "CODEX_HOME": str(codex_home)}


def prepare_schema(root: Path, schema_source_path: Path | None) -> Path | None:
    if schema_source_path is None:
        return None
    schema_text = schema_source_path.read_text()
    return write_hashed_file(schema_store_dir(root), "", ".json", schema_text)


def read_output_json(path: Path) -> Any:
    if not path.exists() or not path.read_text().strip():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return None


def codex_error_text(stdout_text: str, stderr_text: str) -> str:
    fragments: list[str] = [stderr_text]
    for line in stdout_text.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            fragments.append(line)
            continue
        message = item.get("message")
        if isinstance(message, str):
            fragments.append(message)
        error = item.get("error")
        if isinstance(error, dict) and isinstance(error.get("message"), str):
            fragments.append(error["message"])
    return "\n".join(fragments)


def extract_resume_token(stdout_text: str) -> str | None:
    for line in stdout_text.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        for key in ("session_id", "conversation_id", "id"):
            value = item.get(key)
            if isinstance(value, str) and value:
                return value
    return None


def is_capacity_error(text: str) -> bool:
    return "Selected model is at capacity" in text


def is_quota_error(text: str) -> bool:
    quota_markers = [
        "Quota exceeded",
        "You've hit your usage limit",
        "out of credits",
        "You hit your spend cap",
    ]
    return any(marker in text for marker in quota_markers)


def run_codex_exec(
    parameter: AgentCallParameter,
    *,
    root: Path | None = None,
    cwd: Path | None = None,
    config: CmocConfig | None = None,
    purpose: str = "codex exec",
    max_semantic_retries: int = 2,
    max_capacity_retries: int = 8,
    capacity_initial_sleep_sec: float = 5.0,
    quota_poll_interval_sec: float = 1800.0,
    max_quota_polls: int | None = None,
    subcommand_logger: SubcommandLogger | None = None,
) -> CodexExecResult:
    root = root or repo_root()
    cwd = cwd or root
    config = config or load_config(root)
    log_dir = codex_log_dir(root)
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = timestamp()
    stdout_path = log_dir / f"{ts}_stdout.jsonl"
    stderr_path = log_dir / f"{ts}_stderr.log"
    output_path = log_dir / f"{ts}_output.json"
    call_path = log_dir / f"{ts}_call.json"
    codex_home = resolve_codex_home()
    validate_codex_home(codex_home)
    codex_env = codex_subprocess_env(codex_home)
    profile_path = prepare_codex_profile(parameter, config, codex_home)
    profile_name = codex_profile_name(profile_path)
    schema_path = prepare_schema(root, parameter.structured_output_schema_path)
    argv = [
        "codex",
        "exec",
        "--profile",
        profile_name,
        "--json",
        "--output-last-message",
        str(output_path),
    ]
    if schema_path is not None:
        argv.extend(["--output-schema", str(schema_path)])
    argv.append("-")
    call_data = {
        "purpose": purpose,
        "timestamp": ts,
        "argv": argv,
        "codex_home": str(codex_home),
        "profile_name": profile_name,
        "profile_path": str(profile_path),
        "schema_path": str(schema_path) if schema_path else None,
        "stdout_log_path": str(stdout_path),
        "stderr_log_path": str(stderr_path),
        "output_path": str(output_path),
        "model_class": parameter.model_class.value,
        "reasoning_effort": parameter.reasoning_effort.value,
        "file_access_mode": parameter.file_access_mode.value,
    }
    call_path.write_text(json.dumps(call_data, ensure_ascii=False, indent=2) + "\n")
    call_started_at = time.perf_counter()
    quota_wait_sec = 0.0
    logger = subcommand_logger or current_subcommand_logger()

    def emit_codex_event(
        returncode: int, status: str, error: str | None = None
    ) -> None:
        elapsed_sec = time.perf_counter() - call_started_at
        print(
            "\n".join(
                [
                    f"# {console_timestamp()} Codex CLI call",
                    f"- purpose: `{purpose}`",
                    f"- call_log: `{call_path}`",
                    f"- elapsed: `{format_duration(elapsed_sec)}`",
                    f"- returncode: `{returncode}`",
                ]
            ),
            flush=True,
        )
        if logger is None:
            return
        payload: dict[str, Any] = {
            "purpose": purpose,
            "status": status,
            "returncode": returncode,
            "elapsed_sec": elapsed_sec,
            "quota_wait_sec": quota_wait_sec,
            "quota_polls": quota_polls,
            "call_log_path": str(call_path),
            "stdout_log_path": str(stdout_path),
            "stderr_log_path": str(stderr_path),
            "output_path": str(output_path),
            "codex_home": str(codex_home),
            "profile_name": profile_name,
            "profile_path": str(profile_path),
            "schema_path": str(schema_path) if schema_path else None,
        }
        if error is not None:
            payload["error"] = error
        logger.event("codex_call", **payload)

    semantic_attempts = 0
    capacity_attempts = 0
    quota_polls = 0
    sleep_sec = capacity_initial_sleep_sec
    last_result: subprocess.CompletedProcess[str] | None = None
    current_argv = argv
    while True:
        result = subprocess.run(
            current_argv,
            cwd=cwd,
            input=parameter.prompt,
            text=True,
            capture_output=True,
            env=codex_env,
        )
        last_result = result
        stdout_path.write_text(result.stdout)
        stderr_path.write_text(result.stderr)
        error_text = codex_error_text(result.stdout, result.stderr)
        if result.returncode != 0:
            if (
                is_capacity_error(error_text)
                and capacity_attempts < max_capacity_retries
            ):
                capacity_attempts += 1
                time.sleep(sleep_sec)
                sleep_sec *= 2
                continue
            if is_quota_error(error_text):
                global _QUOTA_POLLING
                with _QUOTA_CONDITION:
                    if _QUOTA_POLLING:
                        wait_started_at = time.perf_counter()
                        print(
                            f"# {console_timestamp()} Codex CLI quota wait: waiting for representative probe",
                            flush=True,
                        )
                        _QUOTA_CONDITION.wait_for(lambda: not _QUOTA_POLLING)
                        waited_sec = time.perf_counter() - wait_started_at
                        quota_wait_sec += waited_sec
                        if logger is not None:
                            logger.add_quota_wait(waited_sec)
                        resume_token = extract_resume_token(result.stdout)
                        if resume_token:
                            current_argv = [*argv[:-1], "resume", resume_token, "-"]
                        else:
                            current_argv = argv
                        continue
                    _QUOTA_POLLING = True
                print(
                    f"# {console_timestamp()} Codex CLI quota wait: entering polling mode",
                    flush=True,
                )
                try:
                    while True:
                        if (
                            max_quota_polls is not None
                            and quota_polls >= max_quota_polls
                        ):
                            emit_codex_event(
                                result.returncode, "quota_exhausted", error_text
                            )
                            raise CmocError(
                                "Codex CLI quota が枯渇しました。",
                                [
                                    "quota 回復後に同じ cmoc コマンドを再実行してください。"
                                ],
                                error_text,
                            )
                        quota_polls += 1
                        if logger is not None:
                            logger.add_quota_wait(quota_poll_interval_sec)
                        quota_wait_sec += quota_poll_interval_sec
                        time.sleep(quota_poll_interval_sec)
                        poll = subprocess.run(
                            ["codex", "exec", "--json", "-"],
                            cwd=cwd,
                            input="quota availability probe",
                            text=True,
                            capture_output=True,
                            env=codex_env,
                        )
                        print(
                            f"# {console_timestamp()} Codex CLI quota probe returned {poll.returncode}",
                            flush=True,
                        )
                        if poll.returncode == 0 and not is_quota_error(
                            codex_error_text(poll.stdout, poll.stderr)
                        ):
                            break
                finally:
                    with _QUOTA_CONDITION:
                        _QUOTA_POLLING = False
                        _QUOTA_CONDITION.notify_all()
                print(
                    f"# {console_timestamp()} Codex CLI quota wait: resuming work",
                    flush=True,
                )
                resume_token = extract_resume_token(result.stdout)
                if resume_token:
                    current_argv = [*argv[:-1], "resume", resume_token, "-"]
                else:
                    current_argv = argv
                continue
            emit_codex_event(result.returncode, "failed", error_text)
            raise CmocError(
                "Codex CLI 呼び出しが失敗しました。",
                ["stderr/stdout log を確認して原因を解消してください。"],
                f"call_log: {call_path}\nstdout_log: {stdout_path}\nstderr_log: {stderr_path}\n{error_text}",
            )
        output_json = read_output_json(output_path)
        if schema_path is not None:
            try:
                validate(
                    instance=output_json, schema=json.loads(schema_path.read_text())
                )
            except Exception as exc:
                if semantic_attempts < max_semantic_retries:
                    semantic_attempts += 1
                    continue
                emit_codex_event(
                    result.returncode, "schema_validation_failed", str(exc)
                )
                raise CmocError(
                    "Codex CLI の Structured Output 検証に失敗しました。",
                    ["schema と output を確認してください。"],
                    f"schema: {schema_path}\noutput: {output_path}\nerror: {exc}",
                ) from exc
        output_text = output_path.read_text() if output_path.exists() else ""
        elapsed_sec = time.perf_counter() - call_started_at
        emit_codex_event(result.returncode, "succeeded")
        return CodexExecResult(
            returncode=result.returncode,
            output_text=output_text,
            output_json=output_json,
            call_log_path=call_path,
            stdout_log_path=stdout_path,
            stderr_log_path=stderr_path,
            output_path=output_path,
            codex_home=codex_home,
            profile_name=profile_name,
            profile_path=profile_path,
            schema_path=schema_path,
            elapsed_sec=elapsed_sec,
            quota_wait_sec=quota_wait_sec,
            quota_polls=quota_polls,
        )

    assert last_result is not None


def run_codex_tui(
    parameter: AgentCallParameter,
    *,
    root: Path | None = None,
    cwd: Path | None = None,
    config: CmocConfig | None = None,
    purpose: str = "codex tui",
) -> CommandResult:
    root = root or repo_root()
    cwd = cwd or root
    config = config or load_config(root)
    log_dir = codex_log_dir(root)
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = timestamp()
    call_path = log_dir / f"{ts}_tui_call.json"
    codex_home = resolve_codex_home()
    validate_codex_home(codex_home)
    profile_path = prepare_codex_profile(parameter, config, codex_home)
    profile_name = codex_profile_name(profile_path)
    argv = [
        "codex",
        "--profile",
        profile_name,
        parameter.prompt,
    ]
    call_path.write_text(
        json.dumps(
            {
                "purpose": purpose,
                "timestamp": ts,
                "argv": argv,
                "codex_home": str(codex_home),
                "profile_name": profile_name,
                "profile_path": str(profile_path),
                "model_class": parameter.model_class.value,
                "reasoning_effort": parameter.reasoning_effort.value,
                "file_access_mode": parameter.file_access_mode.value,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        capture_output=True,
        env=codex_subprocess_env(codex_home),
    )
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "codex_tui_call",
            purpose=purpose,
            returncode=result.returncode,
            call_log_path=str(call_path),
            codex_home=str(codex_home),
            profile_name=profile_name,
            profile_path=str(profile_path),
        )
    if result.returncode != 0:
        raise CmocError(
            "Codex CLI/TUI 呼び出しが失敗しました。",
            ["Codex CLI/TUI の出力と call log を確認してください。"],
            f"call_log: {call_path}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
    return CommandResult(result.returncode, result.stdout, result.stderr)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def is_binary(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:4096]
    except OSError:
        return True
    return b"\0" in chunk


def is_git_ignored(root: Path, path: Path) -> bool:
    rel = path.resolve().relative_to(root)
    return run_git(["check-ignore", "-q", str(rel)], root, check=False).returncode == 0
