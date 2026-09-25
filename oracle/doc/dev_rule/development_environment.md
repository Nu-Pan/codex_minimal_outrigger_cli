# cmoc 開発環境

## 責務境界

本書は、Python 環境と文書検索資材の準備、依存関係の追加、および pip の操作に必要な条件を定める。

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

セットアップは推論 runtime、ベクトル演算依存、モデルと tokenizer を取得・構築し、検証済みの固定資材を通常検索へ提供する責務を持つ。通常の検索・明示同期では download/build を行わず、資材不足・不一致は明示的に失敗させる。

初期採用する Node、node-llama-cpp、llama.cpp、sqlite-vec、およびモデルの repository・revision・filename・checksum・pooling 等の正確な識別情報は、`{{cmoc-root}}/oracle/src/oracle/other/document_search.py` の `INITIAL_SEARCH_MATERIALS` を唯一の所有者とする。モデル入力と raw 採点 guard の契約は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「初期方式と推論の失敗」に従う。

セットアップは推移的依存を含む完全な lock と native 配布物の版・integrity を固定し、取得したモデルの checksum を照合する。runtime 更新時は資材定義と lock を整合させ、互換検査を行う。検索開始時も資材 identity を検証し、変更検出後に未検証のモデルを使用しない。取得済み資材は検索 worker から変更させない。

配置と共有単位は、同文書の「identity と保存先」に従う。共有資材を作る前に、セットアップが cmoc-root 側の管理領域へ `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「管理領域の非追跡保証」と同じ検証・修復を適用する。対象 repository の doctor が cmoc installation の設定や依存を構築する責務は持たない。

初期実装用の CPU native 配布物を固定して再構築できるようにする。GPU や別 OS での動作を、CPU の PoC から推定して検証済みとしない。tuning の初期値確定とクリーンな再構築を含む受入条件は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「実現性の根拠と製品受入条件」を参照する。
