"""Codex の read/write 許可領域と追加 writable path を検証する。

根拠:
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
- {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
"""

import shutil
import subprocess
from pathlib import Path

import pytest
from _codex_support import (
    _assert_not_writable,
    _assert_writable,
    _override_permission_filesystem,
    _override_permission_roots,
)
from _git_support import make_repo, run_git

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError
from commons.runtime_codex_profile import build_codex_override_args
from config.cmoc_config import CmocConfig


@pytest.mark.parametrize(
    "mode", [FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ]
)
def test_codex_overrides_readonly_modes_do_not_inject_ignored_gap_writes(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """読み取り専用モードが ignore 判定から書き込み権限を生成しないことを検証する。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("__pycache__/\n/build/\n")
    (root / "src").mkdir()
    (root / "src" / "main.py").write_text("print('ok')\n")
    (root / "src" / "__pycache__").mkdir()
    (root / "src" / "__pycache__" / "main.pyc").write_text("cache\n")
    (root / "oracle" / "spec.md").write_text("# spec\n")
    (root / "oracle" / "__pycache__").mkdir()
    (root / "oracle" / "__pycache__" / "spec.pyc").write_text("cache\n")
    (root / "build").mkdir()
    (root / "build" / "artifact.txt").write_text("tracked\n")
    (root / "build" / "scratch.txt").write_text("scratch\n")
    run_git(root, "add", ".gitignore", "src/main.py", "oracle/spec.md")
    run_git(root, "add", "-f", "build/artifact.txt")
    run_git(root, "commit", "-m", "add tracked files")

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            mode,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )
    _assert_not_writable(override_args, root / "src" / "new.py")
    _assert_not_writable(override_args, root / "oracle" / "new.md")
    _assert_not_writable(override_args, root / "new.md")

    assert _override_permission_roots(override_args, "write") == set()
    _assert_not_writable(override_args, root / "src" / "__pycache__" / "new.pyc")
    _assert_not_writable(override_args, root / "oracle" / "__pycache__" / "new.pyc")
    _assert_not_writable(override_args, root / "build" / "scratch.txt")
    _assert_not_writable(override_args, root / "src" / "main.py")
    _assert_not_writable(override_args, root / "oracle" / "spec.md")
    _assert_not_writable(override_args, root / "build" / "artifact.txt")
    _assert_not_writable(override_args, root / "memo" / "private.md")
    _assert_not_writable(override_args, root / ".cmoc" / "gu" / "state.json")


@pytest.mark.parametrize(
    "mode",
    [
        FileAccessMode.REALIZATION_WRITE,
        FileAccessMode.PURE_ORACLE_WRITE,
        FileAccessMode.REPO_WRITE,
        FileAccessMode.SKILL_AUTHORING_WRITE,
        FileAccessMode.NO_RULE,
    ],
)
def test_codex_overrides_protect_memo_and_future_routing_files(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """memo と将来のルーティングファイルを全書き込みモードで保護することを検証する。"""
    root = make_repo(tmp_path)
    (root / "src").mkdir()
    (root / "test").mkdir()

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            mode,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )

    filesystem = _override_permission_filesystem(override_args)
    assert filesystem[str((root / "memo").resolve())] == "deny"
    routing_rules = filesystem[":workspace_roots"]
    assert routing_rules == {
        "AGENTS.md": "read",
        "INDEX.md": "read",
    }
    _assert_not_writable(override_args, root / "memo" / "private.md")


def test_codex_overrides_no_rule_uses_root_with_fixed_protected_paths(
    tmp_path: Path,
) -> None:
    """NO_RULE は root を開き、active oracle の固定 path だけを保護する。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    root = make_repo(tmp_path)
    for name in (".agents", ".cmoc", ".codex", "memo"):
        (root / name).mkdir()
    (root / "src").mkdir()

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.NO_RULE,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )

    assert _override_permission_roots(override_args, "write") == {str(root.resolve())}
    for relative in (
        ".agents/blocked.md",
        ".cmoc/gu/ar/state.json",
        ".cmoc/gt/ar/config.json",
        ".codex/config.toml",
        ".git/config",
        "memo/private.md",
        "AGENTS.md",
        "INDEX.md",
    ):
        _assert_not_writable(override_args, root / relative)
    _assert_writable(override_args, root / ".cmoc" / "gu" / "state.json")
    _assert_writable(override_args, root / "src" / "new.py")


def test_codex_overrides_skill_authoring_opens_only_agents_skills(
    tmp_path: Path,
) -> None:
    """Skill authoring mode が `.agents/skills` 以外の保護を維持する。"""
    root = make_repo(tmp_path)
    skills = root / ".agents" / "skills"
    existing_skill = skills / "existing"
    existing_skill.mkdir(parents=True)
    (root / ".agents" / ".gitkeep").write_text("")
    (existing_skill / "SKILL.md").write_text("---\nname: existing\n---\n")
    (existing_skill / "AGENTS.md").write_text("protected\n")
    (existing_skill / "INDEX.md").write_text("protected\n")

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.SKILL_AUTHORING_WRITE,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )

    filesystem = _override_permission_filesystem(override_args)
    assert filesystem[str((root / ".agents").resolve())] == "read"
    assert filesystem[str(skills.resolve())] == "write"
    _assert_writable(override_args, root / "src" / "new.py")
    _assert_writable(override_args, existing_skill / "SKILL.md")
    _assert_writable(override_args, skills / "new-skill" / "SKILL.md")
    _assert_not_writable(override_args, root / ".agents" / ".gitkeep")
    _assert_not_writable(override_args, root / ".agents" / "other" / "file.md")
    _assert_not_writable(override_args, existing_skill / "AGENTS.md")
    _assert_not_writable(override_args, existing_skill / "INDEX.md")
    _assert_not_writable(override_args, root / ".git" / "config")
    _assert_not_writable(override_args, root / ".codex" / "config.toml")
    _assert_not_writable(override_args, root / ".cmoc" / "gu" / "ar" / "state.json")
    _assert_not_writable(override_args, root / "memo" / "private.md")


@pytest.mark.parametrize(
    "mode",
    [
        FileAccessMode.REALIZATION_WRITE,
        FileAccessMode.PURE_ORACLE_WRITE,
        FileAccessMode.REPO_WRITE,
        FileAccessMode.NO_RULE,
    ],
)
def test_normal_write_modes_cannot_modify_repo_local_skills(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """専用 mode 以外では repo-local Skill を書き換えられない。"""
    root = make_repo(tmp_path)
    skill_file = root / ".agents" / "skills" / "existing" / "SKILL.md"
    skill_file.parent.mkdir(parents=True)
    skill_file.write_text("---\nname: existing\n---\n")

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            mode,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )

    _assert_not_writable(override_args, skill_file)


@pytest.mark.parametrize(
    "mode", [FileAccessMode.REALIZATION_WRITE, FileAccessMode.REPO_WRITE]
)
def test_codex_overrides_allows_tracked_cmoc_config_but_blocks_local(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """tracked な config は許可し、runtime state と routing file は保護する。"""
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    generated_agent_read_path = root / ".cmoc" / "gu" / "ar"
    generated_agent_read_path.mkdir(parents=True)
    config_path.parent.mkdir(parents=True)
    config_path.write_text("{}\n")
    (root / ".gitignore").write_text("/.cmoc/gu/\n")
    run_git(root, "add", ".gitignore", ".cmoc/gt/ar/config.json")
    run_git(root, "commit", "-m", "add tracked cmoc config")

    override_args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            mode,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )

    _assert_not_writable(override_args, config_path)
    _assert_not_writable(override_args, generated_agent_read_path / "state.json")
    _assert_not_writable(override_args, root / "AGENTS.md")
    _assert_not_writable(override_args, root / "INDEX.md")


def test_codex_overrides_does_not_derive_permissions_from_ignored_dir(
    tmp_path: Path,
) -> None:
    """無視対象 directory の実在 path を個別の権限設定へ変換しない。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("/build/\n")
    (root / "src").mkdir()
    (root / "src" / "main.py").write_text("print('ok')\n")
    (root / "test").mkdir()
    (root / "test" / "test_main.py").write_text("def test_ok(): pass\n")
    (root / "build").mkdir()
    (root / "build" / "artifact.txt").write_text("artifact\n")
    run_git(root, "add", ".gitignore", "src", "test")
    run_git(root, "add", "-f", "build")
    run_git(root, "commit", "-m", "add realization dirs")

    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.REALIZATION_WRITE,
        "prompt",
        None,
    )
    override_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        root,
    )

    expected_roots = {str(root.resolve())}
    assert _override_permission_roots(override_args, "write") == expected_roots
    filesystem = _override_permission_filesystem(override_args)
    build_root = (root / "build").resolve()
    assert all(
        key == ":workspace_roots" or not Path(key).resolve().is_relative_to(build_root)
        for key in filesystem
    )
    _assert_writable(override_args, root / "src" / "main.py")
    _assert_writable(override_args, root / "src" / "new.py")
    _assert_writable(override_args, root / "build" / "artifact.txt")
    _assert_writable(override_args, root / ".gitignore")
    _assert_writable(override_args, root / "build" / "new.txt")
    _assert_not_writable(override_args, root / ".agents" / "blocked.md")
    extra = root / "docs" / "generated.md"

    override_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        root,
        extra_writable_paths=[extra],
    )
    assert _override_permission_roots(override_args, "write") == expected_roots
    _assert_writable(override_args, extra)


@pytest.mark.parametrize("mode", list(FileAccessMode))
def test_codex_overrides_are_invariant_to_ignored_subtree_contents(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """ignored subtree の個別ファイルを permission argv へ注入しない。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("/generated/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "ignore generated output")
    generated = root / "generated"
    generated.mkdir()
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )

    baseline_args = build_codex_override_args(parameter, CmocConfig(), root)
    for directory_index in range(12):
        directory = generated / f"part-{directory_index:02d}"
        directory.mkdir()
        for file_index in range(20):
            (directory / f"artifact-{file_index:02d}.bin").write_text("generated\n")

    populated_args = build_codex_override_args(parameter, CmocConfig(), root)

    assert populated_args == baseline_args
    generated_root = generated.resolve()
    assert all(
        key == ":workspace_roots"
        or Path(key).resolve() == generated_root
        or not Path(key).resolve().is_relative_to(generated_root)
        for key in _override_permission_filesystem(populated_args)
    )


@pytest.mark.parametrize(
    ("mode", "extra"),
    [
        (FileAccessMode.REALIZATION_WRITE, "oracle/blocked.md"),
        (FileAccessMode.REALIZATION_WRITE, "memo/blocked.md"),
        (FileAccessMode.REALIZATION_WRITE, ".agents/blocked.md"),
        (FileAccessMode.REALIZATION_WRITE, ".codex/config.toml"),
        (FileAccessMode.REALIZATION_WRITE, "AGENTS.md"),
        (FileAccessMode.REALIZATION_WRITE, "INDEX.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, "src/blocked.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, "memo/blocked.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, ".agents/blocked.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, "oracle/INDEX.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, "oracle/AGENTS.md"),
        (FileAccessMode.REPO_WRITE, "memo/blocked.md"),
        (FileAccessMode.REPO_WRITE, ".agents/blocked.md"),
        (FileAccessMode.REPO_WRITE, ".git/config"),
        (FileAccessMode.REPO_WRITE, "AGENTS.md"),
        (FileAccessMode.REPO_WRITE, "INDEX.md"),
        (FileAccessMode.REPO_WRITE, "../outside.md"),
        (FileAccessMode.SKILL_AUTHORING_WRITE, ".agents/other/blocked.md"),
        (FileAccessMode.SKILL_AUTHORING_WRITE, ".git/config"),
        (FileAccessMode.SKILL_AUTHORING_WRITE, "AGENTS.md"),
        (FileAccessMode.SKILL_AUTHORING_WRITE, "INDEX.md"),
    ],
)
def test_codex_overrides_rejects_disallowed_extra_writable_paths(
    tmp_path: Path, mode: FileAccessMode, extra: str
) -> None:
    """モードごとの許可領域外にある追加書き込み先を拒否することを検証する。"""
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    (root / "oracle").mkdir()
    (root / "memo").mkdir()
    (root / ".agents").mkdir()

    with pytest.raises(CmocError, match="追加書き込み許可 path"):
        build_codex_override_args(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                mode,
                "prompt",
                None,
            ),
            CmocConfig(),
            root,
            extra_writable_paths=[root / extra],
        )


@pytest.mark.parametrize(
    "mode", [FileAccessMode.REALIZATION_WRITE, FileAccessMode.REPO_WRITE]
)
def test_codex_overrides_allows_new_root_ancillary_file(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """realization write がルート直下の ancillary ファイルを追加許可できることを検証する。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("memo\n")
    (root / "README.md").write_text("# repo\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "add gitignore")

    extra = root / "CHANGELOG.md"
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )
    baseline_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        root,
    )
    _assert_writable(baseline_args, extra)
    assert _override_permission_roots(baseline_args, "write") == {str(root.resolve())}


@pytest.mark.parametrize(
    "mode", [FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ]
)
def test_codex_overrides_readonly_modes_allow_extra_ignored_gap_path(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """読み取り専用モードが ignore された gap path の追加許可を受け入れることを検証する。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("/scratch.tmp\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "add gitignore")
    target = root / "scratch.tmp"

    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )
    baseline_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        root,
    )
    _assert_not_writable(baseline_args, target)

    override_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        root,
        extra_writable_paths=[target],
    )

    _assert_writable(override_args, target)


@pytest.mark.parametrize(
    "mode", [FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ]
)
def test_codex_overrides_does_not_expand_explicit_ignored_directory(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """明示した ignored directory は一つの root として許可し、子を列挙しない。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("/scratch/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "ignore scratch")
    target = root / "scratch"
    nested = target / "nested"
    nested.mkdir(parents=True)
    (nested / "artifact.bin").write_text("scratch\n")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )

    override_args = build_codex_override_args(
        parameter,
        CmocConfig(),
        root,
        extra_writable_paths=[target],
    )

    assert _override_permission_roots(override_args, "write") == {str(target.resolve())}
    filesystem = _override_permission_filesystem(override_args)
    assert all(
        key == ":workspace_roots"
        or Path(key).resolve() == target.resolve()
        or not Path(key).resolve().is_relative_to(target.resolve())
        for key in filesystem
    )
    _assert_writable(override_args, nested / "new.bin")


@pytest.mark.parametrize(
    "mode",
    [
        FileAccessMode.REALIZATION_WRITE,
        FileAccessMode.PURE_ORACLE_WRITE,
        FileAccessMode.REPO_WRITE,
        FileAccessMode.SKILL_AUTHORING_WRITE,
        FileAccessMode.NO_RULE,
    ],
)
def test_codex_permission_profile_is_accepted_by_codex_cli(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """書き込み用 profile の同じ argv を実 Codex CLI の parser に通す。"""
    codex = shutil.which("codex")
    if codex is None:
        pytest.skip("codex CLI is not installed")

    root = make_repo(tmp_path)
    args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            mode,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # Missing schema validation stops before authentication or model execution.
    result = subprocess.run(
        [
            codex,
            "exec",
            "--ignore-user-config",
            "--ignore-rules",
            "--ephemeral",
            "--skip-git-repo-check",
            "--output-schema",
            str(tmp_path / "missing-schema.json"),
            "--json",
            *args,
            "-",
        ],
        cwd=root,
        input="probe\n",
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )
    output = result.stdout + result.stderr
    assert result.returncode == 1
    assert "filesystem glob path" not in output
    assert "Failed to read output schema file" in output
