# `__init__.py`

## Summary
- `acp` 互換の公開入口を扱う。`acp.*` を利用している既存参照を、`oracle.*` または実体モジュールへ移す必要があるときに読む。

## Read this when
- `acp` という公開名を残すべきか、削除できるかを判断したいとき。
- 既存の利用者向け参照を壊さずに、`oracle` 側の実体へ切り替える導線を確認したいとき。

## Do not read this when
- `acp` 配下の具体的な実装内容や移行先の詳細を知りたいだけなら、直接その実体モジュールを読む。
- 互換入口の存廃ではなく、`acp.*` の内部挙動そのものを変えたいだけならここではない。

## hash
- fe0939ab61e919bfb5ae35264e02859ee36efb102a15498d95fcbd45f9670e76

# `builder`

## Summary
- `acp.builder` の互換入口群をまとめるディレクトリ。旧来の `acp.builder.*` import を維持しながら、`oracle.acp_builder` 側の正本実装や各 realization builder・probe・TUI 入口へ到達するための境界を提供する。

## Read this when
- `acp.builder` 配下の互換 import 経路、公開名、モジュール探索順を確認するとき。
- apply、indexing、review、session、TUI、quota probe などの互換入口や canonical 実装への委譲先を調べるとき。
- 互換層の維持・整理・削除可否を判断するとき。

## Do not read this when
- 特定機能の正本仕様や本体実装を確認したいときは、対応する `oracle.acp_builder` 側または委譲先の実体を直接読む。
- 互換入口と無関係な個別サブコマンドの内部ロジックを調べるとき。

## hash
- 77153bacc00daaa85ea56f7e60b670507979857153d8b8daa88c48df20c4d02e
