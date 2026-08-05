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
- ACP builder の互換・委譲パッケージ群をまとめるディレクトリ。既存の acp.builder.* import 経路を維持しつつ、oracle 側の canonical builder、共通の Markdown fence 処理、oracle／realization 用途別 adapter、TUI や quota probe の入口を提供する。
- 互換入口の調査では basic、indexing、session、tui、quota probe を、共通的な prompt section 処理では common を、oracle／realization builder の構成確認では各用途別パッケージを下位入口として利用する。

## Read this when
- ACP builder の互換名前空間、canonical 実装への委譲経路、builder adapter の配置を調査・変更するとき。
- 既存の acp.builder.* import を維持または削除できる条件を確認するとき。
- prompt の動的 section、code fence 保護、oracle・realization command builder、TUI 起動や quota probe の入口を選ぶとき。

## Do not read this when
- canonical な oracle 実装や prompt 仕様そのものを確認・変更するときは、oracle 側の対応対象を直接読む。
- builder の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む。
- 具体的な command、session、indexing、common 処理の実装詳細を確認するときは、該当する下位要素を直接読む。

## hash
- f18b53b0c85076dd53ffd1acba7c2030a10a5b7d7bf5c18f1e20eca0623d0590
