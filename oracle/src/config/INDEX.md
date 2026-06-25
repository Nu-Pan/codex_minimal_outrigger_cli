# `cmoc_config.py`

## Summary
- 開発対象リポジトリごとに変わりうる cmoc の挙動設定を集約し、永続化される設定オブジェクトの構成と既定値を定義する。
- 設定は全体設定、Codex CLI 向け設定、apply fork 向け設定、review oracle 向け設定に分かれ、Enum 系の値は JSON 保存時に value 化される前提を持つ。

## Read this when
- リポジトリ単位で保存される cmoc 設定の項目、既定値、入れ子構造を確認したいとき。
- cmoc init が生成・同期する設定ファイルの内容や、人間が編集する設定の正本仕様を確認したいとき。
- AI エージェント呼び出しの並列数、Codex CLI の model/reasoning effort 対応、apply fork の処理ファイル数上限、review oracle の各ループ回数上限を扱う変更をするとき。

## Do not read this when
- 実行時に設定ファイルを読み書きする具体的な入出力処理、JSON 変換処理、CLI コマンド実装だけを確認したいとき。
- パス語彙やルートディレクトリの定義を確認したいとき。
- apply fork や review oracle のアルゴリズム本体、所見生成・マージ・検証の詳細挙動を確認したいとき。

## hash
- 235cc8f4960fade374f47054db3640086c13ec211e0b2df4ef08fe5d61cb06fd
