# `cmoc_config.py`

## Summary
- 開発対象リポジトリごとに変わりうる cmoc の挙動設定を集約し、永続化される設定 JSON の構造と既定値を示す oracle src。
- AI エージェント呼び出しの最大並列数、Codex CLI 向けモデル名・reasoning effort 名の対応、apply fork と review oracle の各ループ上限を扱う。
- Enum 系の値を JSON 保存時に value 化すること、設定ファイルは初期化処理で生成・同期され人間が編集することを確認する入口になる。

## Read this when
- 開発対象リポジトリ単位で保持される cmoc 設定の責務、永続化先、生成・同期・人間編集の扱いを確認したいとき。
- Codex CLI に渡すモデル名や reasoning effort 名を、cmoc 内部のモデル分類・推論努力度からどう対応させるかを確認したいとき。
- AI エージェント呼び出し、apply fork、review oracle の並列数やループ回数の既定値を仕様根拠として確認したいとき。
- 設定 JSON に保存する際、Enum 系インスタンスをどのような形に変換する前提かを確認したいとき。

## Do not read this when
- パスキーワードやルートディレクトリ概念の定義だけを確認したいとき。
- 設定ファイルを実際に読み書きする処理、JSON 変換処理、初期化サブコマンドの実装手順を探しているとき。
- apply fork や review oracle の具体的なアルゴリズム、所見の形式、サブコマンドの入出力仕様を確認したいとき。
- リポジトリに依存しない固定仕様、テスト方針、または oracle file と realization file の一般的な関係を確認したいとき。

## hash
- ccea2a3965b4022ccab0f635678dd917808b71820431e9e91f76f699315338f6
