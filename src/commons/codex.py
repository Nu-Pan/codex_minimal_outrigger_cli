"""Codex CLI 呼び出しの共通処理。"""

import json
import re
import subprocess
import time
from collections.abc import Callable
from pathlib import Path

from .errors import CmocError
from .timestamps import make_timestamp

_DEFAULT_MODEL = "gpt-5.5"
_DEFAULT_REASONING_EFFORT = "medium"
INDEX_GENERATION_MODEL = "gpt-5.4-mini"
INDEX_GENERATION_REASONING_EFFORT = "medium"
_POLL_MODEL = "gpt-5.4-mini"
_POLL_REASONING_EFFORT = "low"
_QUOTA_POLL_INTERVAL_SECONDS = 30 * 60
_FORBIDDEN_REASONING_EFFORTS = {"high", "xhigh"}


def run_codex_exec(
    repo_root: Path,
    prompt: str,
    *,
    read_only: bool,
    expect_json: bool = False,
    output_schema: dict[str, object] | None = None,
    json_validator: Callable[[object], None] | None = None,
    text_validator: Callable[[str], None] | None = None,
    skip_index_maintenance: bool = False,
    model: str = _DEFAULT_MODEL,
    reasoning_effort: str = _DEFAULT_REASONING_EFFORT,
) -> str:
    """`codex exec` を実行し、フルログを `.cmoc/logs` に保存する。"""
    # Structured Output を要求する呼び出しは schema ファイルを必須にする。
    if expect_json and output_schema is None:
        raise ValueError("expect_json=True requires output_schema.")
    _validate_model_options(model, reasoning_effort)

    # 例外指定された INDEX 生成・merge conflict 解消以外は、Codex 実行直前に INDEX を保守する。
    if not skip_index_maintenance and (repo_root / ".git").exists():
        from .indexing import maintain_indexes

        maintain_indexes(repo_root)

    # 呼び出し単位のログと必要なら output schema ファイルを準備する。
    log_dir = repo_root / ".cmoc" / "logs" / "codex_exec"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{make_timestamp()}.log"
    last_message_path = log_path.with_suffix(".last-message.txt")
    command = _build_codex_command(
        read_only=read_only,
        model=model,
        reasoning_effort=reasoning_effort,
        last_message_path=last_message_path,
    )
    schema_path = _write_output_schema(log_path, output_schema)
    if schema_path is not None:
        command.extend(["--output-schema", str(schema_path)])
    command.append(prompt)

    # JSON 以外でも意味検証がある呼び出しは最大 3 回リトライする。
    attempts = 3 if expect_json or text_validator is not None else 1
    last_output = ""
    last_stdout_log = ""
    last_stderr = ""
    last_validation_error = ""
    for attempt in range(1, attempts + 1):
        # 利用者向けには prompt と回収出力の先頭だけを進捗表示する。
        step = f"codex exec attempt ({attempt}/{attempts})"
        print(f"{step} prompt: {_head80(prompt)}")
        result = _run_codex_command(
            repo_root,
            command,
            log_path,
            prompt,
            attempt,
            schema_path,
            last_message_path,
        )
        last_stdout_log = result.stdout
        last_stderr = result.stderr

        # quota 枯渇だけは待機・resume に入り、それ以外の CLI 失敗は中断する。
        if result.returncode != 0:
            if _looks_like_quota_exhaustion(result.stdout, result.stderr):
                session_id = _extract_session_id(result.stdout, result.stderr)
                command = _resume_command(command, session_id)
                print("quota exhausted; waiting before resume")
                while True:
                    result = _wait_for_quota_and_resume(
                        repo_root,
                        command,
                        log_path,
                        prompt,
                        attempt,
                        schema_path,
                        last_message_path,
                    )
                    last_stdout_log = result.stdout
                    last_stderr = result.stderr
                    if result.returncode == 0:
                        break
                    if not _looks_like_quota_exhaustion(
                        result.stdout,
                        result.stderr,
                    ):
                        _raise_codex_failure(log_path, result)
                    print("quota exhausted again after resume; waiting")
            else:
                _raise_codex_failure(log_path, result)

        try:
            output = _read_last_message(last_message_path)
        except ValueError as error:
            last_validation_error = str(error)
            continue
        print(f"{step} output: {_head80(output)}")
        last_output = output

        if not expect_json:
            if text_validator is None:
                return output
            try:
                text_validator(output)
                return output
            except ValueError as error:
                last_validation_error = str(error)
                continue

        # JSON parse、schema 検査、意味検査のいずれかが失敗した場合だけ次の試行へ進む。
        try:
            value = json.loads(output)
            if output_schema is not None:
                _validate_json_schema(value, output_schema)
            if json_validator is not None:
                json_validator(value)
            if text_validator is not None:
                text_validator(output)
            return output
        except (json.JSONDecodeError, ValueError) as error:
            last_validation_error = str(error)
            continue

    # 全試行失敗時は最後の output/stdout/stderr と検証エラーを診断情報として残す。
    validation_label = "JSON" if expect_json else "text"
    raise CmocError(
        f"codex exec がリトライ後も有効な {validation_label} を返しませんでした。",
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
                f"Last message: {last_message_path}",
                f"Last validation error: {last_validation_error}",
                "Last output-last-message:",
                last_output,
                "Last stdout:",
                last_stdout_log,
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


def _raise_codex_failure(
    log_path: Path,
    result: subprocess.CompletedProcess[str],
) -> None:
    """quota 以外の Codex CLI 非 0 終了を共通エラーにする。"""
    raise CmocError(
        "codex exec が失敗しました。",
        [
            "codex exec のログを確認してください。",
            "Codex CLI またはリポジトリ側の原因を修正してから、cmoc を再実行してください。",
        ],
        f"Log: {log_path}\nSTDERR:\n{result.stderr}",
    )


def _validate_model_options(model: str, reasoning_effort: str) -> None:
    """Codex CLI に渡す model と reasoning effort の制約を検査する。"""
    # oracle は high/xhigh を禁止しているため、呼び出し前に拒否する。
    if not model:
        raise ValueError("model must not be empty.")
    if reasoning_effort in _FORBIDDEN_REASONING_EFFORTS:
        raise ValueError("reasoning_effort high/xhigh is forbidden.")
    if reasoning_effort not in {"low", "medium"}:
        raise ValueError("reasoning_effort must be low or medium.")


def _wait_for_quota_and_resume(
    repo_root: Path,
    command: list[str],
    log_path: Path,
    prompt: str,
    attempt: int,
    schema_path: Path | None,
    last_message_path: Path,
) -> subprocess.CompletedProcess[str]:
    """quota 復活まで疎通確認を繰り返してから元セッションを再開する。"""
    # 復活確認は低コスト model/effort の最小 prompt で行う。
    while True:
        poll_prompt = _quota_poll_prompt(repo_root)
        print("quota poll: running minimal codex exec check")
        print(f"quota poll prompt: {_head80(poll_prompt)}")
        poll_path = log_path.with_suffix(".quota-check.txt")
        poll_command = _build_codex_command(
            read_only=True,
            model=_POLL_MODEL,
            reasoning_effort=_POLL_REASONING_EFFORT,
            last_message_path=poll_path,
        )
        poll_command.append(poll_prompt)
        poll_result = subprocess.run(
            poll_command,
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _append_codex_log(
            log_path,
            poll_command,
            poll_prompt,
            attempt,
            poll_result,
            None,
            poll_path,
        )
        print(f"quota poll result: {poll_result.returncode}")
        if poll_result.returncode == 0:
            poll_output = _read_last_message(poll_path)
            print(f"quota poll output: {_head80(poll_output)}")
            print("quota restored; resuming codex exec")
            return _run_codex_command(
                repo_root,
                command,
                log_path,
                prompt,
                attempt,
                schema_path,
                last_message_path,
            )
        time.sleep(_QUOTA_POLL_INTERVAL_SECONDS)


def _quota_poll_prompt(repo_root: Path) -> str:
    """quota 疎通確認用の read-only prompt を組み立てる。"""
    return "\n".join(
        [
            "あなたは Codex CLI の疎通確認担当です。",
            "この実行環境で最小限の応答が可能か確認してください。",
            "完了条件は `ok` だけを出力することです。",
            "詳細な作業内容:",
            "- ファイル編集は禁止です。",
            f"- `{repo_root / 'memo'}` は読み書き禁止です。",
            "- この疎通確認では、その他のファイルも読む必要はありません。",
        ]
    )


def _build_codex_command(
    *,
    read_only: bool,
    model: str,
    reasoning_effort: str,
    last_message_path: Path,
) -> list[str]:
    """必須オプション込みの `codex exec` コマンドを組み立てる。"""
    # 全呼び出しで model、reasoning effort、json、last message を指定する。
    sandbox = "read-only" if read_only else "workspace-write"
    return [
        "codex",
        "exec",
        "--model",
        model,
        "-c",
        f'model_reasoning_effort="{reasoning_effort}"',
        "--sandbox",
        sandbox,
        "--json",
        "--output-last-message",
        str(last_message_path),
    ]


def _run_codex_command(
    repo_root: Path,
    command: list[str],
    log_path: Path,
    prompt: str,
    attempt: int,
    schema_path: Path | None,
    last_message_path: Path,
) -> subprocess.CompletedProcess[str]:
    """Codex CLI を 1 回起動し、結果をログに追記する。"""
    # 前回 attempt の最終メッセージを誤読しないよう、起動前に消しておく。
    last_message_path.unlink(missing_ok=True)
    result = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    _append_codex_log(
        log_path,
        command,
        prompt,
        attempt,
        result,
        schema_path,
        last_message_path,
    )
    return result


def _read_last_message(path: Path) -> str:
    """`--output-last-message` の成果物を読み取る。"""
    # Codex CLI の成果物は stdout ではなく last message ファイルとする。
    if not path.exists():
        raise ValueError(f"output-last-message was not created: {path}")
    return path.read_text(encoding="utf-8")


def _looks_like_quota_exhaustion(stdout: str, stderr: str) -> bool:
    """Codex CLI 出力から quota 枯渇らしさを判定する。"""
    # Codex の表現ゆれに備えて、limit/credits/quota 系の語を広めに拾う。
    text = f"{stdout}\n{stderr}".lower()
    quota_words = ["quota", "limit", "credit", "credits", "rate limit"]
    exhaustion_words = ["exhaust", "insufficient", "reached", "exceeded"]
    return (
        any(word in text for word in quota_words)
        and any(word in text for word in exhaustion_words)
    )


def _extract_session_id(stdout: str, stderr: str) -> str | None:
    """JSONL ログなどから resume 用 session id を取り出す。"""
    # JSONL と人間向けログのどちらにも耐える最小限の抽出を行う。
    for line in stdout.splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        session_id = _session_id_from_json(value)
        if session_id is not None:
            return session_id
    text = f"{stdout}\n{stderr}"
    match = re.search(r"session[_ -]?id['\":= ]+([A-Za-z0-9_.:-]+)", text)
    if match is None:
        return None
    return match.group(1)


def _session_id_from_json(value: object) -> str | None:
    """ネストした JSON object から session id らしい文字列を探す。"""
    # Codex JSONL のフィールド名変化に備えて再帰的に探す。
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key).lower().replace("-", "_")
            if key_text in {"session_id", "sessionid"} and isinstance(
                child,
                str,
            ):
                return child
            found = _session_id_from_json(child)
            if found is not None:
                return found
    if isinstance(value, list):
        for child in value:
            found = _session_id_from_json(child)
            if found is not None:
                return found
    return None


def _resume_command(command: list[str], session_id: str | None) -> list[str]:
    """元コマンドへ `--resume` を追加する。"""
    # session id が取れない場合も Codex CLI 側の既定 resume に委ねる。
    if "--resume" in command:
        return command
    resumed = [*command[:2], "--resume"]
    if session_id is not None:
        resumed.append(session_id)
    resumed.extend(command[2:])
    return resumed


def _append_codex_log(
    log_path: Path,
    command: list[str],
    prompt: str,
    attempt: int,
    result: subprocess.CompletedProcess[str],
    schema_path: Path | None,
    last_message_path: Path,
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
        f"output_last_message: {last_message_path}",
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
    # oracle の切り詰め対象は、表示用変換前の prompt/output そのものである。
    return value[:80].replace("\n", "\\n")
