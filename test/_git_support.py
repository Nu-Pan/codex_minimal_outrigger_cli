import subprocess
from pathlib import Path

SESSION_ID = "sess_000000_2026-09-29_15-04"
RUN_ID = "run_000000_2026-09-29_15-04"
SESSION_BRANCH = f"cmoc/session/{SESSION_ID}"
RUN_BRANCH = f"cmoc/run/{SESSION_ID}/{RUN_ID}"


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """テスト repository で git command を実行し、command error なら失敗させる。"""
    return subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=True
    )


def current_branch(root: Path) -> str:
    """git-state assertion 用に checkout 済み branch 名を返す。"""
    return run_git(root, "branch", "--show-current").stdout.strip()


def init_repo(root: Path) -> None:
    """既存 directory に user Git 設定から隔離した test repository を初期化する。"""
    # 利用者の Git template に含まれる hook・設定を持ち込まない。
    run_git(root, "init", "--template=/dev/null")
    # Git が生成した配置設定は保ち、fixture の固定設定だけを一度に追記する。
    with (root / ".git" / "config").open("a", encoding="utf-8") as config:
        config.write(
            "\n[user]\n"
            "\temail = cmoc@example.invalid\n"
            "\tname = cmoc test\n"
            "[commit]\n"
            "\tgpgsign = false\n"
            "[core]\n"
            "\thooksPath = /dev/null\n"
            "\texcludesFile = /dev/null\n"
        )


def make_repo(tmp_path: Path) -> Path:
    """cmoc CLI test が対象にできる最小の commit 済み repository を作る。"""
    root = tmp_path / "repo"
    root.mkdir()
    init_repo(root)
    (root / "README.md").write_text("# repo\n")
    (root / "oracle").mkdir()
    (root / "oracle" / "spec.md").write_text("# spec\n")
    run_git(root, "add", ".")
    run_git(root, "commit", "-m", "initial")
    return root


def add_tracked_ignored_oracle_file(root: Path) -> None:
    """repository rule では ignore されるが追跡対象でもある oracle file を作る。"""
    (root / ".gitignore").write_text("oracle/ignored.md\n")
    (root / "oracle" / "ignored.md").write_text("# ignored\n")
    run_git(root, "add", "-f", ".gitignore", "oracle/ignored.md")
    run_git(root, "commit", "-m", "add ignored oracle")
