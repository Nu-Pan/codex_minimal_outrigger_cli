"""リポジトリ構成の命名規則テスト。"""

from pathlib import Path


def test_legacy_routing_files_do_not_exist() -> None:
    """旧ルーティングファイルは INDEX.md へ統合済みとして残さない。"""
    repo_root = Path(__file__).resolve().parents[1]

    assert not (repo_root / "routing.md").exists()
    assert not (repo_root / "ROUTING.md").exists()
