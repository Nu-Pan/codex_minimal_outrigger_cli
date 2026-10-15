"""同じ Codex home と固定 session ID の process 間排他を検証する。"""

import os
import subprocess
import sys
from contextlib import closing
from pathlib import Path

import pytest

from commons.runtime_codex_session import CodexSessionLease
from commons.runtime_errors import CmocError

SESSION_ID = "019efe07-4886-7423-b252-625febbe31eb"


def test_session_exclusion_applies_across_processes(tmp_path):
    home = tmp_path / "codex_home"
    home.mkdir()
    script = """
import sys
from pathlib import Path
from commons.runtime_codex_session import CodexSessionLease
from commons.runtime_errors import CmocError
lease = CodexSessionLease(Path(sys.argv[1]))
try:
    lease.acquire(sys.argv[2])
except CmocError:
    sys.exit(23)
finally:
    lease.close()
"""
    environment = {
        **os.environ,
        "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src"),
    }

    def attempt():
        return subprocess.run(
            [sys.executable, "-c", script, str(home), SESSION_ID],
            cwd=tmp_path,
            env=environment,
            capture_output=True,
            text=True,
            timeout=10,
        )

    with closing(CodexSessionLease(home)) as lease:
        lease.acquire(SESSION_ID)
        assert attempt().returncode == 23
    result = attempt()
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("relationship", ["alias", "other_home", "other_session"])
def test_session_exclusion_uses_resolved_home_and_fixed_id(tmp_path, relationship):
    home = tmp_path / "codex_home"
    home.mkdir()
    candidate_home = home
    session_id = SESSION_ID
    if relationship == "alias":
        candidate_home = tmp_path / "alias"
        candidate_home.symlink_to(home, target_is_directory=True)
    elif relationship == "other_home":
        candidate_home = tmp_path / "other_home"
        candidate_home.mkdir()
    else:
        session_id = "019efe07-4886-7423-b252-625febbe31ec"
    with (
        closing(CodexSessionLease(home)) as lease,
        closing(CodexSessionLease(candidate_home)) as contender,
    ):
        lease.acquire(SESSION_ID)
        if relationship == "alias":
            with pytest.raises(CmocError, match="使用中"):
                contender.acquire(session_id)
        else:
            contender.acquire(session_id)
