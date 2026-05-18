"""`cmoc eval-oracles` の本体処理。"""

from pathlib import Path

from commons.codex import run_codex_exec
from commons.command_runner import run_command
from commons.indexing import maintain_indexes
from commons.repo import (
    changed_oracle_files,
    current_branch,
    ensure_cmoc_ignored,
    has_deleted_oracle_files,
    head_commit,
    is_cmoc_branch,
    list_oracle_files,
    read_branch_base_commit,
)
from commons.timing import StepTimer
from commons.timestamps import make_timestamp


def cmoc_eval_oracles_impl(
    repo_root: Path | None = None,
    *,
    full: bool,
) -> None:
    """oracle 断片を Codex CLI で評価し、レポートを作る。"""
    if repo_root is None:
        run_command(
            lambda resolved_repo_root: cmoc_eval_oracles_impl(
                resolved_repo_root,
                full=full,
            )
        )
        return

    # 評価前に `.cmoc` の ignore 保証を済ませる。
    timer = StepTimer("eval-oracles")
    timer.start("ensure .cmoc is ignored")
    print("eval-oracles (1/5) ensure .cmoc is ignored")
    ensure_cmoc_ignored(repo_root)

    # 既存のユーザー向けステップとして INDEX.md メンテナンスを実行する。
    timer.start("maintain INDEX.md files")
    print("eval-oracles (2/5) maintain INDEX.md files")
    maintain_indexes(repo_root)

    # branch 状態と `--full` から、部分評価か全体評価かを決める。
    timer.start("select oracle files")
    print("eval-oracles (3/5) select oracle files")
    branch_name = current_branch(repo_root)
    base_commit = None
    deleted_oracles = False
    if is_cmoc_branch(branch_name) and not full:
        base_commit = read_branch_base_commit(repo_root, branch_name)
        deleted_oracles = has_deleted_oracle_files(repo_root, base_commit)
    partial = is_cmoc_branch(branch_name) and not full and not deleted_oracles

    # 評価モードに応じて Codex CLI に渡す oracle ファイル一覧を作る。
    all_oracle_files = list_oracle_files(repo_root)
    if partial:
        assert base_commit is not None
        changed_files = set(changed_oracle_files(repo_root, base_commit))
        oracle_files = [
            path for path in all_oracle_files if path in changed_files
        ]
        mode = "partial"
    else:
        oracle_files = all_oracle_files
        mode = "full"

    # oracle ファイルごとに Codex CLI 評価を実行する。
    timer.start("evaluate oracle files")
    print("eval-oracles (4/5) evaluate oracle files")
    evaluations = []
    for index, oracle_file in enumerate(oracle_files, start=1):
        print(f"evaluate oracle ({index}/{len(oracle_files)}) {oracle_file}")
        output = run_codex_exec(
            repo_root,
            _evaluation_prompt(repo_root, oracle_file),
            read_only=True,
            expect_json=False,
        )
        evaluations.append((oracle_file, output))

    # 評価結果を 1 つの Markdown レポートとして保存する。
    timer.start("write report")
    print("eval-oracles (5/5) write report")
    report_path = _write_report(
        repo_root,
        mode,
        branch_name,
        head_commit(repo_root),
        evaluations,
    )
    print(str(report_path))
    timer.report()


def _evaluation_prompt(repo_root: Path, oracle_file: Path) -> str:
    """oracle 評価用 prompt を組み立てる。"""
    # 評価対象 oracle だけでなく、関連仕様と実装も読むよう明示する。
    return "\n".join(
        [
            "あなたはソフトウェア仕様のレビュー担当です。",
            f"`{repo_root}` 内の oracle ファイル `{oracle_file}` を評価してください。",
            "対象 oracle だけで判断せず、同じ oracles ツリー内の関連仕様、",
            "INDEX.md のルーティング情報、必要な実装・テスト・設定",
            "ファイルも読んで評価してください。",
            "完了条件は、致命的な仕様問題の有無と根拠を報告することです。",
            "致命的な問題とは、主要ワークフローを壊す、完了判定を妨げる、または中核目的を満たしたと判断できなくする問題です。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _write_report(
    repo_root: Path,
    mode: str,
    branch_name: str,
    commit_hash: str,
    evaluations: list[tuple[Path, str]],
) -> Path:
    """評価結果を `.cmoc/reports/eval-oracles` に保存する。"""
    # 保存先ディレクトリと timestamp 付きレポートパスを用意する。
    report_dir = repo_root / ".cmoc" / "reports" / "eval-oracles"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{make_timestamp()}.md"

    # frontmatter と oracle ごとの評価本文を結合する。
    lines = [
        "---",
        f"mode: {mode}",
        f"branch: {branch_name}",
        f"commit: {commit_hash}",
        f"oracle_count: {len(evaluations)}",
        "---",
        "",
    ]
    for oracle_file, output in evaluations:
        lines.extend([f"## {oracle_file}", "", output.strip(), ""])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
