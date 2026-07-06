"""apply fork の report と再検査制御を CLI 経由で検証する。

このファイルは 16,000 文字を超えるが、責務境界は apply fork が所見列挙から
適用、commit、変更要約、report、session state 更新へ至る制御を検証することに
閉じている。収束、未収束、error、変更ファイル再調査、rolling fork は同じ loop と
report schema の観測結果として読まれるため、分割すると期待値の文脈が分散する。
現状は apply fork report の読み取り文脈を一箇所に保つ方が凝集性が高い。
根拠: <work-root>/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter
from _support import (
    make_repo,
    run_git,
    runner,
    run_doctor,
    setup_codex_home,
    write_python_executable,
)
from cmoc_runtime import CmocError
from commons.runtime_codex import run_codex_exec as real_run_codex_exec
from config.cmoc_config import CmocConfig
from main import app
from pytest import MonkeyPatch
import sub_commands.apply.fork as apply_fork_module
from sub_commands.apply.fork_report import (
    build_change_summary,
    changed_diff_since_fork,
    changed_paths_since_fork,
    fallback_change_summary,
)


class FakeCodexResult:
    """apply fork テストが参照する Codex 実行結果 field だけを持つ fake。"""

    def __init__(self, output_json: object | None = None, output_text: str = "") -> None:
        """必要な結果 field をテストごとに差し替えられるように保持する。"""
        self.output_json = output_json
        self.output_text = output_text


def run_apply_fork_builder_import(
    tmp_path: Path, code: str
) -> subprocess.CompletedProcess[str]:
    """subprocess の被テスト環境を tmp_path 配下だけに置く。

    根拠: <work-root>/oracle/doc/dev_rule/test_rule.md
    """
    root = Path(__file__).parents[1]
    target = tmp_path / "site"
    shutil.copytree(root / "src" / "acp", target / "acp")
    shutil.copytree(root / "src" / "basic", target / "basic")
    shutil.copytree(root / "oracle" / "src" / "oracle", target / "oracle")

    work = tmp_path / "work"
    (work / ".git").mkdir(parents=True)
    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=work,
        env={**os.environ, "PYTHONPATH": str(target), "PYTHONNOUSERSITE": "1"},
        text=True,
        capture_output=True,
    )


def test_change_summary_builder_imports_with_src_pythonpath_only(tmp_path: Path) -> None:
    result = run_apply_fork_builder_import(
        tmp_path,
        (
            "from acp.builder.apply.fork.change_summary import "
            "build_apply_fork_change_summary_parameter as build; "
            "p = build('diff'); "
            "assert p.structured_output_schema_path.name == 'change_summary.json'; "
            "assert '# oracle and realization basic' in p.prompt"
        ),
    )

    assert result.returncode == 0, result.stderr


def test_file_finding_enumeration_builder_imports_with_src_pythonpath_only(
    tmp_path: Path,
) -> None:
    result = run_apply_fork_builder_import(
        tmp_path,
        (
            "from pathlib import Path; "
            "from acp.builder.apply.fork.file_finding_enumeration import "
            "build_apply_fork_file_finding_enumeration_parameter as build; "
            "p = build(Path('<repo-root>') / 'src' / 'main.py'); "
            "assert p.structured_output_schema_path.name == "
            "'file_finding_enumeration.json'"
        ),
    )

    assert result.returncode == 0, result.stderr


def test_finding_application_builder_imports_with_src_pythonpath_only(
    tmp_path: Path,
) -> None:
    result = run_apply_fork_builder_import(
        tmp_path,
        (
            "from acp.builder.apply.fork.finding_application import "
            "build_apply_fork_finding_application_parameter as build; "
            "p = build([{'title': 't'}]); "
            "assert p.structured_output_schema_path is None; "
            "assert 'realization file' in p.prompt"
        ),
    )

    assert result.returncode == 0, result.stderr


def test_apply_fork_builders_import_from_packaged_layout(tmp_path: Path) -> None:
    result = run_apply_fork_builder_import(
        tmp_path,
        (
            "from pathlib import Path; "
            "from acp.builder.apply.fork.change_summary import "
            "build_apply_fork_change_summary_parameter as change_summary; "
            "from acp.builder.apply.fork.file_finding_enumeration import "
            "build_apply_fork_file_finding_enumeration_parameter as enumerate_file; "
            "from acp.builder.apply.fork.finding_application import "
            "build_apply_fork_finding_application_parameter as apply_finding; "
            "cs = change_summary('diff'); "
            "fe = enumerate_file(Path('<repo-root>') / 'src' / 'main.py'); "
            "fa = apply_finding([{'title': 't'}]); "
            "assert cs.structured_output_schema_path.name == 'change_summary.json'; "
            "assert fe.structured_output_schema_path.name == "
            "'file_finding_enumeration.json'; "
            "assert fa.structured_output_schema_path is None; "
            "assert '# oracle and realization basic' in cs.prompt; "
            "assert 'realization file' in fa.prompt"
        ),
    )

    assert result.returncode == 0, result.stderr


def test_finding_application_prompt_uses_complete_standard_prompt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from acp.builder.apply.fork.finding_application import (
        build_apply_fork_finding_application_parameter,
    )

    repo_root = tmp_path / "repo"
    apply_worktree = repo_root / ".cmoc" / "local" / "worktree" / "session" / "run"
    apply_worktree.mkdir(parents=True)
    (repo_root / ".git").mkdir()
    (apply_worktree / ".git").write_text("gitdir: ignored\n")
    monkeypatch.chdir(apply_worktree)

    parameter = build_apply_fork_finding_application_parameter(
        [
            {
                "title": "first",
                "evidences": [
                    {
                        "path": str(repo_root / "review" / "_comment.md"),
                        "line_start": 1,
                        "line_end": 2,
                        "summary": "comment evidence",
                    }
                ],
            },
            {"title": "second"},
        ]
    )

    assert "# oracle and realization basic" in parameter.prompt
    assert "# realization standard" in parameter.prompt
    assert "# file read write rule - realization_write" in parameter.prompt
    assert "- oracle file は書き込み禁止" in parameter.prompt
    assert "- `<work-root>/memo` は読み書き禁止" in parameter.prompt
    assert "/.agents` ツリー内は書き込み禁止" in parameter.prompt
    assert "## FINDING-00" in parameter.prompt
    assert '"title": "first"' in parameter.prompt
    assert "_comment.md" in parameter.prompt
    assert "## FINDING-01" in parameter.prompt
    assert '"title": "second"' in parameter.prompt
    assert '"findings"' not in parameter.prompt
    assert f"- <work-root> = {apply_worktree}" in parameter.prompt
    assert f"- <repo-root> = {repo_root}" in parameter.prompt


def test_file_finding_enumeration_schema_matches_oracle_source() -> None:
    from acp.builder.apply.fork.file_finding_enumeration import (
        build_apply_fork_file_finding_enumeration_parameter,
    )

    root = Path(__file__).parents[1]
    parameter = build_apply_fork_file_finding_enumeration_parameter(Path(__file__))
    oracle_schema_path = (
        root
        / "oracle"
        / "src"
        / "oracle"
        / "acp_builder"
        / "apply"
        / "fork"
        / "file_finding_enumeration.json"
    )

    assert parameter.structured_output_schema_path == oracle_schema_path
    assert (
        json.loads(parameter.structured_output_schema_path.read_text())["type"]
        == "object"
    )


def test_file_finding_enumeration_prompt_uses_complete_standard_prompt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from acp.builder.apply.fork.file_finding_enumeration import (
        build_apply_fork_file_finding_enumeration_parameter,
    )

    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    target = repo_root / "src" / "app.py"
    target.parent.mkdir()
    target.write_text("print('ok')\n")
    monkeypatch.chdir(repo_root)

    parameter = build_apply_fork_file_finding_enumeration_parameter(
        Path("<repo-root>") / "src" / "app.py"
    )

    assert "# oracle standard" in parameter.prompt
    assert "# realization standard" in parameter.prompt
    assert "# apply review standard" in parameter.prompt
    assert "- `<work-root>/memo` は読み書き禁止" in parameter.prompt
    assert f"- <target-path> = {target}" in parameter.prompt
    assert f"- <work-root> = {repo_root}" in parameter.prompt


def test_file_finding_enumeration_rejects_relative_target_without_root_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from acp.builder.apply.fork.file_finding_enumeration import (
        build_apply_fork_file_finding_enumeration_parameter,
    )

    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    monkeypatch.chdir(repo_root)

    with pytest.raises(ValueError, match="relative path without root path place holder"):
        build_apply_fork_file_finding_enumeration_parameter(Path("src/app.py"))


def report_path_from_stdout(stdout: str) -> Path:
    """apply fork stdout の共通ログ後に出る report full path を返す。"""
    lines = [line for line in stdout.splitlines() if line.startswith("/")]
    assert lines
    return Path(lines[-1])


def test_apply_fork_writes_report_with_change_summary(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """未収束 report に Codex 由来の変更要約と機械生成 commit message が反映される。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Update README",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    calls: list[str] = []
    application_count = 0

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """所見、適用、変更要約の各 Codex 応答を返す。"""
        nonlocal application_count
        purpose = str(kwargs["purpose"])
        calls.append(purpose)
        schema = (
            parameter.structured_output_schema_path.name
            if parameter.structured_output_schema_path
            else None
        )
        if purpose.startswith("apply fork enumerate findings"):
            return FakeCodexResult({"findings": [finding]})
        if purpose == "apply fork finding application":
            application_count += 1
            (Path.cwd() / "README.md").write_text(f"# updated {application_count}\n")
            return FakeCodexResult(None)
        if schema == "change_summary.json":
            return FakeCodexResult(
                {
                    "changes": [
                        {
                            "category": "ドキュメント",
                            "summary": "README を更新した",
                            "changed_paths": ["README.md"],
                        }
                    ]
                }
            )
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 2
    report_path = report_path_from_stdout(result.stdout)
    assert report_path.is_file()
    rendered = report_path.read_text()
    assert "result: unconverged" in rendered
    assert "未収束: 回数上限に達したためループを終了しました。" in rendered
    assert "# cmoc apply fork 作業レポート" in rendered
    assert "## 所見数の推移" in rendered
    count_section = rendered.split("## 所見数の推移\n", 1)[1].split(
        "\n## 変更内容要約", 1
    )[0]
    assert "まだ所見が残っている可能性があります。" in count_section
    assert "ドキュメント: README を更新した (README.md)" in rendered
    assert "apply fork change summary" in calls
    assert "apply fork commit message" not in calls
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "local" / "session" / f"{session_id}.json").read_text())
    apply_branch = state["apply"]["apply_branch"]
    assert (
        run_git(root, "log", "-1", "--pretty=%s", apply_branch).stdout.strip()
        == "Apply finding: Update README"
    )


def test_apply_fork_rechecks_changed_files_until_converged(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """apply 後の変更ファイルを再調査し、新規ディレクトリ配下も展開する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Update README",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    enumerate_calls = 0
    target_rels: list[str] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """変更ファイル再調査が収束するまでの Codex 応答を返す。"""
        nonlocal enumerate_calls
        purpose = str(kwargs["purpose"])
        if purpose.startswith("apply fork enumerate findings"):
            enumerate_calls += 1
            return FakeCodexResult(
                {"findings": [finding] if enumerate_calls == 1 else []}
            )
        if purpose == "apply fork finding application":
            (Path.cwd() / "README.md").write_text("# updated\n")
            (Path.cwd() / "newdir").mkdir()
            (Path.cwd() / "newdir" / "new.py").write_text("print('new')\n")
            return FakeCodexResult(None)
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)
    original_enumerate = apply_fork_module.enumerate_apply_findings_for_target

    def enumerate_findings(
        root_arg: Path,
        target: Path,
        config: object,
        codex_exec: object,
        **kwargs: object,
    ) -> list[dict[str, object]]:
        """実装側の列挙を呼びつつ再検査対象 path を記録する。"""
        target_rels.append(str(target.relative_to(root_arg)))
        return original_enumerate(root_arg, target, config, codex_exec, **kwargs)

    monkeypatch.setattr(
        apply_fork_module, "enumerate_apply_findings_for_target", enumerate_findings
    )

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert enumerate_calls >= 2
    assert "README.md" in target_rels
    assert "newdir/new.py" in target_rels
    report_path = report_path_from_stdout(result.stdout)
    assert "result: converged" in report_path.read_text()


def test_apply_fork_converges_when_last_allowed_target_has_no_findings(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """最後の調査対象が空所見なら上限回でも収束として扱う。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "README.md").write_text("# changed\n")
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("value = 1\n")
    run_git(root, "add", "README.md", "src/app.py")
    run_git(root, "commit", "-m", "change readme")
    config_path = root / ".cmoc" / "config.json"
    config = json.loads(config_path.read_text())
    config["apply_fork"]["num_apply_files"] = 3
    config_path.write_text(json.dumps(config, indent=2) + "\n")
    run_git(root, "add", ".cmoc/config.json")
    run_git(root, "commit", "-m", "set apply file limit")
    enumerate_calls = 0

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """上限内の全調査対象に空所見を返す。"""
        nonlocal enumerate_calls
        purpose = str(kwargs["purpose"])
        if purpose.startswith("apply fork enumerate findings"):
            enumerate_calls += 1
            return FakeCodexResult({"findings": []})
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "session"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert enumerate_calls == 3
    report_path = report_path_from_stdout(result.stdout)
    assert "result: converged" in report_path.read_text()


def test_apply_fork_is_unconverged_when_finding_application_makes_no_diff(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """所見対応で差分が出なくても、所見ありの起点対象は再調査待ちに戻す。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "README.md").write_text("# changed\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "change readme")
    config_path = root / ".cmoc" / "config.json"
    config = json.loads(config_path.read_text())
    config["apply_fork"]["num_apply_files"] = 1
    config_path.write_text(json.dumps(config, indent=2) + "\n")
    run_git(root, "add", ".cmoc/config.json")
    run_git(root, "commit", "-m", "set apply file limit")
    finding = {
        "title": "No-op finding",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    calls: list[str] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """所見は返すが適用では差分を作らない。"""
        purpose = str(kwargs["purpose"])
        calls.append(purpose)
        if purpose.startswith("apply fork enumerate findings"):
            return FakeCodexResult({"findings": [finding]})
        if purpose == "apply fork finding application":
            return FakeCodexResult()
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "session"], catch_exceptions=False
    )

    assert result.exit_code == 2
    assert "apply fork commit message" not in calls
    report_path = report_path_from_stdout(result.stdout)
    assert "result: unconverged" in report_path.read_text()
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "local" / "session" / f"{session_id}.json").read_text())
    assert (
        run_git(root, "rev-parse", state["apply"]["apply_branch"]).stdout.strip()
        == run_git(root, "rev-parse", "HEAD").stdout.strip()
    )


def test_apply_fork_does_not_recover_agent_written_forbidden_file(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """所見適用が禁止領域を汚しても事後修復しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("print('old')\n")
    run_git(root, "add", "src/app.py")
    run_git(root, "commit", "-m", "add app")
    finding = {
        "title": "Update app",
        "evidences": [
            {
                "path": str(root / "src" / "app.py"),
                "line_start": 1,
                "line_end": 1,
                "summary": "app",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update app",
    }
    setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.setattr(apply_fork_module, "enable_indexing_preflight", lambda: None)
    counts = tmp_path / "codex_counts"
    counts.mkdir()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            "args = sys.argv[1:]",
            f"counts = pathlib.Path({str(counts)!r})",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "def bump(name):",
            "    path = counts / f'{name}.txt'",
            "    value = int(path.read_text()) if path.exists() else 0",
            "    path.write_text(str(value + 1))",
            "    return value",
            "schema = None",
            "if '--output-schema' in args:",
            "    schema_path = pathlib.Path(args[args.index('--output-schema') + 1])",
            "    schema = json.loads(schema_path.read_text())",
            "props = (schema or {}).get('properties', {})",
            "if 'findings' in props:",
            f"    finding = {json.dumps(finding)!r}",
            "    output.write_text(json.dumps({'findings': [json.loads(finding)] if bump('findings') == 0 else []}))",
            "elif 'changes' in props:",
            "    output.write_text(json.dumps({'changes': []}))",
            "else:",
            "    if bump('plain') == 0:",
            "        pathlib.Path('src/app.py').write_text(\"print('updated')\\n\")",
            "        pathlib.Path('oracle/spec.md').write_text('# violated\\n')",
            "    else:",
            "        pathlib.Path('oracle/spec.md').write_text('# spec\\n')",
            "    output.write_text('{}')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    def run_real_codex_exec(parameter: AgentCallParameter, **kwargs: object) -> object:
        return real_run_codex_exec(
            parameter,
            capacity_initial_sleep_sec=0,
            **kwargs,
        )

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", run_real_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "session"], catch_exceptions=False
    )

    assert result.exit_code == 0
    calls = []
    for path in sorted((root / ".cmoc" / "local" / "log" / "codex").glob("*_call.json")):
        call = json.loads(path.read_text())
        calls.append((call["purpose"], call["file_access_mode"]))
    assert ("file access rule violation recovery", "realization_write") not in calls
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "local" / "session" / f"{session_id}.json").read_text())
    apply_branch = state["apply"]["apply_branch"]
    assert (
        run_git(root, "show", f"{apply_branch}:src/app.py").stdout
        == "print('updated')\n"
    )
    assert (
        run_git(root, "show", f"{apply_branch}:oracle/spec.md").stdout
        == "# violated\n"
    )


def test_apply_fork_error_report_summarizes_uncommitted_diff(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """エラー report の変更要約は commit 前の working tree 差分も対象にする。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Update README before error",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    applications = 0
    summary_prompt = ""

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """未 commit 差分を残したまま Codex 適用エラーへ進める。"""
        nonlocal applications, summary_prompt
        purpose = str(kwargs["purpose"])
        if purpose.startswith("apply fork enumerate findings"):
            return FakeCodexResult({"findings": [finding]})
        if purpose == "apply fork finding application":
            applications += 1
            (Path.cwd() / "README.md").write_text("# updated before error\n")
            raise CmocError("Codex 適用に失敗しました。", [], "test")
        if purpose == "apply fork change summary":
            summary_prompt = parameter.prompt
            return FakeCodexResult(
                {
                    "changes": [
                        {
                            "category": "実装",
                            "summary": "commit 前に README を更新した",
                            "changed_paths": ["README.md"],
                        }
                    ]
                }
            )
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["apply", "fork", "--scope", "full"])

    assert result.exit_code != 0
    assert applications == 1
    assert "README.md" in summary_prompt
    assert "+# updated before error" in summary_prompt
    rendered = report_path_from_stdout(result.stdout).read_text()
    assert "result: error" in rendered
    assert "実装: commit 前に README を更新した (README.md)" in rendered


def test_apply_fork_change_summary_includes_untracked_files(tmp_path: Path) -> None:
    """report 用変更要約は未追跡 file だけの作業 tree も差分として扱う。"""
    root = make_repo(tmp_path)
    fork_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (root / "new_realization.py").write_text("print('new')\n")

    raw_diff = changed_diff_since_fork(root, fork_commit)
    paths = changed_paths_since_fork(root, fork_commit)
    fallback = fallback_change_summary(root, fork_commit, "fallback")

    assert "new_realization.py" in raw_diff
    assert "+print('new')" in raw_diff
    assert paths == ["new_realization.py"]
    assert fallback == [
        {
            "category": "fallback",
            "summary": "変更 path のみを機械的に記録しました。",
            "changed_paths": ["new_realization.py"],
        }
    ]


def test_apply_fork_change_summary_excludes_deleted_tracked_files(
    tmp_path: Path,
) -> None:
    """管理 branch 上の削除済み file は report 用変更要約の対象外にする。"""
    root = make_repo(tmp_path)
    (root / "deleted_realization.py").write_text("print('delete')\n")
    run_git(root, "add", "deleted_realization.py")
    run_git(root, "commit", "-m", "add deleted target")
    fork_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (root / "deleted_realization.py").unlink()
    (root / "README.md").write_text("# kept change\n")
    captured_prompt = ""

    def fake_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        nonlocal captured_prompt
        captured_prompt = parameter.prompt
        return FakeCodexResult(
            {
                "changes": [
                    {
                        "category": "実装",
                        "summary": "README を更新した",
                        "changed_paths": ["README.md"],
                    }
                ]
            }
        )

    raw_diff = changed_diff_since_fork(root, fork_commit)
    paths = changed_paths_since_fork(root, fork_commit)
    fallback = fallback_change_summary(root, fork_commit, "fallback")
    summary = build_change_summary(
        root, root, fork_commit, CmocConfig(), fake_codex_exec
    )

    assert "README.md" in raw_diff
    assert "+# kept change" in raw_diff
    assert "deleted_realization.py" not in raw_diff
    assert "-print('delete')" not in raw_diff
    assert paths == ["README.md"]
    assert fallback[0]["changed_paths"] == ["README.md"]
    assert summary[0]["changed_paths"] == ["README.md"]
    assert "README.md" in captured_prompt
    assert "deleted_realization.py" not in captured_prompt


@pytest.mark.parametrize("codex_output", [{"changes": []}, {}])
def test_apply_fork_change_summary_fallback_keeps_paths(
    tmp_path: Path, codex_output: dict[str, object]
) -> None:
    """Codex の空要約時も、差分がある report から変更 path を落とさない。"""
    root = make_repo(tmp_path)
    fork_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (root / "README.md").write_text("# fallback path\n")

    def fake_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        return FakeCodexResult(codex_output)

    summary = build_change_summary(
        root, root, fork_commit, CmocConfig(), fake_codex_exec
    )

    assert summary == [
        {
            "category": "変更要約なし",
            "summary": "変更 path のみを機械的に記録しました。",
            "changed_paths": ["README.md"],
        }
    ]


def test_apply_fork_report_does_not_invent_loop_when_no_targets(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """調査対象がない場合、未実行の loop 1 を report しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    monkeypatch.setattr(apply_fork_module, "enumerate_apply_targets", lambda *args: [])

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """変更要約だけを返し、所見列挙が呼ばれたら失敗させる。"""
        purpose = str(kwargs["purpose"])
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["apply", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    rendered = report_path_from_stdout(result.stdout).read_text()
    assert "result: converged" in rendered
    assert "- 所見列挙ループは実行されませんでした" in rendered
    assert "- ループ 1: 0" not in rendered


def test_apply_fork_rolling_uses_previous_apply_join_commit(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """rolling apply fork が前回 apply join 後の変更だけを対象にする。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
    (root / "unrelated.py").write_text("print('before join')\n")
    run_git(root, "add", "unrelated.py")
    run_git(root, "commit", "-m", "change before apply join")
    apply_branch = f"cmoc/apply/{session_id}/manual"
    apply_worktree = root / ".cmoc" / "local" / "worktree" / session_id / "manual"
    oracle_snapshot_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    run_git(root, "worktree", "add", "-b", apply_branch, str(apply_worktree), "HEAD")
    (apply_worktree / "README.md").write_text("# updated by apply\n")
    run_git(apply_worktree, "add", "README.md")
    run_git(apply_worktree, "commit", "-m", "update readme from apply")
    state = json.loads(state_path.read_text())
    state["apply"] = {
        "state": "completed",
        "apply_branch": apply_branch,
        "oracle_snapshot_commit": oracle_snapshot_commit,
    }
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    assert (
        runner.invoke(app, ["apply", "join"], catch_exceptions=False).exit_code == 0
    )
    (root / "oracle" / "spec.md").write_text("# changed after join\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "change oracle after apply join")

    target_rels: list[str] = []

    def enumerate_findings(
        root_arg: Path,
        target: Path,
        config: object,
        codex_exec: object,
        **kwargs: object,
    ) -> list[dict[str, object]]:
        """rolling 対象 path を記録し、追加所見なしとして返す。"""
        target_rels.append(str(target.relative_to(root_arg)))
        return []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """rolling apply fork 用に空所見を返す。"""
        return FakeCodexResult({"findings": []})

    monkeypatch.setattr(
        apply_fork_module, "enumerate_apply_findings_for_target", enumerate_findings
    )
    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        fake_run_codex_exec,
    )

    result = runner.invoke(app, ["apply", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "oracle/spec.md" in target_rels
    assert "README.md" not in target_rels
    assert "unrelated.py" not in target_rels
    state = json.loads(state_path.read_text())["session"]
    assert state["last_joined_apply_oracle_snapshot_commit"] == oracle_snapshot_commit
