# `oracle`

## Summary
- cmoc の agent call、prompt 構築、設定、パス解決、構造化文書、および入力契約を定義する正本仕様群への入口。
- agent call の共通パラメータと用途別起動定義、完全 prompt と policy 部品、設定モデル、Git worktree に基づくパス・placeholder 解決を扱う。
- 構造化文書の Markdown レンダリングと、feedback・editor input handoff の JSON 入力スキーマを確認するための下位要素へ進める。

## Read this when
- cmoc の agent call 構築に必要な共通型、用途別 prompt、Codex 起動設定、Structured Output の入力契約を調べるとき。
- prompt に組み込む作業規定、placeholder の統合、agent call の cwd から導出する root、Git worktree のパス解決を確認するとき。
- 見出し・参照可能ブロック・policy を含む構造化文書の生成や Markdown レンダリングの実装を確認するとき。
- feedback 報告または editor input handoff に渡す JSON 入力項目と制約を確認するとき。

## Do not read this when
- 特定の agent call の実行処理、feedback の収集・重複判定、または TUI の個別ワークフローだけを確認したい場合は、対応する実装や下位仕様を直接読む。
- Codex CLI の sandbox、起動規則、または oracle・realization の作業規定そのものを確認したい場合は、参照される正本仕様を直接読む。
- INDEX.md の更新手順や、このディレクトリ外の CLI 機能・realization 実装を確認したい場合は、この対象を入口にしない。

## hash
- 8b3675f0505f7908c15be54a56953a32add9118ba72f3b907adba87f7ff79318
