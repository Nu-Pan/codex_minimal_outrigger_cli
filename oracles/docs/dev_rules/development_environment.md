# cmoc 開発環境

## 基本環境

- WSL2 Ubuntu 24.04 on Windows 11
- vscode (with Remote Development Extension)
- `<cmoc-root>/codex_minimal_outrigger_cli.code-workspace` を vscode で開いた環境
- Codex CLI が利用可能

## ファイルエンコード

- 原則として UTF-8 BOM なしで統一する
- ツール都合がある場合のみ例外を許容する

## ファイル・ディレクトリ名の命名規則

- oracles で指定されている場合はそちらに従う
    - e.g. `INDEX.md`
- 世間一般の標準的な仕様・規約などで決まっている場合はそちらに従う
    - e.g. `*.code-workspace`, `AGENTS.md`
- 何の指定も無い場合はスネークケースとする
    - e.g. `sub_commands`

## Python 実行環境

- python3>=3.12.3 を前提とする
- システムワイドの `python3` の直接使用は原則禁止（例外として venv 作成時のみ使用可）
- Python 仮想環境として `<cmoc-root>/.venv` を使う
- Python インタプリタは `<cmoc-root>/.venv/bin/python` を使う
- pip は `<cmoc-root>/.venv/bin/python -m pip` を使う

## 仮想環境の管理

### `<cmoc-root>/.venv` の新規作成

```bash
cd "<cmoc-root>"
/usr/bin/python3 -m venv .venv
```

### `<cmoc-root>/.venv` へのパッケージインストール

権限昇格付きでの実行が必要なら、ユーザーに依頼すること。

```bash
cd "<cmoc-root>"
./.venv/bin/python -m pip install -e .
```

### `<cmoc-root>/.venv` への新規パッケージ追加

- `pyproject.toml` に依存関係を追記する
- その後、上記のインストール手順を実行する
