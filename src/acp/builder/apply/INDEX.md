# `__init__.py`

## Summary
- oracle 側の apply builder package と対応する互換 package であることだけを示す package 初期化要素。実処理や公開 API の定義ではなく、同領域を package として扱うための入口に位置づけられる。

## Read this when
- apply builder 領域が oracle 側の package 構造と対応しているかを確認したいとき。
- package 初期化部分に実装意図や互換性メモがあるかを確認したいとき。

## Do not read this when
- apply builder の具体的な処理、変換、適用ロジックを調べたいとき。その場合は同 package 内の実装本体を読む。
- 公開関数、クラス、入出力仕様、エラー処理を確認したいとき。この対象にはそれらの定義は含まれない。

## hash
- a6df93a5897c266e6f48287739c8bf8192733ea9fb19e2f6eb05a302f4165b06

# `fork`

## Summary
- apply fork 系の ACP builder 実装と、その agent 呼び出しに使う structured output schema をまとめるディレクトリ。oracle 側 builder への委譲、repo root 解決、oracle src import 準備、realization 側 AgentCallParameter への変換、および変更要約・所見列挙の出力契約への入口になる。

## Read this when
- `cmoc apply fork` の agent call parameter 生成経路を、変更要約・ファイル単位の所見列挙・所見適用などの段階別に探したいとき。
- apply fork 系 builder が oracle 側の parameter を realization 側の AgentCallParameter や JSON schema path に橋渡しする構造を確認したいとき。
- apply fork の作業レポートやレビュー結果に使う structured output schema の責務を確認したいとき。

## Do not read this when
- fork 作成、git 操作、差分適用、実行制御など `cmoc apply fork` 全体の制御フローを調べたいとき。
- prompt 本文や正本仕様断片としての builder 挙動を確認したいとき。このディレクトリの実装は oracle 側 builder へ委譲する adapter が中心である。
- repo root 解決、path model、AgentCallParameter、enum 型そのものの定義を調べたいとき。ここではそれらを利用するだけで、定義は別の基礎領域にある。

## hash
- 36155a900b41206d9c74b82a4f148cd7731f60c331831dbd922e880b0c44cec8
