# `fork`

## Summary
- `cmoc apply fork` のレビュー・修正・レポート生成で使う AI 呼び出し仕様と、その入出力 schema をまとめる領域。
- fork 適用に伴う差分要約、所見列挙、所見対応修正の各段階について、prompt に渡す前提・制約・モデル設定・Structured Output との接続を確認する入口となる。

## Read this when
- `cmoc apply fork` で、適用後差分を人間向けに要約する処理、ファイル単位の所見を列挙する処理、または所見に基づく修正担当エージェント呼び出しを実装・確認するとき。
- fork 適用後のレビュー結果や変更要約を、機械処理可能な JSON schema と AI 呼び出し prompt のどちらの観点から確認すべきかを切り分けたいとき。
- oracle file、realization file、standard、git diff、所見本文を `cmoc apply fork` の各エージェントへどの権限・制約で渡すかを確認したいとき。

## Do not read this when
- `cmoc apply fork` の CLI 解析、ブランチ作成、実際の差分取得、git 操作、fork 適用フローそのものを調べたいとき。
- oracle file と realization file の基本定義、path keyword、standard 本文、または共通 prompt 構築処理の一般仕様を確認したいとき。
- 個別ファイルのパッチ内容や、検出された所見を受けた具体的な realization file の修正実装を調べたいとき。

## hash
- 37d5d7e3f6d250ba88303e72a7cf7c5a16ef920689e6a458d32e3002af6e692f
