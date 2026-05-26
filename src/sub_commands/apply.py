"""`cmoc apply` の本体処理。"""

import json
from pathlib import Path

from commons.codex import (
    COMMIT_MESSAGE_MODEL,
    COMMIT_MESSAGE_REASONING_EFFORT,
    COST_PERFORMANCE_MODEL,
    COST_PERFORMANCE_REASONING_EFFORT,
    parse_json_object,
    run_codex_exec,
)
from commons.command_runner import run_command
from commons.errors import CmocError
from commons.indexing import maintain_indexes
from commons.repo import (
    assert_no_uncommitted_changes,
    changed_oracle_files,
    changed_paths,
    changed_implementation_files,
    commit_cmoc_initialization_changes,
    commit_if_changed,
    current_branch,
    ensure_cmoc_ignored,
    gitignore_has_cmoc_rule,
    head_commit,
    is_cmoc_branch,
    list_implementation_files,
    list_oracle_files,
    read_branch_base_commit,
    run_git,
    staged_diff_from_head,
)
from commons.timing import StepTimer, start_step
from commons.timestamps import make_timestamp

_APPLY_INCOMPLETE_EXIT_CODE: int = 2
_DISCREPANCY_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["fixing_points"],
    "properties": {
        "git_head_commit_hash": {
            "type": ["string", "null"],
            "description": (
                "要修正点を発見した時点での git HEAD commit hash。"
                "後で機械的にフィルされるので AI による出力は null で良い。"
            ),
        },
        "fixing_points": {
            "type": "array",
            "description": "実装に対する要修正点のリスト。空配列の場合のみ要修正点なしとみなす。",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "title",
                    "evidences",
                    "oracle_requirement",
                    "observed_implementation",
                    "reason",
                    "suggested_fix",
                ],
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "要修正点の短い見出し。",
                    },
                    "evidences": {
                        "type": "array",
                        "description": (
                            "要修正点の根拠となる文言の位置情報。"
                            "`oracles`・実装どちらかのファイルが必ず 1 つは"
                            "根拠として存在するはずであるから空配列は想定しない。"
                        ),
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": [
                                "path",
                                "line_start",
                                "line_end",
                                "summary",
                            ],
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "要修正点の根拠となるファイルの絶対パス。",
                                },
                                "line_start": {
                                    "type": ["integer", "null"],
                                    "description": (
                                        "要修正点の根拠となる記述の開始行。"
                                        "行番号を特定できない場合は null。"
                                    ),
                                },
                                "line_end": {
                                    "type": ["integer", "null"],
                                    "description": (
                                        "要修正点の根拠となる記述の終了行。"
                                        "行番号を特定できない場合は null。"
                                    ),
                                },
                                "summary": {
                                    "type": "string",
                                    "description": (
                                        "該当箇所の短い要約。位置情報がズレた場合に"
                                        "それを検知するための冗長情報。"
                                    ),
                                },
                            },
                        },
                    },
                    "oracle_requirement": {
                        "type": "string",
                        "description": (
                            "oracle が要求している仕様。実装のみから発見した"
                            "要修正点であったとしても必ず関係する仕様を記載する。"
                        ),
                    },
                    "observed_implementation": {
                        "type": "string",
                        "description": "調査時点の実装が実際にどうなっているか。",
                    },
                    "reason": {
                        "type": "string",
                        "description": (
                            "なぜ、明確に問題があり修正が必要であると言えるのか。"
                            "推測や未確認事項は含めない。"
                        ),
                    },
                    "suggested_fix": {
                        "type": "string",
                        "description": "問題を解決するために必要な実装修正の方針。",
                    },
                },
            },
        }
    },
}


def cmoc_apply_impl(
    repo_root: Path | None = None,
    *,
    repeat_investigate_and_fix: int = 5,
    repeat_improove_fixing_list: int = 3,
    full: bool = False,
) -> int | None:
    """oracle と実装の不整合を Codex CLI へ追従させる。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(
            lambda resolved_repo_root: cmoc_apply_impl(
                resolved_repo_root,
                repeat_investigate_and_fix=repeat_investigate_and_fix,
                repeat_improove_fixing_list=(
                    repeat_improove_fixing_list
                ),
                full=full,
            )
        )
        return None

    # apply は cmoc 作業ブランチ上でだけ実行できる。
    timer = StepTimer("apply")
    branch_name = current_branch(repo_root)
    if not is_cmoc_branch(branch_name):
        raise CmocError(
            "`cmoc apply` は cmoc 管理 branch 上で実行してください。",
            [
                "先に `cmoc session fork` を実行してください。",
                "既存の session branch を checkout してください。",
            ],
            f"現在の branch: {branch_name}",
        )
    base_commit = read_branch_base_commit(repo_root, branch_name)

    # `.cmoc` 保証差分と oracle 差分を分離 commit してから、その他の差分を拒否する。
    start_step(timer, 1, 4, "validate repository state")
    had_cmoc_rule = gitignore_has_cmoc_rule(repo_root)
    preexisting_staged_diff = staged_diff_from_head(repo_root)
    ensure_cmoc_ignored(repo_root)
    commit_cmoc_initialization_changes(
        repo_root,
        had_cmoc_rule,
        preexisting_staged_diff,
        "Ensure cmoc directory is ignored",
    )
    commit_if_changed(
        repo_root,
        ["oracles"],
        "Commit oracle changes before apply",
    )
    assert_no_uncommitted_changes(repo_root)

    # ユーザー向けステップとして INDEX.md を明示メンテナンスする。
    start_step(timer, 2, 4, "maintain INDEX.md files")
    maintain_indexes(repo_root)

    if repeat_investigate_and_fix < 0:
        raise CmocError(
            "調査・修正ループ回数に負の値は指定できません。",
            [
                "`--repeat-investigate-and-fix` には 0 以上の整数を指定してください。",
                "既定の上限を使う場合は `--repeat-investigate-and-fix` を省略してください。",
            ],
            f"repeat_investigate_and_fix: {repeat_investigate_and_fix}",
        )
    if repeat_improove_fixing_list < 0:
        raise CmocError(
            "要修正点リスト改善ループ回数に負の値は指定できません。",
            [
                "`--repeat-improove-fixing-list` には 0 以上の整数を指定してください。",
                "既定の上限を使う場合は `--repeat-improove-fixing-list` を省略してください。",
            ],
            f"repeat_improove_fixing_list: {repeat_improove_fixing_list}",
        )

    # 不整合調査と追従作業を指定回数まで反復する。
    start_step(timer, 3, 4, "investigate and apply discrepancies")
    discrepancy_counts: list[int] = []
    completed = False
    for loop_index in range(1, repeat_investigate_and_fix + 1):
        discrepancies = _investigate_discrepancies(
            repo_root,
            base_commit,
            repeat_improove_fixing_list=repeat_improove_fixing_list,
            full=full,
        )
        discrepancy_counts.append(len(discrepancies))
        print(
            "implementation loop "
            f"({loop_index}/{repeat_investigate_and_fix}) discrepancies: "
            f"{len(discrepancies)}"
        )
        if not discrepancies:
            completed = True
            break

        _apply_discrepancies(repo_root, discrepancies)

    # 実行結果を人間向け report と exit code に変換する。
    start_step(timer, 4, 4, "write report")
    report_path = _write_apply_report(
        repo_root,
        branch_name,
        completed,
        discrepancy_counts,
    )
    print(str(report_path))
    timer.report()
    return 0 if completed else _APPLY_INCOMPLETE_EXIT_CODE


def _investigate_discrepancies(
    repo_root: Path,
    base_commit: str,
    *,
    repeat_improove_fixing_list: int,
    full: bool,
) -> list[dict[str, object]]:
    """oracle ファイル・実装ファイルごとに不整合調査を実行する。"""
    # ループごとに部分・全体適用モードと調査対象を再評価する。
    discrepancies: list[dict[str, object]] = []
    # --full の有無だけで全体適用・部分適用を切り替える。
    partial = not full
    oracle_files = _target_oracle_files(repo_root, base_commit, partial)
    implementation_files = _target_implementation_files(
        repo_root,
        base_commit,
        partial,
    )

    # oracle ファイルを 1 件ずつ独立に調査する。
    for index, oracle_file in enumerate(oracle_files, start=1):
        print(
            f"investigate oracle ({index}/{len(oracle_files)}) "
            f"{oracle_file}"
        )
        # Structured Output の fixing_points を 1 つの一覧へ結合する。
        payload = parse_json_object(
            run_codex_exec(
                repo_root,
                _investigation_prompt(repo_root, oracle_file),
                purpose=(
                    f"investigate oracle {oracle_file.relative_to(repo_root)}"
                ),
                read_only=True,
                expect_json=True,
                output_schema=_DISCREPANCY_OUTPUT_SCHEMA,
                json_validator=_validate_discrepancy_payload,
                model=COST_PERFORMANCE_MODEL,
                reasoning_effort=COST_PERFORMANCE_REASONING_EFFORT,
            )
        )
        discrepancies.extend(
            _fixing_points_with_head_commit_hash(repo_root, payload)
        )

    # 実装ファイルも 1 件ずつ独立に調査する。
    for index, implementation_file in enumerate(
        implementation_files,
        start=1,
    ):
        print(
            "investigate implementation "
            f"({index}/{len(implementation_files)}) {implementation_file}"
        )
        payload = parse_json_object(
            run_codex_exec(
                repo_root,
                _implementation_investigation_prompt(
                    repo_root,
                    implementation_file,
                ),
                purpose=(
                    "investigate implementation "
                    f"{implementation_file.relative_to(repo_root)}"
                ),
                read_only=True,
                expect_json=True,
                output_schema=_DISCREPANCY_OUTPUT_SCHEMA,
                json_validator=_validate_discrepancy_payload,
                model=COST_PERFORMANCE_MODEL,
                reasoning_effort=COST_PERFORMANCE_REASONING_EFFORT,
            )
        )
        discrepancies.extend(
            _fixing_points_with_head_commit_hash(repo_root, payload)
        )

    return _improove_fixing_list(
        repo_root,
        discrepancies,
        repeat_improove_fixing_list,
    )


def _target_oracle_files(
    repo_root: Path,
    base_commit: str,
    partial: bool,
) -> list[Path]:
    """適用モードに応じた oracle 調査対象を返す。"""
    # 部分適用では列挙結果を cmoc ブランチ上の変更済みに絞る。
    all_files = list_oracle_files(repo_root)
    if not partial:
        return all_files
    changed = set(changed_oracle_files(repo_root, base_commit))
    return [path for path in all_files if path in changed]


def _target_implementation_files(
    repo_root: Path,
    base_commit: str,
    partial: bool,
) -> list[Path]:
    """適用モードに応じた実装調査対象を返す。"""
    # 部分適用では列挙結果を cmoc ブランチ上の変更済みに絞る。
    all_files = list_implementation_files(repo_root)
    if not partial:
        return all_files
    changed = set(changed_implementation_files(repo_root, base_commit))
    return [path for path in all_files if path in changed]


def _improove_fixing_list(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
    repeat_improove_fixing_list: int,
) -> list[dict[str, object]]:
    """要修正点リストを最大指定回数まで Codex CLI に改善させる。"""
    # 改善結果が前回と同一なら、改善点なしとして早期終了する。
    improved = discrepancies
    for loop_index in range(1, repeat_improove_fixing_list + 1):
        next_improved = _organize_discrepancies(repo_root, improved)
        print(
            "fixing list improvement loop "
            f"({loop_index}/{repeat_improove_fixing_list}) discrepancies: "
            f"{len(next_improved)}"
        )
        if next_improved == improved:
            break
        improved = next_improved
    return improved


def _organize_discrepancies(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
) -> list[dict[str, object]]:
    """連結した不整合リストを Codex CLI に整理させる。"""
    # 整理結果も同じ Structured Output schema で受け取って検証する。
    branch_name = current_branch(repo_root)
    base_commit = read_branch_base_commit(repo_root, branch_name)
    head_commit_hash = head_commit(repo_root)
    payload = parse_json_object(
        run_codex_exec(
            repo_root,
            _organize_prompt(
                repo_root,
                discrepancies,
                branch_name,
                base_commit,
                head_commit_hash,
            ),
            purpose="organize discrepancies",
            read_only=True,
            expect_json=True,
            output_schema=_DISCREPANCY_OUTPUT_SCHEMA,
            json_validator=_validate_discrepancy_payload,
        )
    )
    return _fixing_points_with_head_commit_hash(repo_root, payload)


def _fixing_points_with_head_commit_hash(
    repo_root: Path,
    payload: dict[str, object],
) -> list[dict[str, object]]:
    """Structured Output の要修正点へ発見時 HEAD commit hash を付与する。"""
    # AI 出力の git_head_commit_hash は信用せず、cmoc 側で現在の HEAD を記録する。
    commit_hash = head_commit(repo_root)
    values = payload.get("fixing_points")
    if not isinstance(values, list):
        return []
    fixing_points: list[dict[str, object]] = []
    for value in values:
        if not isinstance(value, dict):
            continue
        fixing_point = dict(value)
        fixing_point["git_head_commit_hash"] = commit_hash
        fixing_points.append(fixing_point)
    return fixing_points


def _apply_discrepancies(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
) -> None:
    """Codex CLI に不整合追従作業を依頼する。"""
    # 不整合 1 件ごとに修正、禁止領域検査、commit までを完結させる。
    for index, discrepancy in enumerate(discrepancies, start=1):
        print(f"apply discrepancy ({index}/{len(discrepancies)})")
        run_codex_exec(
            repo_root,
            _apply_prompt(repo_root, discrepancy),
            purpose=f"apply discrepancy {index}/{len(discrepancies)}",
            read_only=False,
            expect_json=False,
        )
        _assert_forbidden_paths_clean(repo_root)
        _commit_all_changes(repo_root)


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
        purpose="generate commit message",
        read_only=True,
        expect_json=False,
        model=COMMIT_MESSAGE_MODEL,
        reasoning_effort=COMMIT_MESSAGE_REASONING_EFFORT,
    ).strip()
    if not message:
        message = "Apply oracle implementation changes"

    # 最終的な全差分を 1 commit にまとめる。
    run_git(repo_root, ["add", "--all"])
    run_git(repo_root, ["commit", "-m", message])


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
            "実装作業により編集禁止パスが変更されました。",
            [
                "編集禁止パスの変更を確認し、手動で解消してください。",
                "作業ツリーが許容できる状態になってから `cmoc apply` を再実行してください。",
            ],
            "\n".join(forbidden),
        )


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
    result_label = "収束" if completed else "未収束"
    incomplete_instruction = (
        "「未収束」の場合は、不整合件数の推移に「まだ不整合が残っている可能性」を必ず追記してください。"
    )
    prompt = "\n".join(
        [
            "あなたはソフトウェア作業レポートの作成担当です。",
            f"`{repo_root}` のブランチ `{branch_name}` について簡潔な作業レポートを書いてください。",
            "完了条件は、作業結果、不整合件数の推移、ブランチ上の全変更内容を説明することです。",
            "Markdown 見出しとして「作業結果」「不整合件数の推移」「全変更内容」を必ず含めてください。",
            "不整合件数の推移には、ループごとに何件の不整合を見つけたかを書いてください。",
            incomplete_instruction,
            f"ブランチ `{branch_name}` 上の全変更内容は、今回の自動適用処理以前の作業も含めてください。",
            "ブランチ上の変更内容は、変更内容の意味論に基づき「カテゴリ」という語を使って要約してください。",
            f"作業結果の区分は一言で `{result_label}` と書いてください。",
            f"作業結果区分: {result_label}",
            f"不整合件数: {discrepancy_counts}",
            f"`{repo_root / 'oracles'}` と `{repo_root / '.agents'}` は編集禁止です。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )
    maintain_indexes(repo_root)
    report = run_codex_exec(
        repo_root,
        prompt,
        purpose="write apply report",
        read_only=True,
        expect_json=False,
        model=COST_PERFORMANCE_MODEL,
        reasoning_effort=COST_PERFORMANCE_REASONING_EFFORT,
        text_validator=lambda value: _validate_apply_report(
            value,
            branch_name,
            result_label,
            completed,
            discrepancy_counts,
        ),
    )
    try:
        _validate_apply_report(
            report,
            branch_name,
            result_label,
            completed,
            discrepancy_counts,
        )
    except ValueError as error:
        raise CmocError(
            "Codex CLI が生成した apply report に必須内容がありません。",
            [
                "Codex report 生成 prompt を確認してから再実行してください。",
                "問題が続く場合は、Codex CLI の出力を確認してから `cmoc apply` を再実行してください。",
            ],
            str(error),
        ) from error
    report_path.write_text(report, encoding="utf-8")
    return report_path


def _validate_apply_report(
    report: str,
    branch_name: str,
    result_label: str,
    completed: bool,
    discrepancy_counts: list[int],
) -> None:
    """保存前の apply レポートが必須内容を持つことを機械的に確認する。"""
    # Markdown の意味解釈ではなく、必須セクションと既知値の存在を検査する。
    missing: list[str] = []
    if "作業結果" not in report or result_label not in report:
        missing.append("作業結果の区分")
    if "不整合件数の推移" not in report:
        missing.append("不整合件数の推移")
    for index, count in enumerate(discrepancy_counts, start=1):
        if f"{index}" not in report or f"{count}" not in report:
            missing.append(f"不整合件数の推移 loop {index}")
    if (
        not completed
        and "まだ不整合が残っている可能性" not in report
    ):
        missing.append("未収束時の残存可能性")
    if (
        branch_name not in report
        or "全変更内容" not in report
        or "カテゴリ" not in report
    ):
        missing.append("ブランチ上の全変更内容の意味論的カテゴリ別要約")

    # 不完全な Codex 出力をそのまま保存せず、共通エラーとして中断する。
    if missing:
        raise ValueError(
            "Codex CLI が生成した apply report に必須内容がありません:\n"
            + "\n".join(missing)
        )


def _investigation_prompt(repo_root: Path, oracle_file: Path) -> str:
    """不整合調査用 prompt を組み立てる。"""
    # Structured Output schema と禁止事項を prompt 上で明示する。
    return "\n".join(
        [
            "あなたはソフトウェア実装の監査担当です。",
            f"`{oracle_file}` を起点に `{repo_root}` の要修正点を調査してください。",
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            "要修正点には、oracles ファイルと実装との明確な不整合だけでなく、",
            "実装だけから見た成果物品質上の致命的な問題も含めてください。",
            "実装のみから発見した要修正点でも、関係する oracle 仕様を oracle_requirement に記載してください。",
            "指定ファイルは調査の起点であり、必要なら他の oracle・実装ファイルも読んでください。",
            "各要修正点には title、evidences、oracle_requirement、",
            "observed_implementation、reason、suggested_fix を含めてください。",
            "evidences には path、line_start、line_end、summary を含めてください。",
            "明確な要修正点がない場合だけ fixing_points に空配列を返してください。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _implementation_investigation_prompt(
    repo_root: Path,
    implementation_file: Path,
) -> str:
    """実装ファイル起点の不整合調査用 prompt を組み立てる。"""
    # 指定ファイルは調査起点であり、必要な関連ファイル参照は許可する。
    return "\n".join(
        [
            "あなたはソフトウェア実装の監査担当です。",
            f"`{implementation_file}` を起点に、",
            f"`{repo_root}` の要修正点を調査してください。",
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            "要修正点には、oracles ファイルと実装との明確な不整合だけでなく、",
            "実装だけから見た成果物品質上の致命的な問題も含めてください。",
            "実装のみから発見した要修正点でも、関係する oracle 仕様を oracle_requirement に記載してください。",
            "指定ファイルは調査の起点であり、必要なら他の oracle・実装ファイルも読んでください。",
            "各要修正点には title、evidences、oracle_requirement、",
            "observed_implementation、reason、suggested_fix を含めてください。",
            "evidences には path、line_start、line_end、summary を含めてください。",
            "明確な要修正点がない場合だけ fixing_points に空配列を返してください。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _organize_prompt(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
    branch_name: str,
    base_commit: str,
    head_commit_hash: str,
) -> str:
    """不整合リスト整理用 prompt を組み立てる。"""
    # 個別調査結果の重複や矛盾を整理し、同じ schema で返させる。
    structured_discrepancies = _discrepancies_for_structured_output(
        discrepancies
    )
    return "\n".join(
        [
            "あなたはソフトウェア監査結果の整理担当です。",
            f"`{repo_root}` の要修正点リストを整理してください。",
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            "要修正点の内容の品質に明確な問題がない状態を目指してください。",
            (
                "重複する要修正点は 1 件にマージし、"
                "矛盾する修正方針は矛盾しない内容に調整してください。"
            ),
            (
                f"git ブランチ `{branch_name}` の "
                f"`{base_commit}..{head_commit_hash}` "
                "に含まれる過去の修正内容を確認し、その内容を考慮してください。"
            ),
            "False-Positive と判断できる要修正点は除外してください。",
            "要修正点を先頭から順番に対応した時に、作業順序として適切になるよう並べ替えてください。",
            "改善過程で発見した漏れがあれば、要修正点リストに追加してください。",
            "実装のみから発見した要修正点でも、関係する oracle 仕様を oracle_requirement に記載してください。",
            "改善点がない場合は入力と同じ要修正点リストを返してください。",
            "明確な要修正点がない場合だけ fixing_points に空配列を返してください。",
            "連結済み要修正点リスト: "
            f"{json.dumps(structured_discrepancies, ensure_ascii=False)}",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _discrepancies_for_structured_output(
    discrepancies: list[dict[str, object]],
) -> list[dict[str, object]]:
    """cmoc 内部メタデータを Structured Output 用の要修正点から除外する。"""
    # fixing_points item は schema 上 additionalProperties false なので内部キーを出さない。
    return [
        {
            key: value
            for key, value in discrepancy.items()
            if key != "git_head_commit_hash"
        }
        for discrepancy in discrepancies
    ]


def _apply_prompt(
    repo_root: Path,
    discrepancy: dict[str, object],
) -> str:
    """不整合追従作業用 prompt を組み立てる。"""
    # workspace-write 実行用に編集禁止領域を無条件で明示する。
    return "\n".join(
        [
            "あなたはソフトウェア実装担当です。",
            f"`{repo_root}` の実装を、oracle 要求に追従するようベストエフォートで更新してください。",
            "完了条件は、必要と判断した実装修正とテスト更新を終え、変更内容と残課題を報告することです。",
            "作業が必要と判断できる場合は、実装修正と必要なテスト更新を行ってください。",
            "以下の要修正点情報は作業のためのヒントです。",
            "絶対に従わなければならない指示書としては扱わないでください。",
            "実装状況や oracle を確認した結果として不適切なら、この要修正点情報は無視してかまいません。",
            "作業目的は、要修正点が指摘している問題の修正を試みることです。",
            "要修正点本文への逐語的追従や、要修正点で述べている目的を達成した保証は不要です。",
            f"要修正点: {json.dumps(discrepancy, ensure_ascii=False)}",
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
    """不整合調査 Structured Output の schema を検査する。"""
    # top-level は fixing_points と任意の git_head_commit_hash に限定する。
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    allowed_keys = {"fixing_points", "git_head_commit_hash"}
    if "fixing_points" not in value or not set(value).issubset(allowed_keys):
        raise ValueError(
            "Expected fixing_points and optional git_head_commit_hash keys."
        )
    commit_hash = value.get("git_head_commit_hash")
    if commit_hash is not None and not isinstance(commit_hash, str):
        raise ValueError("git_head_commit_hash must be a string or null.")
    fixing_points = value.get("fixing_points")
    if not isinstance(fixing_points, list):
        raise ValueError("fixing_points must be a list.")

    # 各 fixing point item の required keys を完全一致で検査する。
    required_keys = {
        "title",
        "evidences",
        "oracle_requirement",
        "observed_implementation",
        "reason",
        "suggested_fix",
    }
    for index, item in enumerate(fixing_points):
        # item ごとに型と各プロパティの型を検査する。
        if not isinstance(item, dict):
            raise ValueError(f"fixing_points[{index}] must be an object.")
        if set(item) != required_keys:
            raise ValueError(
                f"fixing_points[{index}] keys do not match schema."
            )
        _require_string(item, "title", index)
        _validate_evidences(item["evidences"], index)
        for key in [
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
        raise ValueError(f"fixing_points[{index}].{key} must be a string.")


def _validate_evidences(value: object, item_index: int) -> None:
    """schema 上 evidences の項目を検査する。"""
    # evidence は根拠位置の構造化情報として完全一致で検査する。
    if not isinstance(value, list) or not value:
        raise ValueError(
            f"fixing_points[{item_index}].evidences must be a non-empty list."
        )
    required_keys = {"path", "line_start", "line_end", "summary"}
    for evidence_index, evidence in enumerate(value):
        if not isinstance(evidence, dict):
            raise ValueError(
                "fixing_points"
                f"[{item_index}].evidences[{evidence_index}] "
                "must be an object."
            )
        if set(evidence) != required_keys:
            raise ValueError(
                "fixing_points"
                f"[{item_index}].evidences[{evidence_index}] "
                "keys do not match schema."
            )
        _require_evidence_string(evidence, "path", item_index, evidence_index)
        _require_evidence_absolute_path(evidence, item_index, evidence_index)
        _require_evidence_nullable_int(
            evidence,
            "line_start",
            item_index,
            evidence_index,
        )
        _require_evidence_nullable_int(
            evidence,
            "line_end",
            item_index,
            evidence_index,
        )
        _require_evidence_string(
            evidence,
            "summary",
            item_index,
            evidence_index,
        )


def _require_evidence_string(
    item: dict[object, object],
    key: str,
    item_index: int,
    evidence_index: int,
) -> None:
    """schema 上 evidence 内 string の項目を検査する。"""
    if not isinstance(item[key], str):
        raise ValueError(
            "fixing_points"
            f"[{item_index}].evidences[{evidence_index}].{key} "
            "must be a string."
        )


def _require_evidence_absolute_path(
    item: dict[object, object],
    item_index: int,
    evidence_index: int,
) -> None:
    """schema 上 evidence path が絶対パスであることを検査する。"""
    path = item["path"]
    if not isinstance(path, str) or not Path(path).is_absolute():
        raise ValueError(
            "fixing_points"
            f"[{item_index}].evidences[{evidence_index}].path "
            "must be an absolute path."
        )


def _require_evidence_nullable_int(
    item: dict[object, object],
    key: str,
    item_index: int,
    evidence_index: int,
) -> None:
    """schema 上 evidence 内 integer|null の項目を検査する。"""
    if (
        item[key] is not None
        and (not isinstance(item[key], int) or isinstance(item[key], bool))
    ):
        raise ValueError(
            "fixing_points"
            f"[{item_index}].evidences[{evidence_index}].{key} "
            "must be integer or null."
        )
