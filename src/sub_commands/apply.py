"""`cmoc apply` の本体処理。"""

import json
from pathlib import Path

from commons.codex import parse_json_object, run_codex_exec
from commons.command_runner import run_command
from commons.errors import CmocError
from commons.indexing import maintain_indexes
from commons.repo import (
    assert_only_oracles_uncommitted,
    changed_paths,
    commit_if_changed,
    current_branch,
    ensure_cmoc_ignored,
    is_cmoc_branch,
    list_oracle_files,
    run_git,
)
from commons.timing import StepTimer
from commons.timestamps import make_timestamp

APPLY_INCOMPLETE_EXIT_CODE = 2
_DISCREPANCY_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["discrepancies"],
    "properties": {
        "discrepancies": {
            "type": "array",
            "description": "oracles と実装との明確なズレのリスト。空配列の場合のみズレなしとみなす。",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "oracle_path",
                    "oracle_line_start",
                    "oracle_line_end",
                    "implementation_paths",
                    "title",
                    "oracle_requirement",
                    "observed_implementation",
                    "reason",
                    "suggested_fix",
                ],
                "properties": {
                    "oracle_path": {
                        "type": "string",
                        "description": "ズレの根拠となる oracle ファイルの絶対パス。",
                    },
                    "oracle_line_start": {
                        "type": ["integer", "null"],
                        "description": (
                            "ズレの根拠となる oracle 記述の開始行。"
                            "行番号を特定できない場合は null。"
                        ),
                    },
                    "oracle_line_end": {
                        "type": ["integer", "null"],
                        "description": (
                            "ズレの根拠となる oracle 記述の終了行。"
                            "行番号を特定できない場合は null。"
                        ),
                    },
                    "implementation_paths": {
                        "type": "array",
                        "description": (
                            "ズレに関係する実装・テスト・設定ファイルの"
                            "絶対パス。未実装などで該当ファイルを"
                            "特定できない場合は空配列。"
                        ),
                        "items": {"type": "string"},
                    },
                    "title": {
                        "type": "string",
                        "description": "ズレの短い見出し。",
                    },
                    "oracle_requirement": {
                        "type": "string",
                        "description": "oracle が要求している仕様。",
                    },
                    "observed_implementation": {
                        "type": "string",
                        "description": "調査時点の実装が実際にどうなっているか。",
                    },
                    "reason": {
                        "type": "string",
                        "description": (
                            "なぜ oracle と実装が明確にズレていると"
                            "言えるのか。推測や未確認事項は含めない。"
                        ),
                    },
                    "suggested_fix": {
                        "type": "string",
                        "description": "実装を oracle に追従させるための修正方針。",
                    },
                },
            },
        }
    },
}


def cmoc_apply_impl(repo_root: Path | None = None) -> int | None:
    """oracle と実装のズレを Codex CLI へ追従させる。"""
    if repo_root is None:
        run_command(cmoc_apply_impl)
        return None

    # apply は cmoc 作業ブランチ上でだけ実行できる。
    timer = StepTimer("apply")
    branch_name = current_branch(repo_root)
    if not is_cmoc_branch(branch_name):
        raise CmocError(
            "cmoc apply must be run on a cmoc branch.",
            ["Run `cmoc branch` first.", "Checkout an existing cmoc branch."],
            f"Current branch: {branch_name}",
        )

    # oracle 更新以外の未コミット差分を拒否し、oracle 変更は先に commit する。
    timer.start("validate repository state")
    print("apply (1/4) validate repository state")
    ensure_cmoc_ignored(repo_root)
    assert_only_oracles_uncommitted(repo_root)
    commit_if_changed(repo_root, ["oracles"], "Update oracle files")

    # ユーザー向けステップとして INDEX.md を明示メンテナンスする。
    timer.start("maintain INDEX.md files")
    print("apply (2/4) maintain INDEX.md files")
    maintain_indexes(repo_root)

    # ズレ調査と追従作業を最大 5 回まで反復する。
    timer.start("investigate and apply discrepancies")
    print("apply (3/4) investigate and apply discrepancies")
    discrepancy_counts: list[int] = []
    completed = False
    for loop_index in range(1, 6):
        discrepancies = _investigate_discrepancies(repo_root)
        discrepancy_counts.append(len(discrepancies))
        print(
            f"implementation loop ({loop_index}/5) discrepancies: "
            f"{len(discrepancies)}"
        )
        if not discrepancies:
            completed = True
            break

        # 実装修正後、禁止領域の変更検査と commit を cmoc 側で行う。
        _apply_discrepancies(repo_root, discrepancies)
        _assert_forbidden_paths_clean(repo_root)
        _commit_all_changes(repo_root)

    # 実行結果を人間向け report と exit code に変換する。
    timer.start("write report")
    print("apply (4/4) write report")
    report_path = _write_apply_report(
        repo_root,
        branch_name,
        completed,
        discrepancy_counts,
    )
    print(str(report_path))
    timer.report()
    return 0 if completed else APPLY_INCOMPLETE_EXIT_CODE


def _investigate_discrepancies(repo_root: Path) -> list[dict[str, object]]:
    """oracle ファイルごとにズレ調査を実行する。"""
    # oracle 列挙結果を 1 ファイルずつ Codex CLI に評価させる。
    discrepancies: list[dict[str, object]] = []
    oracle_files = list_oracle_files(repo_root)
    for index, oracle_file in enumerate(oracle_files, start=1):
        print(
            f"investigate oracle ({index}/{len(oracle_files)}) "
            f"{oracle_file}"
        )
        # Structured Output の discrepancies を 1 つの一覧へ結合する。
        payload = parse_json_object(
            run_codex_exec(
                repo_root,
                _investigation_prompt(repo_root, oracle_file),
                read_only=True,
                expect_json=True,
                output_schema=_DISCREPANCY_OUTPUT_SCHEMA,
                json_validator=_validate_discrepancy_payload,
            )
        )
        values = payload.get("discrepancies")
        for value in values:
            discrepancies.append(value)
    return discrepancies


def _apply_discrepancies(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
) -> None:
    """Codex CLI にズレ追従作業を依頼する。"""
    # 実装変更用の workspace-write Codex 呼び出しを実行する。
    run_codex_exec(
        repo_root,
        _apply_prompt(repo_root, discrepancies),
        read_only=False,
        expect_json=False,
    )


def _assert_forbidden_paths_clean(repo_root: Path) -> None:
    """Codex CLI が編集禁止領域を変更していないことを確認する。"""
    # oracles と .agents に差分があれば、commit 前に中断する。
    forbidden = [
        path
        for path in changed_paths(repo_root)
        if path.startswith("oracles/") or path.startswith(".agents/")
    ]
    if forbidden:
        raise CmocError(
            "Forbidden paths were changed by implementation work.",
            [
                "Inspect and manually resolve the forbidden changes.",
                "Run `cmoc apply` again after the working tree is acceptable.",
            ],
            "\n".join(forbidden),
        )


def _commit_all_changes(repo_root: Path) -> None:
    """未コミット差分を Codex 生成メッセージで commit する。"""
    # 差分が無ければ commit message 生成も git commit も行わない。
    if not changed_paths(repo_root):
        return

    # 実装差分によって INDEX.md が古くなった場合は commit 前に更新する。
    maintain_indexes(repo_root)
    _assert_forbidden_paths_clean(repo_root)
    if not changed_paths(repo_root):
        return

    # Codex に 1 行 commit message を生成させ、空なら既定値を使う。
    message = run_codex_exec(
        repo_root,
        _commit_message_prompt(repo_root),
        read_only=True,
        expect_json=False,
    ).strip()
    if not message:
        message = "Apply oracle implementation changes"

    # 最終的な全差分を 1 commit にまとめる。
    run_git(repo_root, ["add", "--all"])
    run_git(repo_root, ["commit", "-m", message])


def _write_apply_report(
    repo_root: Path,
    branch_name: str,
    completed: bool,
    discrepancy_counts: list[int],
) -> Path:
    """作業レポートを Codex CLI に依頼し、ファイル保存する。"""
    # report 保存先と timestamp 付きファイル名を用意する。
    report_dir = repo_root / ".cmoc" / "reports" / "apply"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{make_timestamp()}.md"

    # Codex にはレポート本文だけを生成させ、ファイル保存は cmoc が行う。
    prompt = "\n".join(
        [
            "あなたはソフトウェア作業レポートの作成担当です。",
            f"`{repo_root}` のブランチ `{branch_name}` について簡潔な作業レポートを書いてください。",
            "完了条件は、作業結果、ズレ件数の推移、ブランチ上の全変更内容を説明することです。",
            f"Result: {'complete' if completed else 'incomplete'}",
            f"Discrepancy counts: {discrepancy_counts}",
            f"`{repo_root / 'oracles'}` と `{repo_root / '.agents'}` は編集禁止です。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )
    maintain_indexes(repo_root)
    report = run_codex_exec(
        repo_root,
        prompt,
        read_only=True,
        expect_json=False,
    )
    report_path.write_text(report, encoding="utf-8")
    return report_path


def _investigation_prompt(repo_root: Path, oracle_file: Path) -> str:
    """ズレ調査用 prompt を組み立てる。"""
    # Structured Output schema と禁止事項を prompt 上で明示する。
    return "\n".join(
        [
            "あなたはソフトウェア実装の監査担当です。",
            f"`{oracle_file}` と `{repo_root}` の実装との明確なズレを調査してください。",
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            "各ズレには oracle_path、oracle_line_start、oracle_line_end、",
            "implementation_paths、title、oracle_requirement、",
            "observed_implementation、reason、suggested_fix を",
            "含めてください。",
            "明確なズレがない場合だけ空配列を返してください。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _apply_prompt(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
) -> str:
    """ズレ追従作業用 prompt を組み立てる。"""
    # workspace-write 実行用に編集禁止領域を無条件で明示する。
    return "\n".join(
        [
            "あなたはソフトウェア実装担当です。",
            f"`{repo_root}` の実装を、以下のズレ一覧が解消されるように更新してください。",
            "完了条件は、実装が oracle 要求に追従し、必要なテスト更新も終わっていることです。",
            f"Discrepancies: {json.dumps(discrepancies, ensure_ascii=False)}",
            f"`{repo_root / 'oracles'}` は編集禁止です。",
            f"`{repo_root / '.agents'}` は編集禁止です。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
        ]
    )


def _commit_message_prompt(repo_root: Path) -> str:
    """commit message 生成用 prompt を組み立てる。"""
    # read-only 実行で commit message の文字列だけを要求する。
    return "\n".join(
        [
            "あなたは git commit message の作成担当です。",
            f"`{repo_root}` の現在の変更に対する簡潔な commit message を 1 行で書いてください。",
            "完了条件は、commit message だけを出力することです。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _validate_discrepancy_payload(value: object) -> None:
    """ズレ調査 Structured Output の schema を検査する。"""
    # top-level は discrepancies だけを持つ object に限定する。
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    if set(value) != {"discrepancies"}:
        raise ValueError("Expected only discrepancies key.")
    discrepancies = value.get("discrepancies")
    if not isinstance(discrepancies, list):
        raise ValueError("discrepancies must be a list.")

    # 各 discrepancy item の required keys を完全一致で検査する。
    required_keys = {
        "oracle_path",
        "oracle_line_start",
        "oracle_line_end",
        "implementation_paths",
        "title",
        "oracle_requirement",
        "observed_implementation",
        "reason",
        "suggested_fix",
    }
    for index, item in enumerate(discrepancies):
        # item ごとに型と各プロパティの型を検査する。
        if not isinstance(item, dict):
            raise ValueError(f"discrepancies[{index}] must be an object.")
        if set(item) != required_keys:
            raise ValueError(
                f"discrepancies[{index}] keys do not match schema."
            )
        _require_string(item, "oracle_path", index)
        _require_nullable_int(item, "oracle_line_start", index)
        _require_nullable_int(item, "oracle_line_end", index)
        paths = item["implementation_paths"]
        if not isinstance(paths, list) or not all(
            isinstance(path, str) for path in paths
        ):
            raise ValueError(
                f"discrepancies[{index}].implementation_paths must be "
                "list[str]."
            )
        for key in [
            "title",
            "oracle_requirement",
            "observed_implementation",
            "reason",
            "suggested_fix",
        ]:
            _require_string(item, key, index)


def _require_string(item: dict[str, object], key: str, index: int) -> None:
    """schema 上 string の項目を検査する。"""
    # 対象 key が Python str であることを保証する。
    if not isinstance(item[key], str):
        raise ValueError(f"discrepancies[{index}].{key} must be a string.")


def _require_nullable_int(
    item: dict[str, object],
    key: str,
    index: int,
) -> None:
    """schema 上 integer|null の項目を検査する。"""
    # 行番号は integer または null だけを許容する。
    if item[key] is not None and not isinstance(item[key], int):
        raise ValueError(
            f"discrepancies[{index}].{key} must be integer or null."
        )
