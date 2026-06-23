# `fork`

## Summary
- `cmoc apply fork` のレビュー・修正・レポート生成に使う AI 呼び出し契約と、その入出力 schema をまとめる領域。
- 適用用ブランチ上の差分要約、ファイル単位の所見列挙、所見リストの整理、所見に基づく realization file 修正用 prompt など、fork 適用後の人間向け確認と実装修正支援に関わる仕様断片への入口になる。
- 実際の fork 作成・ブランチ操作・差分適用そのものではなく、apply fork の後段で AI agent に渡す役割、制約、参照標準、出力 schema の接続を扱う。

## Read this when
- `cmoc apply fork` のレビュー結果から所見を列挙・精査し、realization file 修正へつなげる AI 呼び出し条件を確認したいとき。
- fork 適用後の差分を、人間が読める変更カテゴリ別サマリーとして生成する prompt や出力契約を確認・変更したいとき。
- 所見リストや変更要約の Structured Output schema と、それを使う agent 呼び出しとの対応を確認したいとき。
- apply fork 系の agent に渡す oracle standard、realization standard、apply review standard、ファイルアクセス制約、model class、reasoning effort の正本値を調べたいとき。

## Do not read this when
- `cmoc apply fork` の CLI 解析、fork 作成、ブランチ操作、差分取得、実際の適用処理そのものを調べたいとき。
- 個別ファイルのパッチ内容、git 操作の仕様、diff 生成手順を確認したいとき。
- oracle file と realization file の基本定義、path keyword、repo root 解決、共通 prompt 構築処理、standard 本文そのものを調べたいとき。
- ルーティング文書、テスト、実装などの変更種別ごとの具体的な判定ロジックや、利用者向け CLI 表示全体の振る舞いを確認したいとき。

## hash
- 510f41031a2e656030632d5757b9b99460f5ba72245b38c56ea494ae40150164
