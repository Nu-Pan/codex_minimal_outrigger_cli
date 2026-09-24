# `fork`

## Summary
- `cmoc realization apply fork` の差分追従 agent call について、oracle file の変更を realization file に反映する prompt と起動パラメータを定義する。

## Read this when
- `realization apply fork` が agent に渡す commit 範囲の扱い、差分の対象判定、作業権限、実行コンテキストや indexing preflight の設定を確認・変更するとき。

## Do not read this when
- CLI の実行開始、commit 範囲の決定、run の join や報告など、コマンドの実行ライフサイクルを調べるときは実行側の実装を読む。
- `realization refactor fork` の変更要約やファイル単位のレビュー・修正用 agent call を調べるときは、その専用 builder を読む。
- 共通 prompt 構築や共有ポリシー自体を調べるときは、それぞれの定義を読む。

## hash
- e3625e501d3af9ba014ed26f875ed628355f29e89c30552980b479f818ff0044
