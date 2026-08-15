# `oracle`

## Summary
- oracle の agent call 構築、prompt 構築、feedback 入力契約、設定・パスモデル・Standard・構造化 Markdown 生成を扱う実装群への入口。用途別の呼び出し定義を調べる場合は `acp_builder`、プロンプト構成や instruction を調べる場合は `prompt_builder`、feedback reporter の入力契約を調べる場合は `feedback`、共通モデルや文書生成を調べる場合は `other` へ進む。

## Read this when
- cmoc の oracle 側で agent call の論理パラメータ、用途別呼び出し、Structured Output schema の対応を調査・変更するとき。
- agent 向け完全 prompt、placeholder 置換、Standard、file access rule、routing rule、feedback reporting などの構築経路を調査・変更するとき。
- cmoc の設定、agent call のパスコンテキスト、Standard の合成、構造化 Markdown のレンダリング、feedback reporter 入力の構造を調査するとき。

## Do not read this when
- CLI の実行処理、realization implementation、realization test、個別 oracle file の正本仕様を直接確認したいとき。
- agent call 構築や oracle 共通モデルと無関係な永続化処理、実行時の制御ロジック、外部サービス連携だけを調査するとき。
- 既存の INDEX.md のルーティング情報だけを確認するとき。

## hash
- 62bd6282d97042e8f8fa8a8fdd3f4e296bba7485700d8f3f28b7f8a8b97289c6
