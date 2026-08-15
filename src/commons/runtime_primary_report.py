"""非対話サブコマンドの fallback primary report を保存する。

個別処理が正常な primary report を既に保存した場合は、その report を再利用する。
doctor preprocess や事前条件など、個別処理が report を作る前の終了経路だけを
確定済みの runtime 情報から機械的に要約する。

根拠:
- {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
- {{work-root}}/oracle/doc/app_spec/error_handling.md
"""

from contextvars import ContextVar, Token
from dataclasses import dataclass, replace
from pathlib import Path

from .runtime_logging import SubcommandLogger
from .runtime_paths import _reserve_timestamped_path, reports_dir, timestamp
from .runtime_primary_report_render import (
    feedback_statuses,
    oracle_edit_statuses,
    render_primary_report,
)
from .runtime_primary_report_specs import (
    PrimaryReportSpec,
    TerminalClassification,
    primary_report_spec,
)
from .runtime_results import TerminalResult


class PrimaryReportSaveError(RuntimeError):
    """primary report の保存確認に失敗した internal failure。"""

    def __init__(self, target_path: Path | None = None) -> None:
        """console へ未保存 path を漏らさず、診断用に対象だけを保持する。"""
        super().__init__("primary report の保存を確認できませんでした。")
        self.target_path = target_path


@dataclass
class PrimaryReportContext:
    """invocation 中に確定した report 項目を保持する。"""

    spec: PrimaryReportSpec
    fields: dict[str, object]


_PRIMARY_REPORT_CONTEXT: ContextVar[PrimaryReportContext | None] = ContextVar(
    "PRIMARY_REPORT_CONTEXT",
    default=None,
)

_FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "home_branch": ("session_home_branch", "joined_to", "switched_to"),
    "session_state_after": ("session_state",),
    "merge_commit": ("run_join_commit",),
    "state_after": ("session_state",),
    "changed_paths": ("updated_indexes",),
}


def start_primary_report_context(
    command_name: str,
) -> Token[PrimaryReportContext | None]:
    """既知の非対話サブコマンド用 report context を開始する。"""
    spec = primary_report_spec(command_name)
    fields: dict[str, object] = {}
    if command_name == "oracle edit":
        fields = {
            "main_agent_call_status": "not_started",
            "reduction_agent_call_status": "not_started",
        }
    context = PrimaryReportContext(spec, fields) if spec is not None else None
    return _PRIMARY_REPORT_CONTEXT.set(context)


def reset_primary_report_context(token: Token[PrimaryReportContext | None]) -> None:
    """invocation-local な report context を元へ戻す。"""
    _PRIMARY_REPORT_CONTEXT.reset(token)


def update_primary_report_fields(**fields: object) -> None:
    """現在の invocation で確定した report 項目だけを更新する。"""
    context = _PRIMARY_REPORT_CONTEXT.get()
    if context is not None:
        context.fields.update(fields)


def ensure_primary_report(
    repository: Path,
    command_name: str,
    command_argv: tuple[str, ...],
    classification: TerminalClassification,
    exit_code: int,
    result: TerminalResult,
    logger: SubcommandLogger,
) -> TerminalResult:
    """保存済み report を検証し、未作成の終了経路へ fallback を保存する。"""
    if result.primary_report is not None:
        _require_saved_report(result.primary_report)
        return result

    context = _PRIMARY_REPORT_CONTEXT.get()
    spec = context.spec if context is not None else primary_report_spec(command_name)
    if spec is None:
        return result

    target: Path | None = None
    try:
        directory = reports_dir(repository, spec.directory)
        directory.mkdir(parents=True, exist_ok=True)
        generated_at, target = _reserve_timestamped_path(directory, ".md", timestamp)
        fields = _report_fields(
            repository,
            command_name,
            command_argv,
            classification,
            exit_code,
            result,
            logger,
            generated_at,
            spec,
            context,
        )
        content = render_primary_report(spec, fields, classification, result, logger)
        write_reserved_primary_report(target, content)
    except BaseException as exc:
        if target is not None:
            try:
                target.unlink(missing_ok=True)
            except OSError:
                pass
        if isinstance(exc, PrimaryReportSaveError):
            raise
        raise PrimaryReportSaveError(target) from exc
    return replace(
        result,
        primary_report=target.resolve(),
        primary_report_role=spec.role,
    )


def write_reserved_primary_report(path: Path, content: str) -> None:
    """予約済み path へ保存し、失敗時は未確定の部分 file を除く。"""
    try:
        path.write_text(content, encoding="utf-8")
        _require_saved_report(path)
    except BaseException as exc:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
        if isinstance(exc, PrimaryReportSaveError):
            raise
        raise PrimaryReportSaveError(path) from exc


def _require_saved_report(path: Path) -> None:
    """表示前に report が空でない通常 file として存在することを確認する。"""
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size == 0:
            raise PrimaryReportSaveError(path)
    except OSError as exc:
        raise PrimaryReportSaveError(path) from exc


def _report_fields(
    repository: Path,
    command_name: str,
    command_argv: tuple[str, ...],
    classification: TerminalClassification,
    exit_code: int,
    result: TerminalResult,
    logger: SubcommandLogger,
    generated_at: str,
    spec: PrimaryReportSpec,
    context: PrimaryReportContext | None,
) -> list[tuple[str, object]]:
    """共通項目と、確定できた個別項目を front matter 順に並べる。"""
    context_values = dict(context.fields) if context is not None else {}
    detail_values = {name: value for name, value in result.details}
    known = dict(context_values)
    known.update(detail_values)
    if result.result is not None:
        known.setdefault("result", result.result)
    if result.completion_reason is not None:
        known.setdefault("completion_reason", result.completion_reason)
    if command_name == "realization refactor fork" and classification == "error":
        known.setdefault("completion_reason", "error")
    if command_name == "oracle review":
        known.setdefault("scope", _option_value(command_argv, "--scope"))
        known["result"] = (
            "interrupted" if classification == "user_interruption" else "error"
        )
    if command_name == "oracle edit":
        for name, status in oracle_edit_statuses(logger).items():
            known.setdefault(name, status)
    if command_name == "feedback report":
        known.update(feedback_statuses(logger))

    fields: list[tuple[str, object]] = [
        ("command", " ".join(command_argv)),
        ("generated_at", generated_at),
        ("repo_root", repository.resolve()),
        ("terminal_classification", classification),
        ("exit_code", exit_code),
    ]
    used = {name for name, _value in fields}
    for name in spec.fields:
        value = _known_field(name, known)
        fields.append((name, value))
        used.add(name)
    # 処理途中で確定した conflict や rollback 結果も失わず、必須項目の後へ置く。
    fields.extend(
        (name, value) for name, value in context_values.items() if name not in used
    )
    return fields


def _known_field(name: str, known: dict[str, object]) -> object:
    """正本の field 名に一致する確定値または既知 alias を返す。"""
    if name in known:
        return known[name]
    for alias in _FIELD_ALIASES.get(name, ()):
        if alias in known:
            return known[alias]
    return None


def _option_value(argv: tuple[str, ...], option: str) -> str | None:
    """保存済み argv から値を取る option の直後だけを読む。"""
    try:
        return argv[argv.index(option) + 1]
    except (ValueError, IndexError):
        return None
