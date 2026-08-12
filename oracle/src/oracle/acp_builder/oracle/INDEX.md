# `edit`

## Summary
- oracle 編集処理に関する起動設定と、編集担当 agent call のプロンプト・実行条件を確認するための入口です。本文ファイルを含まない空の領域も含み、具体的な起動実装は下位対象から確認します。

## Read this when
- `cmoc oracle edit` の TUI 起動方法や起動パラメータを確認・変更するとき
- oracle 編集用プロンプトの生成、ユーザー指示の組み込み、ログ保存を確認するとき
- 編集担当 agent call のモデル、推論強度、権限、作業ディレクトリ、インデックス事前処理を確認するとき

## Do not read this when
- oracle file の具体的な編集内容や realization 実装を確認するとき
- `cmoc oracle edit` 以外のコマンドの起動設定を確認するとき
- agent call の共通データ型や TUI 一般実装だけを確認するとき
- この領域の具体的な下位ファイルを直接確認できるとき

## hash
- c22b15cf04c9d1af4854be72dea27f3f5f3b5205e4ef19a0595cd0bb013212fc

# `investigation`

## Summary
- oracle investigation 用 TUI の起動条件と、調査用完全プロンプトを組み立てて保存する実装です。調査用モデル、推論強度、ファイルアクセス、作業ディレクトリ、インデックス事前処理などの起動設定を確認・変更する際の入口になります。

## Read this when
- `cmoc oracle investigation` の TUI 起動パラメータや、oracle file 調査用プロンプトの構成・保存先を確認または変更するとき。
- oracle file 調査に用いるモデル、推論強度、読み取り範囲、作業ディレクトリ、インデックス事前処理の設定を確認するとき。

## Do not read this when
- 調査内容そのものや oracle file の仕様を確認したいときは、生成済みの完全プロンプトまたは対象の oracle file を直接読む。
- 一般的な prompt の共通構築規則を確認したいときは、共通 prompt builder の定義を直接読む。

## hash
- 77c11a5aa66d1d6be40862441730e3ca6f318dc190111ab5d05543f3502f5497

# `review`

## Summary
- oracle review の所見列挙・妥当性検証・採否判定・統合整理に関する Structured Output スキーマと、各 agent call のプロンプトおよび起動パラメータを集約するディレクトリ。レビュー工程ごとの入出力契約と呼び出し構築定義への入口となる。

## Read this when
- oracle review の所見レビュー工程を変更・調査するとき。
- 所見の列挙、支持・反証理由の検証、採否判定、重複・矛盾の統合に関するスキーマまたは agent call 設定を確認するとき。

## Do not read this when
- oracle review 以外の処理を確認するとき。
- レビュー対象の oracle file、実装、仕様そのものを調査するとき。
- 共通の prompt 構築規則や agent call 基盤だけを確認するときは、対応する共通実装を直接読む。

## hash
- 0f89d8b99e69e7d674f18d17360f97d44a0ebaa2d9d32606c957a6e1e9caa5c2
