# cmot 開発環境

## 基本環境

- WSL2 Ubuntu 24.04 on Windows 11
- vscode (with Remote Development Extension)
- `<cmot-root>/codex_minimal_outrigger.code-workspace` を vscode で開いた環境
- Codex CLI が利用可能

## ファイルエンコード

- 原則として UTF-8 BOM なしで統一する
- ツール都合がある場合のみ例外を許容する

## Python 実行環境

- python3>=3.12.3 を前提とする
- システムワイドの `python3` の直接使用は原則禁止（例外として venv 作成時のみ使用可）
- Python 仮想環境として `<cmot-root>/.venv` を使う
- Python インタプリタは `<cmot-root>/.venv/bin/python` を使う
- pip は `<cmot-root>/.venv/bin/python -m pip` を使う

## 仮想環境の管理

### `<cmot-root>/.venv` の新規作成

```bash
cd "<cmot-root>"
/usr/bin/python3 -m venv .venv
```

### `<cmot-root>/.venv` へのパッケージインストール

権限昇格付きでの実行が必要なら、ユーザーに依頼すること。

```bash
cd "<cmot-root>"
./.venv/bin/python -m pip install -e .
```

### `<cmot-root>/.venv` への新規パッケージ追加

- `pyproject.toml` に依存関係を追記する
- その後、上記のインストール手順を実行する
