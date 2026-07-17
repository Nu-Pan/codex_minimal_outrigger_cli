import subprocess
from pathlib import Path


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """テスト repository で git command を実行し、command error なら失敗させる。"""
    return subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=True
    )


def current_branch(root: Path) -> str:
    """git-state assertion 用に checkout 済み branch 名を返す。"""
    return run_git(root, "branch", "--show-current").stdout.strip()


def make_repo(tmp_path: Path) -> Path:
    """cmoc CLI test が対象にできる最小の commit 済み repository を作る。"""
    root = tmp_path / "repo"
    root.mkdir()
    run_git(root, "init")
    run_git(root, "config", "user.email", "cmoc@example.invalid")
    run_git(root, "config", "user.name", "cmoc test")
    # {{work-root}}/oracle/doc/dev_rule/test_rule.md: cmoc の制御ロジック実行前に、
    # テストリポジトリが user Git signing や hook 設定へ依存しないようにする。
    run_git(root, "config", "commit.gpgsign", "false")
    run_git(root, "config", "core.hooksPath", "/dev/null")
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
