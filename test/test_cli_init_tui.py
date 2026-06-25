from _support import (
    FileAccessMode,
    ModelClass,
    Path,
    ReasoningEffort,
    app,
    json,
    main_module,
    make_repo,
    parse_markdown_prompt,
    run_git,
    runner,
    setup_codex_home,
    subprocess,
)

def test_init_untracks_existing_cmoc_files_and_commits_cleanup(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    tracked_cmoc_file = root / ".cmoc" / "tracked.txt"
    tracked_cmoc_file.parent.mkdir()
    tracked_cmoc_file.write_text("tracked before init\n")
    run_git(root, "add", ".cmoc/tracked.txt")
    run_git(root, "commit", "-m", "track cmoc file")
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["init"], catch_exceptions=False)

    assert result.exit_code == 0
    assert tracked_cmoc_file.exists()
    assert run_git(root, "ls-files", "--", ".cmoc").stdout.strip() == ""
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", ".cmoc/.__cmoc_ignore_probe__"],
        cwd=root,
    )
    assert ignored.returncode == 0
    assert run_git(root, "status", "--short", "--", ".gitignore").stdout.strip() == ""
    assert "cmoc init" in run_git(root, "log", "--oneline", "-1").stdout


def test_init_does_not_commit_preexisting_staged_changes(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    user_file = root / "user.txt"
    user_file.write_text("user change\n")
    run_git(root, "add", "user.txt")
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["init"], catch_exceptions=False)

    assert result.exit_code == 0
    committed_paths = run_git(
        root, "show", "--name-only", "--format=", "HEAD"
    ).stdout
    assert "user.txt" not in committed_paths
    assert run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() == [
        "user.txt"
    ]


def test_init_does_not_commit_preexisting_gitignore_changes(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    gitignore = root / ".gitignore"
    gitignore.write_text("base\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "add gitignore")
    gitignore.write_text("base\nstaged\n")
    run_git(root, "add", ".gitignore")
    gitignore.write_text("base\nstaged\nunstaged\n")
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["init"], catch_exceptions=False)

    assert result.exit_code == 0
    assert run_git(root, "show", "HEAD:.gitignore").stdout == "base\n\n/.cmoc/\n"
    assert run_git(root, "diff", "--cached", "--", ".gitignore").stdout.count(
        "+staged"
    ) == 1
    assert run_git(root, "diff", "--", ".gitignore").stdout.count("+unstaged") == 1
    assert gitignore.read_text() == "base\nstaged\nunstaged\n\n/.cmoc/\n"


def test_init_keeps_cmoc_ignored_after_preexisting_gitignore_unstaged_delete(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    gitignore = root / ".gitignore"
    gitignore.write_text("base\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "add gitignore")
    gitignore.unlink()
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["init"], catch_exceptions=False)

    assert result.exit_code == 0
    assert run_git(root, "show", "HEAD:.gitignore").stdout == "base\n\n/.cmoc/\n"
    assert gitignore.read_text() == "base\n\n/.cmoc/\n"
    assert (
        subprocess.run(
            ["git", "check-ignore", "-q", ".cmoc/.__cmoc_ignore_probe__"],
            cwd=root,
        ).returncode
        == 0
    )
    assert (
        run_git(root, "diff", "--cached", "--name-only", "--", ".gitignore").stdout
        == ""
    )
    assert run_git(root, "diff", "--name-only", "--", ".gitignore").stdout == ""


def test_init_ignores_worktree_cmoc_from_linked_worktree(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "worktrees" / "linked"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "linked-init", str(linked), "HEAD")
    monkeypatch.chdir(linked)

    result = runner.invoke(app, ["init"], catch_exceptions=False)

    assert result.exit_code == 0
    assert not (root / ".gitignore").exists()
    assert "/.cmoc/" in (linked / ".gitignore").read_text()
    assert (
        subprocess.run(
            ["git", "check-ignore", "-q", ".cmoc/.__cmoc_ignore_probe__"],
            cwd=linked,
        ).returncode
        == 0
    )
    assert (linked / ".cmoc" / "config.json").is_file()
    assert not (root / ".cmoc" / "config.json").exists()
    assert (
        run_git(
            linked,
            "status",
            "--short",
            "--",
            ".cmoc/config.json",
            ".cmoc/log/sub_command",
        ).stdout.strip()
        == ""
    )
    assert "cmoc init" in run_git(linked, "log", "--oneline", "-1").stdout
    committed_paths = run_git(
        linked, "show", "--name-only", "--format=", "HEAD"
    ).stdout.splitlines()
    assert ".gitignore" in committed_paths


def test_init_writes_default_config_json(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["init"], catch_exceptions=False)

    assert result.exit_code == 0
    config_path = root / ".cmoc" / "config.json"
    assert config_path.is_file()
    data = json.loads(config_path.read_text())
    assert data["num_parallel"] == 8
    assert data["codex"]["model"]["mainstream"] == "GPT-5.5"
    assert data["codex"]["model"]["efficiency"] == "GPT-5.4-mini"
    assert data["codex"]["reasoning_effort"]["high"] == "high"
    assert (
        subprocess.run(
            ["git", "check-ignore", "-q", ".cmoc/config.json"], cwd=root
        ).returncode
        == 0
    )
    assert (
        run_git(root, "status", "--short", "--", ".cmoc/config.json").stdout.strip()
        == ""
    )


def test_init_syncs_config_defaults_without_overwriting_human_values(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "config.json"
    config_path.parent.mkdir()
    config_path.write_text(
        json.dumps(
            {
                "num_parallel": 3,
                "codex": {"model": {"mainstream": "CUSTOM-MAIN"}},
            }
        )
        + "\n"
    )
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["init"], catch_exceptions=False)

    assert result.exit_code == 0
    data = json.loads(config_path.read_text())
    assert data["num_parallel"] == 3
    assert data["codex"]["model"]["mainstream"] == "CUSTOM-MAIN"
    assert data["codex"]["model"]["efficiency"] == "GPT-5.4-mini"
    assert data["codex"]["reasoning_effort"]["low"] == "low"
    assert data["apply_fork"]["num_apply_loop"] == 5
    assert data["review_oracle"]["num_validate_findings_loop"] == 3


def test_tui_runs_editor_resolves_parameters_and_launches_codex(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_code = bin_dir / "code"
    fake_code.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import pathlib, sys",
                "path = pathlib.Path(sys.argv[-1])",
                "text = path.read_text()",
                "path.write_text(text + '\\n<!-- remove me -->\\n# 依頼\\n\\nsrc を確認して必要なら直す\\n')",
            ]
        )
        + "\n"
    )
    fake_code.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    exec_calls = []
    tui_calls = []

    class FakeResolveResult:
        output_json = {
            "file_access_mode": {"value": "repo_write", "reason": "repo wide task"},
            "oracle_and_realization_basic": {"value": True, "reason": "needed"},
            "oracle_standard": {"value": False, "reason": "not needed"},
            "realization_standard": {"value": True, "reason": "needed"},
            "review_oracle_standard": {"value": False, "reason": "not needed"},
            "apply_review_standard": {"value": False, "reason": "not needed"},
            "index_entry_standard": {"value": False, "reason": "not needed"},
        }

    def fake_run_codex_exec(parameter, **kwargs):
        exec_calls.append((parameter, kwargs))
        assert kwargs["purpose"] == "tui resolve parameter"
        assert parameter.structured_output_schema_path.name == "resolve_parameter.json"
        assert "remove me" not in parameter.prompt
        assert "src を確認して必要なら直す" in parameter.prompt
        return FakeResolveResult()

    def fake_run_codex_tui(parameter, **kwargs):
        tui_calls.append((parameter, kwargs))
        assert kwargs["purpose"] == "tui codex"
        assert parameter.model_class == ModelClass.MAINSTREAM
        assert parameter.reasoning_effort == ReasoningEffort.MEDIUM
        assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
        assert parameter.structured_output_schema_path is None
        assert parameter.prompt.endswith("_cmpl.md` の指示に従って下さい。")

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)
    monkeypatch.setattr(main_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0
    assert len(exec_calls) == 1
    assert len(tui_calls) == 1
    orig_files = list((root / ".cmoc" / "log" / "tui").glob("*_orig.md"))
    assert len(orig_files) == 1
    assert "TODO ここから書き始める" in orig_files[0].read_text()
    complete_files = list((root / ".cmoc" / "log" / "tui").glob("*_cmpl.md"))
    assert len(complete_files) == 1
    complete_prompt = complete_files[0].read_text()
    assert "# file read write rule - repo_write" in complete_prompt
    assert "# 詳細指示" in complete_prompt
    assert "src を確認して必要なら直す" in complete_prompt
    assert "remove me" not in complete_prompt
    assert str(complete_files[0]) in tui_calls[0][0].prompt
    assert "/.cmoc/" in (root / ".gitignore").read_text()
    assert (root / ".cmoc" / "log" / "sub_command").is_dir()
    assert not (root / ".cmoc" / "logs" / "sub_commands").exists()


def test_tui_saves_complete_prompt_in_linked_worktree(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    linked = root / ".cmoc" / "worktrees" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-test", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "codex_record.json"
    fake_code = bin_dir / "code"
    fake_code.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import pathlib, sys",
                "path = pathlib.Path(sys.argv[-1])",
                "path.write_text(path.read_text() + '\\nlinked worktree task\\n')",
            ]
        )
        + "\n"
    )
    fake_code.chmod(0o755)
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, os, pathlib, sys",
                f"record = pathlib.Path({str(recorder)!r})",
                "args = sys.argv[1:]",
                "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "data = {key: {'value': False, 'reason': 'test'} for key in [",
                "    'oracle_and_realization_basic',",
                "    'oracle_standard',",
                "    'realization_standard',",
                "    'review_oracle_standard',",
                "    'apply_review_standard',",
                "    'index_entry_standard',",
                "]}",
                "data['file_access_mode'] = {'value': 'repo_write', 'reason': 'test'}",
                "output.write_text(json.dumps(data))",
                "record.write_text(json.dumps({'args': args, 'cwd': os.getcwd()}))",
                "print(json.dumps({'type': 'turn.completed'}))",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    tui_calls = []

    def fake_run_codex_tui(parameter, **kwargs):
        tui_calls.append((parameter, kwargs))

    monkeypatch.setattr(main_module, "_run_indexing_before_codex", lambda *_: None)
    monkeypatch.setattr(main_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0
    assert len(tui_calls) == 1
    assert tui_calls[0][1]["root"] == root.resolve()
    assert tui_calls[0][1]["cwd"] == linked.resolve()
    assert len(list((root / ".cmoc" / "log" / "tui").glob("*_orig.md"))) == 1
    assert not list((root / ".cmoc" / "log" / "tui").glob("*_cmpl.md"))
    complete_files = list((linked / ".cmoc" / "log" / "tui").glob("*_cmpl.md"))
    assert len(complete_files) == 1
    assert str(complete_files[0]) in tui_calls[0][0].prompt
    recorded = json.loads(recorder.read_text())
    schema_arg = recorded["args"][recorded["args"].index("--output-schema") + 1]
    assert recorded["cwd"] == str(linked)
    assert Path(schema_arg).parent == linked / ".cmoc" / "state" / "schema"
    assert not (root / ".cmoc" / "state" / "schema").exists()


def test_parse_markdown_prompt_ignores_headings_inside_fenced_code_blocks() -> None:
    parsed = parse_markdown_prompt(
        "\n".join(
            [
                "# 依頼",
                "",
                "```python",
                "# 見出しではない",
                "print('ok')",
                "```",
                "",
                "## 補足",
                "本文",
            ]
        )
    )

    assert [doc.title for doc in parsed] == ["依頼", "補足"]
    assert isinstance(parsed[0].children, str)
    assert "# 見出しではない" in parsed[0].children


def test_parse_markdown_prompt_preserves_preamble_before_headings() -> None:
    parsed = parse_markdown_prompt("最初の依頼\n\n# 詳細\n\n見出し下の依頼")

    assert [doc.title for doc in parsed] == ["本文", "詳細"]
    assert parsed[0].children == "最初の依頼"
    assert parsed[1].children == "見出し下の依頼"
