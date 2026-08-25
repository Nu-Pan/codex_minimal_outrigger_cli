# `doc`

## Summary
- cmoc の正本仕様・開発規約を集約する文書群への入口。app_spec で CLI、session/run lifecycle、共通実行契約などを確認し、branch_model で branch・commit・worktree の関係を確認する。dev_rule では Python 実装、CLI 配置、環境、テスト、品質検査の規則へ進む。considered_alternative は不採用案と採否理由の確認に使う。

## Read this when
- cmoc の現行仕様、設計上の用語、CLI の挙動、session/run や branch/worktree の lifecycle を調査・変更するとき
- Python 実装規約、CLI の責務配置、開発環境、テスト要件、品質検査手順を確認するとき
- 採用されなかった設計・作業方式と、その理由を調査するとき

## Do not read this when
- 特定機能の実装詳細、正確な prompt や Structured Output schema、具体的な保存済み report だけを調べるとき
- 個別仕様の詳細やテスト実行手順など、下位文書が直接の入口になるとき

## hash
- 57185820274aa5c194dab2d107498caafcc9f7f9b910914d23d6dc9f9e4eabe6

# `src`

## Summary
- oracle 配下の agent call 構築、prompt・policy の生成、feedback 入力契約、設定・パス解決・構造化文書の補助モデルを実装する領域です。
- agent call の共通パラメータや目的別起動処理を調べる場合は `acp_builder`、prompt の統合や oracle／realization・routing・feedback の規定を調べる場合は `prompt_builder`、設定・パス解決・構造化文書のモデルとレンダリングを調べる場合は `other`、feedback reporter の入力契約を調べる場合は `feedback` へ進みます。

## Read this when
- agent call のモデル、reasoning effort、ファイルアクセス、作業ディレクトリ、Structured Output schema、indexing preflight の構築を確認または変更するとき
- prompt の統合、placeholder、oracle／realization の基本定義、ファイルアクセス、routing、feedback、review、conflict resolution の policy を確認または変更するとき
- agent call に使う root path の解決、パス境界、設定モデル、Structured Document の Markdown レンダリングを確認するとき
- feedback observation の入力項目・分類・重要度・根拠・継続状態の契約を確認するとき

## Do not read this when
- Codex CLI の実際の実行、backend へのモデル名変換、または外部プロセス起動の実装だけを確認したいとき
- oracle／realization の正本仕様本文や、realization 側の実装・テストを直接確認したいとき
- INDEX.md の既存ルーティング内容を確認したいとき
- agent call、prompt、feedback、設定、パス解決、構造化文書に関係しない CLI 挙動や別領域の仕様・テストだけを調査するとき

## hash
- c3273e05e2785c83946120d4cb928499a9a956fb6a749f806fbe103a4e762849
