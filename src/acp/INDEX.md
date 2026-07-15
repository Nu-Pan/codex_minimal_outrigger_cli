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
- `acp.builder` 配下の互換入口と builder 関連の実装群を案内するディレクトリ。既存の `acp.builder.*` import を維持しつつ、`oracle.acp_builder` の正本実装へ委譲する入口、apply・quota probe・review・session・TUI・indexing の各領域への進入点を提供する。

## Read this when
- `acp.builder.*` の既存 import 互換、正本側への委譲経路、または配下の builder 領域を横断して読む先を判断したいとき。
- apply、quota availability probe、indexing、review、session、TUI のいずれかの互換入口や関連実装を調査・変更するとき。
- 共通 builder 処理の配置や、現在本文ファイルが存在する下位要素を確認したいとき。

## Do not read this when
- 特定機能の正本仕様や実装本体だけを確認したい場合は、該当する下位モジュールまたは `oracle.acp_builder` 側を直接読む。
- `acp.builder.*` の互換入口と無関係な機能、または個別 builder の内部ロジックだけを追う場合は、このディレクトリ案内を読む必要はない。

## hash
- eb2908b68c2d042a50a4f936d04a599ceb882217dbf906aca869a3cd1676b3c6
