"""リポジトリ構成の命名規則テスト。"""

from pathlib import Path


def test_legacy_routing_files_do_not_exist() -> None:
    """旧ルーティングファイルは INDEX.md へ統合済みとして残さない。"""
    repo_root = Path(__file__).resolve().parents[1]

    assert not (repo_root / "routing.md").exists()
    assert not (repo_root / "ROUTING.md").exists()


def test_subcommand_bodies_use_hierarchical_importable_layout() -> None:
    """サブコマンド本体は設計ルールどおり階層化した import 可能モジュールに置く。"""
    repo_root = Path(__file__).resolve().parents[1]
    sub_commands = repo_root / "src" / "sub_commands"

    expected_paths = [
        sub_commands / "apply" / "fork.py",
        sub_commands / "apply" / "join.py",
        sub_commands / "apply" / "abandon.py",
        sub_commands / "session" / "fork.py",
        sub_commands / "session" / "join.py",
        sub_commands / "session" / "abandon.py",
        sub_commands / "eval_oracles.py",
    ]
    legacy_paths = [
        sub_commands / "apply.py",
        sub_commands / "apply_join.py",
        sub_commands / "apply_abandon.py",
        sub_commands / "session_fork.py",
        sub_commands / "session_join.py",
        sub_commands / "session_abandon.py",
        sub_commands / "eval-oracles.py",
    ]

    assert all(path.exists() for path in expected_paths)
    assert not any(path.exists() for path in legacy_paths)
