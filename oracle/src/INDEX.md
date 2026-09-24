# `oracle`

## Summary
- cmoc の agent call に渡す prompt と起動パラメータを組み立て、共通規定、作業固有の指示、参照情報、パス context をまとめる。
- タスク別の構築処理は、oracle の調査・編集、realization の適用・レビュー、join の競合解消、index entry 生成、feedback issue 対応、TUI 起動などを扱う。
- 共通モデルには構造化文書の Markdown 描画、パスと root placeholder、文書参照、アクセス mode、設定があり、editor input handoff のガイド・本文生成と tool 入力契約も含む。

## Read this when
- agent call に注入する共通ポリシーや、特定作業向けの prompt 文面を変更するとき。
- agent call のパラメータ、アクセス mode、cwd と root の対応、構造化 prompt の描画、モデル設定を追うとき。
- editor input handoff のガイドや本文の組み立て、またはその tool 入力契約を変更するとき。
- 特定タスクの prompt と起動パラメータがどの構築処理でまとめられるか調べるとき。

## Do not read this when
- コマンドの意味仕様や利用者向け手順だけを確認するときは、対応する正本仕様を直接読む。
- 実行制御、永続状態、CLI の入出力だけを変更するときは、その処理を担う実装から調べる。
- 機械的な入力・出力の受理条件だけを確認するときは、対応する schema を直接読む。

## hash
- c4b22e1920be566579dc3ca207f5c6e13efc7a19750c4c37d485b84f1827956b
