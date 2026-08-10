# `doc`

## Summary
- cmoc のアプリケーション仕様、branch・commit・worktree のモデル、開発規則、不採用案の検討記録を扱う正本ドキュメント群への入口。各領域の詳細確認時に、該当する下位仕様書へ進むためのルーティングを担う。

## Read this when
- cmoc のアプリケーション挙動や仕様間の責務境界を確認するとき
- branch・commit・worktree のモデルを確認するとき
- 開発規則の対象領域を選ぶとき
- realization refactor で採用しなかった方式の理由を確認するとき

## Do not read this when
- 特定機能の詳細仕様だけを確認する場合は、該当する下位仕様書を直接読む
- 個別の開発手順だけを確認する場合は、対応する開発規則文書を直接読む
- INDEX.md 生成規則や oracle／realization の一般原則だけを確認する場合は、専用の正本仕様を直接読む

## hash
- 4b00d1d2b46dcb0755830f16e18722ae7146ffb0e10ff46a892182e6df6fe542

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
