# `oracle`

## Summary
- oracle src にある cmoc の正本実装群です。ACP 呼び出しパラメータ、完全な agent prompt、oracle・realization の規範、パス解決、設定モデル、構造化文書の Markdown 変換、feedback reporter 入力契約を扱います。用途別の実装を確認する場合は、ACP builder・prompt builder・other・feedback の下位領域が入口になります。

## Read this when
- cmoc の oracle src 実装を調査・変更するとき。
- サブコマンド別の ACP 呼び出し設定や prompt の構築を確認するとき。
- agent prompt に注入する oracle・realization・review・routing・file access などの共通規範を確認するとき。
- リポジトリ設定、パス解決、構造化文書モデル、Markdown 変換などの共通モデルを確認するとき。
- feedback reporter が collector へ渡す入力契約を確認するとき。

## Do not read this when
- oracle の正本ドキュメントや正本テストを確認する場合は、対応する oracle/doc または oracle/test を直接読む。
- realization 側の CLI 挙動や実装を確認する場合は、対応する realization implementation を直接読む。
- 特定の下位領域の責務が明らかな場合は、このディレクトリ全体を読む必要はなく、対応する下位ディレクトリへ直接進む。

## hash
- 571297b0ef9b1647482c9719baa29977021cde26f889dce5e6820ac6f9cd5e3b
