# `oracle`

## Summary
- cmoc の正本側 Python 実装と構造化定義を集約するディレクトリです。agent call の構築、feedback 入力契約、設定・パス・構造化文書の共通モデル、prompt 部品の生成を扱います。
- agent call の用途別定義や起動パラメータを調査するときは `acp_builder`、feedback reporter の入力契約を調査するときは `feedback`、設定・パスモデル・構造化文書を調査するときは `other`、完全 prompt や標準規則の構築を調査するときは `prompt_builder` へ進みます。

## Read this when
- cmoc の正本実装を構成する agent call、prompt、設定、パスモデル、構造化文書、feedback 契約の責務範囲を確認するとき
- agent call の prompt や起動パラメータ、Structured Output 連携の用途別定義を調査するとき
- cmoc 共通の設定値、Codex モデル設定、作業パスの placeholder、agent 向け標準文面、Markdown 構造化処理を調査するとき
- feedback reporter が扱う問題分類・重要度・影響・根拠・継続状態の入力契約を確認するとき

## Do not read this when
- 個別の oracle 文書、realization 実装、realization test の正本内容を確認するときは、該当する対象を直接読む
- collector による feedback の保存・集約・重複判定や、agent call の実行処理を確認するときは、その処理の実装を直接読む
- 既存 INDEX.md のルーティング情報だけを確認・変更するときは、このディレクトリの実装本文を読む必要はない
- Structured Output schema の項目名・型・形式だけを確認するときは、該当 schema を直接読む

## hash
- 08251c7d206b21c8f2f519f8bd05d84ba84b237b5d7edaf983a4e9801dde34b1
