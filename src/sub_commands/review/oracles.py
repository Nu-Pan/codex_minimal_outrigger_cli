"""`cmoc review oracles` の本体処理。"""

from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import sys
import tempfile

from commons.codex import (
    FRONTIER_HIGH_REASONING_EFFORT,
    FRONTIER_MODEL,
    parse_json_object,
    run_codex_exec,
)
from commons.command_runner import run_command
from commons.indexing import maintain_indexes
from commons.report_files import write_timestamped_report
from commons.repo import (
    changed_oracle_files,
    current_branch,
    ensure_cmoc_ignored,
    has_deleted_oracle_files,
    head_commit,
    is_cmoc_branch,
    is_session_branch,
    list_oracle_files,
    read_session_start_commit,
)
from commons.timing import StepTimer, start_step

_SEVERITY_ORDER = ["fatal", "inconclusive", "warning"]
_ISSUE_ID_PREFIXES = {
    "fatal": "FATAL",
    "inconclusive": "INCONCLUSIVE",
    "warning": "WARN",
}
_REPORT_COMMAND = "cmoc review oracles"
_REPORT_DIR_NAME = "review_oracles"
_DEFAULT_REPEAT_IMPROVE_ISSUES_LIST = 3
_MAX_REPEAT_IMPROVE_ISSUES_LIST = 3
_ISSUE_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "severity",
        "title",
        "oracle_path",
        "oracle_line_start",
        "oracle_line_end",
        "referenced_paths",
        "affected_workflow",
        "requirement",
        "problem",
        "reason",
        "suggested_oracle_change",
        "specification_only_basis",
    ],
    "properties": {
        "severity": {
            "type": "string",
            "enum": ["fatal", "warning", "inconclusive"],
            "description": "問題点の分類。",
        },
        "title": {
            "type": "string",
            "description": "問題点の短い見出し。",
        },
        "oracle_path": {
            "type": "string",
            "description": "問題点の根拠となる仕様ファイルの絶対パス。",
        },
        "oracle_line_start": {
            "anyOf": [
                {"type": "integer", "minimum": 1},
                {"type": "null"},
            ],
            "description": (
                "問題点の根拠となる仕様記述の開始行。"
                "特定できない場合は null。"
            ),
        },
        "oracle_line_end": {
            "anyOf": [
                {"type": "integer", "minimum": 1},
                {"type": "null"},
            ],
            "description": (
                "問題点の根拠となる仕様記述の終了行。"
                "特定できない場合は null。"
            ),
        },
        "referenced_paths": {
            "type": "array",
            "description": (
                "この問題点の評価時に参照した仕様ファイルまたは INDEX.md の絶対パス。"
            ),
            "items": {"type": "string"},
        },
        "affected_workflow": {
            "type": "string",
            "description": (
                "影響を受ける workflow / subcommand / concept。"
                "例: apply fork, review, overall。"
            ),
        },
        "requirement": {
            "type": "string",
            "description": "仕様ファイルが要求している、または要求すべき仕様。",
        },
        "problem": {
            "type": "string",
            "description": "仕様上の問題点。",
        },
        "reason": {
            "type": "string",
            "description": (
                "なぜその severity と判断したのか。fatal の場合は"
                "致命的問題の定義との対応を明示する。"
            ),
        },
        "suggested_oracle_change": {
            "type": "string",
            "description": "仕様ファイルをどう修正すべきか。",
        },
        "specification_only_basis": {
            "type": "string",
            "description": (
                "この問題点の評価が仕様ファイルと INDEX.md だけに"
                "基づくことの説明。"
            ),
        },
    },
}
_EVALUATION_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["issues"],
    "properties": {
        "issues": {
            "type": "array",
            "description": "検出した問題点。問題がない場合は空配列。",
            "items": _ISSUE_OUTPUT_SCHEMA,
        },
    },
}


@dataclass(frozen=True)
class _OracleEvaluationSnapshot:
    """review 開始時点の oracles tree を評価用に固定した copy。"""

    original_repo_root: Path
    original_oracle_root: Path
    snapshot_root: Path
    snapshot_oracle_root: Path
    oracle_files: frozenset[Path]
    reference_files: frozenset[Path]


def cmoc_review_oracles_impl(
    repo_root: Path | None = None,
    *,
    full: bool,
    repeat_improve_issues_list: int = _DEFAULT_REPEAT_IMPROVE_ISSUES_LIST,
) -> None:
    """oracle 断片を Codex CLI で評価し、レポートを作る。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(
            lambda resolved_repo_root: cmoc_review_oracles_impl(
                resolved_repo_root,
                full=full,
                repeat_improve_issues_list=repeat_improve_issues_list,
            )
        )
        return
    _validate_repeat_improve_issues_list(repeat_improve_issues_list)

    timer = StepTimer("review oracles")
    mode = None
    branch_name = None
    cmoc_branch = None
    base_commit = None
    commit_hash = None
    deleted_oracles = None
    all_oracle_files: list[Path] = []
    all_oracle_files_known = False
    oracle_files: list[Path] = []
    evaluations = []
    failed_stage = "review oracles 初期化"
    try:
        # 評価前に `.cmoc` の ignore 保証を済ませる。
        failed_stage = ".cmoc ignore 確認"
        start_step(timer, 1, 6, ".cmoc ignore 確認")
        ensure_cmoc_ignored(repo_root)

        # branch 状態と `--full` だけから、部分評価か全体評価かを決める。
        failed_stage = "oracle ファイル選定"
        start_step(timer, 2, 6, "oracle ファイル選定")
        branch_name = current_branch(repo_root)
        cmoc_branch = is_cmoc_branch(branch_name)
        session_branch = is_session_branch(branch_name)
        partial = session_branch and not full
        mode = "partial" if partial else "full"
        if partial:
            base_commit = read_session_start_commit(repo_root, branch_name)
            deleted_oracles = has_deleted_oracle_files(repo_root, base_commit)
        else:
            deleted_oracles = False

        # 評価モードに応じて Codex CLI に渡す oracle ファイル一覧を作る。
        all_oracle_files = list_oracle_files(repo_root)
        all_oracle_files_known = True
        if partial:
            assert base_commit is not None
            changed_files = set(changed_oracle_files(repo_root, base_commit))
            oracle_files = [
                path for path in all_oracle_files if path in changed_files
            ]
        else:
            oracle_files = all_oracle_files
        commit_hash = head_commit(repo_root)

        failed_stage = "oracle snapshot 作成"
        with tempfile.TemporaryDirectory(
            prefix="cmoc-review-oracles-"
        ) as snapshot_dir:
            # Codex CLI が読む oracle 本文は review 開始時点 snapshot に固定する。
            oracle_snapshot = _create_oracle_evaluation_snapshot(
                repo_root,
                all_oracle_files,
                Path(snapshot_dir),
            )

            failed_stage = "INDEX.md メンテナンス"
            start_step(timer, 3, 6, "INDEX.md メンテナンス")
            _maintain_indexes_after_oracle_snapshot(repo_root)
            oracle_snapshot = _sync_maintained_indexes_to_oracle_snapshot(
                repo_root,
                oracle_snapshot,
            )

            # oracle ファイルごとに Codex CLI 評価を実行する。
            failed_stage = "oracle ファイル評価"
            start_step(timer, 4, 6, "oracle ファイル評価")
            for index, oracle_file in enumerate(oracle_files, start=1):
                print(
                    f"oracle 評価 ({index}/{len(oracle_files)}) "
                    f"{oracle_file}"
                )
            if oracle_files:
                with ThreadPoolExecutor(
                    max_workers=len(oracle_files)
                ) as executor:
                    futures = [
                        executor.submit(
                            _evaluate_oracle_file,
                            repo_root,
                            oracle_file,
                            oracle_snapshot,
                        )
                        for oracle_file in oracle_files
                    ]
                    _append_evaluation_records_in_order(futures, evaluations)

            failed_stage = "問題点リスト改善"
            start_step(timer, 5, 6, "問題点リスト改善")
            evaluations = _improve_evaluations(
                repo_root,
                evaluations,
                repeat_improve_issues_list,
                oracle_snapshot,
            )

            # 評価結果を 1 つの Markdown レポートとして保存する。
            failed_stage = "report 書き込み"
            start_step(timer, 6, 6, "report 書き込み")
            report_path = _write_report(
                repo_root,
                mode,
                full,
                branch_name,
                cmoc_branch,
                base_commit,
                commit_hash,
                deleted_oracles,
                len(all_oracle_files),
                oracle_files,
                evaluations,
            )
    except Exception as error:
        try:
            report_path = _write_error_report(
                repo_root,
                mode,
                full,
                branch_name,
                cmoc_branch,
                base_commit,
                commit_hash,
                deleted_oracles,
                len(all_oracle_files) if all_oracle_files_known else None,
                oracle_files,
                evaluations,
                failed_stage,
                error,
            )
        except Exception as report_error:
            error.add_note(
                "review oracles error report generation also failed: "
                f"{type(report_error).__name__}: {report_error}"
            )
            _print_error_report_fallback(
                repo_root,
                mode,
                full,
                branch_name,
                cmoc_branch,
                base_commit,
                commit_hash,
                deleted_oracles,
                len(all_oracle_files) if all_oracle_files_known else None,
                oracle_files,
                evaluations,
                failed_stage,
                error,
                report_error,
            )
        else:
            print(str(report_path))
        raise
    print(str(report_path))
    timer.report()


def _validate_repeat_improve_issues_list(value: int) -> None:
    """問題点リスト改善の反復回数が oracle の上限内か検証する。"""
    if value < 0 or value > _MAX_REPEAT_IMPROVE_ISSUES_LIST:
        raise ValueError(
            "--repeat-improve-issues-list must be between 0 and "
            f"{_MAX_REPEAT_IMPROVE_ISSUES_LIST}."
        )


def _maintain_indexes_after_oracle_snapshot(repo_root: Path) -> bool:
    """評価 snapshot とは分離して INDEX.md をメンテナンスする。"""
    return maintain_indexes(repo_root)


def _create_oracle_evaluation_snapshot(
    repo_root: Path,
    oracle_files: list[Path],
    snapshot_root: Path,
) -> _OracleEvaluationSnapshot:
    """開始時点の oracles tree を一時 copy として固定する。"""
    original_oracle_root = (repo_root / "oracles").resolve()
    snapshot_oracle_root = snapshot_root / "oracles"
    if original_oracle_root.exists():
        _copy_oracles_tree_snapshot(original_oracle_root, snapshot_oracle_root)
    else:
        snapshot_oracle_root.mkdir(parents=True)

    reference_files = {path.resolve() for path in oracle_files}
    reference_files.update(
        _original_path_for_snapshot_path(
            repo_root,
            snapshot_oracle_root,
            index_path,
        )
        for index_path in snapshot_oracle_root.rglob("INDEX.md")
        if index_path.is_file()
    )
    return _OracleEvaluationSnapshot(
        original_repo_root=repo_root.resolve(),
        original_oracle_root=original_oracle_root,
        snapshot_root=snapshot_root.resolve(),
        snapshot_oracle_root=snapshot_oracle_root.resolve(),
        oracle_files=frozenset(path.resolve() for path in oracle_files),
        reference_files=frozenset(reference_files),
    )


def _sync_maintained_indexes_to_oracle_snapshot(
    repo_root: Path,
    snapshot: _OracleEvaluationSnapshot,
) -> _OracleEvaluationSnapshot:
    """メンテナンス後の INDEX.md だけを評価 snapshot へ反映する。"""
    original_oracle_root = (repo_root / "oracles").resolve()
    snapshot_oracle_root = snapshot.snapshot_oracle_root

    live_index_relatives: set[Path] = set()
    if original_oracle_root.exists():
        for original_index_path in original_oracle_root.rglob("INDEX.md"):
            if not original_index_path.is_file():
                continue
            relative_path = original_index_path.relative_to(original_oracle_root)
            live_index_relatives.add(relative_path)
            snapshot_index_path = snapshot_oracle_root / relative_path
            snapshot_index_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                original_index_path,
                snapshot_index_path,
                follow_symlinks=True,
            )

    for snapshot_index_path in snapshot_oracle_root.rglob("INDEX.md"):
        if not snapshot_index_path.is_file():
            continue
        relative_path = snapshot_index_path.relative_to(snapshot_oracle_root)
        if relative_path not in live_index_relatives:
            snapshot_index_path.unlink()

    reference_files = set(snapshot.oracle_files)
    reference_files.update(
        _original_path_for_snapshot_path(
            repo_root,
            snapshot_oracle_root,
            index_path,
        )
        for index_path in snapshot_oracle_root.rglob("INDEX.md")
        if index_path.is_file()
    )
    return _OracleEvaluationSnapshot(
        original_repo_root=snapshot.original_repo_root,
        original_oracle_root=snapshot.original_oracle_root,
        snapshot_root=snapshot.snapshot_root,
        snapshot_oracle_root=snapshot.snapshot_oracle_root,
        oracle_files=snapshot.oracle_files,
        reference_files=frozenset(reference_files),
    )


def _copy_oracles_tree_snapshot(source_root: Path, destination_root: Path) -> None:
    """oracles tree の file 内容を symlink 参照先も含めて固定 copy する。"""
    destination_root.mkdir(parents=True)
    for source_path in source_root.rglob("*"):
        relative_path = source_path.relative_to(source_root)
        destination_path = destination_root / relative_path
        if source_path.is_dir():
            destination_path.mkdir(exist_ok=True)
            continue
        if not source_path.is_file():
            continue
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path, follow_symlinks=True)


def _original_path_for_snapshot_path(
    repo_root: Path,
    snapshot_oracle_root: Path,
    snapshot_path: Path,
) -> Path:
    """snapshot 内 path に対応する元 repo 側の絶対 path を返す。"""
    return (
        repo_root
        / "oracles"
        / snapshot_path.relative_to(snapshot_oracle_root)
    ).resolve()


def _snapshot_path_for_original_path(
    snapshot: _OracleEvaluationSnapshot,
    original_path: Path,
) -> Path:
    """元 repo 側 oracle path に対応する snapshot 側 path を返す。"""
    return (
        snapshot.snapshot_oracle_root
        / original_path.resolve().relative_to(snapshot.original_oracle_root)
    ).resolve()


def _evaluate_oracle_file(
    repo_root: Path,
    oracle_file: Path,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> dict[str, object]:
    """1 oracle ファイルの評価を実行し、report 用レコードを返す。"""
    payload = parse_json_object(
        run_codex_exec(
            repo_root,
            _evaluation_prompt(repo_root, oracle_file, oracle_snapshot),
            purpose=f"oracle 評価 {oracle_file.relative_to(repo_root)}",
            read_only=True,
            expect_json=True,
            output_schema=_EVALUATION_OUTPUT_SCHEMA,
            json_validator=lambda value: _validate_evaluation_payload(
                value,
                repo_root,
                oracle_file,
                oracle_snapshot,
            ),
        )
    )
    return _evaluation_payload_to_record(payload, repo_root, oracle_file)


def _append_evaluation_records_in_order(
    futures: list[Future[dict[str, object]]],
    evaluations: list[dict[str, object]],
) -> None:
    """並列評価結果を dispatch 時の順序で回収する。"""
    for future in futures:
        evaluations.append(future.result())


def _evaluation_prompt(
    repo_root: Path,
    oracle_file: Path,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> str:
    """oracle 評価用 prompt を組み立てる。"""
    # Codex CLI には prompt だけで解釈できる具体的な絶対パスを渡す。
    concrete_repo_root = repo_root.resolve()
    concrete_oracle_file = oracle_file.resolve()
    concrete_oracle_root = (concrete_repo_root / "oracles").resolve()
    concrete_oracle_index = (concrete_oracle_root / "INDEX.md").resolve()
    readable_oracle_file = concrete_oracle_file
    readable_oracle_root = concrete_oracle_root
    readable_oracle_index = concrete_oracle_index
    if oracle_snapshot is not None:
        readable_oracle_file = _snapshot_path_for_original_path(
            oracle_snapshot,
            concrete_oracle_file,
        )
        readable_oracle_root = oracle_snapshot.snapshot_oracle_root
        readable_oracle_index = (
            oracle_snapshot.snapshot_oracle_root / "INDEX.md"
        ).resolve()

    # 仕様の構成順序に従い、完了条件を詳細指示より前に置く。
    lines = [
        "あなたはソフトウェア仕様のレビュー担当です。",
        f"`{concrete_repo_root}` 内の仕様ファイル "
        f"`{concrete_oracle_file}` を評価してください。",
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
        "issues には検出した問題点を入れ、問題がない場合は空配列を返してください。",
    ]
    if oracle_snapshot is not None:
        lines.append(
            "評価時に読む対象ファイルは、開始時点の内容を固定したコピー "
            f"`{readable_oracle_file}` です。"
        )
    lines.extend(
        [
            "問題がある場合、各 issue の referenced_paths には参照した仕様ファイル",
            "または INDEX.md に対応する元リポジトリ側の絶対パスをすべて返してください。",
            f"出力する oracle_path / referenced_paths は `{concrete_oracle_root}` "
            "配下の絶対パスにしてください。",
            "INDEX.md は自動生成されるため評価対象ではありません。",
            "INDEX.md は関連ファイル選定・参照根拠としてだけ読んでください。",
            "各 issue の specification_only_basis には、評価が仕様ファイルと",
            "INDEX.md だけに基づくことの説明を書いてください。",
            "対象仕様ファイル、関連する仕様ファイル、関連判断に必要な",
            f"`{readable_oracle_root}` 配下の INDEX.md だけを読んでください。",
            f"`{readable_oracle_index}` から始まる INDEX.md の Summary /",
            "Read this when / Do not read this when を根拠に、",
            "関連する仕様ファイルを選定してください。",
            f"`{readable_oracle_root}` 外のファイルは一切参照禁止です。",
            "実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。",
            "致命的な問題とは、実装を参照せずに仕様だけから判断・実装したとき、",
            "主要ワークフローを壊す、完了判定を妨げる、または中核目的を",
            "満たしたと判断できなくする問題です。",
            f"`{concrete_repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )
    if oracle_snapshot is not None:
        lines.insert(
            lines.index("実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。"),
            f"`{concrete_oracle_root}` は path 変換のためにだけ使い、読まないでください。",
        )
    return "\n".join(lines)


def _improve_evaluations(
    repo_root: Path,
    evaluations: list[dict[str, object]],
    repeat_improve_issues_list: int,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> list[dict[str, object]]:
    """結合済み issue list を Codex CLI で反復改善する。"""
    if repeat_improve_issues_list == 0:
        return evaluations
    issues = _all_issues(evaluations)
    if not issues:
        return evaluations

    current_payload = {"issues": issues}
    for index in range(repeat_improve_issues_list):
        previous_payload_text = json.dumps(
            current_payload,
            ensure_ascii=False,
            sort_keys=True,
        )
        payload = parse_json_object(
            run_codex_exec(
                repo_root,
                _improvement_prompt(repo_root, current_payload, oracle_snapshot),
                purpose=f"oracle 問題点リスト改善 {index + 1}",
                read_only=True,
                expect_json=True,
                output_schema=_EVALUATION_OUTPUT_SCHEMA,
                model=FRONTIER_MODEL,
                reasoning_effort=FRONTIER_HIGH_REASONING_EFFORT,
                json_validator=lambda value: _validate_issues_payload(
                    value,
                    repo_root,
                    _target_oracle_paths(evaluations),
                    oracle_snapshot,
                ),
            )
        )
        current_payload = payload
        current_payload_text = json.dumps(
            current_payload,
            ensure_ascii=False,
            sort_keys=True,
        )
        if current_payload_text == previous_payload_text:
            break

    return _redistribute_improved_issues(evaluations, current_payload["issues"])


def _improvement_prompt(
    repo_root: Path,
    issue_payload: dict[str, object],
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> str:
    """問題点リスト改善用 prompt を組み立てる。"""
    concrete_repo_root = repo_root.resolve()
    concrete_oracle_root = (concrete_repo_root / "oracles").resolve()
    concrete_oracle_index = (concrete_oracle_root / "INDEX.md").resolve()
    readable_oracle_root = concrete_oracle_root
    readable_oracle_index = concrete_oracle_index
    if oracle_snapshot is not None:
        readable_oracle_root = oracle_snapshot.snapshot_oracle_root
        readable_oracle_index = (
            oracle_snapshot.snapshot_oracle_root / "INDEX.md"
        ).resolve()
    payload_text = json.dumps(issue_payload, ensure_ascii=False, indent=2)
    lines = [
        "あなたはソフトウェア仕様レビュー結果の整理担当です。",
        f"`{concrete_repo_root}` の仕様評価で得られた問題点リストを改善してください。",
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
    ]
    if oracle_snapshot is not None:
        lines.append(
            "必要に応じて読む仕様ファイル群は、開始時点の内容を固定したコピー "
            f"`{readable_oracle_root}` です。"
        )
    lines.extend(
        [
            "入力 issues を意味論的に統合・改善し、重複、矛盾、False-Positive を",
            "ベストエフォートで減らしてください。",
            "問題点がない場合は issues: [] を返してください。",
            "必要に応じて仕様ファイル、関連する仕様ファイル、関連判断に必要な",
            f"`{readable_oracle_root}` 配下の INDEX.md だけを読んでください。",
            f"`{readable_oracle_index}` から始まる INDEX.md の Summary /",
            "Read this when / Do not read this when を根拠に、",
            "関連する仕様ファイルを選定してください。",
            f"`{readable_oracle_root}` 外のファイルは一切参照禁止です。",
            f"出力する oracle_path / referenced_paths は `{concrete_oracle_root}` "
            "配下の絶対パスにしてください。",
            "実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。",
            f"`{concrete_repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
            "入力問題点リスト:",
            payload_text,
        ]
    )
    if oracle_snapshot is not None:
        lines.insert(
            lines.index("実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。"),
            f"`{concrete_oracle_root}` は path 変換のためにだけ使い、読まないでください。",
        )
    return "\n".join(lines)


def _redistribute_improved_issues(
    evaluations: list[dict[str, object]],
    issues: object,
) -> list[dict[str, object]]:
    """改善後 issue を既存 report 集計形式へ戻す。"""
    if not isinstance(issues, list):
        raise ValueError("issues must be a list.")
    result = [
        {
            "target_oracle_path": evaluation["target_oracle_path"],
            "referenced_paths": [],
            "specification_only_basis": "",
            "issues": [],
        }
        for evaluation in evaluations
    ]
    target_to_index = {
        str(evaluation["target_oracle_path"]): index
        for index, evaluation in enumerate(result)
    }
    for issue in issues:
        if not isinstance(issue, dict):
            raise ValueError("issues item must be an object.")
        target = str(Path(str(issue["oracle_path"])).resolve())
        index = target_to_index.get(target, 0)
        result[index]["issues"].append(issue)
    return [_refresh_evaluation_metadata(evaluation) for evaluation in result]


def _evaluation_payload_to_record(
    value: object,
    repo_root: Path,
    oracle_file: Path,
) -> dict[str, object]:
    """Structured Output を report 用の評価レコードへ正規化する。"""
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    if set(value) != {"issues"}:
        raise ValueError("Evaluation payload keys do not match schema.")
    return _refresh_evaluation_metadata(
        {
            "target_oracle_path": str(oracle_file.resolve()),
            "issues": value["issues"],
        }
    )


def _refresh_evaluation_metadata(
    evaluation: dict[str, object],
) -> dict[str, object]:
    """issue 単位の metadata から evaluation 単位の補助 metadata を再構成する。"""
    issues = _evaluation_issues(evaluation)
    referenced_paths = _unique_strings(
        [
            path
            for issue in issues
            for path in _string_list(issue.get("referenced_paths", []))
        ]
    )
    bases = _unique_strings(
        [
            str(issue["specification_only_basis"])
            for issue in issues
            if issue.get("specification_only_basis")
        ]
    )
    basis = " / ".join(bases)
    return {
        "target_oracle_path": str(
            Path(str(evaluation["target_oracle_path"])).resolve()
        ),
        "referenced_paths": referenced_paths,
        "specification_only_basis": basis,
        "issues": issues,
    }


def _validate_evaluation_payload(
    value: object,
    repo_root: Path,
    oracle_file: Path,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> None:
    """oracle 評価 Structured Output の schema と意味制約を検査する。"""
    # run_codex_exec の schema 検査に加え、Python 側でも後段で扱う型を保証する。
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    if set(value) != {"issues"}:
        raise ValueError("Evaluation payload keys do not match schema.")
    _validate_evaluation_issues(value["issues"], repo_root, oracle_snapshot)


def _validate_issues_payload(
    value: object,
    repo_root: Path,
    target_oracle_paths: set[Path],
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> None:
    """改善済み issue list の Structured Output を検査する。"""
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    if set(value) != {"issues"}:
        raise ValueError("Issues payload keys do not match schema.")
    _validate_evaluation_issues(value["issues"], repo_root, oracle_snapshot)


def _target_oracle_paths(evaluations: list[dict[str, object]]) -> set[Path]:
    """評価済み target_oracle_path の集合を返す。"""
    return {
        Path(str(evaluation["target_oracle_path"])).resolve()
        for evaluation in evaluations
    }


def _write_report(
    repo_root: Path,
    mode: str,
    full_requested: bool,
    branch_name: str,
    cmoc_branch: bool,
    base_commit: str | None,
    commit_hash: str,
    deleted_oracles: bool,
    oracle_count_total: int,
    oracle_files: list[Path],
    evaluations: list[dict[str, object]],
) -> Path:
    """評価結果を `.cmoc/reports/review_oracles` に保存する。"""
    report_dir = repo_root / ".cmoc" / "reports" / _REPORT_DIR_NAME
    generated_at = "__CMOC_REPORT_GENERATED_AT__"
    issue_counts = _issue_counts(evaluations)
    result = _evaluation_result(len(oracle_files), issue_counts)

    # frontmatter と問題点単位の本文を結合する。
    lines = [
        "---",
        "schema_version: 1",
        f"command: {_yaml_string(_REPORT_COMMAND)}",
        f"generated_at: {_yaml_string(generated_at)}",
        f"repo_root: {_yaml_string(str(repo_root.resolve()))}",
        f"oracle_root: {_yaml_string(str((repo_root / 'oracles').resolve()))}",
        f"mode: {_yaml_string(mode)}",
        f"full_requested: {str(full_requested).lower()}",
        f"branch: {_yaml_string(branch_name)}",
        f"is_cmoc_branch: {str(cmoc_branch).lower()}",
        f"base_commit: {_yaml_nullable(base_commit)}",
        f"head_commit: {_yaml_string(commit_hash)}",
        f"commit: {_yaml_string(commit_hash)}",
        f"deleted_oracles_detected: {str(deleted_oracles).lower()}",
        f"oracle_count_total: {oracle_count_total}",
        f"oracle_count_evaluated: {len(oracle_files)}",
        f"oracle_count: {len(oracle_files)}",
        f"fatal_issue_count: {issue_counts['fatal']}",
        f"warning_issue_count: {issue_counts['warning']}",
        f"inconclusive_issue_count: {issue_counts['inconclusive']}",
        f"result: {_yaml_string(result)}",
        "---",
        "",
        f"# {_REPORT_COMMAND} report",
        "",
        "## Summary",
        "",
        f"- Result: `{result}`",
        f"- Mode: `{mode}`",
        f"- Evaluated oracle files: `{len(oracle_files)}`",
        f"- Fatal issues: `{issue_counts['fatal']}`",
        f"- Inconclusive issues: `{issue_counts['inconclusive']}`",
        f"- Warning issues: `{issue_counts['warning']}`",
        "",
        "## Verdict",
        "",
        _verdict_text(result),
        "",
        "## Evaluated oracle files",
        "",
        "| No. | Oracle file | Issues |",
        "|---:|---|---:|",
    ]
    issue_count_by_target = _issue_count_by_target(evaluations)
    for index, oracle_file in enumerate(oracle_files, start=1):
        target = str(oracle_file.resolve())
        lines.append(
            f"| {index} | `{oracle_file.relative_to(repo_root)}` | "
            f"{issue_count_by_target.get(target, 0)} |"
        )
    lines.extend([""])
    for severity, heading in [
        ("fatal", "## Fatal issues"),
        ("inconclusive", "## Inconclusive issues"),
        ("warning", "## Warnings"),
    ]:
        lines.extend([heading, ""])
        issues = _issues_for_severity(evaluations, severity)
        if not issues:
            lines.extend(["No issues.", ""])
            continue
        for issue_id, issue in _numbered_issues(severity, issues):
            lines.extend(_issue_lines(repo_root, issue_id, issue))
    lines.extend(["## Referenced files", ""])
    referenced_path_rows = _referenced_path_rows(repo_root, evaluations)
    if referenced_path_rows:
        lines.extend(
            [
                "| No. | Referenced file |",
                "|---:|---|",
            ]
        )
        lines.extend(referenced_path_rows)
    else:
        lines.append("No referenced files.")
    report = "\n".join(lines)
    return write_timestamped_report(
        report_dir,
        lambda timestamp: report.replace(generated_at, timestamp),
    )


def _write_error_report(
    repo_root: Path,
    mode: str | None,
    full_requested: bool,
    branch_name: str | None,
    cmoc_branch: bool | None,
    base_commit: str | None,
    commit_hash: str | None,
    deleted_oracles: bool | None,
    oracle_count_total: int | None,
    oracle_files: list[Path],
    evaluations: list[dict[str, object]],
    failed_stage: str,
    error: Exception,
) -> Path:
    """評価処理失敗時の `result: error` レポートを best effort で保存する。"""
    report_dir = repo_root / ".cmoc" / "reports" / _REPORT_DIR_NAME
    generated_at = "__CMOC_REPORT_GENERATED_AT__"
    issue_counts = _issue_counts(evaluations)
    result = "error"
    lines = [
        "---",
        "schema_version: 1",
        f"command: {_yaml_string(_REPORT_COMMAND)}",
        f"generated_at: {_yaml_string(generated_at)}",
        f"repo_root: {_yaml_string(str(repo_root.resolve()))}",
        f"oracle_root: {_yaml_string(str((repo_root / 'oracles').resolve()))}",
        f"mode: {_yaml_string(mode or 'unknown')}",
        f"full_requested: {str(full_requested).lower()}",
        f"branch: {_yaml_nullable(branch_name)}",
        f"is_cmoc_branch: {_yaml_bool_nullable(cmoc_branch)}",
        f"base_commit: {_yaml_nullable(base_commit)}",
        f"head_commit: {_yaml_nullable(commit_hash)}",
        f"commit: {_yaml_nullable(commit_hash)}",
        f"deleted_oracles_detected: {_yaml_bool_nullable(deleted_oracles)}",
        f"oracle_count_total: {_yaml_int_nullable(oracle_count_total)}",
        f"oracle_count_evaluated: {len(evaluations)}",
        f"oracle_count: {len(evaluations)}",
        f"fatal_issue_count: {issue_counts['fatal']}",
        f"warning_issue_count: {issue_counts['warning']}",
        f"inconclusive_issue_count: {issue_counts['inconclusive']}",
        f"result: {_yaml_string(result)}",
        "---",
        "",
        f"# {_REPORT_COMMAND} report",
        "",
        "## Summary",
        "",
        f"- Result: `{result}`",
        f"- Mode: `{mode or 'unknown'}`",
        f"- Evaluated oracle files: `{len(evaluations)}`",
        f"- Requested oracle files: `{len(oracle_files)}`",
        f"- Fatal issues: `{issue_counts['fatal']}`",
        f"- Inconclusive issues: `{issue_counts['inconclusive']}`",
        f"- Warning issues: `{issue_counts['warning']}`",
        f"- Failed stage: `{failed_stage}`",
        f"- Exception type: `{type(error).__name__}`",
        f"- Exception message: `{str(error)}`",
        "",
        "## Verdict",
        "",
        _verdict_text(result),
        "",
        f"Failed stage: `{failed_stage}`",
        "",
        f"Exception: `{type(error).__name__}: {str(error)}`",
        "",
        "## Evaluated oracle files",
        "",
        "| No. | Oracle file | Evaluation status | Issues |",
        "|---:|---|---|---:|",
    ]
    issue_count_by_target = _issue_count_by_target(evaluations)
    evaluated_files = _evaluated_oracle_files(evaluations)
    for index, oracle_file in enumerate(evaluated_files, start=1):
        target = str(oracle_file)
        lines.append(
            f"| {index} | `{_display_path(repo_root, str(oracle_file))}` | "
            f"evaluated | {issue_count_by_target.get(target, 0)} |"
        )
    not_evaluated_files = _not_evaluated_oracle_files(
        repo_root,
        oracle_files,
        evaluations,
    )
    for index, oracle_file in enumerate(
        not_evaluated_files,
        start=len(evaluated_files) + 1,
    ):
        lines.append(
            f"| {index} | `{_display_path(repo_root, str(oracle_file))}` | "
            "not_evaluated | - |"
        )
    if not evaluated_files and not not_evaluated_files:
        lines.append("| - | No requested oracle files. | - | - |")
    lines.extend([""])
    for severity, heading in [
        ("fatal", "## Fatal issues"),
        ("inconclusive", "## Inconclusive issues"),
        ("warning", "## Warnings"),
    ]:
        lines.extend([heading, ""])
        issues = _issues_for_severity(evaluations, severity)
        if not issues:
            lines.extend(["No issues.", ""])
            continue
        for issue_id, issue in _numbered_issues(severity, issues):
            lines.extend(_issue_lines(repo_root, issue_id, issue))
    lines.extend(["## Referenced files", ""])
    referenced_path_rows = _referenced_path_rows(repo_root, evaluations)
    if referenced_path_rows:
        lines.extend(
            [
                "| No. | Referenced file |",
                "|---:|---|",
            ]
        )
        lines.extend(referenced_path_rows)
    else:
        lines.append("No referenced files.")
    report = "\n".join(lines)
    return write_timestamped_report(
        report_dir,
        lambda timestamp: report.replace(generated_at, timestamp),
    )


def _print_error_report_fallback(
    repo_root: Path,
    mode: str | None,
    full_requested: bool,
    branch_name: str | None,
    cmoc_branch: bool | None,
    base_commit: str | None,
    commit_hash: str | None,
    deleted_oracles: bool | None,
    oracle_count_total: int | None,
    oracle_files: list[Path],
    evaluations: list[dict[str, object]],
    failed_stage: str,
    error: Exception,
    report_error: Exception,
) -> None:
    """error report 保存失敗時に一次失敗情報だけは stderr へ残す。"""
    lines = [
        f"{_REPORT_COMMAND} error report generation failed.",
        "Fallback diagnostic:",
        f"- result: error",
        f"- repo_root: {repo_root.resolve()}",
        f"- mode: {mode or 'unknown'}",
        f"- full_requested: {str(full_requested).lower()}",
        f"- branch: {_yaml_nullable(branch_name)}",
        f"- is_cmoc_branch: {_yaml_bool_nullable(cmoc_branch)}",
        f"- base_commit: {_yaml_nullable(base_commit)}",
        f"- head_commit: {_yaml_nullable(commit_hash)}",
        f"- deleted_oracles_detected: {_yaml_bool_nullable(deleted_oracles)}",
        f"- oracle_count_total: {_yaml_int_nullable(oracle_count_total)}",
        f"- oracle_count_requested: {len(oracle_files)}",
        f"- oracle_count_evaluated: {len(evaluations)}",
        f"- failed_stage: {failed_stage}",
        f"- exception: {type(error).__name__}: {error}",
        f"- report_exception: {type(report_error).__name__}: {report_error}",
    ]
    print("\n".join(lines), file=sys.stderr)


def _validate_referenced_paths(
    value: object,
    repo_root: Path,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> set[Path]:
    """referenced_paths を絶対 oracle / INDEX ファイル配列として検査する。"""
    if not isinstance(value, list):
        raise ValueError("referenced_paths must be a list.")
    paths = set()
    for index, item in enumerate(value):
        paths.add(
            _require_absolute_oracle_reference_path(
                item,
                repo_root,
                f"referenced_paths[{index}]",
                oracle_snapshot,
            )
        )
    return paths


def _validate_evaluation_issues(
    value: object,
    repo_root: Path,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> None:
    """issues 配列の item schema を検査する。"""
    if not isinstance(value, list):
        raise ValueError("issues must be a list.")
    required_keys = {
        "severity",
        "title",
        "oracle_path",
        "oracle_line_start",
        "oracle_line_end",
        "referenced_paths",
        "affected_workflow",
        "requirement",
        "problem",
        "reason",
        "suggested_oracle_change",
        "specification_only_basis",
    }
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"issues[{index}] must be an object.")
        if set(item) != required_keys:
            raise ValueError(f"issues[{index}] keys do not match schema.")
        if item["severity"] not in _SEVERITY_ORDER:
            raise ValueError(f"issues[{index}].severity is invalid.")
        _require_issue_string(item, "title", index)
        _require_issue_oracle_path_string(item["oracle_path"], index)
        _validate_issue_lines(item, index)
        _validate_referenced_paths(
            item["referenced_paths"],
            repo_root,
            oracle_snapshot,
        )
        for key in [
            "affected_workflow",
            "requirement",
            "problem",
            "reason",
            "suggested_oracle_change",
        ]:
            _require_issue_string(item, key, index)
        _require_issue_string(
            item,
            "specification_only_basis",
            index,
            allow_empty=True,
        )


def _require_issue_oracle_path_string(value: object, index: int) -> None:
    """issues[].oracle_path は後処理で必要な最小限だけ検査する。"""
    if not isinstance(value, str):
        raise ValueError(f"issues[{index}].oracle_path must be a string.")
    stripped_value = value.strip()
    if not stripped_value:
        raise ValueError(f"issues[{index}].oracle_path must not be empty.")


def _require_absolute_oracle_reference_path(
    value: object,
    repo_root: Path,
    label: str,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> Path:
    """JSON 値を参照可能な oracle / INDEX file path として検査する。"""
    resolved_path = _require_absolute_oracles_file(
        value,
        repo_root,
        label,
        require_current_existence=oracle_snapshot is None,
    )
    if oracle_snapshot is not None:
        if resolved_path not in oracle_snapshot.reference_files:
            raise ValueError(f"{label} must be an oracle file or INDEX.md.")
        return resolved_path
    if resolved_path.name == "INDEX.md":
        return resolved_path

    oracle_files = {path.resolve() for path in list_oracle_files(repo_root)}
    if resolved_path not in oracle_files:
        raise ValueError(f"{label} must be an oracle file or INDEX.md.")
    return resolved_path


def _require_absolute_oracles_file(
    value: object,
    repo_root: Path,
    label: str,
    *,
    require_current_existence: bool,
) -> Path:
    """JSON 値を oracles 配下の絶対 file path として検査する。"""
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string.")
    path = Path(value)
    if not path.is_absolute():
        raise ValueError(f"{label} must be an absolute path.")
    resolved_path = path.resolve()
    oracle_root = (repo_root / "oracles").resolve()
    try:
        resolved_path.relative_to(oracle_root)
    except ValueError as error:
        raise ValueError(f"{label} must be under oracles.") from error
    if require_current_existence:
        if not resolved_path.exists():
            raise ValueError(f"{label} must exist.")
        if not resolved_path.is_file():
            raise ValueError(f"{label} must be a file.")
    return resolved_path


def _require_issue_string(
    item: dict[object, object],
    key: str,
    index: int,
    *,
    allow_empty: bool = False,
) -> None:
    """issue item の string 項目を検査する。"""
    if not isinstance(item[key], str):
        raise ValueError(f"issues[{index}].{key} must be a string.")
    if not allow_empty and not item[key].strip():
        raise ValueError(f"issues[{index}].{key} must not be empty.")


def _validate_issue_lines(item: dict[object, object], index: int) -> None:
    """issue item の行番号項目を検査する。"""
    start = item["oracle_line_start"]
    end = item["oracle_line_end"]
    if start is not None and not isinstance(start, int):
        raise ValueError(f"issues[{index}].oracle_line_start is invalid.")
    if end is not None and not isinstance(end, int):
        raise ValueError(f"issues[{index}].oracle_line_end is invalid.")
    if isinstance(start, int) and start < 1:
        raise ValueError(f"issues[{index}].oracle_line_start is invalid.")
    if isinstance(end, int) and end < 1:
        raise ValueError(f"issues[{index}].oracle_line_end is invalid.")
    if isinstance(start, int) and isinstance(end, int) and start > end:
        raise ValueError(f"issues[{index}] line range is invalid.")


def _issue_counts(
    evaluations: list[dict[str, object]],
) -> dict[str, int]:
    """severity ごとの issue 件数を数える。"""
    counts = {severity: 0 for severity in _SEVERITY_ORDER}
    for issue in _all_issues(evaluations):
        severity = str(issue["severity"])
        counts[severity] += 1
    return counts


def _evaluation_result(
    oracle_count: int,
    issue_counts: dict[str, int],
) -> str:
    """issue 件数からレポート result を決める。"""
    if oracle_count == 0:
        return "no_targets"
    for severity in _SEVERITY_ORDER:
        if issue_counts[severity] > 0:
            return severity
    return "ok"


def _verdict_text(result: str) -> str:
    """result ごとの Verdict 本文を返す。"""
    if result == "ok":
        return (
            "今回評価した範囲では問題点が検出されませんでした。"
            "ただし、問題点の不存在を完全保証するものではありません。"
        )
    if result == "fatal":
        return (
            "oracle スナップショットには、仕様だけから判断して主要ワークフロー、"
            "完了判定、または中核目的を壊しうる問題があります。"
        )
    if result == "inconclusive":
        return "致命的問題ありとは断定できませんが、仕様評価として判断不能な点があります。"
    if result == "warning":
        return "致命的ではありませんが、仕様品質・可読性・将来の実装安定性に問題があります。"
    if result == "no_targets":
        return "評価対象 oracle が 0 件だったため、問題点の評価は行われませんでした。"
    if result == "error":
        return (
            "評価処理またはレポート生成に失敗したため、成功評価ではありません。"
            "ログと例外情報を確認し、必要な修正または再実行を判断してください。"
        )
    return (
        "未知の result のため、評価状態を成功として扱えません。"
        "ログとレポート生成処理を確認してください。"
    )


def _issue_count_by_target(
    evaluations: list[dict[str, object]],
) -> dict[str, int]:
    """評価対象ファイルごとの issue 件数を返す。"""
    result = {}
    for evaluation in evaluations:
        issues = _evaluation_issues(evaluation)
        target = Path(str(evaluation["target_oracle_path"])).resolve()
        result[str(target)] = len(issues)
    return result


def _evaluated_oracle_files(evaluations: list[dict[str, object]]) -> list[Path]:
    """完了した評価結果に含まれる対象 oracle ファイルを返す。"""
    return [
        Path(str(evaluation["target_oracle_path"])).resolve()
        for evaluation in evaluations
    ]


def _not_evaluated_oracle_files(
    repo_root: Path,
    oracle_files: list[Path],
    evaluations: list[dict[str, object]],
) -> list[Path]:
    """依頼対象のうち評価完了していない oracle ファイルを返す。"""
    evaluated = set(_evaluated_oracle_files(evaluations))
    return [
        oracle_file.resolve()
        for oracle_file in oracle_files
        if oracle_file.resolve() not in evaluated
    ]


def _issues_for_severity(
    evaluations: list[dict[str, object]],
    severity: str,
) -> list[dict[str, object]]:
    """指定 severity の issue を評価順・issue 順で返す。"""
    return [
        issue
        for issue in _all_issues(evaluations)
        if issue["severity"] == severity
    ]


def _numbered_issues(
    severity: str,
    issues: list[dict[str, object]],
) -> list[tuple[str, dict[str, object]]]:
    """severity ごとに report-local id を付ける。"""
    prefix = _ISSUE_ID_PREFIXES[severity]
    return [
        (f"{prefix}-{index:03d}", issue)
        for index, issue in enumerate(issues, start=1)
    ]


def _issue_lines(
    repo_root: Path,
    issue_id: str,
    issue: dict[str, object],
) -> list[str]:
    """issue 1 件を Markdown 行へ変換する。"""
    return [
        f"### {issue_id}: {issue['title']}",
        "",
        f"- Oracle file: `{_display_path(repo_root, str(issue['oracle_path']))}`",
        f"- Lines: `{_line_range(issue)}`",
        f"- Affected workflow: `{issue['affected_workflow']}`",
        "- Requirement:",
        f"  - {issue['requirement']}",
        "- Problem:",
        f"  - {issue['problem']}",
        "- Reason:",
        f"  - {issue['reason']}",
        "- Suggested oracle change:",
        f"  - {issue['suggested_oracle_change']}",
        "- Specification-only basis:",
        f"  - {issue['specification_only_basis']}",
        "",
    ]


def _line_range(issue: dict[str, object]) -> str:
    """issue の行範囲を Markdown 表示用文字列にする。"""
    start = issue["oracle_line_start"]
    end = issue["oracle_line_end"]
    if start is None or end is None:
        return "unknown"
    if start == end:
        return str(start)
    return f"{start}-{end}"


def _referenced_path_rows(
    repo_root: Path,
    evaluations: list[dict[str, object]],
) -> list[str]:
    """全評価結果の referenced_paths を重複排除した表示行を返す。"""
    referenced_paths = _unique_strings(
        [
            path
            for evaluation in evaluations
            for path in _string_list(evaluation["referenced_paths"])
        ]
    )
    result = []
    for index, path in enumerate(referenced_paths, start=1):
        result.append(
            f"| {index} | `{_display_path(repo_root, path)}` |"
        )
    return result


def _all_issues(
    evaluations: list[dict[str, object]],
) -> list[dict[str, object]]:
    """全評価結果の issues を評価順に連結する。"""
    result = []
    for evaluation in evaluations:
        result.extend(_evaluation_issues(evaluation))
    return result


def _evaluation_issues(
    evaluation: dict[str, object],
) -> list[dict[str, object]]:
    """検証済み evaluation から issues を取り出す。"""
    issues = evaluation["issues"]
    if not isinstance(issues, list):
        raise ValueError("issues must be a list.")
    return [issue for issue in issues if isinstance(issue, dict)]


def _string_list(value: object) -> list[str]:
    """JSON 値を文字列配列として検査する。"""
    if not isinstance(value, list) or not all(
        isinstance(item, str) for item in value
    ):
        raise ValueError("Expected list[str].")
    return value


def _yaml_nullable(value: str | None) -> str:
    """YAML frontmatter 用に nullable scalar を返す。"""
    if value is None:
        return "null"
    return _yaml_string(value)


def _yaml_string(value: str) -> str:
    """YAML frontmatter 用に double quoted scalar を返す。"""
    return json.dumps(value, ensure_ascii=False)


def _yaml_bool_nullable(value: bool | None) -> str:
    """YAML frontmatter 用に nullable bool を返す。"""
    if value is None:
        return "null"
    return str(value).lower()


def _yaml_int_nullable(value: int | None) -> str:
    """YAML frontmatter 用に nullable int を返す。"""
    if value is None:
        return "null"
    return str(value)


def _unique_strings(values: list[str]) -> list[str]:
    """文字列配列を順序維持で重複排除する。"""
    result = []
    seen = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _display_path(repo_root: Path, path_text: str) -> str:
    """repo 配下の絶対パスをレポート向けの相対パスにする。"""
    path = Path(path_text)
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path_text
