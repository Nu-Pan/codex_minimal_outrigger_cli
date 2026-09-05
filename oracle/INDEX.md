# `doc`

## Summary
- cmoc の正本仕様、設計判断、開発基準を目的別に参照するための入口。アプリケーション仕様、session・run の branch／commit／worktree モデル、検討済み代替案、Python・CLI・環境・テストの開発ルールを扱う。

## Read this when
- cmoc の共通挙動や実行契約、session・run の隔離・統合モデル、採用しなかった設計案、または開発時の実装・環境・テスト規則を探すとき。
- 複数の仕様・開発ルール文書群にまたがる確認で、目的に応じた下位文書への入口を判断したいとき。

## Do not read this when
- 特定の仕様書、実装、テスト、oracle／realization の具体的内容だけを確認したいときは、対応する下位文書や実ファイルを直接読む。
- INDEX.md の生成・更新規則だけを確認したいときは、indexing の仕様を直接読む。

## hash
- 97927464332eff7034d75a1aa4563e6f56650b8318409fc3341cca0f1f29cc1a

# `src`

## Summary
- `oracle/src` は、cmoc の agent call・prompt・設定・パス解決・構造化文書・入力契約に関する正本仕様の下位要素への入口。
- agent call の共通型や用途別起動定義、prompt と policy 部品、設定モデル、Git worktree に基づくパス解決を扱う。
- Markdown の構造化文書レンダリングと feedback・editor input handoff の入力契約を確認するための起点。

## Read this when
- cmoc の agent call を構築する共通仕様、用途別 prompt、起動設定、または Structured Output の入力契約を調べるとき。
- prompt へ作業規定や placeholder を統合する方法、agent call の cwd から導出する root、Git worktree のパス解決を確認するとき。
- 見出し・参照可能ブロック・policy を含む構造化文書や Markdown レンダリングの仕様を確認するとき。
- feedback 報告または editor input handoff の JSON 入力契約を確認するとき。

## Do not read this when
- 特定の agent call の実行処理、feedback の収集・重複判定、または TUI の個別ワークフローだけを確認したいときは、対応する実装や下位仕様を直接読む。
- Codex CLI の sandbox・起動規則・oracle/realization の作業規定そのものを確認したいときは、参照先の正本仕様を直接読む。
- INDEX.md の更新手順や、`oracle/src` の対象外にある CLI 機能・realization 実装を確認したいときは、この入口を読まず直接それらを調べる。

## hash
- d6279a4fc59f16a23e8d865cca5152aa5ecce083c96fb983b23fcfacfdea1f0a
