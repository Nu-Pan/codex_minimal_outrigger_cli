# `cmoc_config.py`

## Summary
- 開発対象リポジトリごとに変わりうる cmoc の設定を集約する dataclass 群を定義する。
- AI エージェント呼び出しの並列数、Codex CLI 向けのモデル名・reasoning effort 対応、apply fork と review oracle のループ上限など、永続化される設定値の既定値を扱う。
- 設定は `<repo-root>/.cmoc/config.json` に保存され、人間が編集する前提の設定面に対応する。

## Read this when
- cmoc のリポジトリ別設定項目や既定値を確認・変更したいとき。
- `cmoc init` が生成・同期する設定ファイルに含める値や、Enum 系の値を JSON 保存用にどう扱うかを確認したいとき。
- Codex CLI に渡すモデル名・reasoning effort 名の対応、AI 呼び出し並列数、`cmoc apply fork` や `cmoc review oracle` の処理回数上限を調整したいとき。

## Do not read this when
- CLI 引数やサブコマンドの構文、実行時の入出力フローを調べたいだけのとき。
- 設定ファイルの実際の読み書き処理、JSON 変換処理、`.cmoc` 配下のパス解決処理を調べたいとき。
- oracle file や realization file の概念、パスキーワードの定義、INDEX.md 生成ルールそのものを確認したいとき。

## hash
- 235cc8f4960fade374f47054db3640086c13ec211e0b2df4ef08fe5d61cb06fd
