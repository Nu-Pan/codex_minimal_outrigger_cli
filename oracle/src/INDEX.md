# `oracle`

## Summary
- oracle/src/oracle は、cmoc の設定・パスモデル・構造化文書処理と、agent call 用のパラメータ、feedback、prompt 構築などの共通実装をまとめる中核ディレクトリです。用途別の agent call 定義や prompt 部品、共通データモデルへの入口を提供します。

## Read this when
- agent call の共通設定、パラメータ契約、用途別構築定義の関係を確認するとき
- cmoc の設定、パス placeholder 解決、構造化文書の生成処理を確認するとき
- agent 向け prompt の構成、policy の統合、editor input の生成を調査・変更するとき
- feedback 入力契約や、その下位スキーマへの入口を確認するとき

## Do not read this when
- 実際のモデル名やバックエンド固有の解決処理だけを確認したいとき
- oracle や realization の正本仕様、具体的な実装・テストだけを確認したいとき
- CLI サブコマンド解析、共通 prompt 生成以外の処理、TUI の画面処理だけを確認したいとき
- collector による feedback の保存・集約や、問題検出後の継続判断だけを確認したいとき

## hash
- 518f82f5a2bd2e91758cee7937318e9abf555cd6c8c9945532b979129caa3c7d
