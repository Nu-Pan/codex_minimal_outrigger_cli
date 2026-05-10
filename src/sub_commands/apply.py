"""cmot apply サブコマンド。"""

from pathlib import Path

from commons.codex import run_codex_exec
from commons.errors import CmotError, exit_with_error
from commons.git import (
    commit_all,
    commit_cmot_ignore,
    dirty_paths,
    fetch_origin,
    merge_base_ref,
    prepare_repo,
    require_cmot_branch,
    status_entries,
)
from commons.logs import new_log_path
from commons.oracles import list_oracle_files
from commons.process import run_command
from commons.progress import format_elapsed, progress, start_timer


def cmot_apply_impl() -> None:
    """oracles に実装を追従させ、branch 全体の変更レポートを保存する。"""
    started_at = start_timer()
    progress("apply started")
    try:
        # repository root と cmot feature branch を確認する。
        progress("preparing repository")
        repo_root, cmot_ignore_added = prepare_repo()
        current_branch = require_cmot_branch(repo_root)

        # cmot 自身の準備差分は、人間の oracles 差分とは別 commit にする。
        if cmot_ignore_added:
            progress("committing cmot ignore")
            commit_cmot_ignore(repo_root)

        # 作業前の未コミット差分を仕様通り処理する。
        progress("checking working tree")
        paths = dirty_paths(repo_root)
        if paths and all(path.startswith("oracles/") for path in paths):
            progress("committing oracle changes")
            commit_all(repo_root, "Update oracles")
        elif paths:
            raise CmotError("working tree has changes outside oracles")

        # 最大 3 回、差異調査と実装追従を繰り返す。
        for index in range(1, 4):
            progress(f"checking oracle implementation differences ({index}/3)")
            diff_report_path = _write_oracle_implementation_diff(repo_root)
            diff_report = diff_report_path.read_text(encoding="utf-8")
            if _report_has_no_clear_difference(diff_report):
                progress("no clear differences found")
                break

            progress(f"applying oracle changes ({index}/3)")
            prompt = _build_apply_oracles_prompt(
                repo_root,
                diff_report_path,
                diff_report,
            )
            run_codex_exec(repo_root, prompt, read_only=False)

            if status_entries(repo_root):
                progress("generating commit message")
                commit_message = _generate_commit_message(repo_root)
                progress("committing implementation changes")
                commit_all(repo_root, commit_message)
            else:
                progress("no implementation changes produced")
                break

        # default branch remote 最新 commit へ merge した時の変更内容を report にする。
        progress("fetching origin")
        fetch_origin(repo_root)
        base_ref = merge_base_ref(repo_root)
        progress("generating apply report")
        report_prompt = _build_apply_report_prompt(
            repo_root,
            current_branch,
            base_ref,
        )
        report_body = run_codex_exec(repo_root, report_prompt, read_only=True)
        log_path = new_log_path(repo_root, "apply")
        diff_stat = run_command(["git", "diff", "--stat", base_ref, "HEAD"], repo_root)
        log_path.write_text(
            "# cmot apply report\n\n"
            f"Base: `{base_ref}`\n\n"
            "## Summary\n\n"
            f"{report_body.strip()}\n\n"
            "## Diff stat\n\n"
            "```text\n"
            f"{diff_stat.stdout.strip()}\n"
            "```\n",
            encoding="utf-8",
        )
        progress(f"report written: {log_path}")
        print(log_path)
        progress(f"apply completed in {format_elapsed(started_at)}")
    except CmotError as error:
        progress(f"apply failed in {format_elapsed(started_at)}")
        exit_with_error(error)


def _write_oracle_implementation_diff(repo_root: Path) -> Path:
    """oracles ファイル単位の差異調査結果を 1 ファイルにまとめる。

    Args:
        repo_root: 操作対象 repository root。

    Returns:
        差異調査結果ファイル path。
    """
    oracle_files = list_oracle_files(repo_root)
    report_parts = ["# oracles と実装の差異\n"]

    # 各 oracles ファイルと実装との差異を Codex CLI に調査させる。
    for index, oracle_file in enumerate(oracle_files, start=1):
        relative_path = oracle_file.relative_to(repo_root).as_posix()
        progress(
            f"checking oracle {index}/{len(oracle_files)}: {relative_path}",
        )
        prompt = _build_oracle_implementation_diff_prompt(repo_root, oracle_file)
        report = run_codex_exec(repo_root, prompt, read_only=True)
        report_parts.append(f"\n## `{relative_path}`\n\n{report.strip()}\n")

    path = new_log_path(repo_root, "oracle-implementation-diff")
    path.write_text("".join(report_parts), encoding="utf-8")
    progress(f"difference report written: {path}")
    return path


def _build_oracle_implementation_diff_prompt(
    repo_root: Path,
    oracle_file: Path,
) -> str:
    """oracles ファイルと実装との差異調査 prompt を作る。"""
    return (
        "## エージェントのロール\n"
        f"あなたは `{repo_root}` の開発チームの一員で、仕様と実装の差異調査を担当します。\n\n"
        "## かいつまんだ作業内容\n"
        f"`{oracle_file}` と `{repo_root}` の実装との明確な差異がないか確認してください。\n\n"
        "## 作業完了条件\n"
        "明確な差異の有無、差異がある場合はその内容と理由を日本語で報告したら完了です。\n\n"
        "## 詳細な作業内容\n"
        f"- repository root: `{repo_root}`\n"
        f"- 仕様断片ファイル: `{oracle_file}`\n"
        "- 仕様断片ファイルの内容を正として、実装が追従しているかを確認してください。\n"
        "- 対象ファイルと直接関係する実装ファイルを必要に応じて読んでください。\n"
        "- 明確な差異がない場合は、差異がないことを明示してください。\n"
        "- 推測に基づく改善提案ではなく、仕様断片と実装の明確なズレだけを報告してください。\n"
    )


def _build_apply_oracles_prompt(
    repo_root: Path,
    diff_report_path: Path,
    diff_report: str,
) -> str:
    """oracles への実装追従を依頼する prompt を作る。"""
    oracles_dir = repo_root / "oracles"
    return (
        "## エージェントのロール\n"
        f"あなたは `{repo_root}` の開発チームの一員で、仕様追従の実装を担当します。\n\n"
        "## かいつまんだ作業内容\n"
        f"`{repo_root}` の実装を `{oracles_dir}` に記載された仕様断片へ追従させてください。\n\n"
        "## 作業完了条件\n"
        f"`{diff_report_path}` に記載された明確な差異を解消するための実装変更が完了し、"
        "変更内容を簡潔に報告したら完了です。\n\n"
        "## 詳細な作業内容\n"
        f"- repository root: `{repo_root}`\n"
        f"- 仕様断片ディレクトリ: `{oracles_dir}`\n"
        f"- 差異調査結果ファイル: `{diff_report_path}`\n"
        "- 仕様断片の内容を正として、実装側を合わせてください。\n"
        "- `.agents` 配下に対する書き込み操作は禁止。そういった操作が必要になったことは"
        "作業結果として必ず報告してください。\n"
        "- 既存の設計、命名、責務分担に合わせ、必要最小限の変更に留めてください。\n"
        "- 変更後に実行すべき確認コマンドがある場合は実行し、実行できなかった場合は"
        "理由を報告してください。\n\n"
        "### 差異調査結果\n"
        f"{diff_report}"
    )


def _build_apply_report_prompt(
    repo_root: Path,
    current_branch: str,
    base_ref: str,
) -> str:
    """branch 全体の変更要約 report を依頼する prompt を作る。"""
    return (
        "## エージェントのロール\n"
        f"あなたは `{repo_root}` の開発チームの一員で、変更内容の要約を担当します。\n\n"
        "## かいつまんだ作業内容\n"
        f"git ブランチ `{current_branch}` を `{base_ref}` にマージした時の変更内容を"
        "日本語で要約してください。\n\n"
        "## 作業完了条件\n"
        "ブランチ全体の差分に基づく日本語の要約を出力したら完了です。\n\n"
        "## 詳細な作業内容\n"
        f"- repository root: `{repo_root}`\n"
        f"- 要約対象ブランチ: `{current_branch}`\n"
        f"- 比較元 ref: `{base_ref}`\n"
        "- このコマンド実行中に行われた個別作業の履歴ではなく、比較元 ref から"
        "現在の HEAD までの差分内容を要約してください。\n"
        "- 必要に応じて `git diff` や `git log` を読んでください。\n"
    )


def _report_has_no_clear_difference(report: str) -> bool:
    """差異無しと判断できる report かを保守的に判定する。

    Args:
        report: Codex CLI が出力した差異調査 report。

    Returns:
        明確に差異無しと読める場合だけ True。
    """
    lower_report = report.lower()
    difference_markers = [
        "差異があります",
        "差異がある",
        "明確な差異があります",
        "未実装",
        "不足",
        "不一致",
        "ズレ",
        "実装されていません",
        "missing",
        "not implemented",
        "difference exists",
    ]
    if any(marker in lower_report for marker in difference_markers):
        return False

    no_diff_markers = [
        "差異はありません",
        "差異なし",
        "明確な差異はありません",
        "明確な差異なし",
        "no clear difference",
        "no differences",
    ]
    return any(marker in lower_report for marker in no_diff_markers)


def _generate_commit_message(repo_root: Path) -> str:
    """現在の差分に対する commit message を Codex CLI に生成させる。

    Args:
        repo_root: 操作対象 repository root。

    Returns:
        1 行の commit message。
    """
    diff_stat = run_command(["git", "diff", "--stat"], repo_root).stdout
    prompt = _build_commit_message_prompt(repo_root, diff_stat)
    raw_message = run_codex_exec(repo_root, prompt, read_only=True).strip()
    message = raw_message.splitlines()[0].strip() if raw_message else ""
    return message or "Apply oracle changes"


def _build_commit_message_prompt(repo_root: Path, diff_stat: str) -> str:
    """現在の差分に対する commit message 生成 prompt を作る。"""
    return (
        "## エージェントのロール\n"
        f"あなたは `{repo_root}` の開発チームの一員で、git commit message の作成を担当します。\n\n"
        "## かいつまんだ作業内容\n"
        "以下の差分統計に対する簡潔な git commit message を英語で作成してください。\n\n"
        "## 作業完了条件\n"
        "英語の commit message を 1 行だけ出力したら完了です。\n\n"
        "## 詳細な作業内容\n"
        f"- repository root: `{repo_root}`\n"
        "- 引用符、箇条書き、Markdown 装飾、説明文は出力しないでください。\n"
        "- 50 文字前後を目安に、命令形の短い文にしてください。\n\n"
        "### 差分統計\n"
        f"{diff_stat}"
    )
