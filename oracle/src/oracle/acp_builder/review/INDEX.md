# `oracle`

## Summary
- oracle review における所見の列挙・採否判定・重複整理・妥当性検証を担う Structured Output schema と prompt 構築実装をまとめたディレクトリ。所見レビュー処理の出力契約と、各レビュー段階のエージェント呼び出し設定を確認する入口。

## Read this when
- `cmoc oracle review` の所見生成・採否判定・重複整理・賛否理由検証の出力契約を確認したいとき。
- 所見レビュー用 prompt の入力、oracle-only の読み取り制約、モデル設定、Structured Output の接続を調査・変更するとき。
- 所見の重複排除、統合、既知理由との差分抽出、所見がない場合の出力境界を確認したいとき。

## Do not read this when
- oracle review の所見探索手順や判定基準そのものを確認したいときは、対応する oracle review 用の正本文書を直接読む。
- agent call parameter の共通生成処理や共通 Structured Output 定義だけを確認したいときは、対応する共通 builder・型定義を直接読む。
- レビュー結果の CLI 表示、永続化、実際のファイル編集処理を調査したいとき。

## hash
- 37aa25ca8fd9e4c5d1d08d8d77f600d618309fccdde48f151f386e0f2487ba01
