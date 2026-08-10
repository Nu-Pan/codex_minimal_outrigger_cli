# `doc`

## Summary
- cmoc の正本ドキュメントをまとめたディレクトリ。アプリケーション仕様、branch・commit・worktree、採用しなかった設計案、開発規則など、実装や調査の前提となる文書群への入口を提供する。
- 複数の仕様領域にまたがる判断や、作業内容に応じた正本文書の選択が必要な場合の上位ルーティング先となる。

## Read this when
- cmoc の正本仕様や開発規則から、対象領域に対応する文書への入口を探すとき
- CLI、run・session、branch・worktree、実装、テスト、開発環境など複数領域の前提や責務境界を確認するとき
- 採用されなかった設計案やリファクタ方針の背景を確認するとき

## Do not read this when
- 特定の機能や規則の正本文書が特定できているときは、該当文書を直接読む
- 実装・テストの具体的な挙動を確認するときは、対応する実装・テストを直接読む
- 構築済み環境でのテスト選択や実行手順だけを確認するときは、専用の手順文書を直接読む

## hash
- 927c5c89ef7827c5efbbe72c578edacd7bede497932ced7e38b003ba291366ad

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
