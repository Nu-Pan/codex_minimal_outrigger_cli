# `__init__.py`

## Summary
- oracle.acp_builder.apply と互換の package として機能する初期化ファイル。apply builder 互換層へ入るための package 境界を示す。

## Read this when
- oracle.acp_builder.apply 互換 package の有無や package 初期化位置を確認したいとき。
- apply builder 互換層の import 経路を確認する入口が必要なとき。

## Do not read this when
- apply builder の具体的な処理内容や関数実装を確認したいとき。
- oracle.acp_builder.apply 互換以外の builder package や別機能の責務を確認したいとき。

## hash
- a6df93a5897c266e6f48287739c8bf8192733ea9fb19e2f6eb05a302f4165b06

# `fork`

## Summary
- `cmoc apply fork` 向けの ACP builder adapter 群を扱う。oracle 側 builder を realization 側から呼び出すための import 準備、repository root 解決、runtime ACP 型への parameter 変換、変更要約・ファイル単位所見列挙・所見適用の agent call parameter 構築への入口になる。
- apply fork の実行制御本体ではなく、正本側 builder と realization 側 `AgentCallParameter` の接続境界を確認するためのまとまりである。

## Read this when
- `cmoc apply fork` で変更要約、ファイル単位所見列挙、所見適用に渡す agent call parameter の構築経路を確認・変更したいとき。
- apply fork ACP builder が oracle 側 builder を import し、oracle parameter を realization 側 parameter へ変換する接続点を調べたいとき。
- apply fork 互換 package の有無、package 初期化位置、builder 共通処理の責務境界を確認したいとき。

## Do not read this when
- prompt 構成、parameter 内容、所見生成規則などの正本仕様そのものを確認したいときは、対応する oracle src を読む。
- `cmoc apply fork` 全体の CLI 実行制御、git 操作、状態遷移を調べたいときは、apply fork の実行側へ進む。
- fork 以外の ACP builder、CLI 全体の routing、path placeholder の一般仕様、または oracle file の定義を調べたいときは、より直接の対象を読む。

## hash
- 2e2428412495bb18c8be988001d21a56aed5eea5ef59efd166b8e625a79e4e6c
