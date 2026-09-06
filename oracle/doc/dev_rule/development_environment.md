# cmoc 開発環境

## 責務境界

- この文書は、Python 環境の新規構築、依存関係の追加、および pip の操作に必要な条件を定める
- 構築済み環境での既存 test と品質検査の手順は、`{{cmoc-root}}/oracle/doc/dev_rule/test_execution.md` を正本とする。対象は、検査の選択・実行・完了判定・報告とする
- 通常の test 実行だけを理由として、この文書を事前に読む必要はない

## 基本環境

- WSL2 Ubuntu 24.04 on Windows 11
- vscode (with Remote Development Extension)
- `{{cmoc-root}}/codex_minimal_outrigger_cli.code-workspace` を vscode で開いた環境
- Codex CLI が利用可能

## ファイルエンコード

- 原則として UTF-8 BOM なしで統一する
- ツールの都合による場合に限り、例外を許容する

## ファイル・ディレクトリ名の命名規則

- oracle に指定がある場合は、その指定に従う
    - 例：`INDEX.md`
- 一般的な標準仕様・規約などで定められている場合は、それに従う
    - 例：`*.code-workspace`, `AGENTS.md`
- 指定がない場合は、スネークケースとする
    - 例：`sub_commands`

## Python 実行環境

- python3>=3.12.3 を前提とする
- システムワイドの `python3` の直接使用は原則禁止（例外として venv 作成時のみ使用可）
- Python 仮想環境として `{{cmoc-root}}/.venv` を使う
- Python インタプリタは `{{cmoc-root}}/.venv/bin/python` を使う
- pip は `{{cmoc-root}}/.venv/bin/python -m pip` を使う

## 仮想環境の管理

### `{{cmoc-root}}/.venv` の新規作成

```bash
cd "{{cmoc-root}}"
/usr/bin/python3 -m venv .venv
```

### `{{cmoc-root}}/.venv` へのパッケージインストール

権限昇格付きでの実行が必要なら、ユーザーに依頼すること。

```bash
cd "{{cmoc-root}}"
./.venv/bin/python -m pip install -e '.[dev]'
```

### `{{cmoc-root}}/.venv` への新規パッケージ追加

- `pyproject.toml` に依存関係を追記する
- その後、上記のインストール手順を実行する
