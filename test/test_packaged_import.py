"""packaged layout と import 境界を検証する。

分割根拠: {{work-root}}/spec/app_spec/cmoc_basic_instruction.md の
「realization file を扱う判断基準」
"""

import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest


def _run_from_packaged_layout(
    target: Path, code: str, tmp_path: Path
) -> subprocess.CompletedProcess[str]:
    """隔離した packaged layout で Python コードを実行する。

    `-S`、`-P`、および `PYTHONNOUSERSITE` で外部 site-packages と実行ディレクトリの
    影響を除き、
    `PYTHONPATH` でケースごとに選んだ package だけを import 対象にする。cwd と HOME も
    一時ディレクトリ内へ向け、実行者の設定や認証情報を持ち込まない。
    根拠: {{work-root}}/spec/dev_rule/coding_rule.md
    {{work-root}}/spec/dev_rule/test_rule.md
    """
    home = tmp_path / "home"
    home.mkdir()
    return subprocess.run(
        [sys.executable, "-S", "-P", "-c", code],
        cwd=tmp_path,
        env={
            **os.environ,
            "HOME": str(home),
            "PYTHONPATH": str(target),
            "PYTHONNOUSERSITE": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        text=True,
        capture_output=True,
    )


def _copy_readonly_source(source: str, target: str) -> str:
    """import が使わない file metadata をコピーせず、共有 source を読み取り専用にする。"""
    shutil.copyfile(source, target)
    Path(target).chmod(0o444)
    return target


@pytest.fixture(scope="module")
def packaged_sources(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """独立 process が読む不変な source のコピーだけを module 内で共有する。"""
    root = Path(__file__).parents[1]
    sources = tmp_path_factory.mktemp("packaged-sources")
    for relative_path in (
        "src/acp",
        "src/basic",
        "src/commons",
        "src/config",
        "reference/src/oracle",
    ):
        source = root / relative_path
        shutil.copytree(
            source,
            sources / source.name,
            copy_function=_copy_readonly_source,
            ignore=shutil.ignore_patterns("__pycache__", "*.py[cod]"),
        )
    return sources


def _packaged_layout(sources: Path, tmp_path: Path, *packages: str) -> Path:
    """各ケースの import 対象を元と同じ package 集合に限定する。"""
    # source 以外の HOME、repository、入力・出力は各 tmp_path に隔離する。
    target = tmp_path / "site"
    target.mkdir()
    for package in packages:
        (target / package).symlink_to(sources / package, target_is_directory=True)
    return target


def test_quota_probe_and_acp_basic_import_from_packaged_layout(
    tmp_path: Path,
    packaged_sources: Path,
) -> None:
    """quota probe と ACP basic の正本参照を同じ packaged process で検証する。

    acp の型再公開と正本 builder の完全 prompt を、basic・commons を含まない配置で
    確認する。共通の oracle import を一つの独立 process で検証する。
    根拠: {{work-root}}/reference/src/oracle/acp_builder/quota_probe.py
    {{work-root}}/reference/src/oracle/acp_builder/basic.py
    {{work-root}}/spec/dev_rule/test_rule.md
    """
    root = Path(__file__).parents[1]
    pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    setuptools_config = pyproject["tool"]["setuptools"]
    assert "oracle" not in setuptools_config["py-modules"]
    assert setuptools_config["package-dir"]["oracle"] == "reference/src/oracle"
    assert "reference/src" in setuptools_config["packages"]["find"]["where"]

    target = _packaged_layout(packaged_sources, tmp_path, "acp", "oracle")

    # Git metadata の導出は test_basic_runtime.py と quota の polls_and_resumes に残す。
    # ここでは探索結果だけを置換し、packaged builder と prompt の参照を実行する。
    result = _run_from_packaged_layout(
        target,
        (
            "import sys; "
            "from pathlib import Path; "
            "assert '' not in sys.path; "
            "assert str(Path.cwd()) not in sys.path; "
            "import acp.builder; "
            "from acp.builder.basic import AgentCallParameter, FileAccessMode; "
            "from oracle.acp_builder.basic import AgentCallParameter as Canonical; "
            "assert acp.builder.__all__ == ['basic']; "
            "assert sorted(n for n in vars(acp.builder) if not n.startswith('_')) == ['basic']; "
            "assert acp.builder.basic.AgentCallParameter is Canonical; "
            "assert AgentCallParameter is Canonical; "
            "assert FileAccessMode.READONLY.value == 'readonly'; "
            "import oracle.other.path_model as path_model; "
            "path_model._resolve_git_worktree_roots = "
            "lambda start_path=None: (Path.cwd(), Path.cwd()); "
            "from oracle.acp_builder.quota_probe import "
            "build_quota_availability_probe_request as build_probe; "
            "probe = build_probe(Path.cwd()); "
            "assert probe.agent_call_cwd == Path.cwd(); "
            "assert probe.prompt; "
            "assert '# feedback observation reporting' in probe.prompt; "
            "assert '# routing policy' not in probe.prompt"
        ),
        tmp_path,
    )

    assert result.returncode == 0, result.stderr


def test_decision_builders_and_prompt_editor_import_from_packaged_layout(
    tmp_path: Path,
    packaged_sources: Path,
) -> None:
    """decision の builder と editor 入力境界が packaged layout で正本を参照する。

    根拠: {{work-root}}/spec/app_spec/prompt_editor_input.md
    {{work-root}}/reference/src/oracle/acp_builder/decision/apply/launch_exec.py
    {{work-root}}/reference/src/oracle/acp_builder/decision/plan/launch_tui.py
    """
    target = _packaged_layout(packaged_sources, tmp_path, "basic", "commons", "oracle")

    # root 探索の実 Git 境界は test_basic_runtime.py と調査 TUI の結合 test に残す。
    # builder・正本 schema・editor input・handoff guide は packaged module の実経路を通す。
    # submission のない TCP 起動は省き、登録・取得・上書き・drain は
    # test_editor_input_handoff.py、editor と target の結合は test_prompt_editor_input.py に残す。
    # 採番は test_runtime_ids.py、入力 path の ID は test_prompt_editor_input.py に残し、
    # import 検査では確定済み execution ID を渡して SQLite の準備・同期書き込みを省く。
    result = _run_from_packaged_layout(
        target,
        (
            "import commons.prompt_editor_input as editor_input; "
            "import commons.runtime_editor_input_handoff_mcp as handoff_mcp; "
            "from pathlib import Path; "
            "from types import SimpleNamespace; "
            "from oracle.editor_input_handoff.guide import "
            "build_editor_input_handoff_guide; "
            "import oracle.other.path_model as path_model; "
            "path_model._resolve_git_worktree_roots = "
            "lambda start_path=None: (Path.cwd(), Path.cwd()); "
            "from oracle.acp_builder.decision.apply.launch_exec import "
            "build_decision_apply_spec_request_impl, "
            "build_decision_apply_realization_request_impl; "
            "assert callable(build_decision_apply_spec_request_impl); "
            "assert callable(build_decision_apply_realization_request_impl); "
            "from oracle.acp_builder.decision.plan.launch_tui import "
            "build_decision_plan_request as build_plan; "
            "investigation = build_plan('investigate decision'); "
            "assert investigation.file_access_mode.value == 'pure_oracle_read'; "
            "assert investigation.agent_call_cwd == Path.cwd(); "
            "assert investigation.enable_document_search_mcp is True; "
            "assert investigation.enable_editor_input_handoff_mcp is True; "
            "assert 'investigate decision' in investigation.prompt; "
            "listed = handoff_mcp._response({"
            "'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list', 'params': {}}); "
            "assert [tool['name'] for tool in listed['result']['tools']] "
            "== ['get_handoff_guide', 'overwrite']; "
            "assert listed['result']['tools'][1]['inputSchema']['required'] "
            "== ['target_id', 'goal', 'instructions', 'background', "
            "'decisions', 'open_questions', 'oracle_references']; "
            "editor_input.current_execution_id = "
            "lambda root: 'exec_000000_2000-01-01_00-00'; "
            "input_path = "
            "editor_input.reserve_prompt_editor_input(Path.cwd()); "
            "skeleton = build_plan("
            "editor_input.ORIGINAL_PROMPT_PLACEHOLDER).prompt; "
            "assert skeleton in build_editor_input_handoff_guide(skeleton); "
            "editor_input.start_editor_input_handoff = "
            "lambda root, path, prompt: SimpleNamespace("
            "target_id='packaged-target', close=lambda: None); "
            "editor_input._select_editor = lambda: ['fake-editor']; "
            "real_subprocess_run = editor_input.subprocess.run; "
            "editor_input.subprocess.run = lambda argv: "
            "(Path(argv[-1]).write_text('decision を調査する', "
            "encoding='utf-8'), "
            "SimpleNamespace(returncode=0))[1]; "
            "editor_input.edit_prompt_editor_input("
            "Path.cwd(), input_path, skeleton); "
            "editor_input.subprocess.run = real_subprocess_run; "
            "original = editor_input.collect_prompt_editor_input("
            "Path.cwd(), input_path); "
            "p = build_plan(original); "
            "assert input_path.read_text(encoding='utf-8') == "
            "'decision を調査する'; "
            "assert p.structured_output_schema_path is None; "
            "assert p.file_access_mode.value == 'pure_oracle_read'; "
            "assert p.enable_document_search_mcp is True; "
            "original_instruction = p.prompt.split("
            "'<cmoc_block id=\"original_user_instruction\">', 1)[1].split("
            "'</cmoc_block>', 1)[0]; "
            "assert 'decision を調査する' in original_instruction; "
            "assert editor_input.ORIGINAL_PROMPT_PLACEHOLDER "
            "not in original_instruction; "
            "assert not list(input_path.parent.glob('*_cmpl.md')); "
            "assert p.agent_call_cwd == Path.cwd(); "
        ),
        tmp_path,
    )

    assert result.returncode == 0, result.stderr


def test_cmoc_config_reexports_only_config_definitions(
    tmp_path: Path, packaged_sources: Path
) -> None:
    """config の公開面が正本の設定定義だけを再公開することを検証する。

    `__all__` と module namespace の両方を確認し、packaged layout で内部実装が
    意図せず公開されないことを確認する。
    根拠: {{work-root}}/reference/src/oracle/other/cmoc_config.py
    {{work-root}}/spec/dev_rule/test_rule.md
    """
    target = _packaged_layout(packaged_sources, tmp_path, "config", "oracle")

    result = _run_from_packaged_layout(
        target,
        (
            "import config.cmoc_config as c; "
            "expected = ['CmocConfig', 'CmocConfigCodex', "
            "'CodexCallConfig', 'CodexModelProviderConfig', 'JsonTomlValue']; "
            "assert c.__all__ == expected; "
            "assert sorted(n for n in vars(c) if not n.startswith('_')) == expected"
        ),
        tmp_path,
    )

    assert result.returncode == 0, result.stderr
