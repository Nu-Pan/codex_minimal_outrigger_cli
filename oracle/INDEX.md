# `doc`

## Summary
- cmoc の正本ドキュメントを領域別にまとめたディレクトリ。アプリケーション仕様、branch・commit・worktree のモデル、採用しなかった設計案、開発規則など、各仕様文書へ進むための入口。

## Read this when
- cmoc の挙動仕様、ブランチモデル、開発規則、または設計判断の根拠を確認・変更・レビューするとき。
- 目的に応じた正本ドキュメントの所在を特定し、個別文書へ進む前に仕様群の構成を把握したいとき。

## Do not read this when
- 対象が特定の仕様文書や機能に明確に限定されている場合は、該当する下位文書へ直接進む。
- 実装やテストの具体的な内容、または INDEX.md の生成規則だけを確認するときは、対応する直接の参照先を読む。

## hash
- b40afba127e7aabba131f140e1cf6c735ef7f9798d845b45e9a3a67e5556957e

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
