# `oracle`

## Summary
- oracle 関連の agent call 構築機能を、目的別の builder、共通モデル、prompt 構築部品に分けて案内するルーティング対象。agent call の設定・prompt・出力 schema・パス境界など、oracle の呼び出し構成を調べる際の上位入口となる。
- `acp_builder` は、AgentCallParameter を基盤に feedback、indexing、oracle、quota probe、realization、session、TUI など目的別 agent call の prompt・Structured Output・起動条件を構築する下位モジュール群への入口。
- `feedback` は、agent が検出した問題を feedback reporter から collector へ渡す入力契約を扱い、問題の分類・重要度・影響、人間対応の必要性、確信度、根拠、作業継続状態の表現と検証へ進む入口。
- `other` は、cmoc の共通モデルと Markdown 文書生成ヘルパーをまとめ、設定、Codex CLI・oracle review・並列実行の構成、root placeholder と agent call 単位のパス解決、構造化文書ノードと GFM レンダリングを扱う。
- `prompt_builder` は、agent call 用 prompt の基本型、完全 prompt、エディタ入力、prompt 部品、各種 policy の構築を扱い、policy・補助文面・objective・placeholder の統合や oracle／realization の分類説明へ進む入口。

## Read this when
- oracle 関連 agent call の構築責務や、目的別 builder の配置を確認するとき
- agent call の共通モデル、設定、パス境界、構造化 Markdown 文書の扱いを調べるとき
- agent call 用 prompt の全体構成、policy、placeholder、objective、エディタ初期入力の生成を確認するとき
- feedback の入力契約や、問題を人間向け feedback として構造化する処理の入口を探すとき

## Do not read this when
- 個別 builder の具体的な prompt、起動条件、field 値の決定規則だけを確認したいときは `acp_builder` 以下の対象を直接読む
- 共通型や設定モデルだけを確認したいときは `other` 以下の定義元を直接読む
- 個別 policy の本文面や適用条件だけを確認したいときは対応する policy の正本文書を直接読む
- feedback の保存・集約・重複判定や、問題検出・作業継続判断だけを確認したいときは対応する実装を直接読む
- agent call の実行制御、oracle file の編集・調査・レビュー処理、realization 実装そのものを確認したいときは利用側の実装を直接読む
- Structured Output の具体的な項目や形式だけを確認したいときは対応する schema を直接読む

## hash
- a9f94fc227dbc9714ebfc42dadd3bc7caeba361b21de5ce5c13e574352a90ae5
