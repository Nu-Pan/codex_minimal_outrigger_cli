# `oracle`

## Summary
- cmoc の正本となる設定・パスモデル・構造化文書モデルと、agent call の入力契約および prompt 構築定義をまとめた oracle ソース階層。
- agent call の用途別パラメータ定義、prompt の policy・parts、feedback や editor input の入力契約へ進むための上位入口。

## Read this when
- cmoc の設定モデル、Codex provider と agent call の既定値、永続化対象を確認するとき。
- agent call の cwd から導出される worktree・repository ルートや、cmoc のパス placeholder の解決規則を確認するとき。
- 構造化文書ノードや cmoc の文書記法を Markdown へ変換するモデル・処理を確認するとき。
- agent call の入力パラメータ、prompt の policy 構成、用途別の oracle・realization・feedback・TUI 定義の入口を探すとき。
- editor input handoff や feedback reporter など、agent call に渡す JSON 入力契約を確認するとき。

## Do not read this when
- 実際の CLI 実行、agent call の起動、session join の競合解消、oracle や realization 本文の編集処理だけを確認したいとき。
- 特定の agent call の具体的な prompt policy、用途別パラメータ、または JSON Schema の受理条件を確認したいときは、対応する下位対象を直接読むとき。
- cmoc の一般規定や prompt の正本仕様そのものを確認したいときは、対応する仕様文書を直接読むとき。

## hash
- 8e4ca2bf185ddf79b8aad090e5404ed73730df6a062439f095afdb6ca42a7c9c
