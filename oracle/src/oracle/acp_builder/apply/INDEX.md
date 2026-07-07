# `fork`

## Summary
- `cmoc apply fork` で使う agent call parameter と Structured Output schema のうち、fork 適用後のレビュー、所見列挙、所見対応、変更要約に関わる正本仕様断片をまとめるディレクトリ。
- 差分から人間向け変更要約を生成する prompt、ファイル単位の所見リストアップ prompt、検出所見を修正 agent に渡す prompt、それらの出力契約を確認する入口になる。

## Read this when
- `cmoc apply fork` の fork 適用後に、差分要約、実装レビュー所見、所見対応作業をどの agent call parameter と schema で扱うか確認するとき。
- 変更要約や所見列挙の Structured Output schema と、それを使う prompt 側の対応関係を確認したいとき。
- 所見を人間向けレビュー結果として報告し、その後 realization file 修正 agent に渡す流れの正本仕様断片を探すとき。

## Do not read this when
- `cmoc apply fork` の fork 作成、branch 操作、diff 取得、レポート保存、CLI 引数処理など、agent call parameter や出力契約以外の実行制御を調べたいとき。
- apply review standard、oracle standard、realization standard そのものの内容を確認したいとき。
- 共通の prompt builder、path placeholder 解決、markdown rendering、agent call parameter の汎用データ構造の実装を調べたいとき。

## hash
- 34dd7511fe97a86b45ffb37cb7feb9be91c52b9e6e420c674df2e08a9e5d4c18
