"""packaged layout と import 境界を検証する。

分割根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path


def _run_from_packaged_layout(
    target: Path, code: str, tmp_path: Path
) -> subprocess.CompletedProcess[str]:
    """隔離した packaged layout で Python コードを実行する。

    `-S` と `PYTHONNOUSERSITE` で外部 site-packages の影響を除き、
    `PYTHONPATH` でコピーした tree だけを import 対象にする。空の `.git` は
    作業ルート探索が一時ディレクトリ外へ逃げないように置く。HOME も一時
    ディレクトリ内へ向け、実行者の設定や認証情報を持ち込まない。
    根拠: {{work-root}}/oracle/doc/dev_rule/coding_rule.md
    {{work-root}}/oracle/doc/dev_rule/test_rule.md
    """
    work = tmp_path / "work"
    work.mkdir(exist_ok=True)
    (work / ".git").mkdir()
    home = tmp_path / "home"
    home.mkdir()
    return subprocess.run(
        [sys.executable, "-S", "-c", code],
        cwd=work,
        env={
            **os.environ,
            "HOME": str(home),
            "PYTHONPATH": str(target),
            "PYTHONNOUSERSITE": "1",
        },
        text=True,
        capture_output=True,
    )


def test_oracle_review_enumerate_builder_imports_from_packaged_layout(
    tmp_path: Path,
) -> None:
    """oracle review builder の packaged import と出力契約を検証する。

    正本 builder が packaged layout でも schema と prompt を参照し、期待する
    parameter を生成できることを確認する。
    根拠: {{work-root}}/oracle/src/oracle/acp_builder/oracle/review/enumerate_finding.py
    {{work-root}}/oracle/src/oracle/acp_builder/oracle/review/enumerate_finding.json
    {{work-root}}/oracle/doc/dev_rule/test_rule.md
    """
    root = Path(__file__).parents[1]
    pyproject = tomllib.loads((root / "pyproject.toml").read_text())
    setuptools_config = pyproject["tool"]["setuptools"]
    assert "oracle" not in setuptools_config["py-modules"]
    assert setuptools_config["package-dir"]["oracle"] == "oracle/src/oracle"
    assert "oracle/src" in setuptools_config["packages"]["find"]["where"]

    target = tmp_path / "site"
    shutil.copytree(root / "src" / "acp", target / "acp")
    shutil.copytree(root / "src" / "basic", target / "basic")
    shutil.copytree(root / "oracle" / "src" / "oracle", target / "oracle")

    result = _run_from_packaged_layout(
        target,
        (
            "import json; "
            "from pathlib import Path; "
            "from acp.builder.oracle.review.enumerate_finding import "
            "build_oracle_review_enumerate_finding_parameter as build; "
            "p = build(Path('{{work-root}}/oracle/spec.md'), '[]'); "
            "assert p.structured_output_schema_path.name == 'enumerate_finding.json'; "
            "schema = json.loads(p.structured_output_schema_path.read_text()); "
            "assert schema['required'] == ['findings']; "
            "assert '# oracle review standard' in p.prompt"
        ),
        tmp_path,
    )

    assert result.returncode == 0, result.stderr


def test_oracle_edit_builder_imports_from_packaged_layout(tmp_path: Path) -> None:
    """oracle edit TUI adapter が packaged layout で完全 prompt を保存する。"""
    root = Path(__file__).parents[1]
    target = tmp_path / "site"
    for package in ("acp", "basic", "commons"):
        shutil.copytree(root / "src" / package, target / package)
    shutil.copytree(root / "oracle" / "src" / "oracle", target / "oracle")

    result = _run_from_packaged_layout(
        target,
        (
            "from pathlib import Path; "
            "from acp.builder.oracle.edit.launch_tui import "
            "build_oracle_edit_launch_tui_parameter as build; "
            "log = Path.cwd() / '.cmoc/gu/ar/log/editor_input/test_cmpl.md'; "
            "log.parent.mkdir(parents=True); "
            "p = build('test', 'oracle を編集する'); "
            "assert p.structured_output_schema_path is None; "
            "assert p.file_access_mode.value == 'pure_oracle_write'; "
            "assert p.run_indexing_preflight; "
            "assert p.prompt == f'{log} を読んで、その指示に従って下さい'; "
            "assert 'oracle を編集する' in log.read_text(); "
            "assert p.cwd == Path.cwd()"
        ),
        tmp_path,
    )

    assert result.returncode == 0, result.stderr


def test_acp_builder_basic_imports_from_packaged_layout(tmp_path: Path) -> None:
    """ACP basic の canonical 定義再公開を packaged layout で検証する。

    realization 側の公開 import が oracle 側の型を複製せず同一オブジェクトとして
    再公開し、正本の enum 値を利用できることを確認する。
    根拠: {{work-root}}/oracle/src/oracle/acp_builder/basic.py
    {{work-root}}/oracle/doc/dev_rule/test_rule.md
    """
    root = Path(__file__).parents[1]
    target = tmp_path / "site"
    shutil.copytree(root / "src" / "acp", target / "acp")
    shutil.copytree(root / "oracle" / "src" / "oracle", target / "oracle")

    result = _run_from_packaged_layout(
        target,
        (
            "import acp.builder; "
            "from acp.builder.basic import AgentCallParameter, ModelClass; "
            "from oracle.acp_builder.basic import AgentCallParameter as Canonical; "
            "assert acp.builder.basic.AgentCallParameter is Canonical; "
            "assert AgentCallParameter is Canonical; "
            "assert ModelClass.MAINSTREAM.value == 'mainstream'"
        ),
        tmp_path,
    )

    assert result.returncode == 0, result.stderr


def test_cmoc_config_reexports_only_config_definitions(tmp_path: Path) -> None:
    """config の公開面が正本の設定定義だけを再公開することを検証する。

    `__all__` と module namespace の両方を確認し、packaged layout で内部実装が
    意図せず公開されないことを確認する。
    根拠: {{work-root}}/oracle/src/oracle/other/cmoc_config.py
    {{work-root}}/oracle/doc/dev_rule/test_rule.md
    """
    root = Path(__file__).parents[1]
    target = tmp_path / "site"
    shutil.copytree(root / "src" / "config", target / "config")
    shutil.copytree(root / "oracle" / "src" / "oracle", target / "oracle")

    result = _run_from_packaged_layout(
        target,
        (
            "import config.cmoc_config as c; "
            "expected = ['CmocConfig', 'CmocConfigCodex', "
            "'CmocConfigOracleReview', 'CodexModelSpec']; "
            "assert c.__all__ == expected; "
            "assert sorted(n for n in vars(c) if not n.startswith('_')) == expected"
        ),
        tmp_path,
    )

    assert result.returncode == 0, result.stderr
