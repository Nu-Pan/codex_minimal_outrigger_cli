# `oracle`

## Summary
- cmoc の正本仕様を、agent call 構築、エディタ入力、フィードバック入力、周辺基盤モデル、prompt 構築の領域に分けて案内する最上位の入口。
- agent call や prompt の構築仕様を調べるときに、用途別の下位ディレクトリへ進むための分類点。
- 各下位領域では、個別の型定義、JSON Schema、パスモデル、構造化文書、prompt policy などの正本仕様を扱う。

## Read this when
- oracle 配下の正本仕様を横断して、目的に応じた下位領域の読み始めを判断するとき。
- agent call のパラメータ構築、エディタ入力の契約、フィードバック報告入力、基盤モデル、または prompt 構築の仕様を探すとき。

## Do not read this when
- 特定の下位領域の具体的な仕様だけを確認したい場合は、acp_builder、editor_input_handoff、feedback、other、または prompt_builder の該当対象を直接読む。
- JSON Schema の受理条件だけを確認したい場合は、対応する Schema ファイルを直接読む。
- 実装上の agent call 起動処理や CLI ワークフローだけを確認したい場合は、この正本仕様の入口ではなく対応する realization 側の実装を読む。

## hash
- 723e70d34bd6d3ee43246438f01792c764265082dd8399c1140554334d528689
