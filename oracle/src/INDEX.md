# `oracle`

## Summary
- cmoc の oracle 実装を構成する下位領域への入口。AI agent 呼び出し構築、feedback 入力契約、共通モデル・設定、prompt 構築と標準定義を扱う。
- agent call の用途別パラメータや起動定義を確認するときは acp_builder、feedback の入力形式・検証を確認するときは feedback、パス・設定・標準・構造化文書の共通モデルを確認するときは other、完全 prompt や規則部品を確認するときは prompt_builder へ進む。

## Read this when
- oracle 実装の担当領域を特定し、4 つの下位領域のどこから調査を始めるか判断するとき。
- agent call、feedback、共通モデル、prompt 構築の複数領域にまたがる変更や調査で、下位入口を選ぶとき。

## Do not read this when
- 対象となる下位領域や個別ファイルが明確で、そこへ直接進めるとき。
- oracle の正本仕様、realization の実装、または INDEX.md のルーティング規則そのものを確認するとき。

## hash
- dfddd52c9544c67675787ba434ea9dd8821bc80a0e1612658fb7a42e10923636
