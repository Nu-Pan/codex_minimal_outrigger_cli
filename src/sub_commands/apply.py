"""`cmoc apply` の本体処理。"""

import json
from pathlib import Path
from time import sleep

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
    APPLY_BRANCH_PREFIX,
    assert_cmoc_ignored,
    assert_no_uncommitted_changes,
    changed_paths,
    current_branch,
    head_commit,
    is_session_branch,
    read_session_state,
    read_session_start_commit,
    run_git,
    session_id_from_branch,
    write_session_state,
)
from commons.timing import StepTimer, start_step
from commons.timestamps import make_timestamp

_APPLY_INCOMPLETE_EXIT_CODE: int = 2
_DISCREPANCY_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["git_head_commit_hash", "fixing_points"],
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

    # apply は session branch 上で開始し、専用 worktree でだけ実装を変更する。
    timer = StepTimer("apply")
    session_branch = current_branch(repo_root)
    if not is_session_branch(session_branch):
        raise CmocError(
            "`cmoc apply` は session branch 上で実行してください。",
            [
                "先に `cmoc session fork` を実行してください。",
                "既存の session branch を checkout してください。",
            ],
            f"現在の branch: {session_branch or '(detached HEAD)'}",
        )

    start_step(timer, 1, 6, "validate session state")
    session_id = session_id_from_branch(session_branch)
    state = read_session_state(repo_root, session_id)
    session_start_commit = _validate_apply_fork_state(
        state,
        session_branch,
    )
    assert_no_uncommitted_changes(repo_root)
    _validate_repeat_options(
        repeat_investigate_and_fix,
        repeat_improove_fixing_list,
    )

    start_step(timer, 2, 6, "ensure .cmoc is ignored")
    assert_cmoc_ignored(repo_root)
    assert_no_uncommitted_changes(repo_root)
    oracle_snapshot_commit = head_commit(repo_root)

    try:
        start_step(timer, 3, 6, "create apply worktree")
        apply_run_id, apply_branch, apply_worktree = _create_apply_worktree(
            repo_root,
            session_id,
            oracle_snapshot_commit,
        )
        _mark_apply_running(
            repo_root,
            session_id,
            state,
            apply_branch,
            oracle_snapshot_commit,
        )

        # ユーザー向けステップとして INDEX.md を明示メンテナンスする。
        start_step(timer, 4, 6, "maintain INDEX.md files")
        maintain_indexes(apply_worktree)

        # 不整合調査と追従作業を指定回数まで反復する。
        start_step(timer, 5, 6, "investigate and apply discrepancies")
        discrepancy_counts: list[int] = []
        completed = False
        for loop_index in range(1, repeat_investigate_and_fix + 1):
            discrepancies = _investigate_discrepancies(
                apply_worktree,
                session_start_commit,
                oracle_snapshot_commit,
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

            _apply_discrepancies(apply_worktree, discrepancies)

        # 実行結果を人間向け report と exit code に変換する。
        start_step(timer, 6, 6, "write report")
        report_path = _write_apply_report(
            apply_worktree,
            repo_root,
            session_id,
            apply_run_id,
            session_branch,
            apply_branch,
            apply_worktree,
            oracle_snapshot_commit,
            oracle_snapshot_commit,
            head_commit(repo_root),
            completed,
            discrepancy_counts,
        )
        _mark_apply_completed(
            repo_root,
            session_id,
            state,
        )
        print(f"apply run id: {apply_run_id}")
        print(str(report_path))
        timer.report()
        return 0 if completed else _APPLY_INCOMPLETE_EXIT_CODE
    except Exception:
        _mark_apply_error(repo_root, session_id, state)
        raise


def _validate_apply_fork_state(
    state: dict[str, object],
    session_branch: str,
) -> str:
    """apply fork の state 前提条件を検証し、session start commit を返す。"""
    session = state.get("session")
    apply = state.get("apply")
    if not isinstance(session, dict) or not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            ["state JSON の session/apply セクションを確認してください。"],
            f"現在の branch: {session_branch}",
        )
    if session.get("state") != "active":
        raise CmocError(
            "active な session ではありません。",
            [
                "対象 session の state を確認してください。",
                "既に join または abandon 済みの場合は、新しい session を開始してください。",
            ],
            f"session.state: {session.get('state')}",
        )
    if apply.get("state") != "ready":
        raise CmocError(
            "apply run を開始できる状態ではありません。",
            [
                "`cmoc apply join` または `cmoc apply abandon` を完了してから再実行してください。",
                "session state の apply.state を確認してください。",
            ],
            f"apply.state: {apply.get('state')}",
        )
    start_commit = session.get("session_start_commit")
    if not isinstance(start_commit, str) or not start_commit:
        raise CmocError(
            "session start commit が session state に記録されていません。",
            ["session state の session.session_start_commit を確認してください。"],
            f"現在の branch: {session_branch}",
        )
    return start_commit


def _validate_repeat_options(
    repeat_investigate_and_fix: int,
    repeat_improove_fixing_list: int,
) -> None:
    """apply fork の repeat 系オプションを副作用前に検証する。"""
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


def _create_apply_worktree(
    repo_root: Path,
    session_id: str,
    oracle_snapshot_commit: str,
) -> tuple[str, str, Path]:
    """snapshot から apply branch と専用 worktree を作成する。"""
    # timestamp 衝突に備えて短い sleep を挟みながら最大 10 回リトライする。
    for attempt in range(1, 11):
        apply_run_id = make_timestamp()
        apply_branch = (
            f"{APPLY_BRANCH_PREFIX}{session_id}/{apply_run_id}"
        )
        apply_worktree = (
            repo_root
            / ".cmoc"
            / "worktrees"
            / "apply"
            / session_id
            / apply_run_id
        )
        print(f"create apply worktree attempt ({attempt}/10) {apply_branch}")
        branch_result = run_git(
            repo_root,
            ["branch", apply_branch, oracle_snapshot_commit],
            check=False,
        )
        if branch_result.returncode != 0:
            sleep(0.001)
            continue
        worktree_result = run_git(
            repo_root,
            ["worktree", "add", str(apply_worktree), apply_branch],
            check=False,
        )
        if worktree_result.returncode == 0:
            return apply_run_id, apply_branch, apply_worktree
        run_git(repo_root, ["branch", "-D", apply_branch], check=False)
        sleep(0.001)
    raise RuntimeError("リトライ後も一意な apply worktree を作成できませんでした。")


def _mark_apply_running(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
    apply_branch: str,
    oracle_snapshot_commit: str,
) -> None:
    """session state の apply セクションを running に更新する。"""
    apply = _mutable_apply_section(state)
    apply["state"] = "running"
    apply["apply_branch"] = apply_branch
    apply["oracle_snapshot_commit"] = oracle_snapshot_commit
    write_session_state(repo_root, session_id, state)


def _mark_apply_completed(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
) -> None:
    """session state の apply セクションを completed に更新する。"""
    apply = _mutable_apply_section(state)
    apply["state"] = "completed"
    write_session_state(repo_root, session_id, state)


def _mark_apply_error(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
) -> None:
    """開始済み apply run を error として永続化する。"""
    apply = _mutable_apply_section(state)
    if apply.get("state") != "error":
        apply["state"] = "error"
        write_session_state(repo_root, session_id, state)


def _mutable_apply_section(
    state: dict[str, object],
) -> dict[str, object]:
    """session state から更新可能な apply セクションを取り出す。"""
    apply = state.get("apply")
    if not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            ["state JSON の apply セクションを確認してください。"],
        )
    return apply


def _investigate_discrepancies(
    repo_root: Path,
    base_commit: str,
    oracle_snapshot_commit: str,
    *,
    repeat_improove_fixing_list: int,
    full: bool,
) -> list[dict[str, object]]:
    """oracle ファイル・実装ファイルごとに不整合調査を実行する。"""
    # ループごとに部分・全体適用モードと調査対象を再評価する。
    discrepancies: list[dict[str, object]] = []
    # --full の有無だけで全体適用・部分適用を切り替える。
    partial = not full
    oracle_files = _target_oracle_files(
        repo_root,
        base_commit,
        oracle_snapshot_commit,
        partial,
    )
    implementation_files = _target_implementation_files(
        repo_root,
        base_commit,
        oracle_snapshot_commit,
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
        base_commit,
        repeat_improove_fixing_list,
    )


def _target_oracle_files(
    repo_root: Path,
    base_commit: str,
    oracle_snapshot_commit: str,
    partial: bool,
) -> list[Path]:
    """適用モードに応じた oracle 調査対象を返す。"""
    # apply run 開始時の snapshot に調査対象を固定する。
    all_files = _oracle_files_at_commit(repo_root, oracle_snapshot_commit)
    if not partial:
        return all_files
    changed = set(
        _changed_oracle_files_at_commit(
            repo_root,
            base_commit,
            oracle_snapshot_commit,
        )
    )
    return [path for path in all_files if path in changed]


def _target_implementation_files(
    repo_root: Path,
    base_commit: str,
    oracle_snapshot_commit: str,
    partial: bool,
) -> list[Path]:
    """適用モードに応じた実装調査対象を返す。"""
    # apply run 開始時の snapshot に調査対象を固定する。
    all_files = _implementation_files_at_commit(
        repo_root,
        oracle_snapshot_commit,
    )
    if not partial:
        return all_files
    changed = set(
        _changed_implementation_files_at_commit(
            repo_root,
            base_commit,
            oracle_snapshot_commit,
        )
    )
    return [path for path in all_files if path in changed]


def _oracle_files_at_commit(repo_root: Path, commit_hash: str) -> list[Path]:
    """指定 commit に存在する oracle ファイルを列挙する。"""
    paths = _tracked_files_at_commit(repo_root, commit_hash, "oracles")
    return [
        repo_root / path
        for path in paths
        if path.startswith("oracles/")
        and Path(path).name != "INDEX.md"
    ]


def _implementation_files_at_commit(
    repo_root: Path,
    commit_hash: str,
) -> list[Path]:
    """指定 commit に存在する実装ファイルを列挙する。"""
    paths = _tracked_files_at_commit(repo_root, commit_hash, ".")
    return [
        repo_root / path
        for path in paths
        if not _is_excluded_implementation_path(path)
    ]


def _changed_oracle_files_at_commit(
    repo_root: Path,
    base_commit: str,
    commit_hash: str,
) -> list[Path]:
    """指定 commit 範囲で変更された oracle ファイルを列挙する。"""
    return [
        repo_root / path
        for path in _changed_files_between_commits(
            repo_root,
            base_commit,
            commit_hash,
            "oracles",
        )
        if path.startswith("oracles/")
        and Path(path).name != "INDEX.md"
    ]


def _changed_implementation_files_at_commit(
    repo_root: Path,
    base_commit: str,
    commit_hash: str,
) -> list[Path]:
    """指定 commit 範囲で変更された実装ファイルを列挙する。"""
    return [
        repo_root / path
        for path in _changed_files_between_commits(
            repo_root,
            base_commit,
            commit_hash,
            ".",
        )
        if not _is_excluded_implementation_path(path)
    ]


def _tracked_files_at_commit(
    repo_root: Path,
    commit_hash: str,
    pathspec: str,
) -> list[str]:
    """指定 commit の tracked file 一覧を repo 相対 path で返す。"""
    result = run_git(
        repo_root,
        ["ls-tree", "-r", "--name-only", commit_hash, "--", pathspec],
    )
    return sorted(line for line in result.stdout.splitlines() if line)


def _changed_files_between_commits(
    repo_root: Path,
    base_commit: str,
    commit_hash: str,
    pathspec: str,
) -> list[str]:
    """指定 commit 範囲の追加・変更・rename 後 path を返す。"""
    result = run_git(
        repo_root,
        [
            "diff",
            "--name-only",
            "-M",
            "--diff-filter=ACMRT",
            base_commit,
            commit_hash,
            "--",
            pathspec,
        ],
    )
    return sorted(line for line in result.stdout.splitlines() if line)


def _is_excluded_implementation_path(relative_path: str) -> bool:
    """実装ファイル列挙から除外する path か判定する。"""
    path = Path(relative_path)
    return (
        relative_path == "oracles"
        or relative_path.startswith("oracles/")
        or relative_path == ".git"
        or relative_path.startswith(".git/")
        or relative_path == ".cmoc"
        or relative_path.startswith(".cmoc/")
        or path.name == "INDEX.md"
    )


def _improove_fixing_list(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
    base_commit: str,
    repeat_improove_fixing_list: int,
) -> list[dict[str, object]]:
    """要修正点リストを最大指定回数まで Codex CLI に改善させる。"""
    # 改善結果が前回と同一なら、改善点なしとして早期終了する。
    improved = discrepancies
    for loop_index in range(1, repeat_improove_fixing_list + 1):
        next_improved = _organize_discrepancies(
            repo_root,
            improved,
            base_commit,
        )
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
    base_commit: str | None = None,
) -> list[dict[str, object]]:
    """連結した不整合リストを Codex CLI に整理させる。"""
    # 整理結果も同じ Structured Output schema で受け取って検証する。
    branch_name = current_branch(repo_root)
    if base_commit is None:
        base_commit = read_session_start_commit(repo_root, branch_name)
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
    report_repo_root: Path,
    session_id: str,
    apply_run_id: str,
    session_branch: str,
    branch_name: str,
    apply_worktree: Path,
    oracle_snapshot_commit: str,
    session_head_at_apply_start: str,
    session_head_at_apply_finish: str,
    completed: bool,
    discrepancy_counts: list[int],
) -> Path:
    """作業レポートを Codex CLI に依頼し、ファイル保存する。"""
    # report 保存先と timestamp 付きファイル名を用意する。
    report_dir = report_repo_root / ".cmoc" / "reports" / "apply" / "fork"
    report_dir.mkdir(parents=True, exist_ok=True)
    generated_at = make_timestamp()
    report_path = report_dir / f"{generated_at}.md"

    # Codex にはレポート本文だけを生成させ、ファイル保存は cmoc が行う。
    result_label = "収束" if completed else "未収束"
    incomplete_instruction = (
        "「未収束」の場合は、要修正点件数の推移に"
        "「まだ要修正点が残っている可能性」を必ず追記してください。"
    )
    prompt = "\n".join(
        [
            "あなたはソフトウェア作業レポートの作成担当です。",
            f"`{repo_root}` のブランチ `{branch_name}` について簡潔な作業レポートを書いてください。",
            "完了条件は、作業結果、要修正点件数の推移、今回の apply run で行った変更内容を説明することです。",
            "YAML Front Matter は cmoc 側で付与するため、本文 Markdown だけを書いてください。",
            "Markdown 見出しとして「作業結果」「要修正点件数の推移」「全変更内容」を必ず含めてください。",
            "要修正点件数の推移には、ループごとに何件の要修正点を見つけたかを書いてください。",
            incomplete_instruction,
            "全変更内容は、この `cmoc apply fork` が実際に行った作業内容だけに限定してください。",
            f"具体的には `{oracle_snapshot_commit}` から `{branch_name}` の HEAD までの差分だけを対象にしてください。",
            "変更内容は、変更内容の意味論に基づき「カテゴリ」という語を使って要約してください。",
            f"作業結果の区分は一言で `{result_label}` と書いてください。",
            f"作業結果区分: {result_label}",
            f"要修正点件数: {discrepancy_counts}",
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
    report = _apply_report_with_front_matter(
        report_body=report,
        generated_at=generated_at,
        session_id=session_id,
        apply_run_id=apply_run_id,
        session_branch=session_branch,
        apply_branch=branch_name,
        apply_worktree=apply_worktree,
        oracle_snapshot_commit=oracle_snapshot_commit,
        session_head_at_apply_start=session_head_at_apply_start,
        session_head_at_apply_finish=session_head_at_apply_finish,
        result_label=result_label,
        discrepancy_counts=discrepancy_counts,
    )
    _validate_apply_report(
        report,
        branch_name,
        result_label,
        completed,
        discrepancy_counts,
        require_front_matter=True,
    )
    report_path.write_text(report, encoding="utf-8")
    return report_path


def _validate_apply_report(
    report: str,
    branch_name: str,
    result_label: str,
    completed: bool,
    discrepancy_counts: list[int],
    *,
    require_front_matter: bool = False,
) -> None:
    """保存前の apply レポートが必須内容を持つことを機械的に確認する。"""
    # Markdown の意味解釈ではなく、必須セクションと既知値の存在を検査する。
    missing: list[str] = []
    body = report
    if require_front_matter:
        front_matter, body = _split_yaml_front_matter(report)
        required_metadata = [
            "cmoc_session_id",
            "cmoc_apply_run_id",
            "cmoc_session_branch",
            "cmoc_apply_branch",
            "apply_worktree_path",
            "oracle_snapshot_commit",
            "session_head_at_apply_start",
            "session_head_at_apply_finish",
            "result",
            "generated_at",
        ]
        for key in required_metadata:
            if key not in front_matter:
                missing.append(f"YAML Front Matter {key}")
        if front_matter.get("cmoc_apply_branch") != branch_name:
            missing.append("YAML Front Matter cmoc_apply_branch")
        if front_matter.get("result") != result_label:
            missing.append("YAML Front Matter result")

    if "作業結果" not in body or result_label not in body:
        missing.append("作業結果の区分")
    if "要修正点件数の推移" not in body:
        missing.append("要修正点件数の推移")
    for index, count in enumerate(discrepancy_counts, start=1):
        if f"{index}" not in body or f"{count}" not in body:
            missing.append(f"要修正点件数の推移 loop {index}")
    if (
        not completed
        and "まだ要修正点が残っている可能性" not in body
    ):
        missing.append("未収束時の残存可能性")
    if (
        branch_name not in body
        or "全変更内容" not in body
        or "カテゴリ" not in body
    ):
        missing.append("ブランチ上の全変更内容の意味論的カテゴリ別要約")

    # 不完全な Codex 出力をそのまま保存せず、共通エラーとして中断する。
    if missing:
        raise ValueError(
            "Codex CLI が生成した apply report に必須内容がありません:\n"
            + "\n".join(missing)
        )


def _apply_report_with_front_matter(
    *,
    report_body: str,
    generated_at: str,
    session_id: str,
    apply_run_id: str,
    session_branch: str,
    apply_branch: str,
    apply_worktree: Path,
    oracle_snapshot_commit: str,
    session_head_at_apply_start: str,
    session_head_at_apply_finish: str,
    result_label: str,
    discrepancy_counts: list[int],
) -> str:
    """cmoc が確定できる apply report metadata を YAML Front Matter にする。"""
    front_matter = [
        "---",
        f"generated_at: {_yaml_string(generated_at)}",
        f"cmoc_session_id: {_yaml_string(session_id)}",
        f"cmoc_apply_run_id: {_yaml_string(apply_run_id)}",
        f"cmoc_session_branch: {_yaml_string(session_branch)}",
        f"cmoc_apply_branch: {_yaml_string(apply_branch)}",
        f"apply_worktree_path: {_yaml_string(str(apply_worktree))}",
        f"oracle_snapshot_commit: {_yaml_string(oracle_snapshot_commit)}",
        f"session_head_at_apply_start: {_yaml_string(session_head_at_apply_start)}",
        f"session_head_at_apply_finish: {_yaml_string(session_head_at_apply_finish)}",
        f"result: {_yaml_string(result_label)}",
        f"discrepancy_counts: {json.dumps(discrepancy_counts)}",
        "---",
    ]
    return "\n".join([*front_matter, "", report_body.strip(), ""])


def _yaml_string(value: str) -> str:
    """単純な文字列 metadata を YAML double quoted scalar として出力する。"""
    return json.dumps(value, ensure_ascii=False)


def _split_yaml_front_matter(report: str) -> tuple[dict[str, str], str]:
    """apply report の YAML Front Matter を軽量に取り出す。"""
    if not report.startswith("---\n"):
        return {}, report
    front_matter_end = report.find("\n---\n", 4)
    if front_matter_end == -1:
        return {}, report

    front_matter: dict[str, str] = {}
    for line in report[4:front_matter_end].splitlines():
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        value = raw_value.strip()
        if value.startswith('"') and value.endswith('"'):
            try:
                loaded = json.loads(value)
            except json.JSONDecodeError:
                loaded = value[1:-1]
            if isinstance(loaded, str):
                front_matter[key.strip()] = loaded
                continue
        front_matter[key.strip()] = value

    return front_matter, report[front_matter_end + len("\n---\n") :]


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
            "top-level の git_head_commit_hash は必ず含め、値は null で構いません。",
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
            "top-level の git_head_commit_hash は必ず含め、値は null で構いません。",
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
            "top-level の git_head_commit_hash は必ず含め、値は null で構いません。",
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
    # top-level は git_head_commit_hash と fixing_points に限定する。
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    required_keys = {"git_head_commit_hash", "fixing_points"}
    if set(value) != required_keys:
        raise ValueError("Expected git_head_commit_hash and fixing_points keys.")
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
