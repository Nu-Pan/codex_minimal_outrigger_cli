"""cmoc 設定の検証、JSON 変換、読み書き、同期を担う。"""

import json
import math
from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any, NoReturn

from oracle.other.cmoc_config import (
    CodexCallConfig,
    CodexModelProviderConfig,
    DocumentSearchConfig,
    JsonTomlValue,
)
from oracle.other.document_search import (
    SEARCH_CANDIDATE_COUNT_MAX,
    SEARCH_CANDIDATE_COUNT_MIN,
)

from config.cmoc_config import (
    CmocConfig,
    CmocConfigCodex,
)

from .runtime_errors import CmocError
from .runtime_paths import config_path


def _reject_non_json_constant(value: str) -> NoReturn:
    """JSON 仕様外の非有限数リテラルを設定 JSON から拒否する。"""
    raise ValueError(f"non-standard JSON constant: {value}")


def _model_name(value: Any) -> str:
    """Codex の専用 argv へ渡せる非空モデル名へ検証する。"""
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise TypeError
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # model は TOML string ではなく --model の argv へそのまま渡すため、NUL と
    # Unicode surrogate を設定読み込み時に拒否して subprocess 起動失敗を防ぐ。
    validate_json_toml_value(value)
    return value


def _reasoning_effort_name(value: Any) -> str:
    """Codex の TOML override へ渡せる非空 reasoning effort 名へ検証する。"""
    if not isinstance(value, str) or not value.strip():
        raise TypeError
    validate_json_toml_value(value)
    return value


def _model_provider_id(value: Any) -> str:
    """Codex CLI へ直接渡せる必須の model provider ID を検証する。"""
    if not isinstance(value, str) or not value.strip():
        raise TypeError
    validate_json_toml_value(value)
    return value


def _config_object(value: Any, names: Iterable[str], field: str) -> dict[str, Any]:
    """正本で定義した項目集合と一致する object だけを受理する。"""
    if not isinstance(value, dict):
        raise TypeError(f"{field}: object が必要です")
    names = set(names)
    missing = names - value.keys()
    if missing:
        raise TypeError(f"{field}.{sorted(missing)[0]}: 必須項目がありません")
    unknown = value.keys() - names
    if unknown:
        raise TypeError(
            f"{field}.{sorted(unknown, key=str)[0]}: 未知の項目です。手動で除去してください"
        )
    return value


def _config_int(value: Any) -> int:
    """永続化対象の int field が bool や別型に置き換わっていないか検証する。"""
    if type(value) is not int:
        raise TypeError
    return value


class SearchConfigIssue(ValueError):
    """検索設定のどの項目を修正するべきか保持する。"""

    def __init__(self, field: str, reason: str, *, missing: bool = False) -> None:
        super().__init__(reason)
        self.field = field
        self.missing = missing


@dataclass(frozen=True)
class ConfigSyncResult:
    """doctor preprocess が報告する検索設定の検証・保存結果。"""

    config: CmocConfig
    generated: bool
    additions: dict[str, object]
    saved: bool


def _document_search_data(value: Any) -> dict[str, Any]:
    """正本の tuning 制約を検証し、定義順の数値 object を返す。"""
    # 全項目を数値として検証するため、dataclass の再帰コピーは不要。
    if isinstance(value, DocumentSearchConfig):
        data = {field.name: getattr(value, field.name) for field in fields(value)}
    elif isinstance(value, dict):
        data = value
    else:
        raise SearchConfigIssue("document_search", "object が必要です")
    schema_fields = fields(DocumentSearchConfig)
    names = {field.name for field in schema_fields}
    unknown = sorted(data.keys() - names)
    if unknown:
        raise SearchConfigIssue(
            f"document_search.{unknown[0]}", "未知の項目です。手動で除去してください"
        )
    missing = sorted(names - data.keys())
    if missing:
        raise SearchConfigIssue(
            f"document_search.{missing[0]}",
            f"必要な項目が不足しています: {', '.join(missing)}",
            missing=True,
        )
    for name in (
        "chunk_tokens",
        "embedding_context_tokens",
        "batch_tokens",
        "threads",
    ):
        if type(data[name]) is not int or data[name] <= 0:
            raise SearchConfigIssue(
                f"document_search.{name}", "正の JSON 整数が必要です"
            )
    if (
        type(data["candidate_count"]) is not int
        or not SEARCH_CANDIDATE_COUNT_MIN
        <= data["candidate_count"]
        <= SEARCH_CANDIDATE_COUNT_MAX
    ):
        raise SearchConfigIssue(
            "document_search.candidate_count",
            f"{SEARCH_CANDIDATE_COUNT_MIN}〜{SEARCH_CANDIDATE_COUNT_MAX} の JSON 整数へ手動で修正してください",
        )
    overlap = data["chunk_overlap_tokens"]
    if type(overlap) is not int or overlap < 0:
        raise SearchConfigIssue(
            "document_search.chunk_overlap_tokens", "0 以上の JSON 整数が必要です"
        )
    if overlap >= data["chunk_tokens"]:
        raise SearchConfigIssue(
            "document_search.chunk_overlap_tokens, document_search.chunk_tokens",
            f"overlap {overlap} は chunk {data['chunk_tokens']} より小さくしてください",
        )
    for name in (
        "startup_timeout_seconds",
        "request_timeout_seconds",
        "shutdown_grace_seconds",
        "resource_wait_timeout_seconds",
        "sync_no_progress_timeout_seconds",
        "post_sync_search_timeout_seconds",
        "search_request_timeout_seconds",
    ):
        number = data[name]
        try:
            finite = math.isfinite(number) if type(number) in (int, float) else False
        except OverflowError:
            finite = False
        if not finite or number <= 0:
            raise SearchConfigIssue(
                f"document_search.{name}", "有限の正の JSON 数値が必要です"
            )
    if data["chunk_tokens"] >= data["embedding_context_tokens"]:
        raise SearchConfigIssue(
            "document_search.chunk_tokens, document_search.embedding_context_tokens",
            f"chunk_tokens={data['chunk_tokens']} は embedding_context_tokens={data['embedding_context_tokens']} より小さくしてください",
        )
    return {field.name: data[field.name] for field in schema_fields}


def _document_search_config(value: Any) -> DocumentSearchConfig:
    """検索設定を検証して正本の dataclass へ復元する。"""
    return DocumentSearchConfig(**_document_search_data(value))


def config_to_dict(config: CmocConfig) -> dict[str, Any]:
    """正本 config 型を、永続化 JSON の object 境界へ変換する。"""
    # 設定キーを正本から取得し、共有対象の個別上書きも通常の構造検証で拒否する。
    _config_object(
        config.codex.agent_calls, CmocConfigCodex().agent_calls, "codex.agent_calls"
    )
    model_providers: dict[str, dict[str, dict[str, JsonTomlValue]]] = {}
    for provider_id, provider_config in config.codex.model_providers.items():
        if not isinstance(provider_config, CodexModelProviderConfig):
            raise TypeError("invalid Codex model provider definition")
        normalized_provider_id = _model_provider_id(provider_id)
        settings: dict[str, JsonTomlValue] = {}
        for key, setting_value in provider_config.settings.items():
            if not isinstance(key, str):
                raise TypeError("invalid Codex model provider setting key")
            validate_json_toml_value(key)
            settings[key] = validate_json_toml_value(setting_value)
        model_providers[normalized_provider_id] = {"settings": settings}
    agent_calls: dict[str, dict[str, str]] = {}
    for agent_call_kind, call_config in config.codex.agent_calls.items():
        if not isinstance(call_config, CodexCallConfig):
            raise TypeError("invalid Codex agent call definition")
        if call_config.model_provider not in model_providers:
            raise TypeError(
                f"codex.agent_calls.{agent_call_kind}.model_provider: provider 定義がありません"
            )
        agent_calls[agent_call_kind] = {
            "model_provider": _model_provider_id(call_config.model_provider),
            "model": _model_name(call_config.model),
            "reasoning_effort": _reasoning_effort_name(call_config.reasoning_effort),
        }

    search_data = _document_search_data(config.document_search)
    return {
        "num_parallel": _config_int(config.num_parallel),
        "codex": {
            "model_providers": model_providers,
            "agent_calls": agent_calls,
            "num_try_falv_recovery": _config_int(config.codex.num_try_falv_recovery),
        },
        "document_search": search_data,
    }


def _validate_json_toml_value(
    item: Any, active_containers: set[int] | None
) -> JsonTomlValue:
    """呼び出しごとの巡回状態を使い、循環 container も拒否する。"""
    # 関数は共有し、設定の各文字列を検証するたびに自己参照 closure を作らない。
    if isinstance(item, str):
        # TOML string は Unicode scalar value だけを受理する。
        # ASCII には surrogate がないので、文字単位の走査を省ける。
        if not item.isascii() and any(
            0xD800 <= ord(character) <= 0xDFFF for character in item
        ):
            raise TypeError
        return item
    if isinstance(item, bool):
        return item
    if type(item) is int:
        # TOML 1.0 の integer は signed 64 bit に限定される。
        if not -(2**63) <= item < 2**63:
            raise TypeError
        return item
    if isinstance(item, float):
        # NaN と infinity は JSON value ではない。
        if not math.isfinite(item):
            raise TypeError
        return item
    if isinstance(item, (list, dict)):
        # scalar の検証には巡回状態を用意せず、最初の container だけで作る。
        if active_containers is None:
            active_containers = set()
        identity = id(item)
        if identity in active_containers:
            raise TypeError
        active_containers.add(identity)
        try:
            if isinstance(item, list):
                return [
                    _validate_json_toml_value(element, active_containers)
                    for element in item
                ]
            restored: dict[str, JsonTomlValue] = {}
            for key, element in item.items():
                if not isinstance(key, str):
                    raise TypeError
                _validate_json_toml_value(key, active_containers)
                restored[key] = _validate_json_toml_value(element, active_containers)
            return restored
        finally:
            active_containers.remove(identity)
    raise TypeError


def validate_json_toml_value(value: Any) -> JsonTomlValue:
    """JSON と TOML の双方へ意味を変えず保存できる値を検証する。"""

    # 巡回状態は値ごとに隔離し、深さエラーは設定エラーへ変換する。
    try:
        return _validate_json_toml_value(value, None)
    except RecursionError as exc:
        # {{work-root}}/oracle/doc/app_spec/error_handling.md
        # 深すぎる provider-local container も設定エラーとして上位へ返す。
        raise TypeError("JSON/TOML value is too deeply nested") from exc


def _model_provider_map_from_dict(
    data: Any,
) -> dict[str, CodexModelProviderConfig]:
    """provider-local 設定を型検証済みの正本設定型へ戻す。"""
    if not isinstance(data, dict):
        raise TypeError
    restored = {}
    for provider_id, value in data.items():
        normalized_provider_id = _model_provider_id(provider_id)
        value = _config_object(
            value,
            (field.name for field in fields(CodexModelProviderConfig)),
            f"codex.model_providers.{normalized_provider_id}",
        )
        settings = value["settings"]
        if not isinstance(settings, dict):
            raise TypeError
        restored_settings: dict[str, JsonTomlValue] = {}
        for key, setting in settings.items():
            if not isinstance(key, str):
                raise TypeError
            validate_json_toml_value(key)
            restored_settings[key] = validate_json_toml_value(setting)
        restored[normalized_provider_id] = CodexModelProviderConfig(restored_settings)
    return restored


def _agent_call_map_from_dict(
    data: Any,
) -> dict[str, CodexCallConfig]:
    """正本の種別集合と各 call の必須文字列を補完せず復元する。"""
    data = _config_object(data, CmocConfigCodex().agent_calls, "codex.agent_calls")
    restored = {}
    for agent_call_kind, value in data.items():
        value = _config_object(
            value,
            (field.name for field in fields(CodexCallConfig)),
            f"codex.agent_calls.{agent_call_kind}",
        )
        restored[agent_call_kind] = CodexCallConfig(
            model_provider=_model_provider_id(value["model_provider"]),
            model=_model_name(value["model"]),
            reasoning_effort=_reasoning_effort_name(value["reasoning_effort"]),
        )
    return restored


def config_from_dict(data: dict[str, Any]) -> CmocConfig:
    """現行の設定構造と参照整合性を検証し、補完せず復元する。"""
    return _config_from_dict(data)


def _config_from_dict(
    data: dict[str, Any],
    *,
    document_search: DocumentSearchConfig | None = None,
) -> CmocConfig:
    """保存内容の検証で復元済みの検索設定があれば、その結果を再利用する。"""
    # 新規生成には正本の既定状態を使い、入力済みの設定には既定値を混入させない。
    try:
        data = _config_object(
            data, (field.name for field in fields(CmocConfig)), "config"
        )
        codex_data = _config_object(
            data["codex"],
            (field.name for field in fields(CmocConfigCodex)),
            "codex",
        )
        model_providers = _model_provider_map_from_dict(codex_data["model_providers"])
        agent_calls = _agent_call_map_from_dict(codex_data["agent_calls"])
        for kind, call in agent_calls.items():
            if call.model_provider not in model_providers:
                raise TypeError(
                    f"codex.agent_calls.{kind}.model_provider: provider 定義がありません"
                )

        if document_search is None:
            document_search = _document_search_config(data["document_search"])
        return CmocConfig(
            num_parallel=_config_int(data["num_parallel"]),
            document_search=document_search,
            codex=CmocConfigCodex(
                model_providers=model_providers,
                agent_calls=agent_calls,
                num_try_falv_recovery=_config_int(codex_data["num_try_falv_recovery"]),
            ),
        )
    except (RecursionError, TypeError, ValueError) as exc:
        try:
            # {{work-root}}/oracle/doc/app_spec/error_handling.md
            # 不正 JSON には surrogate も含まれうるため、error report を UTF-8 で出力
            # できる ASCII escape へ変換する。
            if isinstance(exc, RecursionError) or isinstance(
                exc.__cause__, RecursionError
            ):
                # JSON 診断も再帰処理なので、深さエラー後の再走査を省く。
                detail = repr(data)
            else:
                detail = json.dumps(data, ensure_ascii=True, indent=2, default=repr)
        except (RecursionError, TypeError, ValueError):
            detail = repr(data)
        detail = detail.encode("utf-8", "backslashreplace").decode("utf-8")
        raise CmocError(
            "cmoc config が不正です。",
            ["{{work-root}}/.cmoc/gt/config.json を確認してから再実行してください。"],
            f"reason: {exc}\n{detail}",
        ) from exc


def _reject_symlinked_config_path(path: Path) -> None:
    """config path の symlink 経由アクセスを拒否する。"""
    # {{work-root}}/oracle/src/oracle/other/cmoc_config.py
    # config は work-root 内の tracked file なので、link 先の設定を読み書きしない。
    current = path.absolute()
    while (parent := current.parent) != current:
        if current.is_symlink():
            raise CmocError(
                "cmoc config path は symlink 経由で扱えません。",
                [
                    "config.json と親 directory を通常の file/directory に戻してから再実行してください。"
                ],
                str(current),
            )
        current = parent


def write_config(path: Path, config: CmocConfig) -> None:
    """config JSON を人間が確認しやすい安定した表現で保存する。"""
    _reject_symlinked_config_path(path)
    # {{work-root}}/oracle/doc/app_spec/error_handling.md
    # FIFO などを open して command が停止しないよう、既存 path は regular file に限る。
    if path.exists() and not path.is_file():
        raise CmocError(
            "cmoc config path は通常ファイルではありません。",
            [
                "config.json を通常の file に戻してから再実行してください。",
            ],
            str(path),
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            config_to_dict(config),
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )


def _search_config_failure(
    path: Path, issue: SearchConfigIssue, *, missing: bool = False
) -> CmocError:
    """設定 path、項目、理由、修復方法を持つ handled failure を作る。"""
    action = (
        f"対象 work-root ({path.parents[2]}) で cmoc doctor を実行してください。"
        if missing
        else f"{path} の {issue.field} を手動で修正してください。"
    )
    return CmocError(
        "文書検索の設定が不足または不正です。",
        [action],
        f"path: {path}\nitem: {issue.field}\nreason: {issue}",
    )


def _read_config_data(path: Path) -> dict[str, Any]:
    """既存 JSON を構造を保ったまま読む。"""
    _reject_symlinked_config_path(path)
    # {{work-root}}/oracle/doc/app_spec/error_handling.md
    # 特殊 file を read_text する前に拒否し、設定読み込みを即時に失敗させる。
    if not path.is_file():
        if not path.exists():
            raise _search_config_failure(
                path,
                SearchConfigIssue("document_search", "設定ファイルが存在しません"),
                missing=True,
            )
        raise CmocError(
            "cmoc config JSON を読み込めません。",
            ["{{work-root}}/.cmoc/gt/config.json を通常の file に修正してください。"],
            str(path),
        )
    try:
        data = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=_reject_non_json_constant,
        )
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        raise CmocError(
            "cmoc config JSON を読み込めません。",
            [f"{path} の JSON 構文と文字エンコーディングを手動で修正してください。"],
            f"path: {path}\nreason: {exc}",
        ) from exc
    if not isinstance(data, dict):
        raise CmocError(
            "cmoc config の top-level は object である必要があります。",
            [f"{path} の top-level を object に手動で修正してください。"],
            f"path: {path}\nitem: <file>\nreason: top-level が object ではありません",
        )
    return data


def _saved_search_config(path: Path, data: dict[str, Any]) -> DocumentSearchConfig:
    """保存された検索設定を既定値の注入なしで検証・復元する。"""
    # 保存済み設定では document_search の欠落を補完しない。
    if "document_search" not in data:
        raise _search_config_failure(
            path,
            SearchConfigIssue("document_search", "検索設定がありません"),
            missing=True,
        )
    try:
        return _document_search_config(data["document_search"])
    except SearchConfigIssue as exc:
        raise _search_config_failure(path, exc, missing=exc.missing) from exc


def _config_from_saved_data(path: Path, data: dict[str, Any]) -> CmocConfig:
    """検索設定・agent call 設定・provider 参照を確認して保存内容を復元する。"""
    # 検索設定の不備は Codex 設定の復元より先に診断する。
    document_search = _saved_search_config(path, data)
    try:
        return _config_from_dict(data, document_search=document_search)
    except CmocError as exc:
        raise CmocError(
            exc.summary,
            [f"{path} の設定を手動で修正してください。"],
            f"path: {path}\n{exc.detail}",
        ) from exc


def load_config(root: Path) -> CmocConfig:
    """保存済み JSON の検索設定を厳格に検証して config に復元する。"""
    path = config_path(root)
    data = _read_config_data(path)
    return _config_from_saved_data(path, data)


def sync_config(
    root: Path,
    *,
    repair_missing: bool = False,
    on_candidate: Callable[[bool, dict[str, object]], None] | None = None,
) -> ConfigSyncResult:
    """通常起動では検証だけ、明示 doctor では不足だけを補完する。"""
    path = config_path(root)
    if not repair_missing:
        return ConfigSyncResult(load_config(root), False, {}, False)
    defaults = asdict(DocumentSearchConfig())
    if not path.exists():
        config = CmocConfig()
        if on_candidate is not None:
            on_candidate(True, defaults)
        write_config(path, config)
        return ConfigSyncResult(config, True, defaults, True)

    data = _read_config_data(path)
    search = data.get("document_search")
    if "document_search" not in data:
        additions = defaults
        search = defaults
    elif isinstance(search, dict):
        additions = {
            name: value for name, value in defaults.items() if name not in search
        }
        search = {**search, **additions}
    else:
        raise _search_config_failure(
            path, SearchConfigIssue("document_search", "object が必要です")
        )
    if on_candidate is not None:
        on_candidate(False, additions)
    candidate = {**data, "document_search": search}
    config = _config_from_saved_data(path, candidate)
    if additions:
        write_config(path, config)
    return ConfigSyncResult(config, False, additions, bool(additions))
