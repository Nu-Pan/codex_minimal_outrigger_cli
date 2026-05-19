"""Codex CLI 呼び出しの共通処理。"""

import json
import subprocess
from collections.abc import Callable
from pathlib import Path

from .errors import CmocError
from .timestamps import make_timestamp


def run_codex_exec(
    repo_root: Path,
    prompt: str,
    *,
    read_only: bool,
    expect_json: bool = False,
    output_schema: dict[str, object] | None = None,
    json_validator: Callable[[object], None] | None = None,
    skip_index_maintenance: bool = False,
) -> str:
    """`codex exec` を実行し、フルログを `.cmoc/logs` に保存する。"""
    # Structured Output を要求する呼び出しは schema ファイルを必須にする。
    if expect_json and output_schema is None:
        raise ValueError("expect_json=True requires output_schema.")

    # 例外指定された INDEX 生成・merge conflict 解消以外は、Codex 実行直前に INDEX を保守する。
    if not skip_index_maintenance and (repo_root / ".git").exists():
        from .indexing import maintain_indexes

        maintain_indexes(repo_root)

    # 呼び出し単位のログと必要なら output schema ファイルを準備する。
    log_dir = repo_root / ".cmoc" / "logs" / "codex_exec"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{make_timestamp()}.log"
    command = ["codex", "exec"]
    if read_only:
        command.extend(["--sandbox", "read-only"])
    else:
        command.extend(["--sandbox", "workspace-write"])
    schema_path = _write_output_schema(log_path, output_schema)
    if schema_path is not None:
        command.extend(["--output-schema", str(schema_path)])
    command.append(prompt)

    # Structured Output 相当の JSON が必要な呼び出しだけ最大 3 回リトライする。
    attempts = 3 if expect_json else 1
    last_stdout = ""
    last_stderr = ""
    last_json_error = ""
    for attempt in range(1, attempts + 1):
        # 利用者向けには prompt/stdout の先頭だけを進捗表示する。
        print(f"codex exec attempt {attempt} prompt: {_head80(prompt)}")
        result = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        last_stdout = result.stdout
        last_stderr = result.stderr
        print(f"codex exec attempt {attempt} stdout: {_head80(result.stdout)}")
        _append_codex_log(
            log_path,
            command,
            prompt,
            attempt,
            result,
            schema_path,
        )

        # Codex CLI 自体の失敗はリトライせず、保存済みログ位置を添えて中断する。
        if result.returncode != 0:
            raise CmocError(
                "codex exec が失敗しました。",
                [
                    "codex exec のログを確認してください。",
                    "Codex CLI またはリポジトリ側の原因を修正してから、cmoc を再実行してください。",
                ],
                f"Log: {log_path}\nSTDERR:\n{result.stderr}",
            )

        if not expect_json:
            return result.stdout

        # JSON parse、schema 検査、意味検査のいずれかが失敗した場合だけ次の試行へ進む。
        try:
            value = json.loads(result.stdout)
            if output_schema is not None:
                _validate_json_schema(value, output_schema)
            if json_validator is not None:
                json_validator(value)
            return result.stdout
        except (json.JSONDecodeError, ValueError) as error:
            last_json_error = str(error)
            continue

    # 全試行失敗時は最後の stdout/stderr と検証エラーを診断情報として残す。
    raise CmocError(
        "codex exec がリトライ後も schema に一致する JSON を返しませんでした。",
        [
            "codex exec のログを確認してください。",
            "prompt または fake Codex CLI の出力を修正してから、cmoc を再実行してください。",
        ],
        "\n".join(
            [
                f"Log: {log_path}",
                (
                    f"Output schema: {schema_path}"
                    if schema_path is not None
                    else "Output schema: none"
                ),
                f"Last JSON error: {last_json_error}",
                "Last stdout:",
                last_stdout,
                "Last stderr:",
                last_stderr,
            ]
        ),
    )


def parse_json_object(raw: str) -> dict[str, object]:
    """Codex CLI の JSON 応答を object として読む。"""
    # 呼び出し側が dict として扱えることをここで保証する。
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise CmocError(
            "codex exec が JSON object 以外を返しました。",
            [
                "Codex CLI の出力 schema を修正してください。",
                "cmoc を再実行してください。",
            ],
            raw,
        )
    return value


def _append_codex_log(
    log_path: Path,
    command: list[str],
    prompt: str,
    attempt: int,
    result: subprocess.CompletedProcess[str],
    schema_path: Path | None,
) -> None:
    """1 回分の Codex CLI 呼び出し情報をフルログへ追記する。"""
    # prompt を含む完全な入出力を、stdout 進捗とは別にログへ保存する。
    content = [
        f"attempt: {attempt}",
        f"command: {' '.join(command[:-1])} <prompt>",
        (
            f"output_schema: {schema_path}"
            if schema_path is not None
            else "output_schema: none"
        ),
        "prompt:",
        prompt,
        f"returncode: {result.returncode}",
        "stdout:",
        result.stdout,
        "stderr:",
        result.stderr,
        "",
    ]
    # 同一 codex exec の複数 attempt は同じログファイルへ追記する。
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write("\n".join(content))


def _write_output_schema(
    log_path: Path,
    output_schema: dict[str, object] | None,
) -> Path | None:
    """Structured Output 用 JSON schema をログ配下へ保存する。"""
    # Structured Output を使わない呼び出しでは schema ファイルを作らない。
    if output_schema is None:
        return None

    # schema はログと同じ stem で保存し、Codex CLI の引数から参照させる。
    schema_dir = log_path.parent / "schemas"
    schema_dir.mkdir(parents=True, exist_ok=True)
    schema_path = schema_dir / f"{log_path.stem}.schema.json"
    schema_path.write_text(
        json.dumps(output_schema, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return schema_path


def _validate_json_schema(value: object, schema: dict[str, object]) -> None:
    """cmoc 側で使う JSON Schema subset を機械的に検査する。"""
    # Codex CLI の応答を cmoc 側でも機械的に再検証する。
    _validate_schema_node(value, schema, "$")


def _validate_schema_node(
    value: object,
    schema: dict[str, object],
    path: str,
) -> None:
    """Structured Output schema の主要 subset を再帰的に検査する。"""
    # 現在 node の type 制約を先に確認する。
    expected_type = schema.get("type")
    if expected_type is not None and not _matches_type(value, expected_type):
        raise ValueError(f"{path} type does not match schema.")

    # object では required、additionalProperties、properties の子 schema を検査する。
    if isinstance(value, dict):
        required = schema.get("required", [])
        if not isinstance(required, list):
            raise ValueError(f"{path} schema required must be a list.")
        missing = [
            key
            for key in required
            if isinstance(key, str) and key not in value
        ]
        if missing:
            raise ValueError(
                f"{path} missing required keys: {', '.join(missing)}."
            )

        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            raise ValueError(f"{path} schema properties must be an object.")
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(properties))
            if extra:
                raise ValueError(
                    f"{path} unexpected keys: {', '.join(extra)}."
                )
        for key, child_schema in properties.items():
            if key not in value:
                continue
            if not isinstance(key, str) or not isinstance(child_schema, dict):
                raise ValueError(f"{path} schema properties are invalid.")
            _validate_schema_node(value[key], child_schema, f"{path}.{key}")

    # array では items schema がある場合だけ各要素へ再帰する。
    if isinstance(value, list):
        item_schema = schema.get("items")
        if item_schema is None:
            return
        if not isinstance(item_schema, dict):
            raise ValueError(f"{path} schema items must be an object.")
        for index, item in enumerate(value):
            _validate_schema_node(item, item_schema, f"{path}[{index}]")


def _matches_type(value: object, expected_type: object) -> bool:
    """JSON Schema の type 指定に値が一致するか判定する。"""
    # type 配列は候補のいずれかに一致すれば受理する。
    if isinstance(expected_type, list):
        return any(_matches_type(value, item) for item in expected_type)

    # cmoc が使う JSON Schema type subset だけを厳密に判定する。
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "null":
        return value is None
    return True


def _head80(value: str) -> str:
    """元文字列の先頭 80 文字を stdout 表示向けに返す。"""
    # oracle の切り詰め対象は、表示用変換前の prompt/stdout そのものである。
    return value[:80].replace("\n", "\\n")
