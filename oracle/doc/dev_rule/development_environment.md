# cmoc 開発環境

## 責務境界

本書は、Python 環境の準備、依存関係の追加、および pip の操作に必要な条件を定め、検索用コンポーネントを準備する公開入口へ案内する。

構築済み環境での既存 test と品質検査の選択・実行・完了判定・報告は、`{{cmoc-root}}/oracle/doc/dev_rule/test_execution.md` の「cmoc の test・品質検査実行手順」を正本とする。通常の test 実行だけを理由として、本書を事前に読む必要はない。

## 基本環境

- WSL2 Ubuntu 24.04 on Windows 11
- VS Code (with Remote Development Extension)
- `{{cmoc-root}}/codex_minimal_outrigger_cli.code-workspace` を VS Code で開いた環境
- Codex CLI が利用可能

## ファイルエンコード

- 原則として UTF-8 BOM なしで統一する
- ツールの都合による場合に限り、例外を許容する

## ファイル・ディレクトリ名の命名規則

- oracle に指定がある場合は、その指定に従う
    - 例：`config.json`
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

## 文書検索のセットアップ

検索用コンポーネントのセットアップは、処理対象の work-root で `cmoc doctor` を実行して行う。利用者に別途の検索専用セットアップ操作を要求しない。doctor を起動するための事前環境と、doctor が準備・修復する範囲は、`{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「共通実行環境の検証」「検索用コンポーネントの準備と検査」に従う。

固定したコンポーネントの正確な定義への委譲、lock・native 配布物・モデルの照合、runtime の互換性、および実モデルの検証は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「初期方式と推論の失敗」「検索用コンポーネントの検証契約」を正本とする。開発で runtime を更新する際も、コンポーネントの定義と lock を整合させ、同じ検証を行う。

配置と共有単位は、同文書の「identity と保存先」、クリーンな再構築を含む受入条件と後続の性能調整は「実現性の根拠と製品受入条件」を参照する。暫定既定値の採用は同文書の「設定と未確定事項」に従う。
