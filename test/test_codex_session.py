"""同じ Codex home と固定 session ID の process 間排他を検証する。"""

import os
import select
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
from contextlib import closing
from pathlib import Path
from commons.runtime_codex_session import CodexSessionLease

with closing(CodexSessionLease(Path(sys.argv[1]))) as lease:
    lease.acquire(sys.argv[2])
    print("ready", flush=True)
    sys.stdin.read()
"""
    environment = {
        **os.environ,
        "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src"),
    }

    # 子を保持側にし、競合拒否と解放後の再取得で Python の起動を共用する。
    # lease とその依存は標準ライブラリだけを使うため、site-packages の初期化を省く。
    with subprocess.Popen(
        [sys.executable, "-S", "-c", script, str(home), SESSION_ID],
        cwd=tmp_path,
        env=environment,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as holder:
        try:
            assert select.select([holder.stdout], [], [], 10)[0], (
                "lease holder timed out"
            )
            assert holder.stdout.readline() == "ready\n"
            with closing(CodexSessionLease(home)) as contender:
                with pytest.raises(CmocError, match="使用中"):
                    contender.acquire(SESSION_ID)
            # stdin の EOF で解放させ、子の正常終了も確認する。
            _, stderr = holder.communicate(timeout=10)
            assert holder.returncode == 0, stderr
        finally:
            if holder.poll() is None:
                holder.kill()
                holder.wait()
    with closing(CodexSessionLease(home)) as lease:
        lease.acquire(SESSION_ID)


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
