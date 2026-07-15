# `fork`

## Summary
- `cmoc apply fork` における変更要約とファイル単位レビュー・修正の AgentCallParameter、および対応する正本スキーマを扱うディレクトリ。変更要約の出力契約、レビュー・修正 prompt、モデル・アクセス設定を確認する入口。

## Read this when
- `cmoc apply fork` の変更要約処理を実装・検証するとき。
- ファイル単位レビュー・修正の prompt、出力スキーマ、AgentCall 設定を調査するとき。
- 変更要約とファイルレビュー・修正に対応する oracle src とスキーマの関係を確認するとき。

## Do not read this when
- 差分取得や fork の作成・適用など、要約・レビューの前後にある実行フローを調査するとき。
- レビュー対象ファイルの具体的な realization 実装やテストを確認するとき。
- 共通 prompt builder、パス解決、構造化文書処理の実装詳細だけを調査するとき。

## hash
- 805a32c97cbd42a5e6cad18cf0d0188d3efc60f61908f5e1d0e43dc5a10edd9a
