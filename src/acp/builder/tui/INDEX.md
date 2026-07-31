# `__init__.py`

## Summary
- 既存の `acp.builder.tui.*` import を維持するためだけに残された、`oracle.acp_builder.tui` 互換 package の入口。
- realization 側と利用者向け公開面からこの参照が消えた後に削除できる互換層として位置づけられる。

## Read this when
- 既存 import 経路 `acp.builder.tui.*` の互換維持や削除可否を確認する。
- `oracle.acp_builder.tui` との互換 package がなぜ残っているかを確認する。

## Do not read this when
- TUI 実装本体の挙動や画面構成を確認したい場合。
- 新しい公開 API や新規 import 経路を設計したい場合。

## hash
- 9e5ae7e28c1e80b5ffa414ac5eea7dd08927b7977f87292b3afa9b714a894d0a

# `launch_tui.py`

## Summary
- TUI 起動用の agent call parameter builder adapter。正本 builder を呼び出し、TUI が free-form prompt を受ける契約に合わせて Structured Output schema path を無効化する。

## Read this when
- TUI 起動時の agent call parameter 生成や、Structured Output schema path の扱いを確認・変更するとき。

## Do not read this when
- TUI 以外の parameter builder、または正本 builder の仕様自体を確認・変更するとき。

## hash
- 2e19ef7b2bbcbcd68134e7bb99c529ff44530bdae06fb7c954f0e99f7190f9ee

# `resolve_parameter.py`

## Summary
- TUI の resolve-parameter builder を旧 import 経路向けに再公開する互換アダプター。正本 builder の結果を利用し、入力プロンプト内のコードフェンスを保護した AgentCallParameter を返す。

## Read this when
- TUI の resolve-parameter building の呼び出し元、互換 import 経路、またはプロンプトのコードフェンス保護を変更・調査するとき。

## Do not read this when
- canonical builder の仕様や実装を変更・調査するときは、指定された oracle builder を直接読む。
- TUI の他の builder や一般的な prompt 構築を扱うだけのとき。

## hash
- bb0a1eb0bfb775c57dff95c2aadc79a249c0520185c3930d1208db768a01a7f3
