# `doc`

## Summary
- cmoc の正本ドキュメントを収める上位ディレクトリ。アプリケーション仕様、branch・commit・worktree のモデル、不採用案の検討記録、開発規則へ進むための入口となる。

## Read this when
- cmoc の仕様・設計・開発規則を調査し、対象領域の正本文書を選ぶとき
- CLI 挙動、session/run の分岐、開発環境、テスト要件・実行手順などの文書入口を探すとき
- realization refactor で採用・不採用となった方式の背景を確認するとき

## Do not read this when
- 特定機能の詳細仕様を確認したい場合は、アプリケーション仕様配下の該当文書へ直接進む
- 実装コードやテストコードの内容だけを確認したい場合は、対応する realization source または test を直接読む
- INDEX.md の生成・更新ルールだけを確認したい場合は、indexing の仕様へ直接進む

## hash
- a23897e0fdbe40c90ca2e88e6a7549ff61d5e6ff478b483659c06850a1ac5625

# `src`

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
- bc5b9604838954b2ee9dde0d538419d06e16b4c1f2a3f61d959e9e96a7bbeb5f
