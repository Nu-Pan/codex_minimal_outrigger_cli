"""packaged layout と import 境界を検証する。

分割根拠: <work-root>/oracle/src/oracle/prompt_builder/parts/realization_standard.py
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
    work = tmp_path / "work"
    work.mkdir(exist_ok=True)
    return subprocess.run(
        [sys.executable, "-S", "-c", code],
        cwd=work,
        env={**os.environ, "PYTHONPATH": str(target), "PYTHONNOUSERSITE": "1"},
        text=True,
        capture_output=True,
    )


def test_review_oracle_enumerate_builder_imports_from_packaged_layout(
    tmp_path: Path,
) -> None:
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
            "from acp.builder.review.oracle.enumerate_finding import "
            "build_review_oracle_enumerate_finding_parameter as build; "
            "p = build(Path('<work-root>/oracle/spec.md'), '[]'); "
            "assert p.structured_output_schema_path.name == 'enumerate_finding.json'; "
            "schema = json.loads(p.structured_output_schema_path.read_text()); "
            "assert schema['required'] == ['findings']; "
            "assert '# review oracle standard' in p.prompt"
        ),
        tmp_path,
    )

    assert result.returncode == 0, result.stderr


def test_acp_builder_basic_imports_from_packaged_layout(tmp_path: Path) -> None:
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
    root = Path(__file__).parents[1]
    target = tmp_path / "site"
    shutil.copytree(root / "src" / "config", target / "config")
    shutil.copytree(root / "oracle" / "src" / "oracle", target / "oracle")

    result = _run_from_packaged_layout(
        target,
        (
            "import config.cmoc_config as c; "
            "expected = ['CmocConfig', 'CmocConfigApplyFork', "
            "'CmocConfigCodex', 'CmocConfigReviewOracle']; "
            "assert c.__all__ == expected; "
            "assert sorted(n for n in vars(c) if not n.startswith('_')) == expected"
        ),
        tmp_path,
    )

    assert result.returncode == 0, result.stderr
