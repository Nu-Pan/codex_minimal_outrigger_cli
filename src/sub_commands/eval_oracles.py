"""cmot eval-oracles サブコマンド。"""

from pathlib import Path

from commons.codex import run_codex_exec
from commons.errors import CmotError, exit_with_error
from commons.git import prepare_repo, require_cmot_branch
from commons.logs import new_log_path
from commons.oracles import list_oracle_files


def cmot_eval_oracles_impl() -> None:
    """oracles の個別評価と関係性評価を行い、レポートを保存する。"""
    try:
        repo_root = prepare_repo()
        require_cmot_branch(repo_root)

        # oracles ファイルごとに Codex CLI で評価する。
        oracle_files = list_oracle_files(repo_root)
        per_file_reports: list[tuple[Path, str]] = []
        for oracle_file in oracle_files:
            prompt = _build_per_file_evaluation_prompt(repo_root, oracle_file)
            per_file_reports.append((oracle_file, run_codex_exec(repo_root, prompt)))

        # 全 oracles 間の関係性を Codex CLI で評価する。
        relation_prompt = _build_cross_file_evaluation_prompt(repo_root, oracle_files)
        relation_report = run_codex_exec(repo_root, relation_prompt)

        # これまでの評価を 1 つのレポートにまとめる。
        report_parts = ["# cmot eval-oracles report\n"]
        report_parts.append("## Oracle files\n")
        if oracle_files:
            report_parts.extend(
                f"- `{path.relative_to(repo_root).as_posix()}`\n"
                for path in oracle_files
            )
        else:
            report_parts.append("- No oracle files found.\n")

        report_parts.append("\n## Per-file evaluation\n")
        for oracle_file, report in per_file_reports:
            relative_path = oracle_file.relative_to(repo_root).as_posix()
            report_parts.append(f"\n### `{relative_path}`\n\n{report.strip()}\n")

        report_parts.append("\n## Cross-file evaluation\n\n")
        report_parts.append(relation_report.strip())
        report_parts.append("\n")

        log_path = new_log_path(repo_root, "eval-oracles")
        log_path.write_text("".join(report_parts), encoding="utf-8")
        print(log_path)
    except CmotError as error:
        exit_with_error(error)


def _build_per_file_evaluation_prompt(repo_root: Path, oracle_file: Path) -> str:
    """oracles ファイル単体を評価させる prompt を作る。"""
    return (
        "## エージェントのロール\n"
        f"あなたは `{repo_root}` の開発チームの一員で、仕様断片のレビューを担当します。\n\n"
        "## かいつまんだ作業内容\n"
        f"`{oracle_file}` を評価してください。\n\n"
        "## 作業完了条件\n"
        "対象ファイルに致命的な問題があるかどうかと、問題がある場合の理由を"
        "日本語で報告したら完了です。\n\n"
        "## 詳細な作業内容\n"
        f"- 対象ファイル: `{oracle_file}`\n"
        f"- 対象ファイルが属する repository root: `{repo_root}`\n"
        "- 対象ファイルの内容だけで判断できない場合は、同じ repository 内の関係する"
        "ファイルも読んでください。\n"
        "- 仕様として曖昧すぎる点、実装不能な点、他の仕様断片と衝突しそうな点を"
        "優先して確認してください。\n"
        "- 致命的な問題が見つからない場合も、その旨を明確に書いてください。\n"
    )


def _build_cross_file_evaluation_prompt(
    repo_root: Path,
    oracle_files: list[Path],
) -> str:
    """oracles ファイル間の関係性を評価させる prompt を作る。"""
    oracle_list = "\n".join(f"- `{path}`" for path in oracle_files)
    if not oracle_list:
        oracle_list = "- 対象ファイルなし"

    return (
        "## エージェントのロール\n"
        f"あなたは `{repo_root}` の開発チームの一員で、仕様断片全体のレビューを担当します。\n\n"
        "## かいつまんだ作業内容\n"
        "以下に列挙する仕様断片ファイルを全て読み、ファイル間の関係性を評価してください。\n\n"
        "## 作業完了条件\n"
        "仕様断片同士に致命的な矛盾、重複による解釈不能、または実装上の重大な"
        "リスクがあるかどうかを日本語で報告したら完了です。\n\n"
        "## 詳細な作業内容\n"
        f"- repository root: `{repo_root}`\n"
        "- 評価対象ファイル:\n"
        f"{oracle_list}\n"
        "- 必要に応じて、同じ repository 内の実装ファイルも読んでください。\n"
        "- 致命的な問題が見つからない場合も、その旨を明確に書いてください。\n"
    )
