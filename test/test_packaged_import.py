"""packaged layout と import 境界を検証する。

分割根拠: <work-root>/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path


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

    work = tmp_path / "work"
    (work / ".git").mkdir(parents=True)
    result = subprocess.run(
        [
            sys.executable,
            "-c",
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
        ],
        cwd=work,
        env={**os.environ, "PYTHONPATH": str(target), "PYTHONNOUSERSITE": "1"},
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
