# cmoc 開発環境

## 基本環境

- WSL2 Ubuntu 24.04 on Windows 11
- vscode (with Remote Development Extension)
- `{{cmoc-root}}/codex_minimal_outrigger_cli.code-workspace` を vscode で開いた環境
- Codex CLI が利用可能

## ファイルエンコード

- 原則として UTF-8 BOM なしで統一する
- ツール都合がある場合のみ例外を許容する

## ファイル・ディレクトリ名の命名規則

- oracle で指定されている場合はそちらに従う
    - e.g. `INDEX.md`
- 世間一般の標準的な仕様・規約などで決まっている場合はそちらに従う
    - e.g. `*.code-workspace`, `AGENTS.md`
- 何の指定も無い場合はスネークケースとする
    - e.g. `sub_commands`

## Python 実行環境

- python3>=3.12.3 を前提とする
- システムワイドの `python3` の直接使用は原則禁止（例外として venv 作成時のみ使用可）
- Python 仮想環境として `{{cmoc-root}}/.venv` を使う
- Python インタプリタは `{{cmoc-root}}/.venv/bin/python` を使う
- pip は `{{cmoc-root}}/.venv/bin/python -m pip` を使う

## 自己開発手順

cmoc 自己開発用 Python 環境の確認、仮想環境の作成、開発用依存関係の導入、および検証コマンドは `$cmoc-self-development-validation` を正本とする。
