# `oracle`

## Summary
- cmoc の正本仕様に属するソースコード、設定スキーマ、agent call builder、prompt builder、および関連モデルをまとめる領域。
- oracle file と realization file の基本モデルを基盤に、agent call の入力・出力契約、用途別の prompt、実行パラメータ、oracle・realization の編集・レビュー・適用処理を構成する。
- quota probe、indexing、feedback、session、TUI、editor input handoff など、cmoc の各機能から利用される実装上の入口を提供する。

## Read this when
- cmoc の oracle src にある agent call 構築、prompt 構築、設定・パス・文書モデル、または JSON schema を調べるとき。
- oracle・realization の編集、レビュー、適用、所見処理や session join の agent call の構成を確認するとき。
- 対象機能に対応する下位ディレクトリや builder、schema の入口を探すとき。

## Do not read this when
- oracle file や realization file の人間向け正本仕様そのものを確認したいときは、該当する仕様文書または対象ファイルを直接読む。
- 特定の下位機能の prompt、出力契約、または実行処理だけを確認したいときは、該当する下位ディレクトリの対象へ直接進む。
- Codex CLI や agent call の共通実行機構の実際の挙動だけを調べるとき。

## hash
- 151801d0bc12eed6d20d4ef9ea96f49ea4acacbc13c95a58131df82465e16a55
