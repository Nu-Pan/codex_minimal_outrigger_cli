# `oracle`

## Summary
- oracle/src/oracle は、cmoc の agent call 構築と設定・パス・文書変換の共通モデル、feedback 入力契約をまとめる oracle 実装領域です。
- acp_builder は agent call の用途別パラメータや起動定義、feedback・oracle・realization・session・TUI 関連の構築入口を扱います。
- other は cmoc 設定、agent call の call-scoped root path 解決、構造化文書の Markdown 変換といった共通基盤を扱います。
- prompt_builder は完全 prompt、エディタ入力、共通 parts、作業目的別 policy の構築を扱います。
- feedback は agent が検出した問題を collector へ渡す reporter input の構造化契約を扱います。

## Read this when
- agent call の用途別起動パラメータや Structured Output 定義を調査・変更するときは acp_builder から確認するとき
- cmoc の設定モデル、root placeholder と agent call cwd からのパス解決、構造化 Markdown 生成を調査・変更するときは other から確認するとき
- 完全 prompt の構成、placeholder、共通部品、用途別 policy の選択や注入を調査・変更するときは prompt_builder から確認するとき
- feedback reporter の入力契約や問題情報の構造化を調査・変更するときは feedback から確認するとき

## Do not read this when
- 特定の CLI サブコマンドの処理フローや realization の具体的な実装・テストだけを確認したいとき
- oracle file の個別仕様本文そのものを確認したいとき
- 既存の INDEX.md のルーティング内容だけを確認したいとき

## hash
- 1749f3bafe7838e531422e7fe89c30ed330890c0620668cf9fd4be3d43497ce6
