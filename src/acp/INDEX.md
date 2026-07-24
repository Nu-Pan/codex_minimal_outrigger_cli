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
- ACP builder の realization 層。oracle 側の canonical builder を旧来の `acp.builder.*` import 経路へ互換公開し、oracle・realization・TUI・session などの builder adapter への入口を提供する。

## Read this when
- `acp.builder` 配下の互換 import 経路、builder adapter の配置、または canonical builder への委譲関係を確認するとき。
- oracle、realization、session、TUI、indexing など特定の builder adapter の責務や呼び出し経路を調査するとき。

## Do not read this when
- canonical な builder の仕様・実装内容そのものを確認するときは、対応する `oracle` 側の実装を直接読む。
- TUI 本体、fork 適用処理、一般的な indexing 処理など、builder の互換公開層に関係しない機能を調査するとき。

## hash
- 5b15edfbe559d1ec453b47900831f4836ca043dcbbe0641f88a283a4ba85a710
