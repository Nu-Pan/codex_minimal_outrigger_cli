"""サブコマンド横断テストを意味カテゴリ別に分割したファイル。"""

from .helpers import *


def test_main_typer_functions_delegate_only_to_impls() -> None:
    """Typer 対応関数は共通 runner ではなく対応する impl 呼び出しだけを持つ。"""
    import main

    source = inspect.getsource(main)
    review_oracles_source = inspect.getsource(main.review_oracles_command)

    assert "def _run_command" not in source
    assert "_run_command(" not in source
    assert "cmoc_init_impl()" in source
    assert "cmoc_indexing_impl()" in source
    assert "cmoc_session_fork_impl()" in source
    assert "importlib.util" not in source
    assert "spec_from_file_location" not in source
    assert (
        "from sub_commands.review.oracles import cmoc_review_oracles_impl"
        in source
    )
    assert "from sub_commands.indexing import cmoc_indexing_impl" in source
    assert "eval-oracles.py" not in source
    assert "eval_oracles_source" not in review_oracles_source
    assert "cmoc_review_oracles_impl(" in source
    assert "scope=scope" in source
    assert "enumerate_findings_loop=enumerate_findings_loop" in source
    assert "merge_findings_loop=merge_findings_loop" in source
    assert "refine_findings_loop=refine_findings_loop" in source
    assert "repeat_investigate_and_fix=repeat_investigate_and_fix" in source
    assert "repeat_improove_fixing_list=repeat_improove_fixing_list" in source
    assert "cmoc_session_join_impl()" in source
    assert "cmoc_session_abandon_impl()" in source
    assert "cmoc_apply_abandon_impl()" in source


def test_cmoc_help_uses_cmoc_command_name() -> None:
    """PATH 経由の `cmoc --help` は Usage に cmoc を表示する。"""
    repo_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "-m", "main", "--help"],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert "Usage: cmoc [OPTIONS] COMMAND [ARGS]..." in result.stdout
    assert "session" in result.stdout
    assert "apply" in result.stdout
    assert "review" in result.stdout
    assert "indexing" in result.stdout
    assert re.search(r"\bbranch\b", result.stdout) is None
    assert re.search(r"\bmerge\b", result.stdout) is None
    assert re.search(r"\beval-oracle(?!s)\b", result.stdout) is None


def test_cmoc_review_oracles_command_and_compat_alias_are_registered() -> None:
    """`review oracles` を正名にし、既存 alias も残す。"""
    repo_root = Path(__file__).resolve().parents[2]
    env = {"PYTHONPATH": str(repo_root / "src")}
    review = subprocess.run(
        [sys.executable, "-m", "main", "review", "oracles", "--help"],
        cwd=repo_root,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    plural_alias = subprocess.run(
        [sys.executable, "-m", "main", "eval-oracles", "--help"],
        cwd=repo_root,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    singular = subprocess.run(
        [sys.executable, "-m", "main", "eval-oracle", "--help"],
        cwd=repo_root,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert review.returncode == 0
    assert plural_alias.returncode == 0
    assert singular.returncode == 0
    assert "Usage: cmoc review oracles [OPTIONS]" in review.stdout
    assert "--scope" in review.stdout
    assert "-s" in review.stdout
    assert "--enumerate-findings" in review.stdout
    assert "--merge-findings-loop" in review.stdout
    assert "--refine-findings-loop" in review.stdout
    assert "--full" not in review.stdout
    assert "--repeat-improve-issu" not in review.stdout
    assert "Usage: cmoc eval-oracles [OPTIONS]" in plural_alias.stdout
    assert "Usage: cmoc eval-oracle [OPTIONS]" in singular.stdout
    assert review.stderr == ""
    assert plural_alias.stderr == ""
    assert singular.stderr == ""


def test_cmoc_indexing_command_is_registered_without_public_options() -> None:
    """`cmoc indexing` は root 直下の明示サブコマンドとして登録される。"""
    repo_root = Path(__file__).resolve().parents[2]
    env = {"PYTHONPATH": str(repo_root / "src")}
    help_result = subprocess.run(
        [sys.executable, "-m", "main", "indexing", "--help"],
        cwd=repo_root,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    extra_arg_result = subprocess.run(
        [sys.executable, "-m", "main", "indexing", "unexpected"],
        cwd=repo_root,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert help_result.returncode == 0
    assert "Usage: cmoc indexing [OPTIONS]" in help_result.stdout
    assert "--check" not in help_result.stdout
    assert "--index-root" not in help_result.stdout
    assert help_result.stderr == ""
    assert extra_arg_result.returncode == 2
    assert extra_arg_result.stderr == ""
    _assert_markdown_error_report(extra_arg_result.stdout)
    assert "Got unexpected extra argument" in extra_arg_result.stdout


def test_cmoc_apply_fork_help_exposes_oracle_repeat_options() -> None:
    """`cmoc apply fork --help` は oracle で定義された正式オプションを表示する。"""
    repo_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "-m", "main", "apply", "fork", "--help"],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert "--apply-loop" in result.stdout
    assert "--improove-fixing" in result.stdout
    assert "--scope" in result.stdout
    assert "-s" in result.stdout
    assert "--full" not in result.stdout


def test_cmoc_apply_fork_repeat_validation_reports_oracle_option_names() -> None:
    """apply fork の回数検証メッセージは oracle の正式オプション名を案内する。"""
    with pytest.raises(CmocError) as apply_loop_error:
        apply_module._validate_repeat_options(-1, 0)
    assert "--apply-loop" in "\n".join(apply_loop_error.value.actions)
    assert "--repeat-investigate-and-fix" not in "\n".join(
        apply_loop_error.value.actions,
    )

    with pytest.raises(CmocError) as fixing_list_loop_error:
        apply_module._validate_repeat_options(0, -1)
    assert "--improove-fixing-list-loop" in "\n".join(
        fixing_list_loop_error.value.actions,
    )
    assert "--repeat-improove-fixing-list" not in "\n".join(
        fixing_list_loop_error.value.actions,
    )


def test_cmoc_review_oracles_accepts_refine_findings_loop_above_default() -> None:
    """CLI 入口では所見リスト検証ループのデフォルト 3 超を parse 時に拒否しない。"""
    repo_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "main",
            "review",
            "oracles",
            "--refine-findings-loop",
            "4",
        ],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode != 0
    assert result.stderr == ""
    _assert_markdown_error_report(result.stdout)
    assert "4 is not in the range 0<=x<=3" not in result.stdout


def test_cmoc_session_and_apply_workflow_commands_are_registered() -> None:
    """公開 CLI は session/apply の階層コマンドを登録する。"""
    repo_root = Path(__file__).resolve().parents[2]
    env = {"PYTHONPATH": str(repo_root / "src")}
    commands = [
        ("session", "fork"),
        ("session", "join"),
        ("session", "abandon"),
        ("apply", "fork"),
        ("apply", "join"),
        ("apply", "abandon"),
    ]

    for command_group, command_name in commands:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "main",
                command_group,
                command_name,
                "--help",
            ],
            cwd=repo_root,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert result.returncode == 0
        assert (
            f"Usage: cmoc {command_group} {command_name} [OPTIONS]"
            in result.stdout
        )
        assert result.stderr == ""


def test_main_returns_nonzero_for_subcommand_error() -> None:
    """サブコマンド内エラーはプロセス終了コードへ反映される。"""
    repo_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "main",
            "apply",
            "fork",
            "--repeat-investigate-and-fix",
            "-1",
        ],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 1
    assert result.stderr == ""
    _assert_markdown_error_report(result.stdout)
    assert "# Command completion report" in result.stdout


def test_main_reports_no_args_error_with_non_empty_detail() -> None:
    """引数なし起動も help と混ざらない stdout エラーレポートにする。"""
    repo_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "-m", "main"],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 2
    assert result.stderr == ""
    _assert_markdown_error_report(result.stdout)
    assert "## Summary\nコマンドが指定されていません。" in result.stdout
    assert "- 利用可能なコマンドを確認するには `cmoc --help` を実行してください。" in result.stdout
    assert "`cmoc indexing`" in result.stdout
    assert "## Detail\ncmoc がサブコマンドなしで起動されました。" in result.stdout
    assert "Traceback (most recent call last):" in result.stdout
    assert "raise _missing_command_error(\"cmoc\")" in result.stdout
    assert "Traceback is not available for this exception." not in result.stdout
    assert "Usage: cmoc [OPTIONS] COMMAND [ARGS]..." not in result.stdout


def test_main_delegates_root_completion_probe_to_typer() -> None:
    """root 補完プローブでは cmoc 独自エラーレポートを出さない。"""
    result = _run_completion_probe([], "cmoc ", 1)

    assert result.returncode == 0
    assert result.stderr == ""
    assert "ERROR" not in result.stdout
    assert "## Summary" not in result.stdout
    assert "init" in result.stdout
    assert "indexing" in result.stdout
    assert "session" in result.stdout
    assert "apply" in result.stdout
    assert "review" in result.stdout


@pytest.mark.parametrize("command_group", ["session", "apply", "review"])
def test_main_reports_command_group_without_subcommand_as_single_error_report(
    command_group: str,
) -> None:
    """command group だけの起動も help と混ぜず stdout に報告する。"""
    repo_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "-m", "main", command_group],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 2
    assert result.stderr == ""
    assert result.stdout.count("ERROR") == 1
    _assert_markdown_error_report(result.stdout)
    assert "## Summary\nコマンドが指定されていません。" in result.stdout
    assert (
        f"- 利用可能なコマンドを確認するには `cmoc {command_group} --help` を実行してください。"
        in result.stdout
    )
    assert (
        f"## Detail\ncmoc {command_group} がサブコマンドなしで起動されました。"
        in result.stdout
    )
    assert "Traceback (most recent call last):" in result.stdout
    assert "Traceback is not available for this exception." not in result.stdout
    assert f"Usage: cmoc {command_group}" not in result.stdout


@pytest.mark.parametrize(
    ("command_group", "expected_commands"),
    [
        ("session", ["fork", "join", "abandon"]),
        ("apply", ["fork", "join", "abandon"]),
        ("review", ["oracles"]),
    ],
)
def test_main_delegates_group_completion_probe_to_typer(
    command_group: str,
    expected_commands: list[str],
) -> None:
    """command group 直下の補完プローブでも独自エラーを出さない。"""
    result = _run_completion_probe(
        [command_group],
        f"cmoc {command_group} ",
        2,
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert "ERROR" not in result.stdout
    assert "## Summary" not in result.stdout
    for expected_command in expected_commands:
        assert expected_command in result.stdout


@pytest.mark.parametrize("complete_value", ["", "bash_complete", "invalid"])
def test_main_delegates_any_completion_probe_value_to_typer(
    monkeypatch: MonkeyPatch,
    complete_value: str,
) -> None:
    """補完指示値の解釈は cmoc 側で事前検査せず Typer に委譲する。"""
    import main

    app_calls: list[dict[str, object]] = []

    def fake_app(*args: object, **kwargs: object) -> None:
        app_calls.append({"args": args, "kwargs": kwargs})

    def fail_missing_command_check(_arguments: list[str]) -> None:
        raise AssertionError("completion probe must not run cmoc pre-checks")

    monkeypatch.setenv("_CMOC_COMPLETE", complete_value)
    monkeypatch.setattr(main, "app", fake_app)
    monkeypatch.setattr(
        main,
        "_raise_missing_command_error_if_needed",
        fail_missing_command_check,
    )

    main.main()

    assert app_calls == [{"args": (), "kwargs": {"prog_name": "cmoc"}}]


def test_format_error_report_fills_empty_generic_detail() -> None:
    """通常例外の文字列表現が空でも Detail を空欄にしない。"""
    error = Exception()

    report = format_error_report(error)

    _assert_markdown_error_report(report)
    assert "## Summary\nException" in report
    assert (
        "- 入力値が誤っている場合は、コマンド引数を修正してから cmoc を再実行してください。"
        in report
    )
    assert (
        "- リポジトリ状態が原因の場合は、Detail と Call stack を確認して作業ツリーや設定を修正してください。"
        in report
    )
    assert "## Detail\nbuiltins.Exception がメッセージなしで発生しました。" in report


def test_format_error_report_includes_called_process_output() -> None:
    """git 失敗時は capture 済みの stderr/stdout を Detail に含める。"""
    error = subprocess.CalledProcessError(
        returncode=128,
        cmd=["git", "switch", "missing branch"],
        output="stdout diagnostic\n",
        stderr="fatal: invalid reference: missing branch\n",
    )

    report = format_error_report(error)

    _assert_markdown_error_report(report)
    assert "## Summary\nCalledProcessError" in report
    assert "## Detail" in report
    assert "returncode:\n128" in report
    assert "cmd:\ngit switch 'missing branch'" in report
    assert "stderr:\nfatal: invalid reference: missing branch" in report
    assert "stdout:\nstdout diagnostic" in report


def test_format_error_report_uses_passed_exception_traceback() -> None:
    """except 外でも、渡された例外自身の traceback を表示する。"""

    def raise_target_error() -> None:
        raise RuntimeError("target failure")

    try:
        raise_target_error()
    except RuntimeError as captured:
        error = captured

    try:
        raise ValueError("unrelated failure")
    except ValueError:
        report = format_error_report(error)

    assert "RuntimeError: target failure" in report
    assert "raise_target_error()" in report
    assert 'raise RuntimeError("target failure")' in report
    assert "ValueError: unrelated failure" not in report


def test_format_error_report_describes_missing_traceback() -> None:
    """未 raise の例外では NoneType ではなく traceback 不在を明示する。"""
    error = RuntimeError("not raised")

    report = format_error_report(error)

    assert "RuntimeError: not raised" not in report
    assert "NoneType: None" not in report
    assert "Traceback is not available for this exception." in report


def test_user_facing_error_text_does_not_keep_known_english_phrases() -> None:
    """共通エラーレポートに渡す説明・次アクションを日本語方針で固定する。"""
    repo_root = Path(__file__).resolve().parents[2]
    target_paths = [
        repo_root / "src" / "commons" / "errors.py",
        repo_root / "src" / "commons" / "repo.py",
        repo_root / "src" / "sub_commands" / "apply" / "fork.py",
        repo_root / "src" / "sub_commands" / "session" / "abandon.py",
        repo_root / "src" / "sub_commands" / "session" / "join.py",
    ]
    forbidden_fragments = [
        "Git repository root was not found.",
        "Move into a git-managed repository.",
        "Uncommitted changes exist.",
        "Commit or stash",
        "cmoc apply must be run on a cmoc managed branch.",
        "Run `cmoc session fork` first.",
        "Failed to resolve cmoc managed branch automatically.",
        "Pass the cmoc managed branch name explicitly.",
        "Inspect git status manually.",
        "Resolve remaining conflict markers manually.",
        "Manual resolution is required.",
    ]
    source_text = "\n".join(
        path.read_text(encoding="utf-8") for path in target_paths
    )

    for fragment in forbidden_fragments:
        assert fragment not in source_text


def test_bin_cmoc_requires_venv_python() -> None:
    """ランチャーは system python3 へフォールバックせず、エラーは stdout へ出す。"""
    repo_root = Path(__file__).resolve().parents[2]
    launcher = (repo_root / "bin" / "cmoc").read_text(encoding="utf-8")

    assert launcher.startswith("#!/bin/sh")
    assert "#!/usr/bin/env python3" not in launcher
    assert 'exec "$venv_python"' in launcher
    assert "} >&2" not in launcher


def test_test_sh_uses_own_worktree_bin_before_venv(tmp_path: Path) -> None:
    """test.sh は自身の worktree の bin/cmoc を PATH で優先する。"""
    repo_root = Path(__file__).resolve().parents[2]
    outside = tmp_path / "outside"
    fake_venv_bin = tmp_path / "fake-venv" / "bin"
    fake_venv_bin.mkdir(parents=True)
    outside.mkdir()
    (fake_venv_bin / "cmoc").write_text(
        "#!/bin/sh\nprintf '%s\\n' fake-venv-cmoc\n",
        encoding="utf-8",
    )
    (fake_venv_bin / "cmoc").chmod(0o755)

    result = subprocess.run(
        [
            "bash",
            "-c",
            (
                "set -eu\n"
                "cd \"$1\"\n"
                "PATH=\"$2:$PATH\"\n"
                ". \"$3/test.sh\"\n"
                "printf '%s\\n' \"$CMOC_ROOT\"\n"
                "printf '%s\\n' \"${PATH%%:*}\"\n"
                "without_first=${PATH#*:}\n"
                "printf '%s\\n' \"${without_first%%:*}\"\n"
                "command -v cmoc\n"
            ),
            "bash",
            str(outside),
            str(fake_venv_bin),
            str(repo_root),
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    lines = result.stdout.splitlines()
    assert result.stderr == ""
    assert lines == [
        str(repo_root),
        str(repo_root / "bin"),
        str(repo_root / ".venv" / "bin"),
        str(repo_root / "bin" / "cmoc"),
    ]


def test_bin_cmoc_reports_missing_venv_to_stdout(tmp_path: Path) -> None:
    """仮想環境が無い場合も共通エラーレポートを stdout へ出す。"""
    repo_root = Path(__file__).resolve().parents[2]
    launcher = tmp_path / "repo" / "bin" / "cmoc"
    launcher.parent.mkdir(parents=True)
    launcher.write_text(
        (repo_root / "bin" / "cmoc").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    launcher.chmod(0o755)

    result = subprocess.run(
        [str(launcher), "--help"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 1
    assert result.stderr == ""
    _assert_markdown_error_report(result.stdout)
    assert "仮想環境 Python" in result.stdout
    assert "at print_missing_venv_error" in result.stdout
    assert "at require_venv_python" in result.stdout
    assert "at main" in result.stdout
    assert "仮想環境 Python の実行可能性チェック" not in result.stdout


@pytest.mark.parametrize("complete_value", ["complete_bash", ""])
def test_bin_cmoc_suppresses_missing_venv_report_for_completion_probe(
    tmp_path: Path,
    complete_value: str,
) -> None:
    """補完プローブでは venv 欠落時も独自エラーレポートを混ぜない。"""
    repo_root = Path(__file__).resolve().parents[2]
    launcher = tmp_path / "repo" / "bin" / "cmoc"
    launcher.parent.mkdir(parents=True)
    launcher.write_text(
        (repo_root / "bin" / "cmoc").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    launcher.chmod(0o755)

    result = subprocess.run(
        [str(launcher)],
        check=False,
        env={
            "_CMOC_COMPLETE": complete_value,
            "COMP_WORDS": "cmoc ",
            "COMP_CWORD": "1",
        },
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 1
    assert result.stderr == ""
    assert result.stdout == ""
