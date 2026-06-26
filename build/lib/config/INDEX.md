# `cmoc_config.py`

## Summary
- cmoc のリポジトリ単位の設定値を表す dataclass 群を定義し、AI 呼び出し並列数、Codex CLI 向けのモデル・reasoning effort 対応、apply fork と review oracle のループ上限などを集約する。
- 設定はリポジトリごとに永続化され、人間が編集する設定 JSON として扱われる前提のデフォルト値と構造を確認する入口になる。

## Read this when
- リポジトリごとの cmoc 設定項目、既定値、設定クラスの構造を確認・変更したいとき。
- Codex CLI に渡すモデル名や reasoning effort 名と、内部のモデル分類・推論努力分類との対応を調べたいとき。
- apply fork や review oracle の処理件数・ループ回数など、サブコマンド別の挙動予算に関わる設定を確認したいとき。
- 設定 JSON へ保存される enum 系の値や、初期化時に生成・同期される設定の意味を把握したいとき。

## Do not read this when
- 設定ファイルの読み書き、JSON 変換、初期化時の生成・同期処理そのものを調べたいとき。
- 個々のサブコマンドの実行フロー、apply fork の実処理、review oracle の所見列挙・マージ・検証ロジックを追いたいとき。
- モデル分類や reasoning effort 分類そのものの定義を確認したいとき。
- ユーザー向け CLI 引数やコマンド体系の定義を調べたいとき。

## hash
- 235cc8f4960fade374f47054db3640086c13ec211e0b2df4ef08fe5d61cb06fd
