"""packaged layout と import 境界を検証する。

分割根拠: {{work-root}}/oracle/doc/app_spec/oracle_and_realization.md の
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
    target: Path, code: str, tmp_path: Path, *, cmoc_process_cwd: Path
) -> subprocess.CompletedProcess[str]:
    """隔離した packaged layout で Python コードを実行する。

    `-S`、`-P`、および `PYTHONNOUSERSITE` で外部 site-packages と実行ディレクトリの
    影響を除き、
    `PYTHONPATH` でケースごとに選んだ package だけを import 対象にする。Git repository が
    必要なケースだけ呼び出し側で用意する。HOME も一時
    ディレクトリ内へ向け、実行者の設定や認証情報を持ち込まない。
    根拠: {{work-root}}/oracle/doc/dev_rule/coding_rule.md
    {{work-root}}/oracle/doc/dev_rule/test_rule.md
    """
    home = tmp_path / "home"
    home.mkdir()
    return subprocess.run(
        [sys.executable, "-S", "-P", "-c", code],
        cwd=cmoc_process_cwd,
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


def _copy_source_tree(source: Path, target: Path) -> None:
    """bytecode cache を除いた source tree を packaged layout へコピーする。

    根拠: {{work-root}}/oracle/doc/dev_rule/test_rule.md
    """
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns("__pycache__", "*.py[cod]"),
    )


@pytest.fixture(scope="module")
def packaged_sources(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """独立 process が読む不変な source のコピーだけを module 内で共有する。"""
    root = Path(__file__).parents[1]
    sources = tmp_path_factory.mktemp("packaged-sources")
    for package in ("acp", "basic", "commons", "config"):
        _copy_source_tree(root / "src" / package, sources / package)
    _copy_source_tree(root / "oracle" / "src" / "oracle", sources / "oracle")
    for path in sources.rglob("*"):
        if path.is_file():
            path.chmod(0o444)
    return sources


def _packaged_layout(sources: Path, tmp_path: Path, *packages: str) -> Path:
    """各ケースの import 対象を元と同じ package 集合に限定する。"""
    # source 以外の HOME、repository、入力・出力は各 tmp_path に隔離する。
    target = tmp_path / "site"
    target.mkdir()
    for package in packages:
        (target / package).symlink_to(sources / package, target_is_directory=True)
    return target


def test_quota_probe_imports_from_packaged_layout(
    tmp_path: Path,
    cli_repository: Path,
    packaged_sources: Path,
) -> None:
    """quota probe の canonical builder を packaged layout で検証する。

    正本 builder が packaged layout でも完全 prompt を参照し、期待する parameter
    を生成できることを確認する。
    根拠: {{work-root}}/oracle/src/oracle/acp_builder/quota_probe.py
    {{work-root}}/oracle/doc/dev_rule/test_rule.md
    """
    root = Path(__file__).parents[1]
    pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    setuptools_config = pyproject["tool"]["setuptools"]
    assert "oracle" not in setuptools_config["py-modules"]
    assert setuptools_config["package-dir"]["oracle"] == "oracle/src/oracle"
    assert "oracle/src" in setuptools_config["packages"]["find"]["where"]

    target = _packaged_layout(packaged_sources, tmp_path, "acp", "basic", "oracle")

    result = _run_from_packaged_layout(
        target,
        (
            "import sys; "
            "from pathlib import Path; "
            "assert '' not in sys.path; "
            "assert str(Path.cwd()) not in sys.path; "
            "from basic.acp import AgentCallParameter, FileAccessMode; "
            "from acp.builder.quota_probe import "
            "build_quota_availability_probe_parameter as build_probe; "
            "base = AgentCallParameter('base', FileAccessMode.READONLY, "
            "'base', None, Path.cwd()); "
            "probe = build_probe(base); "
            "assert probe.prompt; "
            "assert '# feedback observation reporting' in probe.prompt; "
            "assert '# routing policy' not in probe.prompt"
        ),
        tmp_path,
        # probe の path context は Git root だけを使い、追跡 file・commit は不要。
        cmoc_process_cwd=cli_repository,
    )

    assert result.returncode == 0, result.stderr


def test_oracle_edit_and_prompt_editor_import_from_packaged_layout(
    tmp_path: Path,
    cli_repository: Path,
    packaged_sources: Path,
) -> None:
    """oracle edit と editor 入力境界が packaged layout で正本を参照する。

    根拠: {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    {{work-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_exec.py
    """
    target = _packaged_layout(
        packaged_sources, tmp_path, "acp", "basic", "commons", "oracle"
    )

    result = _run_from_packaged_layout(
        target,
        (
            "import commons.prompt_editor_input as editor_input; "
            "import commons.runtime_editor_input_handoff_mcp as handoff_mcp; "
            "import acp.builder.oracle.edit.launch_exec as edit_module; "
            "from pathlib import Path; "
            "from types import SimpleNamespace; "
            "from acp.builder.oracle.edit.launch_exec import "
            "build_oracle_edit_main_launch_exec_parameter as build_main; "
            "assert edit_module.__all__ == "
            "['build_oracle_edit_main_launch_exec_parameter']; "
            "assert sorted(n for n in vars(edit_module) if not n.startswith('_')) "
            "== sorted(edit_module.__all__); "
            "listed = handoff_mcp._response({"
            "'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list', 'params': {}}); "
            "assert [tool['name'] for tool in listed['result']['tools']] "
            "== ['get_handoff_guide', 'overwrite']; "
            "assert listed['result']['tools'][1]['inputSchema']['required'] "
            "== ['target_id', 'goal', 'instructions', 'background', "
            "'decisions', 'open_questions', 'oracle_references']; "
            "input_path = "
            "editor_input.reserve_prompt_editor_input(Path.cwd()); "
            "skeleton = build_main("
            "editor_input.ORIGINAL_PROMPT_PLACEHOLDER).prompt; "
            "editor_input._select_editor = lambda: ['fake-editor']; "
            "real_subprocess_run = editor_input.subprocess.run; "
            "editor_input.subprocess.run = lambda argv: "
            "(Path(argv[-1]).write_text('oracle \\u3092\\u7de8\\u96c6\\u3059\\u308b', "
            "encoding='utf-8'), "
            "SimpleNamespace(returncode=0))[1]; "
            "editor_input.edit_prompt_editor_input("
            "Path.cwd(), input_path, skeleton); "
            "editor_input.subprocess.run = real_subprocess_run; "
            "original = editor_input.collect_prompt_editor_input("
            "Path.cwd(), input_path); "
            "p = build_main(original); "
            "assert input_path.read_text(encoding='utf-8') == "
            "'oracle \\u3092\\u7de8\\u96c6\\u3059\\u308b'; "
            "assert p.structured_output_schema_path is None; "
            "assert p.file_access_mode.value == 'pure_oracle_write'; "
            "assert p.enable_document_search_mcp is True; "
            "assert 'oracle \\u3092\\u7de8\\u96c6\\u3059\\u308b' in p.prompt; "
            "assert editor_input.ORIGINAL_PROMPT_PLACEHOLDER not in p.prompt; "
            "assert not list(input_path.parent.glob('*_cmpl.md')); "
            "assert p.agent_call_cwd == Path.cwd(); "
        ),
        tmp_path,
        cmoc_process_cwd=cli_repository,
    )

    assert result.returncode == 0, result.stderr


def test_acp_builder_basic_imports_from_packaged_layout(
    tmp_path: Path, packaged_sources: Path
) -> None:
    """ACP basic の canonical 定義再公開を packaged layout で検証する。

    realization 側の公開 import が oracle 側の型を複製せず同一オブジェクトとして
    再公開し、正本の file access mode を利用できることを確認する。
    根拠: {{work-root}}/oracle/src/oracle/acp_builder/basic.py
    {{work-root}}/oracle/doc/dev_rule/test_rule.md
    """
    target = _packaged_layout(packaged_sources, tmp_path, "acp", "oracle")

    result = _run_from_packaged_layout(
        target,
        (
            "import acp.builder; "
            "from acp.builder.basic import AgentCallParameter, FileAccessMode; "
            "from oracle.acp_builder.basic import AgentCallParameter as Canonical; "
            "assert acp.builder.__all__ == ['basic']; "
            "assert sorted(n for n in vars(acp.builder) if not n.startswith('_')) == ['basic']; "
            "assert acp.builder.basic.AgentCallParameter is Canonical; "
            "assert AgentCallParameter is Canonical; "
            "assert FileAccessMode.READONLY.value == 'readonly'"
        ),
        tmp_path,
        cmoc_process_cwd=tmp_path,
    )

    assert result.returncode == 0, result.stderr


def test_cmoc_config_reexports_only_config_definitions(
    tmp_path: Path, packaged_sources: Path
) -> None:
    """config の公開面が正本の設定定義だけを再公開することを検証する。

    `__all__` と module namespace の両方を確認し、packaged layout で内部実装が
    意図せず公開されないことを確認する。
    根拠: {{work-root}}/oracle/src/oracle/other/cmoc_config.py
    {{work-root}}/oracle/doc/dev_rule/test_rule.md
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
        cmoc_process_cwd=tmp_path,
    )

    assert result.returncode == 0, result.stderr
