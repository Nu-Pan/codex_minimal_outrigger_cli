# `cmoc_config.py`

## Summary
- 開発対象リポジトリごとに変わりうる cmoc の挙動設定を集約するデータ構造を定義している。
- 設定は永続化される JSON の内容に対応し、Enum 系の値化、初期化時の生成・同期、人間による編集を前提にした設定項目の入口になる。
- AI エージェント呼び出しの並列数、Codex CLI 向けのモデル名・reasoning effort 名の対応、apply fork と review oracle のループ上限などの既定値を扱う。

## Read this when
- リポジトリごとの cmoc 設定項目、既定値、設定データ構造を確認または変更したいとき。
- Codex CLI に渡すモデル種別や reasoning effort の対応表を確認または変更したいとき。
- apply fork や review oracle の処理件数・ループ回数など、サブコマンドの挙動調整値を確認または変更したいとき。
- 永続化される設定 JSON と Python 側の設定クラスとの対応を追う必要があるとき。

## Do not read this when
- 設定ファイルの読み書き、JSON 変換、同期処理そのものの実装を探しているとき。
- モデル種別や reasoning effort の概念定義そのものを確認したいとき。
- 各サブコマンドの実行ロジックやレビュー所見の生成・マージ・検証処理を確認したいとき。
- cmoc のパス語彙、oracle file、realization file などの基本概念を調べたいとき。

## hash
- d102ed1e07a4c9a7241b4e731ec3783b392d8dfb274e702c452dbf9c6b387dc6
