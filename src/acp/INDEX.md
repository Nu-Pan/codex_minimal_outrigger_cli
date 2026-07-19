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
- acp.builder の互換入口と builder adapter 群をまとめる realization package。既存の acp.builder.* import 経路を維持しつつ、oracle 側の canonical builder、quota probe、oracle/realization workload、session、TUI、indexing への公開・委譲入口を提供する。
- 下位要素には、互換パッケージ、各 workload の builder adapter、quota probe の fallback、TUI 起動準備、索引・session 関連の再公開層がある。

## Read this when
- acp.builder 配下の互換 import 経路、canonical builder への委譲先、または builder adapter の配置を確認・変更するとき。
- oracle、realization、session、TUI、indexing、quota probe の builder 入口を辿る必要があるとき。

## Do not read this when
- oracle 側の canonical builder の仕様や実装本体を確認したいとき。
- builder adapter 以外の CLI、ACP runtime、TUI 本体、または具体的な workload 処理を調査するとき。

## hash
- f8920ba33af1a4d685d0d7fcdd7123ac938897f9d0c3eaf22ef019ca5b9cee60
